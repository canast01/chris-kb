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


def _adjust_border(stripped: str, open_ch: str, close_ch: str, dash: str) -> str:
    """Resize a top or bottom border line to OUTER_WIDTH by trimming/extending trailing dashes."""
    if len(stripped) == OUTER_WIDTH:
        return stripped
    # Remove closing char, adjust trailing dash run, re-add closing char
    body = stripped[:-1]           # drop close_ch
    # Find last run of dashes
    rstripped = body.rstrip(dash)
    needed = OUTER_WIDTH - 1 - len(rstripped)
    if needed < 1:
        needed = 1
    return rstripped + (dash * needed) + close_ch


def fix_file(path, dry_run=False):
    with open(path) as f:
        lines = f.readlines()

    fixed = []
    changed = False
    for line in lines:
        stripped = line.rstrip('\n')

        if stripped.startswith('│') and stripped.endswith('│') and len(stripped) != OUTER_WIDTH:
            # Content line: pad/trim inner content
            without_close = stripped[:-1].rstrip()
            padded = without_close.ljust(OUTER_WIDTH - 1) + '│'
            fixed.append(padded + '\n')
            changed = True

        elif stripped.startswith('┌') and stripped.endswith('┐') and len(stripped) != OUTER_WIDTH:
            # Top border: adjust trailing dashes
            fixed.append(_adjust_border(stripped, '┌', '┐', '─') + '\n')
            changed = True

        elif stripped.startswith('└') and stripped.endswith('┘') and len(stripped) != OUTER_WIDTH:
            # Bottom border: adjust trailing dashes
            fixed.append(_adjust_border(stripped, '└', '┘', '─') + '\n')
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
