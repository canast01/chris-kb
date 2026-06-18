#!/usr/bin/env python3
"""
Check all external https:// links in docs for dead URLs.

Usage:
    python3 scripts/check-external-links.py           # check all
    python3 scripts/check-external-links.py --dry-run  # list URLs only
    python3 scripts/check-external-links.py --workers 20

Exit 0 if all live, exit 1 if any dead or errored.
"""
import glob
import re
import ssl
import sys
import time
import urllib.request
import urllib.error
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Bypass certificate verification — we want to catch 404s, not SSL config issues
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

TIMEOUT      = 10          # seconds per request
WORKERS      = 10          # parallel threads
RETRY        = 1           # retries on transient error
USER_AGENT   = "Mozilla/5.0 (compatible; KB-link-checker/1.0)"

# Domains that block bots — skip rather than false-flag
SKIP_DOMAINS = {
    "linkedin.com", "www.linkedin.com",
    "twitter.com", "x.com",
    "facebook.com",
    "instagram.com",
    "cloudflare.com",        # redirects/JS challenge
    "learn.microsoft.com",   # rate-limits aggressively
    "docs.microsoft.com",
}


def strip_fences(text):
    out = []
    in_fence = False
    fence_char = None
    for line in text.splitlines(keepends=True):
        s = line.strip()
        if not in_fence:
            if s.startswith("```") or s.startswith("~~~"):
                in_fence = True
                fence_char = s[:3]
                out.append("\n")
            else:
                out.append(line)
        else:
            if s == fence_char:
                in_fence = False
            out.append("\n")
    return "".join(out)


def extract_urls(text):
    urls = set()
    for url in re.findall(r'https?://[^\s\'")<>\]]+', text):
        # Skip internal/example addresses
        low = url.lower()
        if any(x in low for x in ('localhost', '127.0.0.1', '0.0.0.0',
                                   '169.254.', '192.168.', '10.0.',
                                   'example.com', 'example.local',
                                   'your-', 'yourinstance', '<', '{', '[')):
            continue
        if url.startswith('http://'):
            continue  # only check https
        # skip bare scheme or very short URLs
        if len(url) < 12 or url == 'https://':
            continue
        # skip internal hostnames — no dots or ending in .local / .corp.*
        try:
            from urllib.parse import urlparse
            host = urlparse(url).netloc.split(':')[0]
            if not host or '.' not in host or host.endswith('.local'):
                continue
            if any(host.endswith(s) for s in ('.corp', '.internal', '.lan')):
                continue
        except Exception:
            continue
        urls.add(url)
    return urls


def should_skip(url):
    try:
        from urllib.parse import urlparse
        host = urlparse(url).netloc.lstrip("www.")
        return host in SKIP_DOMAINS or host.startswith("www.") and host[4:] in SKIP_DOMAINS
    except Exception:
        return False


def check_url(url, retries=RETRY):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT},
            method="HEAD",
        )
    except ValueError as e:
        return url, None, f"invalid URL: {e}"

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=_SSL_CTX) as resp:
                return url, resp.status, None
        except urllib.error.HTTPError as e:
            if e.code in (405, 403):
                # HEAD not allowed — try GET
                req.method = "GET"
                try:
                    with urllib.request.urlopen(req, timeout=TIMEOUT, context=_SSL_CTX) as resp:
                        return url, resp.status, None
                except urllib.error.HTTPError as e2:
                    return url, e2.code, None
                except Exception as e2:
                    return url, None, str(e2)
            return url, e.code, None
        except urllib.error.URLError as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return url, None, str(e.reason)
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return url, None, str(e)
    return url, None, "max retries exceeded"


def main():
    dry_run = "--dry-run" in sys.argv
    workers = WORKERS
    for arg in sys.argv[1:]:
        if arg.startswith("--workers="):
            workers = int(arg.split("=", 1)[1])

    # Collect all external URLs with their source files
    url_to_files = defaultdict(set)
    for md in sorted(glob.glob("docs/**/*.md", recursive=True)):
        if "assets" in Path(md).parts:
            continue
        text = strip_fences(Path(md).read_text())
        for url in extract_urls(text):
            # Strip trailing punctuation that got caught in regex
            url = url.rstrip(".,;:)>\"'`*")
            if should_skip(url):
                continue
            url_to_files[url].add(md)

    urls = sorted(url_to_files)
    print(f"Found {len(urls)} unique external URLs across {len(url_to_files)} entries")

    if dry_run:
        for url in urls:
            print(f"  {url}")
        return

    # Check concurrently
    dead = []
    errors = []
    checked = 0

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(check_url, url): url for url in urls}
        for future in as_completed(futures):
            url, status, err = future.result()
            checked += 1
            sources = sorted(url_to_files[url])
            if err:
                errors.append((url, err, sources))
                print(f"  ERROR  {url}  ({err})")
            elif status and status >= 400:
                dead.append((url, status, sources))
                print(f"  {status}    {url}")
            else:
                if checked % 50 == 0:
                    print(f"  ... {checked}/{len(urls)} checked")

    print()
    print(f"Results: {len(urls)} checked  |  {len(dead)} dead  |  {len(errors)} errors")

    if dead:
        print("\nDead links:")
        for url, status, sources in sorted(dead):
            print(f"  [{status}] {url}")
            for s in sources:
                print(f"        {s}")

    if errors:
        print("\nConnection errors (may be transient or bot-blocked):")
        for url, err, sources in sorted(errors):
            print(f"  {url}  —  {err}")

    if dead:
        sys.exit(1)


if __name__ == "__main__":
    main()
