"""
Validate real external reference links (markdown `[text](https://...)` links
in prose, e.g. "See also" sections and inline citations) using concurrent
requests. Deliberately does NOT check bare URLs inside code fences or
illustrative example hostnames -- this KB's command/config examples are
full of intentionally-fake addresses (10.0.1.10, jira.company.local,
*.example.com, 169.254.169.254 cloud metadata, localhost:PORT, etc.) that
were never meant to resolve. An earlier version of this script treated
every http(s):// substring anywhere in the file as a real link and got
1441/1666 "dead" results -- almost all of them were these intentional
examples, not real link rot.

Usage:
  python3 scripts/check_external_links.py                # check all, print report
  python3 scripts/check_external_links.py --workers 25    # tune concurrency
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

# Only a real markdown link `[text](https://...)`, not a bare URL substring
# -- this is what actually renders as a clickable reference on the page.
MD_LINK_RE = re.compile(r'\[([^\]]*)\]\((https?://[^)\s]+)\)')
FENCE_RE = re.compile(r'^(```|~~~)', re.MULTILINE)
TIMEOUT = 8

# Known-illustrative hostnames/patterns that occasionally leak into real
# markdown links (rare, but happens in "example config" style callouts) --
# skip these even outside code fences since they're never real.
PLACEHOLDER_RE = re.compile(
    r'://(localhost|127\.|0\.0\.0\.0|10\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.|169\.254\.|'
    r'[\w.-]*\.(example|internal|local|corp\.example)\b|[\w-]+-svc\b|[\w-]+\.company\.local)',
    re.IGNORECASE,
)


def strip_code_fences(text: str) -> str:
    """Blank out fenced code blocks (preserving line count/offsets aren't
    needed here since we only care about presence, not position)."""
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith(('```', '~~~')):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return '\n'.join(out)


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / 'docs'


def collect_urls():
    urls = {}  # url -> list of files referencing it
    for path in DOCS_DIR.rglob('*.md'):
        text = path.read_text(errors='replace')
        prose = strip_code_fences(text)
        for m in MD_LINK_RE.finditer(prose):
            url = m.group(2).rstrip('.,;)>')
            if PLACEHOLDER_RE.search(url):
                continue
            if '[' in url:  # malformed/truncated template placeholder, e.g. https://[instance]...
                continue
            urls.setdefault(url, []).append(str(path.relative_to(REPO_ROOT)))
    return urls


def check_one(url):
    # GET, not HEAD: several vendor sites (confirmed: mysupport.netapp.com)
    # return 404 to HEAD but 200 to GET -- a small enough URL set (dozens, not
    # thousands) that the HEAD optimization isn't worth the false positives.
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CONTEXT)
        return url, resp.status, None
    except urllib.error.HTTPError as e:
        return url, e.code, None
    except Exception as e:
        return url, None, str(e)


def main():
    workers = 20
    if '--workers' in sys.argv:
        workers = int(sys.argv[sys.argv.index('--workers') + 1])

    url_map = collect_urls()
    print(f'Checking {len(url_map)} unique real reference links with {workers} workers...\n')

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
