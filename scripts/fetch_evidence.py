"""Fetch registered public text evidence without approving its factual claims.

No credentials, cookies, source messages, or API keys are sent. Captures remain
private. Every redirect is checked; local/private network destinations are refused.
Binary media is not downloaded. Fetch success is never a review disposition.
"""
import argparse
import concurrent.futures
import hashlib
import ipaddress
import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research/external'
MAX_BYTES = 2_000_000


def public_url(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('Not an unauthenticated HTTP(S) URL')
    if p.port not in (None, 80, 443):
        raise ValueError('Nonstandard destination port')
    addresses = socket.getaddrinfo(p.hostname, p.port or 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('Nonpublic destination refused')
    return url


class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return super().redirect_request(req, fp, code, msg, headers, public_url(newurl))


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'svg'):
            self.hidden += 1
        if tag in ('p', 'div', 'li', 'h1', 'h2', 'h3', 'br', 'tr', 'pre'):
            self.parts.append('\n')
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg'):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def retrieve(url):
    request = urllib.request.Request(public_url(url), headers={'User-Agent': 'JevKnowledgeResearch/1.0', 'Accept': 'text/html,text/plain,application/json'})
    opener = urllib.request.build_opener(Redirects())
    with opener.open(request, timeout=15) as response:
        content_type = response.headers.get_content_type()
        if not (content_type.startswith('text/') or content_type in ('application/json', 'application/xhtml+xml')):
            return {'status': 'nontext_not_downloaded', 'content_type': content_type, 'final_url': response.url}
        raw = response.read(MAX_BYTES + 1)
        truncated = len(raw) > MAX_BYTES
        body = raw[:MAX_BYTES].decode(response.headers.get_content_charset() or 'utf-8', errors='replace')
        links = []
        if 'html' in content_type:
            parser = Text()
            parser.feed(body)
            body = '\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())
            links = list(dict.fromkeys(urllib.parse.urljoin(response.url, link) for link in parser.links))
        return {'status': 'text_fetched', 'content_type': content_type, 'final_url': response.url,
                'text': body, 'links': links, 'truncated': truncated,
                'body_sha256': hashlib.sha256(raw).hexdigest()}


def fetch(entry):
    url = entry['url']
    path = OUT / (hashlib.sha256(url.encode()).hexdigest() + '.json')
    if path.exists():
        return json.loads(path.read_text())['status']
    record = {'url': url, 'attempted_at': datetime.now(timezone.utc).isoformat(),
              'review_status': 'pending_content_review', 'attempts': []}
    candidates = [url]
    parts = urllib.parse.urlsplit(url)
    segments = parts.path.strip('/').split('/')
    # Read public README text first for repository roots, retaining requested URL.
    if parts.hostname == 'github.com' and len(segments) == 2:
        owner, repo = segments
        candidates = [f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md'
                      for branch in ('HEAD',)] + candidates
    for candidate in candidates:
        try:
            result = retrieve(candidate)
            record['attempts'].append({'url': candidate, 'status': result['status']})
            record.update(result)
            break
        except (OSError, ValueError, urllib.error.URLError) as error:
            record['attempts'].append({'url': candidate, 'status': 'access_failed', 'error': str(error)[:250]})
            record['status'] = 'access_failed'
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return record['status']


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--limit', type=int, default=1000)
    parser.add_argument('--workers', type=int, default=8)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = json.loads((ROOT / 'resource-pool/sources/external-links.json').read_text())
    rows = [row for row in rows if row.get('review_status') == 'not_reviewed'][:args.limit]
    from collections import Counter
    counts = Counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for index, status in enumerate(executor.map(fetch, rows), 1):
            counts[status] += 1
            if index % 50 == 0:
                print(json.dumps({'processed': index, 'statuses': counts}), flush=True)
    print(json.dumps({'processed': len(rows), 'statuses': counts}), flush=True)


if __name__ == '__main__':
    main()
