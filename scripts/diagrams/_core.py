"""
Shared primitives, DIAGRAMS registry, and kb_diagram decorator.
All diagram submodules import from here.
"""

import os
import re
import sys

# ── Diagram registry ─────────────────────────────────────────────────────────
DIAGRAMS = {}  # populated at import time by @kb_diagram decorators

def kb_diagram(key, file, description):
    """Decorator that auto-registers a diagram function. Usage:

        @kb_diagram('my-key', 'docs/path/index.md', 'Short description')
        def my_diagram():
            ...
    """
    def _register(fn):
        DIAGRAMS[key] = {'fn': fn, 'file': file, 'description': description}
        return fn
    return _register

# ── Core primitives ──────────────────────────────────────────────────────────

def row(positions, w):
    """Render one diagram line. positions: {col: char} (0-indexed in inner space).
    Columns outside [0, w) are silently ignored."""
    r = [' '] * w
    for col, ch in positions.items():
        if 0 <= col < w:
            r[col] = ch
    return '│' + ''.join(r) + '│'

def _hspan(d, l, r, fill='─', lc=None, rc=None):
    for i in range(l, r + 1):
        d[i] = fill
    if lc:
        d[l] = lc
    if rc:
        d[r] = rc

def bTop(l, r, tees=()):
    """Top border of a box. tees: column positions to replace ─ with ┴.
    ┴ is correct here: the horizontal bar is the top border, and the stem
    points UP toward the incoming connector above the box."""
    d = {}
    _hspan(d, l, r, '─', '┌', '┐')
    for t in tees:
        d[t] = '┴'
    return d

def bMid(l, r, text=''):
    """One content row of a box. text is centred and truncated to inner width."""
    iw = r - l - 1
    if len(text) > iw:
        raise ValueError(f'bMid: text too long ({len(text)} > {iw}): {text!r}')
    txt = text.center(iw)[:iw]
    d = {l: '│', r: '│'}
    for i, c in enumerate(txt):
        d[l + 1 + i] = c
    return d

def bBot(l, r, tees=()):
    """Bottom border of a box. tees: column positions to replace ─ with ┴."""
    d = {}
    _hspan(d, l, r, '─', '└', '┘')
    for t in tees:
        d[t] = '┴'
    return d

def sections(l, r, divs, texts):
    """
    A single content row spanning box (l..r) split by internal dividers.

    divs  — list of column positions for internal │ dividers (must be sorted)
    texts — list of strings, one per section (len == len(divs) + 1)

    Example: sections(51, 99, [67, 83], ['Ops/Logs', 'Automation', 'Suite Lifecycle'])
    """
    boundaries = [l] + list(divs) + [r]
    d = {}
    for pos in boundaries:
        d[pos] = '│'
    for i, text in enumerate(texts):
        sl = boundaries[i]
        sr = boundaries[i + 1]
        iw = sr - sl - 1
        if len(text) > iw:
            raise ValueError(f'sections[{i}]: text too long ({len(text)} > {iw}): {text!r}')
        txt = text.center(iw)[:iw]
        for j, c in enumerate(txt):
            d[sl + 1 + j] = c
    return d

def connector(cols):
    """A row of vertical │ stems between a box bottom and the next box top."""
    return {c: '│' for c in cols}

def arrow(cols):
    """A row of ▼ arrows pointing down."""
    return {c: '▼' for c in cols}

def title_border(w, title, top=True):
    """
    Outer border line with an embedded title, e.g.:
      ┌───────────── My Title ─────────────┐
    w     — inner width (same w passed to make_helpers)
    title — string to embed (centred with ─ padding); pass '' for a plain border
    top   — True for ┌/┐, False for └/┘
    """
    lc, rc = ('┌', '┐') if top else ('└', '┘')
    if title:
        padded = f' {title} '
        if len(padded) > w:
            raise ValueError(f'title_border: title too long ({len(padded)} > {w}): {title!r}')
        left_dashes = (w - len(padded)) // 2
        right_dashes = w - len(padded) - left_dashes
        inner = '─' * left_dashes + padded + '─' * right_dashes
    else:
        inner = '─' * w
    return lc + inner + rc

def merge(*dicts):
    """Merge position dicts left to right (later dicts override earlier)."""
    out = {}
    for d in dicts:
        out.update(d)
    return out

def make_helpers(w):
    """
    Return (R, txt_row) bound to inner width w.

    R(d)                      — render one diagram line (wraps row(d, w))
    txt_row(text='', indent=2) — left-aligned text line inside the outer border

    Use at the top of every diagram function, then call bTop/bMid/bBot/
    sections/merge/arrow/connector directly from module scope:

        W2 = 95
        R, txt_row = make_helpers(W2)
    """
    def R(d):
        return row(d, w)

    def txt_row(text='', indent=2):
        r = [' '] * w
        for i, c in enumerate(text):
            pos = indent + i
            if pos >= w:
                raise ValueError(f'txt_row: text too long (truncates at col {w}, indent={indent}): {text!r}')
            if 0 <= pos < w:
                r[pos] = c
        return '│' + ''.join(r) + '│'

    return R, txt_row

def layout(inner_widths, margin=3, gap=2):
    """
    Print and return (L, R) positions for a row of boxes.

    inner_widths — desired inner widths per box (chars between the │ walls)
    margin       — left offset before the first box (default 3)
    gap          — spaces between adjacent box walls (default 2)

    Example:
      layout([20, 20, 47], margin=3, gap=2)
      →  Box 1: L=3,  R=24   inner=20
         Box 2: L=27, R=48   inner=20
         Box 3: L=51, R=99   inner=47
    """
    positions = []
    l = margin
    for iw in inner_widths:
        r = l + iw + 1
        positions.append((l, r))
        l = r + gap + 1
    for i, (bl, br) in enumerate(positions):
        print(f'  Box {i + 1}: L={bl:3d}, R={br:3d}   inner={br - bl - 1}   total={br - bl + 1}')
    return positions


# ── Diagrams ─────────────────────────────────────────────────────────────────
# Each function returns list[str].
# Start with:  W2 = <width>;  R, txt_row = make_helpers(W2)
# Then use bTop/bMid/bBot/sections/merge/arrow/connector from module scope.
# Register every new function in DIAGRAMS at the bottom of this file.
