"""
Scan all KB SVG diagrams for text that likely overflows its enclosing box.

Approach: parse each <text> element's position/font-size/anchor, estimate its
rendered width with a per-character-class width table (Helvetica-ish metrics),
find the smallest <rect> that spatially contains the text's anchor point, and
flag cases where the estimated text extent exceeds that rect's bounds.

This is a heuristic (no real font metrics), so results are "likely overflow"
candidates for visual triage, not a pixel-exact guarantee.
"""
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import sys

NS = '{http://www.w3.org/2000/svg}'
TRANSLATE_RE = re.compile(r'translate\(\s*(-?[\d.]+)[ ,]+(-?[\d.]+)\s*\)')


def translate_offset(elem):
    """Return (dx, dy) for a translate(...) transform attribute, or (0, 0)."""
    t = elem.get('transform')
    if not t:
        return 0.0, 0.0
    m = TRANSLATE_RE.search(t)
    if not m:
        return 0.0, 0.0
    return float(m.group(1)), float(m.group(2))


def walk_absolute(elem, ox=0.0, oy=0.0):
    """Yield (child_elem, abs_x_offset, abs_y_offset) for every descendant,
    resolving nested translate() transforms into a cumulative offset."""
    dx, dy = translate_offset(elem)
    ox, oy = ox + dx, oy + dy
    for child in elem:
        yield child, ox, oy
        yield from walk_absolute(child, ox, oy)

# Approximate Helvetica/Arial character widths as a fraction of font-size (1 em = font-size).
NARROW = set('iIjl.,:;\'!|()[]{}/ ')
WIDE = set('mMWQ%@&')
DIGITS = set('0123456789')


def char_width_em(c: str) -> float:
    if c in NARROW:
        return 0.28
    if c in WIDE:
        return 0.78
    if c in DIGITS:
        return 0.56
    if c.isupper():
        return 0.68
    return 0.50


def text_width_px(s: str, font_size: float, bold: bool) -> float:
    em_sum = sum(char_width_em(c) for c in s)
    px = em_sum * font_size
    if bold:
        px *= 1.08
    return px


def local_text(elem) -> str:
    return ''.join(elem.itertext()).strip()


def get_font_size(elem, default=10.0) -> float:
    fs = elem.get('font-size')
    if fs:
        try:
            return float(fs.replace('px', ''))
        except ValueError:
            pass
    return default


def is_bold(elem) -> bool:
    fw = elem.get('font-weight', '')
    return fw in ('bold', '700', '800', '900')


def canvas_clipped_rects(path: Path):
    """Find <rect> elements (after resolving transforms) that fall partly or
    fully outside the SVG's own declared width/height -- i.e. content
    rendered off-canvas, invisible to the user."""
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return []
    root = tree.getroot()
    try:
        cw = float(root.get('width'))
        ch = float(root.get('height'))
    except (TypeError, ValueError):
        return []

    clipped = []
    for elem, ox, oy in walk_absolute(root):
        if elem.tag != f'{NS}rect':
            continue
        try:
            x = float(elem.get('x', 0)) + ox
            y = float(elem.get('y', 0)) + oy
            w = float(elem.get('width', 0))
            h = float(elem.get('height', 0))
        except ValueError:
            continue
        if w <= 0 or h <= 0:
            continue
        if y + h > ch + 1 or x + w > cw + 1 or x < -1 or y < -1:
            clipped.append((x, y, w, h, cw, ch))
    return clipped


