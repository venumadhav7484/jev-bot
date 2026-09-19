"""Account for captured attachment URLs without equating access with inspection."""
import argparse
import concurrent.futures
import csv
import hashlib
import json
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import re
from fetch_evidence import Redirects, public_url

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'research/media'


def review_is_complete(review):
    """A sampled clip or access attempt cannot close an attachment gap."""
    return bool(review) and review.get('complete', True) is True and review.get('status') in {
        'image_visually_reviewed', 'video_fully_reviewed', 'document_reviewed',
        'file_content_reviewed', 'audio_fully_reviewed',
    }


def validate_review_provenance(messages, reviews):
    observed = set()
    for row in messages:
        for url in row['attachment_urls']:
            match = re.search(r'/attachments/\d+/(\d+)/', url)
            if match:
                observed.add((row['message_id'], match[1]))
    seen = set()
    for review in reviews:
        key = (review['message_id'], review['attachment_id'])
        if key not in observed:
            raise ValueError(f'Media review does not match captured message/attachment pair: {key}')
        if key in seen:
            raise ValueError(f'Duplicate media review: {key}')
        seen.add(key)


def probe(url):
    path = OUT/(hashlib.sha256(url.encode()).hexdigest()+'.json')
    if path.exists():
        return json.loads(path.read_text())
    result = {'url': url, 'checked_at': datetime.now(timezone.utc).isoformat(),
              'review_status': 'content_not_inspected', 'method': 'HTTP_HEAD'}
    try:
        request = urllib.request.Request(public_url(url), method='HEAD')
        with urllib.request.build_opener(Redirects()).open(request, timeout=12) as response:
            result.update(access_status='accessible', http_status=response.status,
                          content_type=response.headers.get_content_type(),
                          bytes=response.headers.get('Content-Length'), final_url=response.url)
    except (OSError, ValueError) as error:
        result.update(access_status='access_failed', error=str(error)[:300],
                      next_action='Reopen original source message for a fresh attachment URL; do not infer media content from filename.')
    path.write_text(json.dumps(result, indent=2)+'\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true', help='Use saved access probes only; do not make network requests.')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    messages = json.loads((ROOT/'research/triage/media-backlog.json').read_text())['entries']
    urls = sorted({url for row in messages for url in row['attachment_urls']})
    if args.offline:
        records = []
        for url in urls:
            path = OUT/(hashlib.sha256(url.encode()).hexdigest()+'.json')
            records.append(json.loads(path.read_text()) if path.exists() else
                           {'url': url, 'access_status': 'not_attempted', 'review_status': 'content_not_inspected'})
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            records = list(executor.map(probe, urls))
    by_url = {r['url']:r for r in records}
    reviews_path = ROOT/'resource-pool/sources/media-reviews.json'
    reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else []
    validate_review_provenance(messages, reviews)
    reviewed = {(r['message_id'], r['attachment_id']): r for r in reviews}
    editorial_path = ROOT/'resource-pool/sources/editorial-review.json'
    editorial = json.loads(editorial_path.read_text()) if editorial_path.exists() else {}
    cases_for = {}
    with (ROOT/'resource-pool/cases.tsv').open() as handle:
        for case in csv.DictReader(handle, delimiter='\t'):
            for mid in case['message_ids'].split(','):
                cases_for.setdefault(mid, []).append(case['id'])
    for row in messages:
        row['attachments'] = []
        for url in row['attachment_urls']:
            attachment = dict(by_url[url])
            match = re.search(r'/attachments/\d+/(\d+)/', url)
            review = reviewed.get((row['message_id'], match[1])) if match else None
            if review:
                attachment['content_review'] = review
                attachment['review_status'] = review['status']
            row['attachments'].append(attachment)
        complete = sum(review_is_complete(r.get('content_review')) for r in row['attachments'])
        touched = any('content_review' in r for r in row['attachments'])
        row['case_ids'] = cases_for.get(row['message_id'], [])
        decision = editorial.get(row['message_id'], {})
        row['text_disposition'] = decision.get('status', 'cited_in_case' if row['case_ids'] else 'unclassified')
        row['text_disposition_reason'] = decision.get('reason', 'See associated curated case.')
        row['status'] = ('content_reviewed' if complete == len(row['attachments']) else
                         'partially_reviewed' if touched else 'content_review_pending')
        # Text relevance and HTTP access never silently close a media review.
        row['remaining_attachments'] = len(row['attachments']) - complete
    reviewed_urls = {a['url'] for r in messages for a in r['attachments']
                     if review_is_complete(a.get('content_review'))}
    document = {'scope': 'Saved attachment URLs only; HEAD access is not visual, audio, video or file-content review.',
                'unique_urls': len(urls), 'messages': len(messages), 'access_counts': dict(Counter(r['access_status'] for r in records)),
                'content_review_counts': dict(Counter(r['status'] for r in messages)),
                'attachments_reviewed': len(reviewed_urls),
                'attachments_pending': len(urls) - len(reviewed_urls),
                'entries': messages}
    (ROOT/'resource-pool/sources/media-accounting.json').write_text(json.dumps(document, indent=2)+'\n')
    print(json.dumps({k:v for k,v in document.items() if k!='entries'}))


if __name__ == '__main__':
    main()
