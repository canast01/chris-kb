"""
Convert a Mermaid `graph`/`flowchart` block containing `subgraph` groups into
a clean, non-crossing layered SVG diagram, and replace the block in its
source .md page with an <img> reference to the generated asset.

Why: Mermaid's own auto-layout renders these with crossing arrows because it
doesn't understand the semantic grouping. This script instead does a real
(if simplified) layered-graph layout: treat each subgraph as one visual
"unit" containing its member nodes, treat each standalone node as its own
unit, rank units by longest path from a root, order units within a rank by
the average position of their predecessors (barycenter heuristic), and draw
edges strictly top-to-bottom between adjacent ranks -- so nothing crosses.

Usage:
  python3 scripts/mermaid_subgraph_to_svg.py --dry-run     # generate SVGs only, report
  python3 scripts/mermaid_subgraph_to_svg.py --apply       # generate SVGs + inject into pages
  python3 scripts/mermaid_subgraph_to_svg.py --apply path/to/one.md   # single file
  python3 scripts/mermaid_subgraph_to_svg.py --selftest    # run parser regression tests
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svg_overflow_check import text_width_px  # noqa: E402

W = 820
PALETTE = [
    ("#e3f2fd", "#1565c0", "#1a2744"),  # blue
    ("#e8eaf6", "#3949ab", "#1a2744"),  # indigo
    ("#e8f5e9", "#2e7d32", "#1a2744"),  # green
    ("#fff8e1", "#f57f17", "#1a2744"),  # amber
    ("#fce4ec", "#c62828", "#1a2744"),  # red
]

MERMAID_RE = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
ARROW_RE = re.compile(r'(<-->|-\.->|--[ox]|-->)\s*(?:\|"?([^|]*?)"?\|)?\s*')
SUBGRAPH_START_RE = re.compile(r'^subgraph\s+(.+)$')
SUBGRAPH_ID_BRACKET_RE = re.compile(r'^(\S+)\s*\[(.*)\]$')
SUBGRAPH_QUOTED_ONLY_RE = re.compile(r'^"(.*)"$')


def slugify(s: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9]+', '_', s).strip('_')
    return s or 'sg'


def split_unquoted(text: str, sep: str) -> list:
    """Split text on sep, but never inside a "..." quoted region -- a label
    like ["Command Authorization\\n& Accounting"] contains a literal & that
    must not be mistaken for the fan-out A --> B & C syntax."""
    parts = []
    buf = []
    in_quotes = False
    for ch in text:
        if ch == '"':
            in_quotes = not in_quotes
            buf.append(ch)
        elif ch == sep and not in_quotes:
            parts.append(''.join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append(''.join(buf))
    return parts
NODE_DECL_RE = re.compile(r'^(\w+)\s*(\(\[|\[\(|\(\(|\[\[|\{\{|\[|\(|\{)(.*)$')
CLOSE_FOR = {'([': '])', '[(': ')]', '((': '))', '[[': ']]', '{{': '}}',
             '[': ']', '(': ')', '{': '}'}


def xe(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


BR_RE = re.compile(r'<br\s*/?>', re.IGNORECASE)


HTML_ENTITIES = {'&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'"}


def norm_label(s: str) -> str:
    """Normalize a Mermaid label: unescape HTML entities (source often has
    &amp; for a literal &, which our own xe() would otherwise double-escape
    into a literal "&amp;" on the page), and turn \\n / <br/> into real
    newlines."""
    for ent, ch in HTML_ENTITIES.items():
        s = s.replace(ent, ch)
    s = BR_RE.sub('\n', s)
    return s.replace('\\n', '\n')


def strip_label(raw: str, open_tok: str) -> str:
    """Given text after the opening bracket token, strip the matching close
    and any surrounding quotes, return the inner label."""
    close = CLOSE_FOR[open_tok]
    if raw.endswith(close):
        raw = raw[: -len(close)]
    raw = raw.strip()
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    return raw


class Graph:
    def __init__(self):
        self.nodes = {}       # id -> {'label': str, 'subgraph': id or None}
        self.subgraphs = {}   # id -> {'title': str, 'members': [id,...]}
        self.sg_order = []    # order subgraphs first appear
        self.edges = []       # (src_id, dst_id, label, style)

    def ensure_node(self, node_id, label=None, subgraph=None):
        if node_id not in self.nodes:
            self.nodes[node_id] = {'label': label or node_id, 'subgraph': subgraph}
            if subgraph:
                self.subgraphs[subgraph]['members'].append(node_id)
        elif label and self.nodes[node_id]['label'] == node_id:
            self.nodes[node_id]['label'] = label


def parse_mermaid(src: str) -> Graph:
    g = Graph()
    sg_stack = []
    for raw_line in src.splitlines():
        line = raw_line.strip()
        if not line or line.startswith('%%'):
            continue
        if line.startswith(('graph ', 'flowchart ')):
            continue
        if line.startswith('direction '):
            continue
        m = SUBGRAPH_START_RE.match(line)
        if m:
            rest = m.group(1).strip()
            mb = SUBGRAPH_ID_BRACKET_RE.match(rest)
            mq = SUBGRAPH_QUOTED_ONLY_RE.match(rest)
            if mb:
                # subgraph id["Title"]  or  subgraph id[Title]
                sg_id, title = mb.group(1), mb.group(2).strip()
                if title.startswith('"') and title.endswith('"'):
                    title = title[1:-1]
            elif mq:
                # subgraph "Title"  -- no separate id, derive one from the title
                title = mq.group(1)
                sg_id = slugify(title)
                while sg_id in g.subgraphs:
                    sg_id += '_'
            else:
                # subgraph id  -- bare id, no title
                sg_id = rest
                title = sg_id
            g.subgraphs[sg_id] = {'title': title, 'members': []}
            g.sg_order.append(sg_id)
            sg_stack.append(sg_id)
            continue
        if line == 'end':
            if sg_stack:
                sg_stack.pop()
            continue

        cur_sg = sg_stack[-1] if sg_stack else None

        # A pure node declaration line (no arrow on it)
        if '-->' not in line and '-.->' not in line and '<-->' not in line \
                and '--x' not in line and '--o' not in line:
            m = NODE_DECL_RE.match(line)
            if m:
                node_id, open_tok, rest = m.groups()
                label = norm_label(strip_label(rest, open_tok))
                g.ensure_node(node_id, label, cur_sg)
            continue

        # An edge line, possibly a chain and/or with & fan-out/fan-in
        pos = 0
        groups = []
        arrows = []
        for am in ARROW_RE.finditer(line):
            groups.append(line[pos:am.start()])
            arrows.append((am.group(1), am.group(2)))
            pos = am.end()
        groups.append(line[pos:])

        def parse_group(text, subgraph_hint):
            ids = []
            for tok in split_unquoted(text, '&'):
                tok = tok.strip()
                if not tok:
                    continue
                m2 = NODE_DECL_RE.match(tok)
                if m2:
                    nid, open_tok, rest = m2.groups()
                    label = norm_label(strip_label(rest, open_tok))
                    g.ensure_node(nid, label, subgraph_hint)
                    ids.append(nid)
                else:
                    nid = tok.split()[0] if tok.split() else tok
                    g.ensure_node(nid, None, subgraph_hint)
                    ids.append(nid)
            return ids

        node_groups = [parse_group(t, cur_sg) for t in groups]
        for i, (arrow, label) in enumerate(arrows):
            style = 'dotted' if arrow == '-.->' else ('bidir' if arrow == '<-->' else 'solid')
            for src in node_groups[i]:
                for dst in node_groups[i + 1]:
                    edge_label = BR_RE.sub(' ', (label or '')).replace('\\n', ' ')
                    for _ent, _ch in HTML_ENTITIES.items():
                        edge_label = edge_label.replace(_ent, _ch)
                    g.edges.append((src, dst, edge_label, style))
    return g


def unit_of(g: Graph, node_id: str) -> str:
    sg = g.nodes[node_id]['subgraph']
    return f'sg:{sg}' if sg else f'n:{node_id}'


def layout(g: Graph):
    """Rank subgraph/standalone units by longest path from roots, order
    within rank by predecessor barycenter, return (ranks, unit_edges,
    internal_edges_by_sg)."""
    unit_edges = set()
    internal = {sg: [] for sg in g.subgraphs}
    for src, dst, label, style in g.edges:
        us, ud = unit_of(g, src), unit_of(g, dst)
        if us == ud and us.startswith('sg:'):
            internal[us[3:]].append((src, dst, label, style))
        elif us != ud:
            unit_edges.add((us, ud))

    all_units = set()
    for nid in g.nodes:
        all_units.add(unit_of(g, nid))

    preds = {u: set() for u in all_units}
    succs = {u: set() for u in all_units}
    for us, ud in unit_edges:
        preds[ud].add(us)
        succs[us].add(ud)

    rank = {}

    def compute_rank(u, seen):
        if u in rank:
            return rank[u]
        if u in seen:
            return 0  # cycle guard
        seen = seen | {u}
        if not preds[u]:
            rank[u] = 0
        else:
            rank[u] = 1 + max(compute_rank(p, seen) for p in preds[u])
        return rank[u]

    for u in all_units:
        compute_rank(u, set())

    max_rank = max(rank.values()) if rank else 0
    rows = [[] for _ in range(max_rank + 1)]
    for u, r in rank.items():
        rows[r].append(u)

    # order rank 0 by first-appearance in node dict; subsequent ranks by
    # barycenter of predecessor x-index in previous row
    first_seen_order = []
    for nid in g.nodes:
        u = unit_of(g, nid)
        if u not in first_seen_order:
            first_seen_order.append(u)

    rows[0].sort(key=lambda u: first_seen_order.index(u))
    prev_index = {u: i for i, u in enumerate(rows[0])}
    for r in range(1, len(rows)):
        def bary(u):
            ps = [prev_index[p] for p in preds[u] if p in prev_index]
            return sum(ps) / len(ps) if ps else first_seen_order.index(u)
        rows[r].sort(key=bary)
        prev_index = {u: i for i, u in enumerate(rows[r])}

    return rows, unit_edges, internal


def render_svg(title: str, g: Graph, rows, unit_edges, internal) -> str:
    HEADER_H = 30
    ROW_GAP = 40
    NODE_H = 40
    NODE_W_MIN = 140
    SG_PAD = 12
    SG_HEADER_H = 22
    MARGIN_X = 20

    def measure(label_lines, font_size, bold_first=False):
        widest = 0
        for i, ln in enumerate(label_lines):
            w = text_width_px(ln, font_size, bold_first and i == 0)
            widest = max(widest, w)
        return widest

    # Precompute each unit's intrinsic width and internal height
    unit_w = {}
    unit_h = {}
    unit_members = {}
    for r_units in rows:
        for u in r_units:
            if u.startswith('sg:'):
                sg = u[3:]
                members = g.subgraphs[sg]['members']
                unit_members[u] = members
                mem_widths = []
                for m in members:
                    lines = g.nodes[m]['label'].split('\n')
                    w = measure(lines, 10) + 20
                    mem_widths.append(max(w, 110))
                title_w = measure([g.subgraphs[sg]['title']], 11, True) + 24
                content_w = sum(mem_widths) + 10 * (len(mem_widths) + 1)
                unit_w[u] = max(content_w, title_w, NODE_W_MIN)
                lines_per_member = max(len(g.nodes[m]['label'].split('\n')) for m in members) if members else 1
                unit_h[u] = SG_HEADER_H + 10 + lines_per_member * 15 + 14
            else:
                nid = u[2:]
                unit_members[u] = [nid]
                lines = g.nodes[nid]['label'].split('\n')
                w = measure(lines, 11, True) + 24
                unit_w[u] = max(w, NODE_W_MIN)
                unit_h[u] = 20 + len(lines) * 17

    row_h = [max((unit_h[u] for u in r_units), default=NODE_H) for r_units in rows]

    y_cursor = HEADER_H + 20
    row_y = []
    for h in row_h:
        row_y.append(y_cursor)
        y_cursor += h + ROW_GAP
    content_bottom = y_cursor - ROW_GAP

    # Canvas width must fit the widest row -- never clip content to a fixed
    # 820px. Grow (never shrink) if a row genuinely needs more room.
    gap = 30
    row_widths = [sum(unit_w[u] for u in r_units) + gap * (len(r_units) - 1) for r_units in rows]
    widest_row = max(row_widths, default=0)
    canvas_w = max(W, int(widest_row + 2 * MARGIN_X))

    # x positions: center each row's units, spaced evenly
    unit_pos = {}
    for r_units, ry, rh, total_w in zip(rows, row_y, row_h, row_widths):
        start_x = max(MARGIN_X, (canvas_w - total_w) / 2)
        x = start_x
        for u in r_units:
            unit_pos[u] = (x, ry, unit_w[u], rh)
            x += unit_w[u] + gap

    footer_y = content_bottom + 10
    total_h = footer_y + 30

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{total_h}" '
        f'viewBox="0 0 {canvas_w} {total_h}">'
    )
    parts.append('<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" '
                  'refX="10" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" '
                  'fill="#455a64" /></marker></defs>')
    parts.append(f'<rect x="0" y="0" width="{canvas_w}" height="{HEADER_H}" fill="#1a2744" />')
    parts.append(f'<text x="10" y="20" font-family="Arial,Helvetica,sans-serif" '
                 f'font-size="14" font-weight="bold" fill="#ffffff">{xe(title)}</text>')

    color_by_unit = {}
    color_i = 0
    for r_units in rows:
        for u in r_units:
            color_by_unit[u] = PALETTE[color_i % len(PALETTE)]
            color_i += 1

    anchor = {}  # unit -> (top_cx, top_y, bot_cx, bot_y)
    node_anchor = {}  # node_id -> (cx, top_y, bot_y) absolute, for internal edges

    for u in [uu for r in rows for uu in r]:
        ux, uy, uw, uh = unit_pos[u]
        light, dark, textdark = color_by_unit[u]
        cx = ux + uw / 2
        anchor[u] = (cx, uy, cx, uy + uh)

        if u.startswith('sg:'):
            sg = u[3:]
            members = unit_members[u]
            parts.append(f'<rect x="{ux:.1f}" y="{uy:.1f}" width="{uw:.1f}" height="{uh:.1f}" '
                         f'rx="6" fill="{light}" stroke="{dark}" stroke-width="1.2" />')
            parts.append(f'<text x="{cx:.1f}" y="{uy+16:.1f}" text-anchor="middle" '
                         f'font-family="Arial,Helvetica,sans-serif" font-size="11" '
                         f'font-weight="700" fill="{textdark}">{xe(g.subgraphs[sg]["title"])}</text>')
            n = len(members)
            gap = 10
            mem_widths = []
            for m in members:
                lines = g.nodes[m]['label'].split('\n')
                w = max(measure(lines, 10) + 20, 110)
                mem_widths.append(w)
            content_w = sum(mem_widths) + gap * (n + 1)
            mx = ux + (uw - content_w) / 2 + gap
            my = uy + SG_HEADER_H + 8
            mh = uh - SG_HEADER_H - 16
            for m, mw in zip(members, mem_widths):
                mcx = mx + mw / 2
                parts.append(f'<rect x="{mx:.1f}" y="{my:.1f}" width="{mw:.1f}" height="{mh:.1f}" '
                             f'rx="4" fill="#ffffff" stroke="{dark}" stroke-width="1" />')
                lines = g.nodes[m]['label'].split('\n')
                ly = my + mh / 2 - (len(lines) - 1) * 7.5 + 4
                for ln in lines:
                    parts.append(f'<text x="{mcx:.1f}" y="{ly:.1f}" text-anchor="middle" '
                                 f'font-family="Arial,Helvetica,sans-serif" font-size="9.5" '
                                 f'fill="#37474f">{xe(ln)}</text>')
                    ly += 14
                node_anchor[m] = (mcx, my, my + mh)
                mx += mw + gap
        else:
            nid = members = unit_members[u][0]
            parts.append(f'<rect x="{ux:.1f}" y="{uy:.1f}" width="{uw:.1f}" height="{uh:.1f}" '
                         f'rx="6" fill="{light}" stroke="{dark}" stroke-width="1.2" />')
            lines = g.nodes[nid]['label'].split('\n')
            ly = uy + uh / 2 - (len(lines) - 1) * 8 + 4
            for i, ln in enumerate(lines):
                parts.append(f'<text x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle" '
                             f'font-family="Arial,Helvetica,sans-serif" font-size="11" '
                             f'font-weight="{"700" if i == 0 else "400"}" '
                             f'fill="{textdark}">{xe(ln)}</text>')
                ly += 16
            node_anchor[nid] = (cx, uy, uy + uh)

    # inter-rank edges (unit -> unit), drawn from bottom-center of src to
    # top-center of dst; label at midpoint
    label_i = 0
    for us, ud in sorted(unit_edges, key=lambda e: (rows_index(rows, e[0]), rows_index(rows, e[1]))):
        sx, _, _, sby = anchor[us]
        dx, dty, _, _ = anchor[ud]
        # find a representative edge label if any
        lbl = ''
        for s, d, label, style in g.edges:
            if unit_of(g, s) == us and unit_of(g, d) == ud and label:
                lbl = label
                break
        mid_y = (sby + dty) / 2
        parts.append(f'<line x1="{sx:.1f}" y1="{sby:.1f}" x2="{dx:.1f}" y2="{dty:.1f}" '
                     f'stroke="#455a64" stroke-width="1.5" marker-end="url(#arrowhead)" />')
        if lbl:
            lcx = (sx + dx) / 2
            lbl_w = text_width_px(lbl, 8.5, False) + 10
            parts.append(f'<rect x="{lcx-lbl_w/2:.1f}" y="{mid_y-9:.1f}" width="{lbl_w:.1f}" '
                         f'height="14" fill="#ffffff" opacity="0.85"/>')
            parts.append(f'<text x="{lcx:.1f}" y="{mid_y+2:.1f}" text-anchor="middle" '
                         f'font-family="Arial,Helvetica,sans-serif" font-size="8.5" '
                         f'fill="#546e7a">{xe(lbl)}</text>')

    # internal (within-subgraph) edges: draw a short connector between the
    # two member boxes if they are adjacent; otherwise a small curved hint
    for sg, edges in internal.items():
        for src, dst, label, style in edges:
            if src not in node_anchor or dst not in node_anchor:
                continue
            sx, sty, sby = node_anchor[src]
            dx, dty, dby = node_anchor[dst]
            y = (sby + dty) / 2 if sby <= dty else min(sby, dby) - 6
            parts.append(f'<line x1="{sx:.1f}" y1="{sby:.1f}" x2="{dx:.1f}" y2="{dty:.1f}" '
                         f'stroke="#78909c" stroke-width="1.2" stroke-dasharray="3,2" '
                         f'marker-end="url(#arrowhead)" />' if abs(sx - dx) < 1 else
                         f'<line x1="{sx:.1f}" y1="{(sty+sby)/2:.1f}" x2="{dx:.1f}" y2="{(dty+dby)/2:.1f}" '
                         f'stroke="#78909c" stroke-width="1.2" stroke-dasharray="3,2" />')

    parts.append(f'<rect x="0" y="{footer_y:.1f}" width="{canvas_w}" height="30" fill="#f5f7fa" />')
    parts.append(f'<text x="10" y="{footer_y+20:.1f}" font-family="Arial,Helvetica,sans-serif" '
                 f'font-size="10" fill="#9e9e9e">Diagram Type: {xe(title)}</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


def rows_index(rows, unit):
    for i, r in enumerate(rows):
        if unit in r:
            return i
    return 0


# ── Page-level driver ───────────────────────────────────────────────────────

H1_RE = re.compile(r'^#\s+(.+)$', re.MULTILINE)
HEADING_BEFORE_RE = re.compile(r'^##+\s+(.+)$', re.MULTILINE)


def strip_code_fences(text: str) -> str:
    """Blank out fenced code-block bodies (preserving exact line lengths, so
    character offsets in the result still line up with the original text)
    so a '##'-prefixed bash/text comment inside a fence can't be mistaken
    for a real Markdown heading."""
    out = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.strip().startswith(('```', '~~~')):
            in_fence = not in_fence
            out.append(line)
        elif in_fence:
            stripped = line.rstrip('\n')
            out.append(' ' * len(stripped) + line[len(stripped):])
        else:
            out.append(line)
    return ''.join(out)


def page_title(md_text: str, block_start: int) -> str:
    """Nearest ## heading before the mermaid block, else the H1, else 'Diagram'."""
    clean = strip_code_fences(md_text)
    headings = list(HEADING_BEFORE_RE.finditer(clean, 0, block_start))
    if headings:
        return headings[-1].group(1).strip()
    h1 = H1_RE.search(clean)
    if h1:
        return h1.group(1).strip()
    return 'Diagram'


