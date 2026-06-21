#!/usr/bin/env python3
"""
Generate content-page SVGs for KB operational content pages.

One SVG per page; diagram type determined by filename:
  cli-reference   → CLI command flow
  backup-restore  → Backup / restore workflow
  install-upgrade → Install / upgrade sequence
  scripts         → Automation / scripting flow
  ports           → Network port topology flow

Usage:
  python3 scripts/generate_svgs_content.py --dry-run
  python3 scripts/generate_svgs_content.py
  python3 scripts/generate_svgs_content.py --type cli-reference backup-restore
"""
import argparse
import re
from pathlib import Path
from xml.etree import ElementTree as ET

REPO   = Path(__file__).parent.parent.resolve()
DOCS   = REPO / 'docs'
ASSETS = REPO / 'docs' / 'assets'

NAVY      = '#1a2744'
GREEN     = '#2e7d32'
GREEN_L   = '#e8f5e9'
TEXT_DARK = '#1a2744'
TEXT_MID  = '#37474f'
TEXT_LIGHT= '#78909c'
FOOTER_FG = '#7a8fbb'

SVG_W = 820
SVG_H = 200
HDR_H = 42
FTR_H = 26
FTR_Y = SVG_H - FTR_H
BOX_Y = HDR_H + 14
BOX_H = 58
PAD   = 18
ARW_W = 14

PAGE_TYPES = {
    'cli-reference': {
        'subtitle': 'CLI Reference Flow',
        'boxes': [
            ('Identify', 'Command Group', '#e3f2fd', '#1565c0'),
            ('Check', 'Syntax & Options', '#e8eaf6', '#3949ab'),
            ('Execute', 'Command', '#fff8e1', '#f57f17'),
            ('Parse', 'Output', '#fce4ec', '#c62828'),
            ('✓ Document', 'Result', GREEN_L, GREEN),
        ],
        'footer': 'CLI Reference',
    },
    'backup-restore': {
        'subtitle': 'Backup / Restore Workflow',
        'boxes': [
            ('Schedule /', 'Trigger', '#e3f2fd', '#1565c0'),
            ('Snapshot /', 'Agent', '#e8eaf6', '#3949ab'),
            ('Transfer to', 'Target', '#fff8e1', '#f57f17'),
            ('Verify', 'Integrity', '#fce4ec', '#c62828'),
            ('✓ RPO/RTO', 'Met', GREEN_L, GREEN),
        ],
        'footer': 'Backup & Restore Reference',
    },
    'install-upgrade': {
        'subtitle': 'Install / Upgrade Sequence',
        'boxes': [
            ('Pre-Check', '& Staging', '#e3f2fd', '#1565c0'),
            ('Download /', 'Stage Image', '#e8eaf6', '#3949ab'),
            ('Apply &', 'Reboot', '#fff8e1', '#f57f17'),
            ('Validate', 'Services', '#fce4ec', '#c62828'),
            ('✓ Version', 'Confirmed', GREEN_L, GREEN),
        ],
        'footer': 'Install & Upgrade Reference',
    },
    'scripts': {
        'subtitle': 'Automation / Script Flow',
        'boxes': [
            ('Trigger /', 'Schedule', '#e3f2fd', '#1565c0'),
            ('Validate', 'Inputs', '#e8eaf6', '#3949ab'),
            ('Execute', 'Logic', '#fff8e1', '#f57f17'),
            ('Log', 'Results', '#fce4ec', '#c62828'),
            ('✓ Verify', 'Output', GREEN_L, GREEN),
        ],
        'footer': 'Scripts Reference',
    },
    'ports': {
        'subtitle': 'Network Port Topology',
        'boxes': [
            ('Management', 'Ports', '#e3f2fd', '#1565c0'),
            ('Cluster /\nHA Ports', '', '#e8eaf6', '#3949ab'),
            ('Data /\nProtocol', '', '#fff8e1', '#f57f17'),
            ('Replication', 'Ports', '#fce4ec', '#c62828'),
            ('✓ All Ports', 'Secured', GREEN_L, GREEN),
        ],
        'footer': 'Ports Reference',
    },
}

_ASCII_RE   = re.compile(r'```text\n┌[^`]*?┘[ \t]*\n```', re.DOTALL)
_H1_RE      = re.compile(r'^# .+$', re.MULTILINE)
_SUMMARY_RE = re.compile(r'<div class="kb-summary">.*?</div>', re.DOTALL)


