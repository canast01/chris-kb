#!/usr/bin/env python3
"""
Fix remaining untagged ``` code blocks:

1. Remove empty ``` / ``` artifact pairs (leftover from duplicate removal).
2. Tag remaining untagged blocks as 'text' where the content is plain prose
   (navigation paths, formulas, banners, headings-as-text, etc.).
3. Skip blocks inside admonitions (indented ``` — handled by MkDocs separately).

Run from repo root: python3 scripts/fix_untagged_blocks.py [--dry-run]
"""
import glob, re, sys

DRY_RUN = '--dry-run' in sys.argv


def fix_file(path):
    with open(path) as f:
        original = f.read()

    lines = original.splitlines(keepends=True)
    result = []
    i = 0
    depth = 0
    changes = 0

    while i < len(lines):
        l = lines[i]
        s = l.strip()

        # Skip indented fences (inside admonitions)
        is_indented = l.startswith('    ') or l.startswith('\t')

        if (s.startswith('```') or s.startswith('~~~')) and not is_indented:
            after = s[3:].strip()

            if depth == 0:
                if after == '' and s.startswith('```'):
                    # Plain backtick open — check what follows
                    # Collect the run of consecutive ``` lines (blank lines allowed)
                    run = [i]
                    j = i + 1
                    while j < len(lines):
                        sj = lines[j].strip()
                        if sj == '```':
                            run.append(j)
                            j += 1
                        elif sj == '':
                            j += 1
                        else:
                            break

                    if len(run) >= 2:
                        # N consecutive plain ``` lines — all artifact empty blocks
                        # Drop all of them; the real block opener (```text etc.) follows
                        changes += len(run)
                        i = j
                        depth = 0
                        if not DRY_RUN and path:
                            pass  # handled via result tracking below
                        # Re-process from j without adding any of the run lines
                        continue
                    else:
                        # Single untagged open — look at first content line
                        first_content = ''
                        for k in range(i + 1, min(i + 4, len(lines))):
                            fc = lines[k].strip()
                            if fc:
                                first_content = fc
                                break

                        # Don't tag if content is box-drawing (already tagged by
                        # previous script pass or is the diagram itself)
                        is_box = first_content and any(
                            first_content.startswith(c) for c in '┌│└')
                        # Don't tag if first content is another fence (already
                        # handled above as empty run — this shouldn't happen here)
                        is_fence = first_content.startswith('```')

                        if not is_box and not is_fence and first_content:
                            # Tag as text
                            result.append('```text\n')
                            changes += 1
                            depth = 1
                            i += 1
                            continue

                depth = 1

            elif after == '':
                depth = 0

        result.append(l)
        i += 1

    if not changes:
        return 0

    new_content = ''.join(result)
    if new_content == original:
        return 0

    if DRY_RUN:
        print(f'  {path}: {changes} changes')
        return changes

    with open(path, 'w') as f:
        f.write(new_content)
    return changes


def main():
    pages = sorted(glob.glob('docs/**/*.md', recursive=True))
    changed = 0

    for p in pages:
        n = fix_file(p)
        if n:
            changed += 1
            if not DRY_RUN:
                print(f'  Fixed ({n} edits): {p}')

    print(f'\n{"DRY RUN — " if DRY_RUN else ""}Files changed: {changed}')


if __name__ == '__main__':
    main()
