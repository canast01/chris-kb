"""
Fix two vertical text-positioning bugs found by manual visual inspection
across docs/assets/*.svg, neither caught by the existing
svg_overflow_check.py (which only measures horizontal text width):

Bug A -- vertical box overflow: grow the containing rect's height (never
shrink) so its last text line has proper bottom clearance. Same
"grow, never shrink" philosophy as svg_canvas_fix.py.

Bug B -- z-order text occlusion: a later-painted opaque rect's top edge
overlaps an earlier text element's glyph area (most commonly: a table's
first data-row rect starts a few px too early and paints over the
header text above it). Fixed as an "insert vertical space" cascade:
- insertion_y = the offending rect's original top edge.
- delta = exactly enough to give the occluded text CLEAR_MARGIN px of
  clearance.
- Every rect/text/line at or below insertion_y, within the offending
  rect's x-range (i.e. the same table/column family), shifts DOWN by
  delta as a rigid unit -- so each row keeps its own original height,
  its own text's original padding, AND its own fill color in its
  original relative order (no shrink, no color/row mismatch).
- Any rect or vertical line that SPANS insertion_y (an enclosing
  container, a column divider) instead GROWS by delta at its lower
  edge, so it still contains everything now shifted inside it.
- The SVG canvas (root width/height/viewBox) grows by the total delta
  so nothing is pushed off the bottom of the drawing.
This never shrinks anything -- same "grow, never shrink" philosophy as
Bug A and svg_canvas_fix.py -- and never leaves a row's own text pressed
against its rect with no padding, which a plain top-edge-only shrink did.

Locates each target rect/text/line by its POSITIONAL INDEX among all raw
tags of that name (the Nth rect in the parsed XML tree is always the Nth
<rect> tag in the raw source, since document order is preserved), not by
matching attribute values -- an earlier version matched by value and had
to skip ~15 files where multiple sibling rects inside <g transform>
groups shared identical LOCAL (0,0)-relative sizing, making value-based
matching ambiguous. Positional indexing has no such ambiguity. Each fix
edits only the exact tag span found this way, so nothing else in the
file is touched or reformatted.

Usage:
  python3 svg_vertical_bugs_fix.py            # dry-run, report only
  python3 svg_vertical_bugs_fix.py --apply     # write fixes
  python3 svg_vertical_bugs_fix.py --apply path/to/one.svg
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from svg_overflow_check import walk_absolute, NS  # noqa: E402
import defusedxml.ElementTree as ET  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / 'docs' / 'assets'
BOTTOM_MARGIN = 10   # px of breathing room below the last line for Bug A
CLEAR_MARGIN = 2      # px of breathing room above the glyph top for Bug B

RAW_RECT_TAG_RE = re.compile(r'<rect\b[^>]*?/?>')
RAW_TEXT_TAG_RE = re.compile(r'<text\b[^>]*?>')
RAW_LINE_TAG_RE = re.compile(r'<line\b[^>]*?/?>')


def fmt_num(n):
    return str(int(n)) if float(n).is_integer() else str(n)


def parse_elements(path):
    """Return [{'kind':'rect', 'raw_rect_index': N, ...},
               {'kind':'text', 'raw_text_index': N, ...},
               {'kind':'line', 'raw_line_index': N, ...}]
    in document order, absolute coords resolved via transform-walk. Each
    raw_*_index counts ALL elements of that tag encountered (including
    ones filtered out below), so it stays a valid index into the raw
    text's list of that tag regardless of which ones this function keeps."""
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return None
    root = tree.getroot()
    elems = []
    rect_counter = 0
    text_counter = 0
    line_counter = 0
    for elem, ox, oy in walk_absolute(root):
        tag = elem.tag
        if tag == f'{NS}rect':
            idx = rect_counter
            rect_counter += 1
            try:
                lx, ly = elem.get('x', '0'), elem.get('y', '0')
                lw, lh = elem.get('width', '0'), elem.get('height', '0')
                x, y = float(lx) + ox, float(ly) + oy
                w, h = float(lw), float(lh)
            except (TypeError, ValueError):
                continue
            if w <= 0 or h <= 0:
                continue
            fill = elem.get('fill')
            fo = elem.get('fill-opacity')
            opacity = float(fo) if fo else 1.0
            if fill in ('none', 'transparent') or opacity < 0.5:
                continue
            elems.append({'kind': 'rect', 'raw_rect_index': idx, 'x': x, 'y': y, 'w': w, 'h': h})
        elif tag == f'{NS}text':
            idx = text_counter
            text_counter += 1
            try:
                lx, ly = elem.get('x', '0'), elem.get('y', '0')
                x, y = float(lx) + ox, float(ly) + oy
            except (TypeError, ValueError):
                continue
            fs = elem.get('font-size')
            try:
                size = float(fs.replace('px', '')) if fs else 10.0
            except ValueError:
                size = 10.0
            content = ''.join(elem.itertext()).strip()
            if not content:
                continue
            elems.append({'kind': 'text', 'raw_text_index': idx, 'x': x, 'y': y, 'size': size,
                          'content': content})
        elif tag == f'{NS}line':
            idx = line_counter
            line_counter += 1
            try:
                x1, y1 = float(elem.get('x1', '0')) + ox, float(elem.get('y1', '0')) + oy
                x2, y2 = float(elem.get('x2', '0')) + ox, float(elem.get('y2', '0')) + oy
            except (TypeError, ValueError):
                continue
            elems.append({'kind': 'line', 'raw_line_index': idx, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
    # order index needed by find_bug_b_events for "later in document order"
    for i, e in enumerate(elems):
        e['order'] = i
    return elems


def find_bug_a(elems):
    fixes = []
    rects = [e for e in elems if e['kind'] == 'rect']
    texts = [e for e in elems if e['kind'] == 'text']
    for r in rects:
        if r['w'] < 60 or r['h'] < 30:
            continue
        member_ys = [t['y'] for t in texts
                     if r['x'] - 2 <= t['x'] <= r['x'] + r['w'] + 2
                     and r['y'] - 2 <= t['y'] <= r['y'] + r['h'] + 8]
        if len(member_ys) < 2:
            continue
        last_y = max(member_ys)
        clearance = (r['y'] + r['h']) - last_y
        if clearance < 4:
            needed_h = (last_y - r['y']) + BOTTOM_MARGIN
            new_h = max(r['h'], needed_h)
            if new_h > r['h'] + 0.5:
                fixes.append({**r, 'new_h': new_h})
    return fixes


def ranges_overlap(a_lo, a_hi, b_lo, b_hi):
    return not (a_hi <= b_lo or a_lo >= b_hi)


def find_bug_b_events(elems):
    """Detect z-order text occlusion and classify each instance into one of
    two real, structurally-distinct fix strategies -- not a heuristic guess:

    - 'grid': the offending rect has sibling rects below it sharing its
      x-range (a repeating row pattern, e.g. a table). The whole downstream
      grid (rects + their own text + dividers) shifts down as a rigid unit,
      preserving each row's own color and its text's original padding.

    - 'standalone': no sibling rects below it -- e.g. a fixed-position
      footer/caption bar that collides with unrelated pre-existing content
      above it (such as a glossary list that grew longer than the space
      reserved for it). Only the rect and its OWN caption (text painted
      AFTER it in document order, i.e. rendered on top of it) move; the
      pre-existing content is never touched. compute_shifts() resolves
      exactly how far down it needs to go.

    One event per distinct offending rect (deduped -- several occluded
    words, e.g. header cells, can share one rect)."""
    all_rects = [e for e in elems if e['kind'] == 'rect']
    events = []
    seen_rects = set()
    for i, t in enumerate(elems):
        if t['kind'] != 'text':
            continue
        glyph_top = t['y'] - t['size'] * 0.75
        glyph_bottom = t['y'] + t['size'] * 0.25
        glyph_h = glyph_bottom - glyph_top
        for r in elems[i + 1:]:
            if r['kind'] != 'rect' or r['order'] <= t['order']:
                continue
            if not (r['x'] - 2 <= t['x'] <= r['x'] + r['w'] + 2):
                continue
            overlap_top = max(glyph_top, r['y'])
            overlap_bottom = min(glyph_bottom, r['y'] + r['h'])
            overlap = max(0, overlap_bottom - overlap_top)
            if overlap / glyph_h > 0.4:
                rix = r['raw_rect_index']
                if rix in seen_rects:
                    break
                x_lo, x_hi = r['x'], r['x'] + r['w']
                # True table rows share near-identical x/width by construction
                # (proven across every validated pilot). A loose "any overlap"
                # test wrongly matched a hierarchy of differently-indented
                # nested boxes, and a narrow mermaid label chip against a much
                # wider unrelated container, as if they were repeating grid
                # rows -- both caused real regressions. Require a tight match.
                has_sibling_below = any(
                    o['raw_rect_index'] != rix and o['y'] > r['y']
                    and abs(o['x'] - r['x']) < 3 and abs(o['w'] - r['w']) < 3
                    for o in all_rects
                )
                if has_sibling_below:
                    delta = (glyph_bottom + CLEAR_MARGIN) - r['y']
                    if delta > 0.5:
                        seen_rects.add(rix)
                        events.append({
                            'mode': 'grid', 'insertion_y': r['y'], 'x_lo': x_lo, 'x_hi': x_hi,
                            'delta': delta, 'offending_rect': r,
                        })
                else:
                    seen_rects.add(rix)
                    events.append({'mode': 'standalone', 'rect': r, 'x_lo': x_lo, 'x_hi': x_hi})
                break
    return events


def compute_shifts(elems, events):
    """For every element, sum the shift/grow contribution of each event it
    falls under, keyed by (kind, raw_index). shift_y moves the whole
    element down. grow_h extends only the lower edge of anything spanning
    an insertion point (an enclosing container rect, a vertical divider
    line). Mutates 'standalone' events in place with a '_resolved_delta'
    (needed by apply_fixes for canvas-growth accounting)."""
    shifts = {}
    all_texts = [e for e in elems if e['kind'] == 'text']

    def bump(key, shift_y=0.0, grow_h=0.0):
        d = shifts.setdefault(key, {'shift_y': 0.0, 'grow_h': 0.0})
        d['shift_y'] += shift_y
        d['grow_h'] += grow_h

    for e in events:
        if e['mode'] == 'grid':
            iy, x_lo, x_hi, delta = e['insertion_y'], e['x_lo'], e['x_hi'], e['delta']
            for el in elems:
                if el['kind'] == 'rect':
                    if not ranges_overlap(el['x'], el['x'] + el['w'], x_lo, x_hi):
                        continue
                    if el['y'] < iy - 0.5 < el['y'] + el['h']:
                        bump(('rect', el['raw_rect_index']), grow_h=delta)
                    elif el['y'] >= iy - 0.5:
                        bump(('rect', el['raw_rect_index']), shift_y=delta)
                elif el['kind'] == 'text':
                    if not (x_lo - 2 <= el['x'] <= x_hi + 2):
                        continue
                    glyph_top = el['y'] - el['size'] * 0.75
                    if glyph_top >= iy - 0.5:
                        bump(('text', el['raw_text_index']), shift_y=delta)
                elif el['kind'] == 'line':
                    lo_x, hi_x = min(el['x1'], el['x2']), max(el['x1'], el['x2'])
                    if not ranges_overlap(lo_x, hi_x, x_lo, x_hi):
                        continue
                    lo_y, hi_y = min(el['y1'], el['y2']), max(el['y1'], el['y2'])
                    if lo_y >= iy - 0.5:
                        bump(('line', el['raw_line_index']), shift_y=delta)
                    elif hi_y >= iy - 0.5:
                        bump(('line', el['raw_line_index']), grow_h=delta)

        elif e['mode'] == 'standalone':
            r, x_lo, x_hi = e['rect'], e['x_lo'], e['x_hi']
            # Only text painted BEFORE this rect can be occluded by it --
            # that's the pre-existing content it must clear. Text painted
            # AFTER it (its own caption) moves WITH it, never against it.
            conflicts = [t for t in all_texts if t['order'] < r['order']
                         and x_lo - 2 <= t['x'] <= x_hi + 2]
            y, h = r['y'], r['h']
            total_delta = 0.0
            changed, guard = True, 0
            while changed and guard < 50:
                changed, guard = False, guard + 1
                for t in conflicts:
                    glyph_top = t['y'] - t['size'] * 0.75
                    glyph_bottom = t['y'] + t['size'] * 0.25
                    glyph_h = glyph_bottom - glyph_top
                    overlap_top = max(glyph_top, y)
                    overlap_bottom = min(glyph_bottom, y + h)
                    overlap = max(0, overlap_bottom - overlap_top)
                    if overlap / glyph_h > 0.4:
                        needed = (glyph_bottom + CLEAR_MARGIN) - y
                        if needed > 0.5:
                            y += needed
                            total_delta += needed
                            changed = True
            e['_resolved_delta'] = total_delta
            if total_delta > 0.5:
                bump(('rect', r['raw_rect_index']), shift_y=total_delta)
                own_texts = [t for t in all_texts if t['order'] > r['order']
                             and x_lo - 2 <= t['x'] <= x_hi + 2
                             and r['y'] - 2 <= t['y'] <= r['y'] + r['h'] + 8]
                for ot in own_texts:
                    bump(('text', ot['raw_text_index']), shift_y=total_delta)
    return shifts


def get_tag_span(raw, tag_re, raw_index):
    """Return (start, end) of the Nth match of tag_re in raw, or None."""
    for i, m in enumerate(tag_re.finditer(raw)):
        if i == raw_index:
            return m.start(), m.end()
    return None


def get_rect_tag_span(raw, raw_rect_index):
    return get_tag_span(raw, RAW_RECT_TAG_RE, raw_rect_index)


def edit_tag_attr(tag_text, attr, old_val, new_val):
    pattern = r'(\b' + re.escape(attr) + r'=")' + re.escape(old_val) + r'(")'
    new_tag, n = re.subn(pattern, lambda mm: mm.group(1) + new_val + mm.group(2), tag_text, count=1)
    return new_tag if n == 1 else None


def compute_max_bottom(raw_text):
    """Parse the (possibly already-edited) raw SVG text and return the
    maximum bottom-edge across all elements (y+height for rects, the
    lower endpoint for lines, y + a small descent margin for text).

    Used as a geometry-truth check after ALL edits (Bug A + Bug B) are
    applied, rather than analytically summing each fix's contribution --
    a rect that receives BOTH a Bug-A height-grow AND a Bug-B position
    shift needs canvas growth reflecting both, and summing deltas from
    two independently-computed fix passes is exactly the kind of
    double-accounting that's easy to get wrong (confirmed: it did)."""
    try:
        root = ET.fromstring(raw_text)
    except ET.ParseError:
        return None
    max_bottom = 0.0
    for elem, ox, oy in walk_absolute(root):
        tag = elem.tag
        try:
            if tag == f'{NS}rect':
                y = float(elem.get('y', '0')) + oy
                h = float(elem.get('height', '0'))
                max_bottom = max(max_bottom, y + h)
            elif tag == f'{NS}line':
                y1 = float(elem.get('y1', '0')) + oy
                y2 = float(elem.get('y2', '0')) + oy
                max_bottom = max(max_bottom, y1, y2)
            elif tag == f'{NS}text':
                y = float(elem.get('y', '0')) + oy
                fs = elem.get('font-size')
                size = float(fs.replace('px', '')) if fs else 10.0
                max_bottom = max(max_bottom, y + size * 0.3)
        except (TypeError, ValueError):
            continue
    return max_bottom


def grow_svg_canvas(raw, min_height):
    """Grow the <svg> root's height + viewBox (never width, never shrink)
    to at least min_height, so shifted/grown content still fits on the
    canvas. Same 'grow, never shrink' philosophy as svg_canvas_fix.py."""
    m = re.search(r'<svg\b[^>]*>', raw)
    if not m:
        return raw
    tag = m.group(0)
    hm = re.search(r'\bheight="([\d.]+)"', tag)
    vm = re.search(r'\bviewBox="([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)"', tag)
    if not hm or not vm:
        return raw
    old_h = float(hm.group(1))
    if min_height <= old_h:
        return raw
    new_h = fmt_num(round(min_height, 1))
    new_tag = edit_tag_attr(tag, 'height', hm.group(1), new_h)
    if new_tag is None:
        return raw
    vb_x, vb_y, vb_w, vb_h = vm.groups()
    new_vb_h = fmt_num(round(min_height, 1))
    old_vb = f'{vb_x} {vb_y} {vb_w} {vb_h}'
    new_vb = f'{vb_x} {vb_y} {vb_w} {new_vb_h}'
    new_tag2 = edit_tag_attr(new_tag, 'viewBox', old_vb, new_vb)
    if new_tag2 is None:
        return raw
    return raw[:m.start()] + new_tag2 + raw[m.end():]


def apply_fixes(path, dry_run):
    elems = parse_elements(path)
    if elems is None:
        return None
    a_fixes = find_bug_a(elems)
    b_events = find_bug_b_events(elems)
    b_shifts = compute_shifts(elems, b_events) if b_events else {}
    if not a_fixes and not b_shifts:
        return None

    raw = path.read_text(encoding='utf-8')
    applied = []

    for fix in a_fixes:
        span = get_rect_tag_span(raw, fix['raw_rect_index'])
        if span is None:
            applied.append(('A', 'INDEX NOT FOUND', fix))
            continue
        start, end = span
        tag_text = raw[start:end]
        hm = re.search(r'\bheight="([^"]+)"', tag_text)
        if not hm:
            applied.append(('A', 'NO HEIGHT ATTR', fix))
            continue
        old_h_str = hm.group(1)
        try:
            old_h_val = float(old_h_str)
        except ValueError:
            applied.append(('A', 'BAD HEIGHT VALUE', fix))
            continue
        delta = fix['new_h'] - fix['h']
        new_h_str = fmt_num(round(old_h_val + delta, 1))
        new_tag = edit_tag_attr(tag_text, 'height', old_h_str, new_h_str)
        if new_tag is None:
            applied.append(('A', 'EDIT FAILED', fix))
            continue
        raw = raw[:start] + new_tag + raw[end:]
        applied.append(('A', 'height', old_h_str, '->', new_h_str))

    for (kind, raw_index), d in sorted(b_shifts.items(), key=lambda kv: kv[0]):
        shift_y, grow_h = d['shift_y'], d['grow_h']
        if abs(shift_y) < 0.05 and abs(grow_h) < 0.05:
            continue

        if kind == 'rect':
            span = get_rect_tag_span(raw, raw_index)
            if span is None:
                applied.append(('B', 'RECT INDEX NOT FOUND', raw_index))
                continue
            start, end = span
            tag_text = raw[start:end]
            new_tag = tag_text
            if abs(shift_y) >= 0.05:
                # A rect being shifted (not grown) always has an explicit
                # y in this corpus -- a shiftable row/box is never the
                # implicit-(0,0) full-canvas background rect.
                ym = re.search(r'\by="([^"]+)"', tag_text)
                if not ym:
                    applied.append(('B', 'RECT MISSING Y', raw_index))
                    continue
                new_y_str = fmt_num(round(float(ym.group(1)) + shift_y, 1))
                t2 = edit_tag_attr(new_tag, 'y', ym.group(1), new_y_str)
                if t2 is None:
                    applied.append(('B', 'RECT Y EDIT FAILED', raw_index))
                    continue
                new_tag = t2
            if abs(grow_h) >= 0.05:
                hm = re.search(r'\bheight="([^"]+)"', tag_text)
                if not hm:
                    applied.append(('B', 'RECT MISSING HEIGHT', raw_index))
                    continue
                new_h_str = fmt_num(round(float(hm.group(1)) + grow_h, 1))
                t3 = edit_tag_attr(new_tag, 'height', hm.group(1), new_h_str)
                if t3 is None:
                    applied.append(('B', 'RECT HEIGHT EDIT FAILED', raw_index))
                    continue
                new_tag = t3
            raw = raw[:start] + new_tag + raw[end:]
            applied.append(('B', 'rect', raw_index, 'shift_y', round(shift_y, 1), 'grow_h', round(grow_h, 1)))

        elif kind == 'text':
            span = get_tag_span(raw, RAW_TEXT_TAG_RE, raw_index)
            if span is None:
                applied.append(('B', 'TEXT INDEX NOT FOUND', raw_index))
                continue
            start, end = span
            tag_text = raw[start:end]
            ym = re.search(r'\by="([^"]+)"', tag_text)
            if not ym:
                applied.append(('B', 'TEXT MISSING Y', raw_index))
                continue
            new_y_str = fmt_num(round(float(ym.group(1)) + shift_y, 1))
            new_tag = edit_tag_attr(tag_text, 'y', ym.group(1), new_y_str)
            if new_tag is None:
                applied.append(('B', 'TEXT Y EDIT FAILED', raw_index))
                continue
            raw = raw[:start] + new_tag + raw[end:]
            applied.append(('B', 'text', raw_index, 'shift_y', round(shift_y, 1)))

        elif kind == 'line':
            span = get_tag_span(raw, RAW_LINE_TAG_RE, raw_index)
            if span is None:
                applied.append(('B', 'LINE INDEX NOT FOUND', raw_index))
                continue
            start, end = span
            tag_text = raw[start:end]
            y1m = re.search(r'\by1="([^"]+)"', tag_text)
            y2m = re.search(r'\by2="([^"]+)"', tag_text)
            if not y1m or not y2m:
                applied.append(('B', 'LINE MISSING Y1/Y2', raw_index))
                continue
            # Track current (possibly already-shifted) values as strings so
            # each edit searches for what's actually in new_tag right now --
            # a line can accumulate both shift_y (from one event) and grow_h
            # (from another) when a file has multiple independent tables,
            # so the grow edit must not search for the stale pre-shift value.
            cur_y1_str, cur_y2_str = y1m.group(1), y2m.group(1)
            cur_y1_val, cur_y2_val = float(cur_y1_str), float(cur_y2_str)
            new_tag = tag_text
            if abs(shift_y) >= 0.05:
                new_y1 = fmt_num(round(cur_y1_val + shift_y, 1))
                new_y2 = fmt_num(round(cur_y2_val + shift_y, 1))
                t2 = edit_tag_attr(new_tag, 'y1', cur_y1_str, new_y1)
                if t2 is None:
                    applied.append(('B', 'LINE Y1 EDIT FAILED', raw_index))
                    continue
                t3 = edit_tag_attr(t2, 'y2', cur_y2_str, new_y2)
                if t3 is None:
                    applied.append(('B', 'LINE Y2 EDIT FAILED', raw_index))
                    continue
                new_tag = t3
                cur_y1_str, cur_y2_str = new_y1, new_y2
                cur_y1_val, cur_y2_val = float(new_y1), float(new_y2)
            if abs(grow_h) >= 0.05:
                # spans insertion_y: extend only the lower endpoint
                attr, old_val = ('y1', cur_y1_str) if cur_y1_val > cur_y2_val else ('y2', cur_y2_str)
                new_val = fmt_num(round(float(old_val) + grow_h, 1))
                t4 = edit_tag_attr(new_tag, attr, old_val, new_val)
                if t4 is None:
                    applied.append(('B', 'LINE GROW EDIT FAILED', raw_index))
                    continue
                new_tag = t4
            raw = raw[:start] + new_tag + raw[end:]
            applied.append(('B', 'line', raw_index, 'shift_y', round(shift_y, 1), 'grow_h', round(grow_h, 1)))

    if b_events or a_fixes:
        final_bottom = compute_max_bottom(raw)
        if final_bottom is not None:
            m = re.search(r'<svg\b[^>]*>', raw)
            hm = re.search(r'\bheight="([\d.]+)"', m.group(0)) if m else None
            if hm:
                cur_h = float(hm.group(1))
                target = final_bottom + BOTTOM_MARGIN
                if target > cur_h + 0.5:
                    raw = grow_svg_canvas(raw, target)
                    applied.append(('B', 'canvas_grow', round(target - cur_h, 1)))

    if not dry_run:
        path.write_text(raw, encoding='utf-8')

    return applied


def main():
    dry_run = '--apply' not in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    files = [Path(a) for a in args] if args else sorted(ASSETS.glob('*.svg'))

    total_files = 0
    total_a = total_b = total_errors = 0
    error_types = {}
    for f in files:
        result = apply_fixes(f, dry_run)
        if not result:
            continue
        total_files += 1
        errs = [r for r in result if isinstance(r[1], str) and (
            'NOT FOUND' in r[1] or 'FAILED' in r[1] or 'ATTR' in r[1] or 'VALUE' in r[1]
            or 'MISSING' in r[1])]
        for e in errs:
            error_types[e[1]] = error_types.get(e[1], 0) + 1
        total_errors += len(errs)
        a_count = len([r for r in result if r[0] == 'A' and r not in errs])
        b_count = len([r for r in result if r[0] == 'B' and r not in errs
                        and r[1] in ('rect', 'text', 'line')])
        total_a += a_count
        total_b += b_count
        print(f'{f.name}: A={a_count} B={b_count} errors={len(errs)}')
        for r in errs:
            print(f'    ERROR: {r}')

    mode = 'DRY RUN' if dry_run else 'APPLIED'
    print(f'\n{mode}: {total_files} files, {total_a} Bug-A fixes, {total_b} Bug-B fixes, {total_errors} errors')
    if error_types:
        print('Error breakdown:', error_types)


if __name__ == '__main__':
    main()
