#!/usr/bin/env python3
"""
Fix ASCII diagrams that are not properly wrapped in a code fence.

Tracks fence parity (open/close alternation) to correctly identify
whether the ``` before a diagram is an OPEN or CLOSE fence.
If it's a CLOSE fence (the diagram is outside), inserts open+close fences.
"""
import glob, sys

FULL_WIDTH_MIN = 100


def fence_parity_before(lines, target_line):
    """
    Count plain ``` fences before target_line.
    Odd count = we're inside a fence. Even count = we're outside.
    Returns True if outside (even count of plain fences before target).
    """
    count = 0
    in_fence = False
    fence_char = None
    for i in range(target_line):
        stripped = lines[i].strip()
        if not in_fence:
            if stripped.startswith('```') or stripped.startswith('~~~'):
                in_fence = True
                fence_char = stripped[:3]
        else:
            if stripped == fence_char:
                in_fence = False
    return not in_fence  # True = outside fence


def process_file(path, dry_run=False):
    with open(path) as f:
        lines = f.readlines()

    outer_tops = [i for i, l in enumerate(lines)
                  if l.startswith('┌') and len(l) >= FULL_WIDTH_MIN]
    outer_bots = [i for i, l in enumerate(lines)
                  if l.startswith('└') and len(l) >= FULL_WIDTH_MIN]

    if not outer_tops or len(outer_tops) > 1:
        return 'skip'

    t = outer_tops[0]
    b = outer_bots[0] if outer_bots else None
    if b is None:
        return 'skip'

    # Check if diagram is outside a fence using parity tracking
    outside = fence_parity_before(lines, t)
    if not outside:
        return 'already_fenced'

    # Check if there's already a close fence right after b
    fences_after = [i for i, l in enumerate(lines)
                    if i > b and i <= b + 3 and l.strip() == '```']

    # Insert open fence before t, close fence after b
    new_lines = lines[:t] + ['```\n'] + lines[t:b + 1] + ['```\n'] + lines[b + 1:]

    if not dry_run:
        with open(path, 'w') as f:
            f.writelines(new_lines)

    return 'fixed'


def main():
    dry_run = '--dry-run' in sys.argv
    pages = sorted(glob.glob('docs/**/*.md', recursive=True))

    counts = {}
    for p in pages:
        r = process_file(p, dry_run=dry_run)
        counts[r] = counts.get(r, 0) + 1

    mode = 'DRY RUN' if dry_run else 'APPLIED'
    print(f"[{mode}]")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")


if __name__ == '__main__':
    main()
