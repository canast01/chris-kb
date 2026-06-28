#!/usr/bin/env python3
"""
Fix broken directory-style See also links caused by MkDocs depth shift.
Non-index .md files (foo.md → foo/index.html) need one extra ../ in their
relative directory links. Tries prepending ../ and validates against site/.
"""
import os, re, sys
from pathlib import Path

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
SITE = os.path.join(REPO, 'site')

_SEE_ALSO = re.compile(r'(## See also\n)(.*?)(?=\n##|\Z)', re.DOTALL)
_LINK = re.compile(r'\[([^\]]+)\]\(([^)#?]+)\)')

fixed = 0
skipped = 0
unchanged = 0

for root, dirs, files in os.walk(DOCS):
    dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.cache'}]
    for fname in files:
        if not fname.endswith('.md'):
            continue
        path = os.path.join(root, fname)
        rel = os.path.relpath(path, DOCS)
        p = Path(rel)

        # Only non-index files get the depth shift
        if p.name == 'index.md':
            continue

        content = open(path).read()
        sm = _SEE_ALSO.search(content)
        if not sm:
            continue

        # Effective dir in site/ for this non-index file
        eff_dir = os.path.join(SITE, str(p.parent), p.stem)

        block = sm.group(2)
        new_block = block
        changed = False

        for lm in _LINK.finditer(block):
            href = lm.group(2)
            if href.startswith(('http', 'mailto', 'data:', '#')) or href.endswith('.md'):
                continue
            # Check if the current link is broken
            target = os.path.normpath(os.path.join(eff_dir, href))
            current_ok = (os.path.exists(target)
                          or os.path.exists(os.path.join(target, 'index.html')))
            if current_ok:
                continue
            # Try adding one ../ prefix
            new_href = '../' + href
            new_target = os.path.normpath(os.path.join(eff_dir, new_href))
            new_ok = (os.path.exists(new_target)
                      or os.path.exists(os.path.join(new_target, 'index.html')))
            if new_ok:
                old_link = f'[{lm.group(1)}]({href})'
                new_link = f'[{lm.group(1)}]({new_href})'
                new_block = new_block.replace(old_link, new_link, 1)
                changed = True
                fixed += 1
            else:
                skipped += 1

        if changed:
            new_content = content[:sm.start(2)] + new_block + content[sm.end(2):]
            open(path, 'w').write(new_content)
        else:
            unchanged += 1

print(f'Fixed: {fixed} links across pages')
print(f'Skipped (no fix found): {skipped}')
