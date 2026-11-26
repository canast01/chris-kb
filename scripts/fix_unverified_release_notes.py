#!/usr/bin/env python3
"""Flag unverified release-notes version tables and remove dead "(#)" links.

Background (2026-11-25, cert-KB Phase A): every docs/**/release-notes.md was
generated from one template whose version tables link each row to
"[Release Notes](#)" -- a dead link -- and several tables contain invented
versions/dates (e.g. "COD 3.2", "DCNM 12.x", "90-day max validity enforcement").
Real URLs can't be invented, so this script:

  1. replaces every "[Release Notes](#)" cell with "Not yet verified";
  2. inserts a warning admonition under "## Version History" saying the table
     has not been checked against the vendor's official release notes.

Phase B replaces each table with verified data and removes the warning.
site_audit.py Check 71 enforces both rules. Idempotent.

Usage: python3 scripts/fix_unverified_release_notes.py [--apply]
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
DEAD = '[Release Notes](#)'
MARKER = 'Unverified version history'
WARNING = (
    f'!!! warning "{MARKER}"\n'
    '    This table has not yet been checked against the vendor\'s official release\n'
    '    notes. Treat the versions, dates and summaries below as unconfirmed until\n'
    '    they are verified.\n'
)


def fix(text):
    """Return (new_text, dead_links_removed, warning_added)."""
    n = text.count(DEAD)
    text = text.replace(DEAD, 'Not yet verified')
    added = False
    if MARKER not in text and '\n## Version History\n' in text:
        text = text.replace('\n## Version History\n',
                            '\n## Version History\n\n' + WARNING, 1)
        added = True
    return text, n, added


def main():
    apply = '--apply' in sys.argv
    files = links = warns = 0
    for root, dirs, fs in os.walk(DOCS):
        dirs.sort()
        if 'release-notes.md' not in fs:
            continue
        p = os.path.join(root, 'release-notes.md')
        old = open(p, encoding='utf-8').read()
        new, n, added = fix(old)
        if new != old:
            files += 1
            links += n
            warns += added
            if apply:
                open(p, 'w', encoding='utf-8').write(new)
    mode = 'APPLIED' if apply else 'DRY RUN (use --apply)'
    print(f'{mode}: {files} files, {links} dead links replaced, {warns} warnings added')


if __name__ == '__main__':
    main()
