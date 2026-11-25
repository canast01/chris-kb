#!/usr/bin/env python3
"""
Fix ASCII diagram box alignment in KB markdown files.

Outer box lines (start and end with │) must be exactly 105 chars wide.
Lines that are shorter get right-padded with spaces before the closing │.
Lines that are longer are left alone (padding can't shrink them).

Multi-column tables (e.g. `aws ... --output table` sample output) are skipped:
from a ┌ border containing ┬ through the next └ border. Padding a table row
would push the last column's border out of line.
A file is only reported/rewritten when its content actually changes; before
2026-11-25 every over-wide line set "changed", so the pre-commit hook printed
[FIXED] for a file it never modified.

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
    in_table = False
    for line in lines:
        stripped = line.rstrip('\n')

        # A box whose top border has column junctions (┌──┬──┐) is a table:
        # leave every line through its └ border untouched. Row-level detection
        # (inner │) would also catch nested boxes in diagrams, which DO need padding.
        if stripped.startswith('┌') and '┬' in stripped:
            in_table = True
        if in_table:
            fixed.append(line)
            if stripped.startswith('└'):
                in_table = False
            continue

        if len(stripped) == OUTER_WIDTH:
            fixed.append(line)

        elif stripped.startswith('│') and stripped.endswith('│'):
            # Content line: pad inner content
            without_close = stripped[:-1].rstrip()
            fixed.append(without_close.ljust(OUTER_WIDTH - 1) + '│\n')

        elif stripped.startswith('┌') and stripped.endswith('┐'):
            # Top border: adjust trailing dashes
            fixed.append(_adjust_border(stripped, '┌', '┐', '─') + '\n')

        elif stripped.startswith('└') and stripped.endswith('┘'):
            # Bottom border: adjust trailing dashes
            fixed.append(_adjust_border(stripped, '└', '┘', '─') + '\n')

        else:
            fixed.append(line)

    # Compare output, not intent: a "fix" that reproduces the line is no change.
    # (Lines lacking a trailing newline get one added above; only real diffs count.)
    changed = [l.rstrip('\n') for l in fixed] != [l.rstrip('\n') for l in lines]
    if changed and not dry_run:
        with open(path, 'w') as f:
            f.writelines(fixed)

    return changed


def selftest():
    """Regression cases (2026-11-25: false [FIXED] on over-wide AWS CLI tables)."""
    import os, tempfile
    W = OUTER_WIDTH
    table = '┌────┬────┐\n│ a  │ b  │\n├────┼────┤\n│ 1  │ 2  │\n└────┴────┘\n'
    over = '│' + 'x' * 130 + '│\n'
    cases = [
        # (name, input, expect_changed, check(output))
        ('short box padded to 105', '┌──┐\n│ hi │\n└──┘\n', True,
         lambda o: all(len(l) == W for l in o.splitlines())),
        ('nested-box row still padded', '│ │ inner │ │\n', True,
         lambda o: len(o.splitlines()[0]) == W),
        ('table untouched, not reported', table, False, lambda o: o == table),
        ('over-wide line: no false FIXED', over, False, lambda o: o == over),
        ('clean file not reported', '│' + ' ' * (W - 2) + '│\n', False, lambda o: True),
        ('line after table still fixed', table + '│ after │\n', True,
         lambda o: o.startswith(table) and len(o.splitlines()[-1]) == W),
    ]
    failed = 0
    with tempfile.TemporaryDirectory() as d:
        for i, (name, text, want, check) in enumerate(cases):
            p = os.path.join(d, f'{i}.md')
            with open(p, 'w') as fh:
                fh.write(text)
            got = fix_file(p)
            with open(p) as fh:
                ok = got == want and check(fh.read())
            failed += not ok
            print(f"  {'PASS' if ok else 'FAIL'} {name}")
    print(f"selftest: {len(cases) - failed}/{len(cases)} passed")
    return 1 if failed else 0


def main():
    if '--selftest' in sys.argv:
        sys.exit(selftest())
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