def slug_for(md_path: Path, index: int) -> str:
    parts = [p for p in md_path.parts if p not in ('docs', 'index.md')]
    base = '-'.join(parts).replace('.md', '')
    base = re.sub(r'[^a-z0-9-]', '-', base.lower())
    base = re.sub(r'-+', '-', base).strip('-')
    suffix = f'-{index}' if index else ''
    return f'{base}-mermaid-svg{suffix}.svg'


def rel_to_assets(md_path: Path) -> str:
    parts = md_path.parts
    docs_idx = parts.index('docs')
    depth = len(parts) - docs_idx - 2
    return '../' * depth + 'assets/'


def process_file(md_path: Path, assets_dir: Path, dry_run: bool):
    text = md_path.read_text(encoding='utf-8')
    matches = list(MERMAID_RE.finditer(text))
    sg_matches = [m for m in matches if 'subgraph' in m.group(1)]
    if not sg_matches:
        return None

    results = []
    new_text = text
    offset_shift = 0
    for idx, m in enumerate(sg_matches):
        src = m.group(1)
        try:
            g = parse_mermaid(src)
            if not g.nodes:
                results.append((md_path, idx, 'SKIP: no nodes parsed'))
                continue
            rows, unit_edges, internal = layout(g)
            title = page_title(text, m.start())
            svg = render_svg(title, g, rows, unit_edges, internal)
        except Exception as e:
            results.append((md_path, idx, f'ERROR: {e}'))
            continue

        fname = slug_for(md_path, idx)
        svg_path = assets_dir / fname
        if not dry_run:
            svg_path.write_text(svg, encoding='utf-8')

        rel = rel_to_assets(md_path)
        img_md = f'![{title}]({rel}{fname})'
        if not dry_run:
            start = m.start() + offset_shift
            end = m.end() + offset_shift
            new_text = new_text[:start] + img_md + new_text[end:]
            offset_shift += len(img_md) - (end - start)

        results.append((md_path, idx, f'OK: {fname} ({len(g.nodes)} nodes, '
                                       f'{len(g.subgraphs)} subgraphs, {len(rows)} ranks)'))

    if not dry_run and new_text != text:
        md_path.write_text(new_text, encoding='utf-8')

    return results


