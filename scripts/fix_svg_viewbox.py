#!/usr/bin/env python3
"""Add viewBox to SVGs that are missing it.

Without viewBox, CSS max-width:100% clips the SVG instead of scaling it,
causing text to appear truncated on narrower screens.
"""

import os
import re

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      'docs', 'assets')

fixed = 0
skipped = 0
errors = 0

for fname in sorted(os.listdir(ASSETS)):
    if not fname.endswith('.svg'):
        continue
    path = os.path.join(ASSETS, fname)
    try:
        text = open(path, encoding='utf-8', errors='replace').read()
    except Exception as e:
        print(f'ERROR reading {fname}: {e}')
        errors += 1
        continue

    # Already has viewBox — skip
    if 'viewBox' in text:
        skipped += 1
        continue

    # Extract width and height from the opening <svg ...> tag
    m = re.match(r'(<svg\b[^>]*?)\bwidth="(\d+)"\s+height="(\d+)"([^>]*>)', text, re.DOTALL)
    if not m:
        # Try height before width
        m = re.match(r'(<svg\b[^>]*?)\bheight="(\d+)"\s+width="(\d+)"([^>]*>)', text, re.DOTALL)
        if m:
            before, h, w, after = m.groups()
            new_tag = f'{before}viewBox="0 0 {w} {h}" width="{w}" height="{h}"{after}'
        else:
            print(f'SKIP (no w/h): {fname}')
            skipped += 1
            continue
    else:
        before, w, h, after = m.groups()
        new_tag = f'{before}width="{w}" height="{h}" viewBox="0 0 {w} {h}"{after}'

    new_text = text[:m.start()] + new_tag + text[m.end():]
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        fixed += 1
    except Exception as e:
        print(f'ERROR writing {fname}: {e}')
        errors += 1

print(f'Fixed: {fixed}  |  Already had viewBox: {skipped}  |  Errors: {errors}')
