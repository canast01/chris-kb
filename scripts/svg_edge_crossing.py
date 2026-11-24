#!/usr/bin/env python3
"""Detect SVG arrows that pass through a box they don't start or end at.

Found 2026-11-23: the Git "Distributed Model" and VCF "How It Works" diagrams
(converted from Mermaid subgraphs) had straight arrows cutting through
unrelated boxes, e.g. origin->"Dev B" drawn straight through "Fork Remote".
No audit check covered it.

An "arrow" is a <line> or <polyline> with marker-end. A "box" is a <rect> at
least 20x20 that is fully opaque (label backgrounds use opacity<1), and isn't
a full-width band (title bar, footer, canvas). A box is exempt for a given
arrow if it contains either endpoint (its source/target box, or a group box
enclosing them). Only translate() transforms are supported; a file with any
other transform is skipped.

Usage: python3 scripts/svg_edge_crossing.py [files...]   (default: docs/assets/*.svg)
"""
import os, re, sys
import defusedxml.ElementTree as ET

NS = '{http://www.w3.org/2000/svg}'
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'assets')
TOL = 3.0     # px: endpoint-in-box tolerance
INSET = 2.0   # px: shrink box before testing, so edges grazing a border don't count


def _f(v, d=0.0):
    try:
        return float(re.sub(r'[a-z%]+$', '', v.strip()))
    except (AttributeError, ValueError):
        return d


def _translate(el):
    """Return (dx, dy) for translate(), (0,0) for none, None for unsupported."""
    t = el.get('transform')
    if not t:
        return (0.0, 0.0)
    m = re.fullmatch(r'\s*translate\(\s*([-\d.]+)(?:[\s,]+([-\d.]+))?\s*\)\s*', t)
    if not m:
        return None
    return (float(m.group(1)), float(m.group(2) or 0))


def parse(path):
    """Return (rects, arrows) in absolute coords, or None if unsupported/unparseable."""
    try:
        root = ET.parse(path).getroot()
    except Exception:
        return None
    width = _f(root.get('width'), 0) or _f((root.get('viewBox') or '0 0 0 0').split()[2])
    rects, arrows = [], []

    def walk(el, ox, oy):
        tr = _translate(el)
        if tr is None:
            raise ValueError('unsupported transform')
        ox, oy = ox + tr[0], oy + tr[1]
        tag = el.tag.replace(NS, '')
        if tag == 'rect':
            x, y = _f(el.get('x')) + ox, _f(el.get('y')) + oy
            w, h = _f(el.get('width')), _f(el.get('height'))
            op = _f(el.get('opacity'), 1.0) * _f(el.get('fill-opacity'), 1.0)
            if w >= 20 and h >= 20 and op >= 1.0 and not (width and w >= width - 1):
                rects.append((x, y, x + w, y + h))
        elif tag in ('line', 'polyline') and el.get('marker-end'):
            if tag == 'line':
                pts = [(_f(el.get('x1')), _f(el.get('y1'))), (_f(el.get('x2')), _f(el.get('y2')))]
            else:
                nums = [float(n) for n in re.findall(r'-?[\d.]+', el.get('points', ''))]
                pts = list(zip(nums[0::2], nums[1::2]))
            if len(pts) >= 2:
                arrows.append([(px + ox, py + oy) for px, py in pts])
        for c in el:
            walk(c, ox, oy)

    try:
        walk(root, 0.0, 0.0)
    except ValueError:
        return None
    return rects, arrows


def _inside(p, r, tol):
    return r[0] - tol <= p[0] <= r[2] + tol and r[1] - tol <= p[1] <= r[3] + tol


def _seg_hits(a, b, r):
    """Liang-Barsky: does segment a-b intersect the interior of rect r?"""
    x0, y0, x1, y1 = r[0] + INSET, r[1] + INSET, r[2] - INSET, r[3] - INSET
    if x0 >= x1 or y0 >= y1:
        return False
    dx, dy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if p == 0:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return t1 - t0 > 1e-6


def find_crossings(path):
    """List of (arrow_start, arrow_end, rect) where an arrow cuts through an unrelated box."""
    parsed = parse(path)
    if parsed is None:
        return []
    rects, arrows = parsed
    out = []
    for pts in arrows:
        start, end = pts[0], pts[-1]
        for r in rects:
            if _inside(start, r, TOL) or _inside(end, r, TOL):
                continue
            if any(_seg_hits(pts[i], pts[i + 1], r) for i in range(len(pts) - 1)):
                out.append((start, end, r))
    return out


def main():
    files = sys.argv[1:] or sorted(os.path.join(ASSETS, f) for f in os.listdir(ASSETS) if f.endswith('.svg'))
    n = 0
    for f in files:
        hits = find_crossings(f)
        if hits:
            n += 1
            print(f'{os.path.basename(f)}: {len(hits)} crossing(s)')
            for s, e, r in hits[:5]:
                print(f'    arrow ({s[0]:.0f},{s[1]:.0f})->({e[0]:.0f},{e[1]:.0f}) crosses box '
                      f'({r[0]:.0f},{r[1]:.0f})-({r[2]:.0f},{r[3]:.0f})')
    print(f'{n} file(s) with crossings')


if __name__ == '__main__':
    main()
