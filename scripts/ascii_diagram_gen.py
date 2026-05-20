#!/usr/bin/env python3
"""
ASCII box-drawing diagram generator for KB markdown files.

Every diagram is built from a shared position dict (col → char) then rendered
with row().  Because positions are set by index, all │ symbols land at the
exact same column on every line — guaranteed straight verticals.

HOW TO ADD A NEW DIAGRAM
─────────────────────────
Diagram functions live in scripts/diagrams/ — edit the right submodule:
  storage.py      — storage, pure, dell, netapp
  cloud.py        — cloud, aws, azure
  vmware_core.py  — vmware, esxi, vsan, nsx, vcenter, vcf
  vmware_aria.py  — aria-automation, aria-operations, aria-logs, aria-networks, aria-lcm
  vmware_apps.py  — horizon, srm, tanzu, vsphere-replication
  vxrail.py       — vxrail, vmware-vxrail-*
  other.py        — compute, linux, windows, san, cisco-san, brocade

1. Add a decorated function at the end of the relevant submodule:

       @kb_diagram('my-key', 'docs/section/index.md', 'Short description')
       def my_diagram():
           W2 = 103
           R, txt_row = make_helpers(W2)
           # layout constants …
           lines = []
           lines.append(title_border(W2, 'My Title'))
           lines.append(txt_row())
           lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
           lines.append(R(merge(bMid(L1, R1, 'Label'), bMid(L2, R2, 'Label'))))
           lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
           lines.append('└' + '─' * W2 + '┘')
           return lines

   Arrow sections between tiers always follow this four-line pattern:
       lines.append(txt_row('  <explanation of what the arrows mean>'))
       lines.append(txt_row())
       lines.append(R(arrow([MID1, MID2, ...])))
       lines.append(txt_row())
   Never put annotations inline on the arrow line — put them in the label above.

2. The @kb_diagram decorator auto-registers the function — no separate DIAGRAMS entry.
3. Run:  python3 scripts/ascii_diagram_gen.py my-key --write

USAGE
─────
  python3 scripts/ascii_diagram_gen.py                         # list all diagrams
  python3 scripts/ascii_diagram_gen.py vmware                  # print to stdout
  python3 scripts/ascii_diagram_gen.py vmware --write          # update markdown file
  python3 scripts/ascii_diagram_gen.py --write-all             # update all files
  python3 scripts/ascii_diagram_gen.py --check                 # verify files are in sync
  python3 scripts/ascii_diagram_gen.py --layout 20 20 47       # calculate box positions
  python3 scripts/ascii_diagram_gen.py --layout 20 20 47 --margin 3 --gap 2

POSITION CALCULATION
─────────────────────
Key formula:  L  R  inner_width  total_width
              L  R  R - L - 1    R - L + 1

Given margin m, gap g between boxes, and a list of desired inner widths:
  L[0]   = m
  R[0]   = L[0] + inner[0] + 1
  L[n+1] = R[n] + g + 1          ← gap chars, then next left wall
  R[n+1] = L[n+1] + inner[n+1] + 1

Use layout() to print positions without manual arithmetic.

HELPER REFERENCE
────────────────
  make_helpers(w)               — returns (R, txt_row) bound to inner width w
  layout(inner_widths, m, gap)  — print (L, R) positions for a box row
  row(d, w)                     — render one line; outer │ walls added
  bTop(l, r, tees)              — ┌────┐ with optional ┴ at tees (stem up, toward incoming)
  bMid(l, r, text)              — │ text │  (text centred, truncated)
  bBot(l, r, tees)              — └────┘ with optional ┴ at tees (stem up, exit downward)
  sections(l, r, divs, texts)   — │ sec1 │ sec2 │ sec3 │ with dividers
  connector(cols)               — row of │ stems
  arrow(cols)                   — row of ▼ arrows
  title_border(w, title, top)   — ┌──── Title ────┐ outer border line
  merge(*dicts)                 — combine position dicts (last write wins)
"""

import os
import re
import sys

# Add the scripts/ directory to the path so `diagrams` package is importable.
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

# Import primitives for any code below that uses them directly.
from diagrams._core import (  # noqa: F401
    DIAGRAMS, kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)
# Importing the package triggers all @kb_diagram registrations.
import diagrams  # noqa: F401

