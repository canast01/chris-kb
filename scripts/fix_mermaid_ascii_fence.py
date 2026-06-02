#!/usr/bin/env python3
"""
Fix KB pages where an ASCII diagram immediately follows any code-block
close-fence with no opening fence of its own.

Pattern found (3 variants):
  ```lang
  ...code...
  ```
  ┌─── ASCII diagram (NO opening ``` here!) ───┐
  │ ...
  └───────────────────────────────────────────┘
  ```         <- intended to close ASCII block (variant A: next line is non-fence)
  ```         <- variant B: spurious extra plain ``` immediately after
  ```lang     <- variant C: spurious ``` + language tag immediately after

Fix:
  1. Insert ``` before the ┌ line
  2. If the 2nd non-blank line after └ is also a ``` (with or without lang) → delete it

Run from repo root: python3 scripts/fix_mermaid_ascii_fence.py [--dry-run]
"""
import glob, os, re, sys

DRY_RUN = '--dry-run' in sys.argv


def fix_file(path):
    with open(path) as f:
        lines = f.readlines()

    depth = 0
    block_closed = False
    inserts = []   # (line_idx, text)
    deletes = set()  # line indices to remove

    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith('```'):
            after = s[3:].strip()
            if depth == 0:
                depth = 1
                block_closed = False
            elif after == '':
                block_closed = True
                depth = 0
        elif depth == 0 and block_closed and s.startswith('┌'):
            # Unguarded ASCII diagram — insert opening fence before this line
            inserts.append((i, '```\n'))
            block_closed = False

            # Locate the diagram's closing └
            for j in range(i + 1, len(lines)):
                if lines[j].startswith('└'):
                    # Collect up to 3 non-blank lines after └
                    non_blank = []
                    for k in range(j + 1, min(j + 8, len(lines))):
                        if lines[k].strip():
                            non_blank.append((k, lines[k].strip()))
                            if len(non_blank) == 2:
                                break
                    # non_blank[0] = ``` that closes ASCII block (always present)
                    # non_blank[1] = if it's also a fence, it's spurious → delete
                    if (len(non_blank) >= 2
                            and non_blank[1][1].startswith('```')):
                        deletes.add(non_blank[1][0])
                    break
        elif depth == 0 and s and not s.startswith('#') and not s.startswith('<'):
            block_closed = False

    if not inserts and not deletes:
        return 0

    if DRY_RUN:
        print(f'  {path}')
        for idx, txt in inserts:
            print(f'    INSERT before L{idx+1}: {txt.strip()}')
        for idx in sorted(deletes):
            print(f'    DELETE L{idx+1}: {lines[idx].strip()}')
        return len(inserts) + len(deletes)

    # Apply: deletes first (in reverse), then inserts (adjusted)
    new_lines = list(lines)
    for idx in sorted(deletes, reverse=True):
        del new_lines[idx]

    for ins_idx, txt in sorted(inserts, reverse=True):
        adj = sum(1 for d in deletes if d < ins_idx)
        new_lines.insert(ins_idx - adj, txt)

    with open(path, 'w') as f:
        f.writelines(new_lines)

    return len(inserts) + len(deletes)


def verify_fences(path):
    """Return final fence depth (0 = clean)."""
    with open(path) as f:
        lines = f.readlines()
    depth = 0
    for l in lines:
        s = l.strip()
        if not s.startswith('```'):
            continue
        after = s[3:].strip()
        if depth == 0:
            depth = 1
        elif after == '':
            depth = 0
    return depth


def main():
    pages = sorted(glob.glob('docs/**/*.md', recursive=True))
    changed = 0
    errors = []

    for p in pages:
        n = fix_file(p)
        if n:
            changed += 1
            if not DRY_RUN:
                depth = verify_fences(p)
                if depth != 0:
                    errors.append(p)
                    print(f'  ERROR (unclosed fence after fix): {p}')
                else:
                    print(f'  Fixed ({n} edits): {p}')

    print(f'\n{"DRY RUN — " if DRY_RUN else ""}Files changed: {changed}')
    if errors:
        print(f'Errors (unclosed fences): {len(errors)}')
    else:
        print('All fixed files have clean fence structure.')


if __name__ == '__main__':
    main()
