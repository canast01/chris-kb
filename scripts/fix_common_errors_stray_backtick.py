#!/usr/bin/env python3
"""Fix "Common errors" table rows whose Error cell has a stray trailing backtick.

Artifact of the 2026-07-13 prose->table conversion: "**`code` (note)`**" became
"| `code` (note)` | ...", an odd backtick count that breaks code-span parsing for
the rest of the row. Removes the final backtick of cell 1 when cell 1 has an odd
backtick count and ends with one. Idempotent. Usage: [--dry-run]
"""
import os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), '..', 'docs')
DRY = '--dry-run' in sys.argv


def split_cells(row):
    """Split a table row on | outside backtick code spans (Python-Markdown rules)."""
    r = row.strip()[1:]
    if r.endswith('|'):
        r = r[:-1]
    out, cur, code, i = [], '', False, 0
    while i < len(r):
        c = r[i]
        if c == '\\' and i + 1 < len(r):
            cur += r[i:i + 2]; i += 2; continue
        if c == '`':
            code = not code
        if c == '|' and not code:
            out.append(cur); cur = ''
        else:
            cur += c
        i += 1
    out.append(cur)
    return out


def error_cell_unbalanced(row):
    """True if the Error cell (up to the first "` | ") has an odd backtick count.

    Catches rows that still split into 2 cells but at the wrong boundary,
    because the stray backtick shifted which | sits inside a code span.
    """
    m = re.match(r'^    \| (.*?`) \| ', row)
    return bool(m) and m.group(1).count('`') % 2 == 1


def fix_row(row):
    # Cell 1 ends at the first "` | " boundary. Drop its stray final backtick
    # only if that yields a clean 2-cell row; otherwise leave the row alone.
    m = re.match(r'^(    \| )(.*?`)( \| )(.*)$', row)
    if m:
        c1 = m.group(2)
        if c1.count('`') % 2 == 1:
            fixed = m.group(1) + c1[:-1] + m.group(3) + m.group(4)
            if len(split_cells(fixed)) == 2:
                return fixed
    return row


def main():
    changed_rows = changed_files = 0
    for root, _, files in os.walk(DOCS):
        for f in files:
            if not f.endswith('.md'):
                continue
            p = os.path.join(root, f)
            lines = open(p, errors='replace').read().split('\n')
            dirty = False
            for i, l in enumerate(lines):
                if l != '!!! warning "Common errors"':
                    continue
                j = i + 3
                while j < len(lines) and lines[j].startswith('    |'):
                    if len(split_cells(lines[j])) != 2 or error_cell_unbalanced(lines[j]):
                        new = fix_row(lines[j])
                        if new != lines[j]:
                            lines[j] = new; dirty = True; changed_rows += 1
                    j += 1
            if dirty:
                changed_files += 1
                if not DRY:
                    open(p, 'w').write('\n'.join(lines))
    print(f"{'[dry-run] ' if DRY else ''}fixed {changed_rows} rows in {changed_files} files")


if __name__ == "__main__":
    main()
