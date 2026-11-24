#!/usr/bin/env python3
"""Reroute SVG arrows that cut through unrelated boxes (fixes audit Check 68).

For each <line marker-end> that svg_edge_crossing.find_crossings() flags,
replace it with an orthogonal <polyline> that avoids every box, and move its
label (the opacity<1 <rect> + <text> pair that immediately follows the line)
onto the new route. Everything else in the file is left byte-for-byte alone,
so earlier hand fixes survive.

Route search: anchor on the facing edges of the source/target boxes (bottom->top
when the target is below, top->bottom when above, side->side when level), then
try straight, Z-shaped (one horizontal jog) and U-shaped (detour through a free
vertical channel) paths; keep the cheapest one with no box crossings, penalising
bends and running along another arrow. If no clean route exists, the line is
left unchanged and reported.

Usage: python3 scripts/svg_reroute_crossing_edges.py [--dry-run] [files...]
       (default: every SVG Check 68 flags)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svg_edge_crossing import parse, find_crossings, _seg_hits, _inside, ASSETS, TOL

DRY = '--dry-run' in sys.argv
LINE_RE = re.compile(r'<line\b[^>]*marker-end[^>]*/>')
LABEL_RE = re.compile(r'\s*(<rect\b[^>]*opacity="0?\.\d+"[^>]*/>)\s*(<text\b[^>]*>[^<]*</text>)')
CLEAR = 12     # px gap kept between a detour and the boxes it avoids


def attr(tag, name):
    m = re.search(rf'\b{name}="([^"]*)"', tag)
    return m.group(1) if m else None


def setattr_(tag, name, val):
    return re.sub(rf'\b{name}="[^"]*"', f'{name}="{val}"', tag, count=1)


def smallest(rects, p):
    c = [r for r in rects if _inside(p, r, TOL)]
    return min(c, key=lambda r: (r[2] - r[0]) * (r[3] - r[1])) if c else None


def plen(pts):
    return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def collinear_overlap(seg, others):
    """Length of seg running on top of any other arrow segment (within 3px)."""
    (ax, ay), (bx, by) = seg
    tot = 0.0
    for (cx, cy), (dx, dy) in others:
        if ax == bx and cx == dx and abs(ax - cx) < 3:
            lo, hi = max(min(ay, by), min(cy, dy)), min(max(ay, by), max(cy, dy))
            tot += max(0.0, hi - lo)
        elif ay == by and cy == dy and abs(ay - cy) < 3:
            lo, hi = max(min(ax, bx), min(cx, dx)), min(max(ax, bx), max(cx, dx))
            tot += max(0.0, hi - lo)
    return tot


def route(S, D, obstacles, other_segs, width, texts=()):
    """Cheapest clean orthogonal route from box S to box D, or None."""
    def xs(r):
        w = r[2] - r[0]
        return [r[0] + w * f for f in (0.5, 0.3, 0.7, 0.15, 0.85)]

    def ys(r):
        h = r[3] - r[1]
        return [r[1] + h * f for f in (0.5, 0.3, 0.7)]

    cands = []
    if D[1] >= S[3] - 1 or D[3] <= S[1] + 1:           # vertical relationship
        down = D[1] >= S[3] - 1
        y0, y1 = (S[3], D[1]) if down else (S[1], D[3])
        step = 1 if down else -1
        for sx in xs(S):
            for dx in xs(D):
                if abs(sx - dx) < 1:
                    cands.append([(sx, y0), (sx, y1)])
                lo, hi = sorted((y0, y1))
                for ym in range(int(lo) + 6, int(hi) - 5, 3):
                    cands.append([(sx, y0), (sx, ym), (dx, ym), (dx, y1)])
                # U-detour via a free vertical channel
                ya, yb = y0 + step * CLEAR, y1 - step * CLEAR
                chans = {min(r[0] for r in obstacles + [S, D]) - CLEAR,
                         max(r[2] for r in obstacles + [S, D]) + CLEAR}
                chans |= {r[0] - CLEAR for r in obstacles} | {r[2] + CLEAR for r in obstacles}
                for xc in chans:
                    if 4 <= xc <= width - 4:
                        cands.append([(sx, y0), (sx, ya), (xc, ya), (xc, yb), (dx, yb), (dx, y1)])
    else:                                              # side by side
        right = D[0] >= S[2] - 1
        x0, x1 = (S[2], D[0]) if right else (S[0], D[2])
        for sy in ys(S):
            for dy in ys(D):
                if abs(sy - dy) < 1:
                    cands.append([(x0, sy), (x1, sy)])
                lo, hi = sorted((x0, x1))
                for xm in range(int(lo) + 6, int(hi) - 5, 3):
                    cands.append([(x0, sy), (xm, sy), (xm, dy), (x1, dy)])

    best = None
    for pts in cands:
        segs = list(zip(pts, pts[1:]))
        if any(_seg_hits(a, b, r) for a, b in segs for r in obstacles):
            continue
        cost = plen(pts) + 40 * (len(pts) - 2) + 25 * sum(collinear_overlap(s, other_segs) for s in segs)
        cost += 80 * sum(1 for a, b in segs for t in texts if _seg_hits(a, b, t))
        if best is None or cost < best[0]:
            best = (cost, pts)
    return best[1] if best else None


TEXT_RE = re.compile(r'<text\b([^>]*)>([^<]*)</text>')


def text_boxes(svg):
    """Approximate bounding boxes of every <text> element (no transforms)."""
    out = []
    for m in TEXT_RE.finditer(svg):
        a = m.group(1)
        x, y = attr(a, 'x'), attr(a, 'y')
        if x is None or y is None:
            continue
        x, y = float(x), float(y)
        fs = float(attr(a, 'font-size') or 10)
        n = len(re.sub(r'&\w+;', '_', m.group(2)))
        w = n * fs * 0.56
        anc = attr(a, 'text-anchor') or 'start'
        x0 = x - w / 2 if anc == 'middle' else (x - w if anc == 'end' else x)
        out.append((x0, y - fs * 0.8, x0 + w, y + fs * 0.25))
    return out


def _overlap(a, b):
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def place_label(pts, rect_tag, text_tag, rects, occupied, width):
    """Put the label pair where it overlaps the fewest boxes, labels and texts.

    Candidates: several points along each segment (longest first), centred on
    the line, or offset beside it (vertical segment) / above-below it
    (horizontal). Containers that fully enclose the label don't count.
    """
    w = float(attr(rect_tag, 'width'))
    h = float(attr(rect_tag, 'height'))
    segs = sorted(zip(pts, pts[1:]), key=lambda s: -plen(list(s)))
    best = None
    for rank, (a, b) in enumerate(segs):
        vertical = abs(a[0] - b[0]) < 1
        for t in (0.5, 0.35, 0.65, 0.2, 0.8):
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            offs = [(0, 0)] + ([(w / 2 + 5, 0), (-w / 2 - 5, 0)] if vertical else [(0, -h / 2 - 3), (0, h / 2 + 3)])
            for k, (ox, oy) in enumerate(offs):
                cx, cy = px + ox, py + oy
                box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
                if box[0] < 2 or box[2] > width - 2:
                    continue
                cost = 0.0
                for r in rects:
                    if r[0] <= box[0] and r[1] <= box[1] and r[2] >= box[2] and r[3] >= box[3]:
                        continue  # enclosing container
                    cost += _overlap(box, r)
                cost += sum(_overlap(box, o) for o in occupied) * 2
                cost += rank * 5 + k * 3 + abs(t - 0.5) * 10
                if best is None or cost < best[0]:
                    best = (cost, cx, cy, box)
    _, cx, cy, box = best
    occupied.append(box)
    rect_tag = setattr_(setattr_(rect_tag, 'x', f'{cx - w / 2:.1f}'), 'y', f'{cy - h / 2:.1f}')
    text_tag = setattr_(setattr_(text_tag, 'x', f'{cx:.1f}'), 'y', f'{cy + 3.5:.1f}')
    return rect_tag, text_tag


def fix_file(path):
    text = open(path, encoding='utf-8').read()
    parsed = parse(path)
    if parsed is None:
        return 0, 0
    rects, arrows = parsed
    width = float(re.search(r'width="([\d.]+)"', text).group(1))
    bad = {(round(s[0], 1), round(s[1], 1), round(e[0], 1), round(e[1], 1)) for s, e, _ in find_crossings(path)}
    all_segs = [seg for pts in arrows for seg in zip(pts, pts[1:])]
    # Everything a moved label must avoid: all text, plus label backgrounds
    # (the rerouted edges' own labels are removed from this as they're moved).
    occupied = text_boxes(text)
    fixed = failed = 0
    out, pos = [], 0
    for m in LINE_RE.finditer(text):
        tag = m.group(0)
        p1 = (float(attr(tag, 'x1')), float(attr(tag, 'y1')))
        p2 = (float(attr(tag, 'x2')), float(attr(tag, 'y2')))
        if (round(p1[0], 1), round(p1[1], 1), round(p2[0], 1), round(p2[1], 1)) not in bad:
            continue
        S, D = smallest(rects, p1), smallest(rects, p2)
        if not S or not D or S == D:
            failed += 1
            continue
        obstacles = [r for r in rects if not (_inside(p1, r, TOL) or _inside(p2, r, TOL))] + [S, D]
        own = ((p1, p2),)
        pts = route(S, D, obstacles, [s for s in all_segs if s not in own], width, occupied)
        if not pts:
            failed += 1
            continue
        keep = re.sub(r'\s*\b(x1|y1|x2|y2)="[^"]*"', '', tag)[len('<line'):]
        poly = f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none"{keep}'
        end = m.end()
        lab = LABEL_RE.match(text, end)
        out.append(text[pos:m.start()])
        out.append(poly)
        if lab:
            # drop this label's own old text box from the occupied set
            old = text_boxes(lab.group(2))
            if old and old[0] in occupied:
                occupied.remove(old[0])
            r_tag, t_tag = place_label(pts, lab.group(1), lab.group(2), rects, occupied, width)
            out.append('\n' + r_tag + '\n' + t_tag)
            end = lab.end()
        pos = end
        all_segs.extend(zip(pts, pts[1:]))
        fixed += 1
    out.append(text[pos:])
    new = ''.join(out)
    if fixed and not DRY:
        open(path, 'w', encoding='utf-8').write(new)
    return fixed, failed


def main():
    files = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not files:
        files = [os.path.join(ASSETS, f) for f in sorted(os.listdir(ASSETS))
                 if f.endswith('.svg') and find_crossings(os.path.join(ASSETS, f))]
    tf = tx = 0
    for f in files:
        fx, fl = fix_file(f)
        tf += fx; tx += fl
        left = len(find_crossings(f)) if not DRY else '?'
        print(f'{os.path.basename(f)}: rerouted {fx}, unroutable {fl}, crossings left {left}')
    print(f'{"[dry-run] " if DRY else ""}total rerouted {tf}, unroutable {tx}')


if __name__ == '__main__':
    main()