def analyze_svg(path: Path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        return [], f'PARSE ERROR: {e}'
    root = tree.getroot()

    # Single document-order pass, each rect/text tagged with its order index.
    # Every generator in this KB draws a label's background rect immediately
    # before that label's <text> (verified 2026-07-09 against 6 files flagged
    # as "overflow" that turned out to be false positives -- the real,
    # correctly-sized rect was always the nearest PRECEDING one in document
    # order, not the smallest-area rect among all spatially-overlapping
    # candidates, which is what this used to pick). Multiple small edge-label
    # rects often overlap in x-range at similar y (adjacent edges on the same
    # rank), so spatial containment alone is ambiguous; document-order
    # proximity resolves that ambiguity correctly.
    rects = []  # (order_index, x, y, w, h)
    texts = []  # (order_index, elem, ox, oy)
    for i, (elem, ox, oy) in enumerate(walk_absolute(root)):
        tag = elem.tag
        if tag == f'{NS}rect':
            try:
                x = float(elem.get('x', 0)) + ox
                y = float(elem.get('y', 0)) + oy
                w = float(elem.get('width', 0))
                h = float(elem.get('height', 0))
            except ValueError:
                continue
            if w <= 0 or h <= 0:
                continue
            rects.append((i, x, y, w, h))
        elif tag == f'{NS}text':
            texts.append((i, elem, ox, oy))

    findings = []
    for text_i, t, ox, oy in texts:
        x_attr = t.get('x')
        y_attr = t.get('y')
        if x_attr is None:
            # fall back to first tspan's x
            tspan = t.find(f'{NS}tspan')
            x_attr = tspan.get('x') if tspan is not None else None
        if y_attr is None:
            tspan = t.find(f'{NS}tspan')
            y_attr = tspan.get('y') if tspan is not None else None
        if x_attr is None or y_attr is None:
            continue
        try:
            x, y = float(x_attr) + ox, float(y_attr) + oy
        except ValueError:
            continue

        content = local_text(t)
        if not content:
            continue

        font_size = get_font_size(t)
        anchor = t.get('text-anchor', 'start')
        bold = is_bold(t)
        width = text_width_px(content, font_size, bold)

        if anchor == 'middle':
            left, right = x - width / 2, x + width / 2
        elif anchor == 'end':
            left, right = x - width, x
        else:
            left, right = x, x + width

        # Enclosing rect whose box contains the anchor point (x, y), with a
        # little vertical slack since y is a text baseline near the box bottom.
        # Require a small horizontal margin from the box edges: a text start
        # that sits exactly on (or past) a box's edge is a floating
        # arrow-caption label next to the box, not content inside it.
        #
        # Among all spatially-containing candidates, prefer the one nearest
        # in document order BEFORE this text (its own background rect, per
        # every generator's draw-rect-then-draw-text convention) over the
        # old smallest-area heuristic, which picked unrelated overlapping
        # rects when multiple edge labels sit close together.
        MARGIN = 5
        candidates = []
        for (rect_i, rx, ry, rw, rh) in rects:
            if (rx + MARGIN) <= x <= (rx + rw - MARGIN) and (ry - 4) <= y <= (ry + rh + 4):
                candidates.append((rect_i, rx, ry, rw, rh))

        if not candidates:
            continue

        preceding = [c for c in candidates if c[0] < text_i]
        if preceding:
            best = max(preceding, key=lambda c: c[0])[1:]
        else:
            best = min(candidates, key=lambda c: c[3] * c[4])[1:]

        rx, ry, rw, rh = best
        overflow_left = rx - left
        overflow_right = right - (rx + rw)
        overflow = max(overflow_left, overflow_right, 0)

        if overflow > 3:  # tolerance in px
            findings.append({
                'text': content[:80],
                'font_size': font_size,
                'anchor': anchor,
                'box_w': rw,
                'est_text_w': round(width, 1),
                'overflow_px': round(overflow, 1),
            })

    return findings, None


def main():
    root = Path('docs')
    svgs = sorted(root.rglob('*.svg'))
    print(f'Scanning {len(svgs)} SVGs...')

    results = []
    errors = []
    clipped_files = []
    for svg in svgs:
        findings, err = analyze_svg(svg)
        if err:
            errors.append((svg, err))
            continue
        if findings:
            results.append((svg, findings))
        clipped = canvas_clipped_rects(svg)
        if clipped:
            clipped_files.append((svg, clipped))

    if clipped_files:
        print(f'\n{len(clipped_files)} SVGs have <rect> elements rendered '
              f'partly/fully off-canvas (content invisible):')
        for svg, clipped in clipped_files:
            for (x, y, w, h, cw, ch) in clipped:
                print(f'  {svg}: rect at ({x:.0f},{y:.0f}) {w:.0f}x{h:.0f} '
                      f'vs canvas {cw:.0f}x{ch:.0f}')

    total_findings = sum(len(f) for _, f in results)
    print(f'\n{len(results)}/{len(svgs)} SVGs have at least one likely overflow '
          f'({total_findings} total flagged text elements)')
    if errors:
        print(f'{len(errors)} SVGs failed to parse:')
        for svg, err in errors[:20]:
            print(f'  {svg}: {err}')

    # Rank files by worst single overflow for triage.
    ranked = sorted(results, key=lambda kv: max(f['overflow_px'] for f in kv[1]), reverse=True)

    out_path = Path('scripts/svg_overflow_report.txt')
    with out_path.open('w') as out:
        for svg, findings in ranked:
            worst = max(f['overflow_px'] for f in findings)
            out.write(f'{svg}  (worst={worst}px, {len(findings)} flagged)\n')
            for f in findings:
                out.write(f"    [{f['overflow_px']}px over] \"{f['text']}\" "
                          f"(font={f['font_size']}, anchor={f['anchor']}, "
                          f"box_w={f['box_w']}, est_w={f['est_text_w']})\n")

    print(f'\nFull report written to {out_path}')
    print('\nTop 15 worst offenders:')
    for svg, findings in ranked[:15]:
        worst = max(f['overflow_px'] for f in findings)
        print(f'  {worst:>6}px  {svg}  ({len(findings)} flagged)')


if __name__ == '__main__':
    sys.exit(main())
