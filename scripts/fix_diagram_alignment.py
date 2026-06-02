#!/usr/bin/env python3
"""
Fix ASCII diagram box alignment in KB markdown files.

Outer box lines (start and end with │) must be exactly 105 chars wide.
Lines that are shorter get right-padded with spaces before the closing │.
Lines that are longer get trimmed.

Uses Python len() (Unicode code points) — not byte length — so box-drawing
characters (─ │ → — ·) count as 1, same as displayed.
"""
import glob, sys

OUTER_WIDTH = 105   # │ + 103 content chars + │


def fix_file(path, dry_run=False):
    with open(path) as f:
        lines = f.readlines()

    fixed = []
    changed = False
    for line in lines:
        stripped = line.rstrip('\n')
        if stripped.startswith('│') and stripped.endswith('│') and len(stripped) != OUTER_WIDTH:
            without_close = stripped[:-1].rstrip()
            padded = without_close.ljust(OUTER_WIDTH - 1) + '│'
            fixed.append(padded + '\n')
            changed = True
        else:
            fixed.append(line)

    if changed and not dry_run:
        with open(path, 'w') as f:
            f.writelines(fixed)

    return changed


def main():
    dry_run = '--dry-run' in sys.argv
    pages = sorted(glob.glob('docs/**/*.md', recursive=True))

    fixed_files = []
    for p in pages:
        if fix_file(p, dry_run=dry_run):
            fixed_files.append(p)

    if fixed_files:
        label = 'DRY RUN' if dry_run else 'FIXED'
        for p in fixed_files:
            print(f"  [{label}] {p}")
    else:
        print("  No alignment issues found.")


if __name__ == '__main__':
    main()
