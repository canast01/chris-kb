"""Shared SVG builder helpers and page-injection utilities for KB diagrams."""
from pathlib import Path
import re

# ── Canvas constants ──────────────────────────────────────────────────────────
W, H = 820, 750
FOOTER_Y = 720

# 3-column layout (x-origin and width)
C1X, C2X, C3X = 20, 285, 550
CW = 250

# Column internals
COL_Y, COL_H = 72, 390
ITEM_YS = [126, 152, 178, 204, 230]
NOTE_YS = [282, 300, 318, 336, 354, 372, 390, 408]

# Comparison table
TABLE_Y, TABLE_H = 480, 222

# Matches a ```text ASCII diagram block (the full fence including corners)
ASCII_RE = re.compile(r'```text\n┌[^`]*?┘[ \t]*\n```', re.DOTALL)


# ── XML safety ────────────────────────────────────────────────────────────────

def xe(s: str) -> str:
    """Escape characters that are invalid in SVG/XML text nodes."""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ── SVG element builders ──────────────────────────────────────────────────────

def svg_header(title: str, subtitle: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f"font-family=\"'Segoe UI',Arial,sans-serif\">\n"
        f'  <rect width="{W}" height="{H}" fill="#f4f6f9"/>\n'
        f'  <rect x="0" y="0" width="{W}" height="58" fill="#1a2744"/>\n'
        f'  <text x="410" y="36" text-anchor="middle" fill="white" '
        f'font-size="20" font-weight="700" letter-spacing="0.5">{xe(title)}</text>\n'
        f'  <text x="410" y="52" text-anchor="middle" fill="#7a8fbb" '
        f'font-size="11">{xe(subtitle)}</text>'
    )


def svg_column(cx: int, name: str, sub: str,
               hdr: str, light: str, dark: str, mid: str,
               items: list, notes: list) -> str:
    """Render one column with header, up to 5 item boxes, and up to 8 note lines."""
    mx = cx + CW // 2
    lines = [
        f'  <rect x="{cx}" y="{COL_Y}" width="{CW}" height="{COL_H}" '
        f'fill="#fff" rx="6" stroke="#dde2ec" stroke-width="1.2"/>',
        f'  <rect x="{cx}" y="{COL_Y}" width="{CW}" height="42" fill="{hdr}" rx="6"/>',
        f'  <rect x="{cx}" y="{COL_Y + 28}" width="{CW}" height="14" fill="{hdr}"/>',
        f'  <text x="{mx}" y="{COL_Y + 25}" text-anchor="middle" fill="white" '
        f'font-size="13" font-weight="700">{xe(name)}</text>',
        f'  <text x="{mx}" y="{COL_Y + 39}" text-anchor="middle" fill="{mid}" '
        f'font-size="9">{xe(sub)}</text>',
    ]
    for y, item in zip(ITEM_YS, items[:5]):
        lines += [
            f'  <rect x="{cx + 10}" y="{y}" width="{CW - 20}" height="22" '
            f'fill="{light}" rx="3" stroke="{mid}" stroke-width="1"/>',
            f'  <text x="{mx}" y="{y + 15}" text-anchor="middle" fill="{dark}" '
            f'font-size="9" font-weight="700">{xe(item)}</text>',
        ]
    for y, note in zip(NOTE_YS, notes[:8]):
        lines.append(
            f'  <text x="{mx}" y="{y}" text-anchor="middle" '
            f'fill="#78909c" font-size="9">{xe(note)}</text>'
        )
    return '\n'.join(lines)


