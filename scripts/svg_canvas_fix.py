"""
Fix SVG canvas dimensions that are smaller than their actual content.

Several generator scripts computed row Y-positions correctly but left a
stale/wrong top-level <svg width height viewBox>, so footers (and sometimes
whole rows) render below/right of the visible canvas -- invisible content,
not just a text-overflow issue.

This only ever grows width/height (never shrinks), and only touches the
<svg ...> opening tag's width/height/viewBox via targeted string replace so
the rest of the file is untouched byte-for-byte.
"""
import re
import sys
from pathlib import Path

from svg_overflow_check import (
    NS, walk_absolute, get_font_size, is_bold, text_width_px, local_text,
)
import defusedxml.ElementTree as ET

SVG_TAG_RE = re.compile(
    r'(<svg\b[^>]*\bwidth=")(\d+(?:\.\d+)?)("[^>]*\bheight=")(\d+(?:\.\d+)?)("[^>]*\bviewBox="0 0 )'
    r'(\d+(?:\.\d+)?)( )(\d+(?:\.\d+)?)(")'
)


def content_extent(path: Path):
    """Return (max_right, max_bottom) across all rects/lines/text in the file,
    after resolving <g transform="translate(...)"> offsets."""
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return None
    root = tree.getroot()

    max_x, max_y = 0.0, 0.0

    def bump(x, y):
        nonlocal max_x, max_y
        max_x, max_y = max(max_x, x), max(max_y, y)

    for elem, ox, oy in walk_absolute(root):
        tag = elem.tag
        if tag == f'{NS}rect':
            try:
                x = float(elem.get('x', 0)) + ox
                y = float(elem.get('y', 0)) + oy
                w = float(elem.get('width', 0))
                h = float(elem.get('height', 0))
            except ValueError:
                continue
            bump(x + w, y + h)
        elif tag == f'{NS}line':
            for xa, ya in (('x1', 'y1'), ('x2', 'y2')):
                try:
                    bump(float(elem.get(xa, 0)) + ox, float(elem.get(ya, 0)) + oy)
                except ValueError:
                    continue
        elif tag == f'{NS}text':
            x_attr, y_attr = elem.get('x'), elem.get('y')
            if x_attr is None or y_attr is None:
                tspan = elem.find(f'{NS}tspan')
                if tspan is not None:
                    x_attr = x_attr or tspan.get('x')
                    y_attr = y_attr or tspan.get('y')
            if x_attr is None or y_attr is None:
                continue
            try:
                x, y = float(x_attr) + ox, float(y_attr) + oy
            except ValueError:
                continue
            content = local_text(elem)
            if not content:
                continue
            font_size = get_font_size(elem)
            width = text_width_px(content, font_size, is_bold(elem))
            anchor = elem.get('text-anchor', 'start')
            if anchor == 'middle':
                right = x + width / 2
            elif anchor == 'end':
                right = x
            else:
                right = x + width
            bump(right, y + font_size * 0.3)  # small allowance for descenders

    return max_x, max_y


def fix_file(path: Path, dry_run: bool):
    raw = path.read_text(encoding='utf-8')
    m = SVG_TAG_RE.search(raw)
    if not m:
        return None  # non-standard <svg> tag, skip

    cur_w, cur_h = float(m.group(2)), float(m.group(4))
    extent = content_extent(path)
    if extent is None:
        return None
    max_x, max_y = extent

    new_w = max(cur_w, max_x)
    new_h = max(cur_h, max_y)
    if new_w <= cur_w + 0.5 and new_h <= cur_h + 0.5:
        return None  # already fits

    new_w_i, new_h_i = int(round(new_w)), int(round(new_h))
    new_tag = (
        f'{m.group(1)}{new_w_i}{m.group(3)}{new_h_i}{m.group(5)}'
        f'{new_w_i}{m.group(7)}{new_h_i}{m.group(9)}'
    )
    new_raw = raw[:m.start()] + new_tag + raw[m.end():]

    if not dry_run:
        path.write_text(new_raw, encoding='utf-8')

    return (cur_w, cur_h, new_w_i, new_h_i)


def main():
    dry_run = '--apply' not in sys.argv
    root = Path('docs')
    svgs = sorted(root.rglob('*.svg'))
    changed = []
    for svg in svgs:
        result = fix_file(svg, dry_run)
        if result:
            changed.append((svg, result))

    mode = 'DRY RUN' if dry_run else 'APPLIED'
    print(f'{mode}: {len(changed)}/{len(svgs)} SVGs need a larger canvas\n')
    for svg, (ow, oh, nw, nh) in changed:
        print(f'  {svg}: {ow:.0f}x{oh:.0f} -> {nw}x{nh}')

    if dry_run:
        print('\nRe-run with --apply to write these changes.')


if __name__ == '__main__':
    sys.exit(main())
