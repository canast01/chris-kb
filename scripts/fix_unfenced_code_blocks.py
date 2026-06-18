#!/usr/bin/env python3
"""
Fix code blocks that lost their opening fence.

Pattern: a line of code (shell comment, command, etc.) appears at depth=0
IMMEDIATELY AFTER a close fence (```) with no content in between other than
blank lines, followed eventually by a plain ``` close fence.

This happens when a code block's opening fence is missing. Without the opener
the content is rendered as raw Markdown — shell comments become H1 headings.

The key guard: only act when `block_closed` is True (we just saw a close fence
at depth=0). Page titles at line 1 are safe because no close fence precedes
them.

Language detection (from file path):
  powershell → powershell
  python     → python
  default    → bash

Run from repo root: python3 scripts/fix_unfenced_code_blocks.py [--dry-run]
"""
import glob, re, sys

DRY_RUN = '--dry-run' in sys.argv


def lang_for(path):
    p = path.lower()
    if '/powershell/' in p:
        return 'powershell'
    if '/python/' in p:
        return 'python'
    return 'bash'


def fix_file(path):
    with open(path) as f:
        lines = f.readlines()

    depth = 0
    block_closed = False
    inserts = []
    deletes = set()

    i = 0
    while i < len(lines):
        s = lines[i].strip()

        if s.startswith('```'):
            after = s[3:].strip()
            if depth == 0:
                depth = 1
                block_closed = False
            elif after == '':
                depth = 0
                block_closed = True
            i += 1
            continue

        if depth == 0:
            if s == '':
                # Blank lines don't reset block_closed
                i += 1
                continue

            if block_closed and re.match(r'^# \S', lines[i]):
                # Code comment immediately after a close fence: find close ahead
                close_idx = None
                for j in range(i + 1, min(i + 300, len(lines))):
                    sj = lines[j].strip()
                    if sj == '```':
                        close_idx = j
                        break
                    if re.match(r'^## ', lines[j]) and j > i + 2:
                        break

                if close_idx is not None:
                    lang = lang_for(path)
                    inserts.append((i, f'```{lang}\n'))
                    depth = 1
                    i += 1
                    block_closed = False
                    continue

            # Any non-blank, non-fence line resets block_closed
            block_closed = False

        i += 1

    if not inserts and not deletes:
        return 0

    if DRY_RUN:
        print(f'  {path}')
        for idx, txt in inserts:
            print(f'    INSERT before L{idx+1}: {txt.strip()}')
        return len(inserts)

    new_lines = list(lines)
    for ins_idx, txt in sorted(inserts, reverse=True):
        new_lines.insert(ins_idx, txt)

    with open(path, 'w') as f:
        f.writelines(new_lines)

    return len(inserts)


def verify_fences(path):
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
                    print(f'  ERROR (unclosed fence): {p}')
                else:
                    print(f'  Fixed ({n} edits): {p}')

    print(f'\n{"DRY RUN — " if DRY_RUN else ""}Files changed: {changed}')
    if errors:
        print(f'Errors: {len(errors)}')
        for e in errors:
            print(f'  {e}')
    else:
        print('All fixed files have clean fence structure.')


if __name__ == '__main__':
    main()
