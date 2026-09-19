"""Recognize private provenance without loading private project inputs."""
from urllib.parse import unquote, urlsplit


def normalized_location(url):
    parts = urlsplit(url)
    return (parts.hostname or '').lower(), unquote(parts.path).rstrip('/')


def private_artifact_roots(urls):
    roots = set()
    for url in urls:
        host, path = normalized_location(url)
        if host in ('github.com', 'www.github.com'):
            # A private PR or branch implies the repository is private too.
            path = '/' + '/'.join(path.strip('/').split('/')[:2])
            host = 'github.com'
        roots.add((host, path.casefold()))
    return roots


def is_private_artifact(url, roots):
    host, path = normalized_location(url)
    parts = path.strip('/').split('/')
    if host == 'www.github.com':
        host = 'github.com'
    if host == 'raw.githubusercontent.com' and len(parts) >= 2:
        host, path = 'github.com', '/' + '/'.join(parts[:2])
    path = path.casefold()
    return any(host == private_host and
               (path == private_path or path.startswith(private_path + '/'))
               for private_host, private_path in roots)


def is_discord_url(url):
    host = (urlsplit(url).hostname or '').lower()
    return any(host == domain or host.endswith('.' + domain)
               for domain in ('discord.com', 'discordapp.com', 'discordapp.net', 'discord.gg'))