# ── Write / check helpers ─────────────────────────────────────────────────────

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Matches the first bare ``` block (no language tag on the opening line).
_BLOCK_RE = re.compile(r'^```\n.*?^```$', re.MULTILINE | re.DOTALL)
# Matches the first ```mermaid block (fallback for pages that have mermaid diagrams).
_MERMAID_RE = re.compile(r'^```mermaid\n.*?^```$', re.MULTILINE | re.DOTALL)


def _width_str(lines):
    widths = {len(l) for l in lines}
    if len(widths) == 1:
        return str(next(iter(widths)))
    return f'{min(widths)}-{max(widths)}'


def _write(name):
    """Replace the first bare ``` block with fresh output.

    Insertion priority when no ``` block exists:
      1. ```mermaid block → strip it, re-insert after kb-summary (MkDocs placement rule)
      2. No block at all → insert after kb-summary </div>, or before kb-grid, or after title
    """
    entry = DIAGRAMS[name]
    lines = entry['fn']()
    target = os.path.join(REPO_ROOT, entry['file'])
    try:
        with open(target, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'  ERROR: file not found: {entry["file"]}', file=sys.stderr)
        return False
    replacement = '```\n' + '\n'.join(lines) + '\n```'
    new_content, n = _BLOCK_RE.subn(replacement, content, count=1)
    # If block exists but is after the kb-grid, strip it and let the fallback re-insert correctly.
    if n == 1:
        grid_m = re.search(r'^<div class="kb-grid', content, re.MULTILINE)
        block_m = _BLOCK_RE.search(content)
        if grid_m and block_m and block_m.start() > grid_m.start():
            new_content = _BLOCK_RE.sub('', content, count=1)
            n = 0
    if n == 0:
        # Mermaid fallback: strip it, then re-insert at the correct position.
        stripped, n = _MERMAID_RE.subn('', content, count=1)
        base = stripped if n else content
        # Find insertion point: after kb-summary </div>, else before kb-grid, else after title
        summary_end = re.search(r'</div>\n', base)
        grid_start = re.search(r'^<div class="kb-grid', base, re.MULTILINE)
        title_end = re.search(r'^# .+\n', base, re.MULTILINE)
        if summary_end and (not grid_start or summary_end.end() <= grid_start.start()):
            pos = summary_end.end()
        elif grid_start:
            pos = grid_start.start()
        elif title_end:
            pos = title_end.end()
        else:
            pos = 0
        new_content = base[:pos] + '\n' + replacement + '\n' + base[pos:].lstrip('\n')
        n = 1  # mark as handled
    if new_content == content:
        print(f'  OK (unchanged)  {entry["file"]}')
        return True
    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  Updated  {entry["file"]}  [{len(lines)} lines, w={_width_str(lines)}]')
    return True


