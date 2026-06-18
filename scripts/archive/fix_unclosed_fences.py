#!/usr/bin/env python3
"""
Fix diagrams that have an opening ``` fence but no closing ``` after the └ bottom.
Inserts a closing ``` immediately after the └───┘ line.
"""
import glob, sys

FULL_WIDTH_MIN = 100


def fix_file(path, dry_run=False):
    with open(path) as f:
        lines = f.readlines()

    outer_bots = [i for i, l in enumerate(lines)
                  if l.startswith('└') and len(l) >= FULL_WIDTH_MIN]

    if not outer_bots:
        return 'skip'

    # Check each outer bottom for a missing close fence
    changed = False
    offset = 0

    for b_orig in outer_bots:
        b = b_orig + offset

        # Is there already a close fence within 3 lines after b?
        post_fences = [j for j in range(b + 1, min(len(lines) + offset, b + 4))
                       if lines[j].strip() == '```']
        if post_fences:
            continue  # already closed

        # Is there an open fence before this diagram?
        outer_tops = [i for i, l in enumerate(lines[:b])
                      if l.startswith('┌') and len(l) >= FULL_WIDTH_MIN]
        if not outer_tops:
            continue
        t = outer_tops[-1]
        pre_fences = [j for j in range(max(0, t - 3), t)
                      if lines[j].strip() == '```']
        if not pre_fences:
            continue  # no open fence either — skip

        # Insert close fence after b
        lines.insert(b + 1, '```\n')
        offset += 1
        changed = True

    if not changed:
        return 'no_change'

    if not dry_run:
        with open(path, 'w') as f:
            f.writelines(lines)

    return 'fixed'


def main():
    dry_run = '--dry-run' in sys.argv
    pages = sorted(glob.glob('docs/**/*.md', recursive=True))

    counts = {'fixed': 0, 'no_change': 0, 'skip': 0}
    for p in pages:
        r = fix_file(p, dry_run=dry_run)
        counts[r] = counts.get(r, 0) + 1

    print(f"Results ({'DRY RUN' if dry_run else 'APPLIED'}):")
    print(f"  Fixed unclosed fences: {counts['fixed']}")
    print(f"  No change needed:      {counts['no_change']}")
    print(f"  Skipped (no diagram):  {counts['skip']}")


if __name__ == '__main__':
    main()
