#!/usr/bin/env python3
"""Fix Mermaid-converter dashed connectors that run through child-box text.

mermaid_subgraph_to_svg.py drew a within-subgraph edge A->B as a dashed line
from A's centre to B's centre, straight through both boxes' text (and any
box in between). Replace each such line with:

  * neighbours (no box between A and B): a short solid arrow spanning only the
    gap between A's facing edge and B's facing edge;
  * non-neighbours: a dashed orthogonal polyline that drops out of A's bottom
    into the band under the row, runs along it, and rises into B's bottom
    with a small arrowhead.

Adds a small userSpaceOnUse marker (#arrowsm) to <defs> once per file.
Only touches dashed <line>s that find_text_crossings() flags. Idempotent.
Usage: python3 scripts/svg_fix_internal_connectors.py [--dry-run] [files...]
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svg_edge_crossing import parse, find_text_crossings, _inside, _seg_hits, TOL, ASSETS

DRY = '--dry-run' in sys.argv
DASHED_RE = re.compile(r'<line\b[^>]*stroke-dasharray[^>]*/>')
MARKER = ('<marker id="arrowsm" markerWidth="6" markerHeight="5" refX="6" refY="2.5" '
          'orient="auto" markerUnits="userSpaceOnUse"><polygon points="0 0, 6 2.5, 0 5" fill="#78909c" /></marker>')


def a(tag, k):
    m = re.search(rf'\b{k}="([^"]*)"', tag)
    return m.group(1) if m else None


def smallest(rects, p):
    c = [r for r in rects if _inside(p, r, TOL)]
    return min(c, key=lambda r: (r[2] - r[0]) * (r[3] - r[1])) if c else None


def fix_file(path):
    svg = open(path, encoding='utf-8').read()
    parsed = parse(path)
    if parsed is None:
        return 0, 0
    rects = parsed[0]
    flagged = {(round(s[0], 1), round(s[1], 1), round(e[0], 1), round(e[1], 1)) for s, e, _ in find_text_crossings(path)}
    lane = {}          # parent rect -> number of detours already routed under that row
    fixed = skipped = 0

    def repl(m):
        nonlocal fixed, skipped
        tag = m.group(0)
        p1 = (float(a(tag, 'x1')), float(a(tag, 'y1')))
        p2 = (float(a(tag, 'x2')), float(a(tag, 'y2')))
        if (round(p1[0], 1), round(p1[1], 1), round(p2[0], 1), round(p2[1], 1)) not in flagged:
            return tag
        S, D = smallest(rects, p1), smallest(rects, p2)
        if not S or not D or S == D or abs(p1[1] - p2[1]) > 0.5:
            skipped += 1
            return tag
        right = D[0] >= S[2] - 1
        between = [r for r in rects if r not in (S, D) and not (_inside(p1, r, TOL) or _inside(p2, r, TOL))
                   and _seg_hits(p1, p2, r)]
        y = p1[1]
        if not between:
            x0, x1 = (S[2], D[0]) if right else (S[0], D[2])
            fixed += 1
            return (f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="#78909c" '
                    f'stroke-width="1.2" marker-end="url(#arrowsm)" />')
        parents = [r for r in rects if r not in (S, D) and _inside(p1, r, TOL) and _inside(p2, r, TOL)]
        floor = min(parents, key=lambda r: (r[2] - r[0]) * (r[3] - r[1]))[3] if parents else max(S[3], D[3]) + 8
        bottom = max(S[3], D[3])
        key = parents and min(parents, key=lambda r: (r[2] - r[0]) * (r[3] - r[1]))
        n = lane.get(key, 0)
        lane[key] = n + 1
        band = bottom + (floor - bottom) * (0.5 if n == 0 else (0.3 if n % 2 else 0.7))
        sx, dx = (S[0] + S[2]) / 2, (D[0] + D[2]) / 2
        fixed += 1
        return (f'<polyline points="{sx:.1f},{S[3]:.1f} {sx:.1f},{band:.1f} {dx:.1f},{band:.1f} {dx:.1f},{D[3]:.1f}" '
                f'fill="none" stroke="#78909c" stroke-width="1.2" stroke-dasharray="3,2" marker-end="url(#arrowsm)" />')

    new = DASHED_RE.sub(repl, svg)
    if fixed and 'id="arrowsm"' not in new:
        if '<defs>' in new:
            new = new.replace('<defs>', '<defs>' + MARKER, 1)
        else:
            new = re.sub(r'(<svg\b[^>]*>)', r'\1<defs>' + MARKER + '</defs>', new, count=1)
    if fixed and not DRY:
        open(path, 'w', encoding='utf-8').write(new)
    return fixed, skipped


def main():
    files = [x for x in sys.argv[1:] if not x.startswith('--')]
    if not files:
        files = [os.path.join(ASSETS, f) for f in sorted(os.listdir(ASSETS))
                 if f.endswith('.svg') and DASHED_RE.search(open(os.path.join(ASSETS, f), encoding='utf-8').read())]
    tf = ts = nf = 0
    for f in files:
        fx, sk = fix_file(f)
        if fx or sk:
            nf += 1
            print(f'{os.path.basename(f)}: fixed {fx}, skipped {sk}')
        tf += fx; ts += sk
    print(f'{"[dry-run] " if DRY else ""}{tf} connectors fixed, {ts} skipped, in {nf} files')


if __name__ == '__main__':
    main()
