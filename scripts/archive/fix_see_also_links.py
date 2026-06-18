#!/usr/bin/env python3
"""
Fix broken "See also" internal links (Check 35).

Rules applied in order:
  A. common-issues.md → common-issues/
  B. link ending in known-issues/  → known-issues.md
  C. link ending in ports/         → ports.md
  D. single-level link with no ../ → try adding ../ and check existence
  E. still broken                  → remove the line

Usage:
    python3 scripts/fix_see_also_links.py          # dry-run (print changes)
    python3 scripts/fix_see_also_links.py --write  # apply changes
"""

import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
WRITE = '--write' in sys.argv


def exists(page_dir, href):
    href = href.rstrip('/')
    target = os.path.normpath(os.path.join(page_dir, href))
    return (os.path.exists(target)
            or os.path.exists(target + '.md')
            or os.path.exists(os.path.join(target, 'index.md')))


def fix_href(page_dir, href):
    """Return (new_href, action) or (href, 'remove')."""
    if href.startswith(('http', 'mailto', '#', '/')):
        return href, None

    # A: common-issues.md → common-issues/
    if href == 'common-issues.md':
        if exists(page_dir, 'common-issues/'):
            return 'common-issues/', 'fixed'

    # B: */known-issues/ → */known-issues.md
    if re.search(r'known-issues/?$', href):
        new = re.sub(r'known-issues/?$', 'known-issues.md', href)
        if exists(page_dir, new):
            return new, 'fixed'

    # C: */ports/ → */ports.md
    if href.rstrip('/').endswith('/ports') or href == 'ports/':
        new = href.rstrip('/').rstrip('ports').rstrip('/') + '/ports.md'
        # simpler: just replace trailing ports/ with ports.md
        new = re.sub(r'ports/?$', 'ports.md', href)
        if exists(page_dir, new):
            return new, 'fixed'

    # Already valid
    if exists(page_dir, href):
        return href, None

    # D: try adding ../
    if not href.startswith('..') and not '/' in href.lstrip('./'):
        new = '../' + href
        if exists(page_dir, new):
            return new, 'fixed'
    # Also try ../ for multi-segment links that don't start with ..
    if not href.startswith('..'):
        new = '../' + href
        if exists(page_dir, new):
            return new, 'fixed'

    # E: nothing works — remove
    return href, 'remove'


def process_file(path):
    content = open(path, errors='replace').read()
    if '## See also' not in content:
        return 0

    page_dir = os.path.dirname(path)
    rel = os.path.relpath(path, DOCS)

    # Split on ## See also, preserve everything before it
    parts = re.split(r'(## See also\n)', content, maxsplit=1)
    if len(parts) < 3:
        return 0

    before, header, after = parts[0], parts[1], parts[2]

    # Split after into the See also block and the rest (next ## heading or EOF)
    block_match = re.match(r'(.*?)(\n##|\Z)', after, re.DOTALL)
    if not block_match:
        return 0

    see_block = block_match.group(1)
    remainder = after[block_match.end(1):]

    new_lines = []
    changes = 0

    for line in see_block.splitlines(keepends=True):
        m = re.search(r'\[([^\]]*)\]\(([^)]+)\)', line)
        if not m:
            new_lines.append(line)
            continue

        link_text, href = m.group(1), m.group(2)
        new_href, action = fix_href(page_dir, href)

        if action is None:
            new_lines.append(line)
        elif action == 'fixed':
            new_line = line[:m.start(2)] + new_href + line[m.end(2):]
            new_lines.append(new_line)
            print(f'  FIX  {rel}: "{href}" → "{new_href}"')
            changes += 1
        elif action == 'remove':
            print(f'  DROP {rel}: "{href}" (no target found)')
            changes += 1
            # skip this line

    new_content = before + header + ''.join(new_lines) + remainder

    if changes and WRITE:
        with open(path, 'w') as f:
            f.write(new_content)

    return changes


total = 0
for root, dirs, files in os.walk(DOCS):
    dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
    for fname in sorted(files):
        if fname.endswith('.md'):
            path = os.path.join(root, fname)
            total += process_file(path)

mode = 'APPLIED' if WRITE else 'DRY RUN'
print(f'\n[{mode}] {total} changes across all files')
if not WRITE:
    print('Re-run with --write to apply.')