def _check(name):
    """Return True if the file's ``` block matches current output, False if out of sync, None if not found."""
    entry = DIAGRAMS[name]
    lines = entry['fn']()
    target = os.path.join(REPO_ROOT, entry['file'])
    try:
        with open(target, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return None
    m = _BLOCK_RE.search(content)
    if not m:
        return None
    # Strip the opening ``` line and the closing ``` line to get the diagram body.
    body = m.group(0).split('\n', 1)[1].rsplit('\n', 1)[0]
    return body.split('\n') == lines


# ── CLI ───────────────────────────────────────────────────────────────────────

def _list():
    col = max(len(n) for n in DIAGRAMS) + 2
    print('Registered diagrams:\n')
    for name, entry in sorted(DIAGRAMS.items()):
        print(f'  {name:<{col}}  {entry["description"]}')
        print(f'  {"":<{col}}  → {entry["file"]}')
        print()


def _audit_placement():
    """Return list of (name, file, issue) for placement violations."""
    issues = []
    for name, entry in DIAGRAMS.items():
        path = os.path.join(REPO_ROOT, entry['file'])
        if not os.path.exists(path):
            continue
        with open(path) as f:
            lines = f.read().split('\n')
        fence = next((i + 1 for i, l in enumerate(lines) if l == '```'), None)
        grid  = next((i + 1 for i, l in enumerate(lines) if 'kb-grid' in l), None)
        if fence is None:
            issues.append((name, entry['file'], 'NO FENCE'))
        elif grid and fence >= grid:
            issues.append((name, entry['file'], f'fence={fence} after grid={grid}'))
    return issues


def _audit_widths():
    """Run all diagram functions and collect WARNs, grouped by diagram name.
    Returns dict of name -> list of warn strings (empty means clean)."""
    import io, contextlib
    results = {}
    for name, entry in sorted(DIAGRAMS.items()):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            entry['fn']()
        warns = [l.strip() for l in buf.getvalue().splitlines() if 'WARN' in l]
        if warns:
            results[name] = warns
    return results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog='ascii_diagram_gen.py',
        description='ASCII diagram generator for KB markdown files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  python3 scripts/ascii_diagram_gen.py                      # list diagrams\n'
            '  python3 scripts/ascii_diagram_gen.py vmware               # print to stdout\n'
            '  python3 scripts/ascii_diagram_gen.py vmware --write       # update file\n'
            '  python3 scripts/ascii_diagram_gen.py --write-all          # update all\n'
            '  python3 scripts/ascii_diagram_gen.py --check              # sync + widths + placement\n'
            '  python3 scripts/ascii_diagram_gen.py --validate           # width WARNs grouped by name\n'
            '  python3 scripts/ascii_diagram_gen.py --layout 20 20 47    # box positions\n'
        ),
    )
    parser.add_argument('name', nargs='?', help='diagram name (omit to list all)')
    parser.add_argument('--write', action='store_true',
                        help='write diagram to its registered markdown file')
    parser.add_argument('--write-all', action='store_true',
                        help='update all registered markdown files')
    parser.add_argument('--check', action='store_true',
                        help='verify sync, width limits, and fence placement for all files')
    parser.add_argument('--validate', action='store_true',
                        help='run all functions and report width WARNs grouped by diagram name')
    parser.add_argument('--layout', nargs='+', type=int, metavar='W',
                        help='calculate box (L, R) positions for given inner widths')
    parser.add_argument('--margin', type=int, default=3,
                        help='left margin for --layout (default 3)')
    parser.add_argument('--gap', type=int, default=2,
                        help='gap between boxes for --layout (default 2)')

    args = parser.parse_args()

    if args.layout:
        layout(args.layout, margin=args.margin, gap=args.gap)

    elif args.write_all:
        for name in sorted(DIAGRAMS):
            _write(name)

    elif args.validate:
        width_issues = _audit_widths()
        if not width_issues:
            print('All diagrams clean — no width WARNs.')
        else:
            print(f'{len(width_issues)} diagram(s) have width WARNs:\n')
            for name, warns in width_issues.items():
                print(f'  {name}:')
                for w in warns:
                    print(f'    {w}')
        sys.exit(1 if width_issues else 0)

    elif args.check:
        all_ok = True
        col = max(len(n) for n in DIAGRAMS) + 2

        # 1. Sync check
        print('── Sync ──')
        for name, entry in sorted(DIAGRAMS.items()):
            result = _check(name)
            if result is None:
                status = 'NO BLOCK   '
                all_ok = False
            elif result:
                status = 'OK         '
            else:
                status = 'OUT OF SYNC'
                all_ok = False
            if result is None or not result:
                print(f'  {name:<{col}}  {status}  {entry["file"]}')
        if all_ok:
            print(f'  All {len(DIAGRAMS)} diagrams in sync.\n')

        # 2. Width check
        print('── Widths ──')
        width_issues = _audit_widths()
        if not width_issues:
            print(f'  All {len(DIAGRAMS)} diagrams within width limits.\n')
        else:
            all_ok = False
            for name, warns in width_issues.items():
                print(f'  {name}: {len(warns)} WARN(s)')
                for w in warns[:3]:
                    print(f'    {w}')

        # 3. Placement check
        print('── Placement ──')
        placement_issues = _audit_placement()
        if not placement_issues:
            print(f'  All {len(DIAGRAMS)} diagrams correctly placed before kb-grid.\n')
        else:
            all_ok = False
            for name, filepath, issue in placement_issues:
                print(f'  {name:<{col}}  {issue}  {filepath}')

        if not all_ok:
            sys.exit(1)

    elif args.name:
        if args.name not in DIAGRAMS:
            known = ', '.join(sorted(DIAGRAMS))
            print(f'ERROR: unknown diagram "{args.name}". Known: {known}', file=sys.stderr)
            sys.exit(1)
        if args.write:
            _write(args.name)
        else:
            lines = DIAGRAMS[args.name]['fn']()
            for line in lines:
                print(line)
            print(f'\n[w={_width_str(lines)}  lines={len(lines)}]', file=sys.stderr)

    else:
        _list()

