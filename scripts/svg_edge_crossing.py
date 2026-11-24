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


# ── Connector lines through text (audit Check 69) ───────────────────────────
# Found 2026-11-24: the Mermaid-subgraph converter drew within-subgraph edges
# as a dashed line from one child box's centre to the other's, straight
# through both boxes' text (e.g. "Source VM", "VFS Layer"). Labels that sit
# on a line on purpose (text over an opacity<1 background rect) are exempt.
_TEXT_RE = re.compile(r'<text\b([^>]*)>([^<]*)</text>')
_CONN_RE = re.compile(r'<(line|polyline)\b[^>]*/>')
_LBL_RECT_RE = re.compile(r'<rect\b[^>]*opacity="0?\.\d+"[^>]*/>')


def _a(tag, name):
    m = re.search(rf'\b{name}="([^"]*)"', tag)
    return m.group(1) if m else None


_FONTS = {}


def _text_width(txt, fs, bold):
    """Rendered width in px using real Arial metrics; 0.56em/char fallback."""
    import html
    txt = ' '.join(html.unescape(txt).split())  # SVG collapses whitespace
    key = bold
    if key not in _FONTS:
        try:
            from PIL import ImageFont
            name = 'Arial Bold.ttf' if bold else 'Arial.ttf'
            _FONTS[key] = ImageFont.truetype('/System/Library/Fonts/Supplemental/' + name, 100)
        except Exception:
            _FONTS[key] = None
    f = _FONTS[key]
    return f.getlength(txt) * fs / 100 if f else len(txt) * fs * 0.56


def _text_boxes(svg):
    out = []
    for m in _TEXT_RE.finditer(svg):
        a = m.group(1)
        x, y = _a(a, 'x'), _a(a, 'y')
        if x is None or y is None:
            continue
        x, y = float(x), float(y)
        fs = float(_a(a, 'font-size') or 10)
        bold = (_a(a, 'font-weight') or '') in ('bold', '600', '700', '800', '900')
        w = _text_width(m.group(2), fs, bold)
        anc = _a(a, 'text-anchor') or 'start'
        x0 = x - w / 2 if anc == 'middle' else (x - w if anc == 'end' else x)
        out.append((x0, y - fs * 0.8, x0 + w, y + fs * 0.25))
    return out


def find_text_crossings(path):
    """List of (start, end, textbox) for connector lines that cut through text."""
    try:
        svg = open(path, encoding='utf-8').read()
    except OSError:
        return []
    if 'transform=' in svg:
        return []
    labels = []
    for t in _LBL_RECT_RE.findall(svg):
        x, y, w, h = (float(_a(t, k) or 0) for k in ('x', 'y', 'width', 'height'))
        labels.append((x, y, x + w, y + h))
    texts = [t for t in _text_boxes(svg)
             if not any(l[0] - 2 <= (t[0] + t[2]) / 2 <= l[2] + 2 and l[1] - 2 <= (t[1] + t[3]) / 2 <= l[3] + 2
                        for l in labels)]
    out = []
    parsed = parse(path)
    rects = parsed[0] if parsed else []
    for m in _CONN_RE.finditer(svg):
        tag = m.group(0)
        if m.group(1) == 'line':
            pts = [(float(_a(tag, 'x1') or 0), float(_a(tag, 'y1') or 0)),
                   (float(_a(tag, 'x2') or 0), float(_a(tag, 'y2') or 0))]
        else:
            n = [float(v) for v in re.findall(r'-?[\d.]+', _a(tag, 'points') or '')]
            pts = list(zip(n[0::2], n[1::2]))
        hit = False
        for t in texts:
            if any(_seg_hits(a, b, (t[0] - INSET, t[1] - INSET, t[2] + INSET, t[3] + INSET))
                   for a, b in zip(pts, pts[1:])):
                out.append((pts[0], pts[-1], t))
                hit = True
                break
        if not hit and 'marker-end' not in tag:
            # undecorated connector starting/ending deep inside a box: drawn
            # through that box's content (the Mermaid centre-to-centre bug)
            for p in (pts[0], pts[-1]):
                deep = [r for r in rects if r[0] + DEEP < p[0] < r[2] - DEEP and r[1] + DEEP < p[1] < r[3] - DEEP]
                if deep and not any(_inside(pts[0], r, 0) and _inside(pts[-1], r, 0) and
                                    min(r[2] - r[0], r[3] - r[1]) > 0 for r in
                                    [min(deep, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))]):
                    out.append((pts[0], pts[-1], min(deep, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))))
                    break
    return out


DEEP = 6.0  # px from every edge = "inside" a box, not on its border


# ── Child box sticking out of its container (audit Check 70) ────────────────
# Found 2026-11-24: two Mermaid-converted SVGs had one child box taller than
# its siblings (54.9 vs 38, 96.9 vs 83) -- an artefact of an earlier
# automated overflow fix -- so it poked out of the bottom of its group box.
def find_child_overflow(path):
    """List of (child, container) where a box is mostly inside a larger box but pokes out >2px."""
    parsed = parse(path)
    if parsed is None:
        return []
    rects, out = parsed[0], []
    for c in rects:
        ca = (c[2] - c[0]) * (c[3] - c[1])
        for q in rects:
            if q == c or (q[2] - q[0]) * (q[3] - q[1]) <= ca * 1.5:
                continue
            ix = max(0.0, min(c[2], q[2]) - max(c[0], q[0]))
            iy = max(0.0, min(c[3], q[3]) - max(c[1], q[1]))
            if 0.6 < ix * iy / ca < 0.999 and (c[3] - q[3] > 2 or q[1] - c[1] > 2 or c[2] - q[2] > 2 or q[0] - c[0] > 2):
                out.append((c, q))
                break
    return out
