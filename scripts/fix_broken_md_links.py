#!/usr/bin/env python3
"""
Fix broken .md See also links where the target file doesn't exist in docs/.
Strategy 1: strip one ../ prefix and check again.
Strategy 2: apply known path corrections for restructured sections.
"""
import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')

_SEE_ALSO = re.compile(r'(## See [Aa]lso\n)(.*?)(?=\n##|\Z)', re.DOTALL)
_MD_LINK = re.compile(r'(\[([^\]]+)\]\(([^)#?]+\.md)\))')

# Known path corrections: (wrong_pattern, correct_replacement) — applied as string replacement
PATH_FIXES = {
    '../../vmware/vsan/index.md': '../../virtualization/vmware/vsan/index.md',
    '../../vmware/vcenter/index.md': '../../virtualization/vmware/vcenter/index.md',
    '../../storage/ontap/index.md': '../../storage/netapp/ontap/index.md',
    '../../../compute/vmware/nsx/security/index.md': '../../virtualization/vmware/nsx/security/index.md',
}


def target_exists(src_dir, href):
    stem = href[:-3]
    tgt = os.path.normpath(os.path.join(src_dir, stem))
    return (os.path.exists(tgt + '.md')
            or os.path.exists(os.path.join(tgt, 'index.md')))


fixed = 0
skipped = 0

for root, dirs, files in os.walk(DOCS):
    dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.cache'}]
    for fname in files:
        if not fname.endswith('.md'):
            continue
        path = os.path.join(root, fname)
        src_dir = os.path.dirname(path)
        content = open(path).read()
        sm = _SEE_ALSO.search(content)
        if not sm:
            continue

        block = sm.group(2)
        new_block = block
        changed = False

        for m in _MD_LINK.finditer(block):
            full, text, href = m.group(1), m.group(2), m.group(3)
            if target_exists(src_dir, href):
                continue  # already fine

            new_href = None

            # Strategy 1: known path corrections
            if href in PATH_FIXES:
                candidate = PATH_FIXES[href]
                if target_exists(src_dir, candidate):
                    new_href = candidate

            # Strategy 2: strip one or two ../ prefixes
            if new_href is None:
                cand = href
                for _ in range(2):
                    if not cand.startswith('../'):
                        break
                    cand = cand[3:]
                    if target_exists(src_dir, cand):
                        new_href = cand
                        break

            if new_href:
                old = f'[{text}]({href})'
                new = f'[{text}]({new_href})'
                new_block = new_block.replace(old, new, 1)
                changed = True
                fixed += 1
            else:
                skipped += 1

        if changed:
            new_content = content[:sm.start(2)] + new_block + content[sm.end(2):]
            open(path, 'w').write(new_content)

print(f'Fixed: {fixed}  Skipped: {skipped}')