def svg_table(table_title: str, col_headers: list, rows: list) -> str:
    """Render a 4-column comparison table. rows = list of (label, c1, c2, c3)."""
    TW, TX = 780, 20
    HDR_XS = [120, 320, 520, 700]
    lines = [
        f'  <rect x="{TX}" y="{TABLE_Y}" width="{TW}" height="{TABLE_H}" '
        f'fill="#fff" rx="6" stroke="#dde2ec" stroke-width="1.2"/>',
        f'  <rect x="{TX}" y="{TABLE_Y}" width="{TW}" height="36" fill="#1a2744" rx="6"/>',
        f'  <rect x="{TX}" y="{TABLE_Y + 24}" width="{TW}" height="12" fill="#1a2744"/>',
        f'  <text x="410" y="{TABLE_Y + 24}" text-anchor="middle" fill="white" '
        f'font-size="13" font-weight="700">{xe(table_title)}</text>',
        f'  <rect x="{TX}" y="{TABLE_Y + 36}" width="{TW}" height="28" fill="#eceff1"/>',
    ]
    for x, h in zip(HDR_XS, col_headers[:4]):
        lines.append(
            f'  <text x="{x}" y="{TABLE_Y + 55}" text-anchor="middle" '
            f'fill="#37474f" font-size="10" font-weight="700">{xe(h)}</text>'
        )
    for dx in [220, 415, 610]:
        lines.append(
            f'  <line x1="{TX + dx}" y1="{TABLE_Y + 36}" '
            f'x2="{TX + dx}" y2="{TABLE_Y + TABLE_H}" stroke="#dde2ec" stroke-width="1"/>'
        )
    for i, row in enumerate(rows[:6]):
        # Pad row to 4 elements
        padded = list(row) + ['', '', '', '']
        label, c1, c2, c3 = padded[:4]
        ry = TABLE_Y + 64 + i * 26
        if i % 2 == 0:
            lines.append(
                f'  <rect x="{TX}" y="{ry - 14}" width="{TW}" height="26" fill="#f7f9fb"/>'
            )
        lines += [
            f'  <text x="120" y="{ry}" text-anchor="middle" '
            f'fill="#455a64" font-size="9">{xe(label)}</text>',
            f'  <text x="320" y="{ry}" text-anchor="middle" '
            f'fill="#546e7a" font-size="9">{xe(c1)}</text>',
            f'  <text x="520" y="{ry}" text-anchor="middle" '
            f'fill="#546e7a" font-size="9">{xe(c2)}</text>',
            f'  <text x="700" y="{ry}" text-anchor="middle" '
            f'fill="#546e7a" font-size="9">{xe(c3)}</text>',
        ]
    lines.append(
        f'  <line x1="{TX}" y1="{TABLE_Y + TABLE_H}" '
        f'x2="{TX + TW}" y2="{TABLE_Y + TABLE_H}" stroke="#dde2ec" stroke-width="1"/>'
    )
    return '\n'.join(lines)


def svg_footer(text: str) -> str:
    return (
        f'  <rect x="0" y="{FOOTER_Y}" width="{W}" height="30" fill="#1a2744"/>\n'
        f'  <text x="410" y="{FOOTER_Y + 19}" text-anchor="middle" '
        f'fill="#7a8fbb" font-size="9">{xe(text)}</text>\n'
        '</svg>'
    )


def make_svg(title: str, subtitle: str, cols: list,
             table_title: str, col_headers: list, rows: list,
             footer: str) -> str:
    """
    Build a complete 3-column SVG.
    cols: list of exactly 3 tuples:
      (name, sub, hdr_color, light_color, dark_color, mid_color, [items], [notes])
    """
    parts = [svg_header(title, subtitle)]
    for cx, col in zip([C1X, C2X, C3X], cols[:3]):
        name, sub, hdr, light, dark, mid, items, notes = col
        parts.append(svg_column(cx, name, sub, hdr, light, dark, mid, items, notes))
    parts.append(svg_table(table_title, col_headers, rows))
    parts.append(svg_footer(footer))
    return '\n'.join(parts)


# ── Path helpers ──────────────────────────────────────────────────────────────

def rel_to_assets(page_abs: str) -> str:
    """
    Return the relative path from a page file to docs/assets/.
    e.g. docs/virtualization/vmware/vcenter/index.md -> '../../../assets/'
    """
    parts = Path(page_abs).parts
    try:
        docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    except StopIteration:
        raise ValueError(f"'docs' directory not found in path: {page_abs}")
    # depth = number of directories between docs/ and the file (excluding filename)
    depth = len(parts) - docs_idx - 2
    return '../' * depth + 'assets/'


# ── Page injection ────────────────────────────────────────────────────────────

def inject_svgs(page_abs: str, insertions: list, dry_run: bool = False) -> bool:
    """
    Replace the first ASCII diagram block in page_abs with SVG <img> tags.

    insertions: list of (alt_text, svg_filename) tuples.
      svg_filename is just the bare filename (e.g. 'vcenter-capabilities-overview.svg').
      The relative path to docs/assets/ is computed automatically.

    Returns True if the file was (or would be) modified.
    """
    page = Path(page_abs)
    if not page.exists():
        print(f'  ERROR: file not found: {page_abs}')
        return False

    content = page.read_text(encoding='utf-8')

    # Skip if already injected (check for first SVG filename)
    if insertions[0][1] in content:
        print(f'  SKIP (already injected): {page_abs}')
        return False

    rel = rel_to_assets(page_abs)
    img_block = '\n\n'.join(
        f'![{alt}]({rel}{fname})' for alt, fname in insertions
    )

    if ASCII_RE.search(content):
        new_content = ASCII_RE.sub(img_block, content, count=1)
    else:
        # No ASCII block found — insert after the kb-summary closing </div>
        idx = content.find('</div>')
        if idx != -1:
            ins = idx + len('</div>')
            new_content = content[:ins] + '\n\n' + img_block + content[ins:]
        else:
            new_content = content + '\n\n' + img_block

    if dry_run:
        print(f'  DRY RUN: would update {page_abs}')
        return True

    page.write_text(new_content, encoding='utf-8')
    print(f'  Updated: {page_abs}')
    return True