# ── Regression tests ─────────────────────────────────────────────────────────
# Both found 2026-07-04, AFTER the initial 137-diagram conversion had already
# shipped and been verified "clean" -- the bugs didn't crash anything, they
# silently produced wrong/garbage output that only surfaced on a second,
# closer look. Encoded here so the parser can never silently regress on
# these two syntax forms again.

def _selftest():
    cases_passed = 0

    # Bug 1: `subgraph "Title"` (quoted title, no separate id) was completely
    # unrecognized -- SUBGRAPH_START_RE required an id before an optional
    # [bracketed] title, so a bare quoted title matched nothing at all and
    # its member nodes silently fell out of the subgraph entirely.
    src1 = '''graph LR
  subgraph "My Title"
    A["Node A"]
    B["Node B"]
  end
  A --> B
'''
    g1 = parse_mermaid(src1)
    assert len(g1.subgraphs) == 1, f'expected 1 subgraph, got {len(g1.subgraphs)}'
    title = list(g1.subgraphs.values())[0]['title']
    assert title == 'My Title', f'expected title "My Title", got {title!r}'
    assert g1.nodes['A']['subgraph'] is not None, 'node A should be inside the subgraph'
    cases_passed += 1

    # Bug 2: a literal & inside a quoted label (e.g. "Authorization\n& Accounting")
    # was mistaken for the A --> B & C fan-out syntax, splitting one label into
    # a garbage node whose id was literally the tail of the label plus a
    # trailing quote/bracket.
    src2 = '''graph LR
  A["Start"]
  A --> B["Command Authorization\\n& Accounting"]
'''
    g2 = parse_mermaid(src2)
    assert 'B' in g2.nodes, 'node B should exist'
    assert g2.nodes['B']['label'] == 'Command Authorization\n& Accounting', \
        f'label corrupted: {g2.nodes["B"]["label"]!r}'
    assert len(g2.nodes) == 2, f'expected exactly 2 nodes, got {len(g2.nodes)}: {list(g2.nodes)}'
    cases_passed += 1

    print(f'selftest: {cases_passed}/2 regression cases passed')
    return 0


def main():
    if '--selftest' in sys.argv:
        return _selftest()

    dry_run = '--apply' not in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]

    assets_dir = Path('docs/assets')
    if args:
        files = [Path(a) for a in args]
    else:
        files = sorted(Path('docs').rglob('*.md'))

    total_ok, total_err, total_skip = 0, 0, 0
    for f in files:
        text = f.read_text(encoding='utf-8')
        if 'subgraph' not in text or '```mermaid' not in text:
            continue
        results = process_file(f, assets_dir, dry_run)
        if not results:
            continue
        for path, idx, status in results:
            print(f'{path} [{idx}]: {status}')
            if status.startswith('OK'):
                total_ok += 1
            elif status.startswith('ERROR'):
                total_err += 1
            else:
                total_skip += 1

    mode = 'DRY RUN' if dry_run else 'APPLIED'
    print(f'\n{mode}: {total_ok} converted, {total_err} errors, {total_skip} skipped')


if __name__ == '__main__':
    sys.exit(main())
