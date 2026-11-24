#!/usr/bin/env python3
"""Fix the 3-column comparison table in *-overview SVGs (Check 69).

Found 2026-11-24: the generator centred cell text on equal thirds
(x=183/411/639) but drew the column dividers at x=346/573, so wide cells ran
over a divider. Table spans x=20..803 (header rect at y=510). Rewrites it as
three equal columns: dividers at 281/542, text centred at 150.5/411.5/672.5.
Only touches files with that exact header rect. Idempotent.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svg_edge_crossing import _text_width, ASSETS

HDR = '<rect x="20" y="510" width="783" height="30" fill="#1e293b"/>'
DIV = {'346': '281', '573': '542'}
TXT = {'183': '150.5', '411': '411.5', '639': '672.5'}
COL_W = 783 / 3


def fix(path):
    s = open(path, encoding='utf-8').read()
    if HDR not in s:
        return False
    m = re.search(r'<line x1="346" y1="510" x2="346" y2="(\d+)"', s)
    if not m:
        return False
    y_end = int(m.group(1))

    def div(mm):
        return f'<line x1="{DIV[mm.group(1)]}" y1="510" x2="{DIV[mm.group(1)]}" y2="{mm.group(2)}"'
    s = re.sub(r'<line x1="(346|573)" y1="510" x2="\1" y2="(\d+)"', div, s)

    def txt(mm):
        y = float(mm.group(2))
        if not 510 <= y <= y_end:
            return mm.group(0)
        body = mm.group(0)
        fs = float(re.search(r'font-size="([\d.]+)"', body).group(1))
        content = re.search(r'>([^<]*)</text>', body).group(1)
        if _text_width(content, fs, 'bold' in body) > COL_W - 12:
            print(f'  WARN {os.path.basename(path)}: "{content}" wider than column')
        return f'<text x="{TXT[mm.group(1)]}" y="{mm.group(2)}"' + body[mm.end(2) + 1 - mm.start():]
    s = re.sub(r'<text x="(183|411|639)" y="([\d.]+)"[^>]*>[^<]*</text>', txt, s)
    open(path, 'w', encoding='utf-8').write(s)
    return True


if __name__ == '__main__':
    n = sum(fix(os.path.join(ASSETS, f)) for f in sorted(os.listdir(ASSETS)) if f.endswith('.svg'))
    print(f'fixed {n} files')


# ── interaction-map-*.svg: 4-column integration table ───────────────────────
# Same bug, found the same day: text centred at x=120/320/520/700 but the
# dividers drawn at 240/435/630. Move dividers to the midpoints between column
# centres (220/420/610) so every column's text sits inside its column.
IM_DIV = {'240': '220', '435': '420', '630': '610'}


def fix_interaction_map(path):
    s = open(path, encoding='utf-8').read()
    if '<text x="120" y="535"' not in s:
        return False
    new = re.sub(r'<line x1="(240|435|630)" y1="516" x2="\1"',
                 lambda m: f'<line x1="{IM_DIV[m.group(1)]}" y1="516" x2="{IM_DIV[m.group(1)]}"', s)
    if new != s:
        open(path, 'w', encoding='utf-8').write(new)
    return new != s


if __name__ == '__main__':
    n = sum(fix_interaction_map(os.path.join(ASSETS, f)) for f in sorted(os.listdir(ASSETS))
            if f.startswith('interaction-map-') and f.endswith('.svg'))
    print(f'interaction maps fixed: {n}')
