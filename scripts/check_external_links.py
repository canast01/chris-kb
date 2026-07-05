"""
Validate all external (http/https) links referenced anywhere in docs/ and
report which ones are actually dead, using concurrent requests.

Why not just use `site_audit.py --check-links`: that check is a plain
sequential loop with an 8s timeout per URL. For ~1,100 URLs that's up to
~2.4 hours worst-case, which is almost certainly why it has never actually
been run in practice despite existing. This script does the same HTTP
HEAD/GET check but with a thread pool, typically finishing in 1-3 minutes.

Usage:
  python3 scripts/check_external_links.py                # check all, print report
  python3 scripts/check_external_links.py --workers 30    # tune concurrency
"""
import re
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

URL_RE = re.compile(r'https?://[^\s\)\]"\'<>]+')
TIMEOUT = 8


def collect_urls():
    urls = {}  # url -> list of files referencing it
    for path in Path('docs').rglob('*.md'):
        text = path.read_text(errors='replace')
        for m in URL_RE.finditer(text):
            url = m.group(0).rstrip('.,;)>')
            urls.setdefault(url, []).append(str(path))
    return urls


def check_one(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
    try:
        resp = urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CONTEXT)
        return url, resp.status, None
    except urllib.error.HTTPError as e:
        if e.code == 405:  # HEAD not allowed, retry with GET
            try:
                req2 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                resp2 = urllib.request.urlopen(req2, timeout=TIMEOUT, context=SSL_CONTEXT)
                return url, resp2.status, None
            except Exception as e2:
                return url, None, str(e2)
        return url, e.code, None
    except Exception as e:
        return url, None, str(e)


def main():
    workers = 20
    if '--workers' in sys.argv:
        workers = int(sys.argv[sys.argv.index('--workers') + 1])

    url_map = collect_urls()
    print(f'Checking {len(url_map)} unique external URLs with {workers} workers...\n')

    dead = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(check_one, url): url for url in url_map}
        done = 0
        for fut in as_completed(futures):
            url, status, err = fut.result()
            done += 1
            if err or (status and status >= 400):
                dead.append((url, status, err, url_map[url]))
            if done % 100 == 0:
                print(f'  ...{done}/{len(url_map)} checked')

    print(f'\n{len(dead)}/{len(url_map)} URLs appear dead or errored:\n')
    for url, status, err, files in sorted(dead):
        reason = f'HTTP {status}' if status else err
        print(f'{reason}: {url}')
        for f in files[:3]:
            print(f'    referenced by {f}')
        if len(files) > 3:
            print(f'    ...and {len(files) - 3} more')


if __name__ == '__main__':
    sys.exit(main())