def xe(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _rel_assets(page: Path) -> str:
    depth = len(page.parts) - len(DOCS.parts) - 1
    return '../' * depth + 'assets/'


def _product_label(page: Path) -> str:
    parts = page.parts
    docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    segs = [s for s in parts[docs_idx + 1: -1]
            if s not in ('operations', 'security', 'troubleshooting')]
    return ' / '.join(s.replace('-', ' ').title() for s in segs[:3])


def make_svg(page_type: str, product_label: str, page_title: str) -> str:
    cfg = PAGE_TYPES[page_type]
    boxes = cfg['boxes']
    n = len(boxes)
    total_arrow = (n - 1) * ARW_W
    box_w = (SVG_W - 2 * PAD - total_arrow) // n

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" '
        f"font-family=\"'Segoe UI',Arial,sans-serif\">",
        f'  <rect width="{SVG_W}" height="{SVG_H}" fill="#f4f6f9"/>',
        f'  <rect x="0" y="0" width="{SVG_W}" height="{HDR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="25" text-anchor="middle" fill="white" '
        f'font-size="13" font-weight="700">{xe(page_title[:80])}</text>',
        f'  <text x="410" y="37" text-anchor="middle" fill="{FOOTER_FG}" '
        f'font-size="9">{xe(product_label)} — {xe(cfg["subtitle"])}</text>',
    ]

    x = PAD
    for i, (l1, l2, fill, stroke) in enumerate(boxes):
        l1_clean = l1.replace('\n', ' ').strip()
        cx = x + box_w // 2
        lines.append(
            f'  <rect x="{x}" y="{BOX_Y}" width="{box_w}" height="{BOX_H}" '
            f'fill="{fill}" rx="4" stroke="{stroke}" stroke-width="1.5"/>'
        )
        ty = BOX_Y + (BOX_H // 2 - (5 if l2 else 0))
        lines.append(
            f'  <text x="{cx}" y="{ty}" text-anchor="middle" '
            f'fill="{TEXT_DARK}" font-size="10" font-weight="700">{xe(l1_clean)}</text>'
        )
        if l2:
            lines.append(
                f'  <text x="{cx}" y="{ty + 14}" text-anchor="middle" '
                f'fill="{TEXT_MID}" font-size="9">{xe(l2)}</text>'
            )
        if i < n - 1:
            ax = x + box_w
            ay = BOX_Y + BOX_H // 2
            lines += [
                f'  <line x1="{ax}" y1="{ay}" x2="{ax + ARW_W - 3}" y2="{ay}" '
                f'stroke="{TEXT_LIGHT}" stroke-width="1.5"/>',
                f'  <polygon points="{ax + ARW_W - 3},{ay - 4} '
                f'{ax + ARW_W + 1},{ay} {ax + ARW_W - 3},{ay + 4}" fill="{TEXT_LIGHT}"/>',
            ]
        x += box_w + ARW_W

    lines += [
        f'  <rect x="0" y="{FTR_Y}" width="{SVG_W}" height="{FTR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="{FTR_Y + 16}" text-anchor="middle" '
        f'fill="{FOOTER_FG}" font-size="9">{xe(product_label)} · {xe(cfg["footer"])}</text>',
        '</svg>',
    ]

    svg = '\n'.join(lines)
    ET.fromstring(svg)
    return svg


def _slug_from_path(page: Path) -> str:
    parts = page.parts
    docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    slug = '-'.join(parts[docs_idx + 1:]).replace('/', '-').replace('.md', '')
    return re.sub(r'[^a-z0-9-]', '-', slug.lower()).strip('-')[:60]


def _page_title(text: str, page: Path) -> str:
    m = _H1_RE.search(text)
    if m:
        return m.group(0).lstrip('# ').strip()
    return page.stem.replace('-', ' ').title()


def process_page(page: Path, dry_run: bool = False) -> int:
    page_type = page.stem
    if page_type not in PAGE_TYPES:
        return 0

    text = page.read_text(encoding='utf-8')
    product_label = _product_label(page)
    title = _page_title(text, page)
    rel_assets = _rel_assets(page)
    svg_fname = _slug_from_path(page) + '.svg'
    svg_path  = ASSETS / svg_fname

    if not dry_run:
        svg = make_svg(page_type, product_label, title)
        svg_path.write_text(svg, encoding='utf-8')

        new_text = _ASCII_RE.sub('', text)
        img_ref = f'\n![{title}]({rel_assets}{svg_fname})\n'
        already = img_ref.strip() in new_text
        if not already:
            if _SUMMARY_RE.search(new_text):
                new_text = _SUMMARY_RE.sub(lambda m: m.group(0) + img_ref, new_text, count=1)
            else:
                new_text = _H1_RE.sub(lambda m: m.group(0) + img_ref, new_text, count=1)
            page.write_text(new_text, encoding='utf-8')

    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--type', nargs='+', metavar='TYPE',
                        choices=list(PAGE_TYPES.keys()),
                        help='Limit to specific page types')
    parser.add_argument('--path', help='Limit to pages under this docs/ subpath')
    args = parser.parse_args()

    target_types = set(args.type) if args.type else set(PAGE_TYPES.keys())

    pages = [
        p for p in sorted(DOCS.rglob('*.md'))
        if p.stem in target_types
    ]
    if args.path:
        pages = [p for p in pages if args.path in str(p)]

    total = 0
    for page in pages:
        total += process_page(page, dry_run=args.dry_run)

    print(f'Total SVGs {"(dry run)" if args.dry_run else "generated"}: {total}')


if __name__ == '__main__':
    main()
