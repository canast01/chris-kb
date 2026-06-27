#!/usr/bin/env python3
"""
ascii_to_svg.py — Convert ```text ASCII diagram blocks to proper SVG files.

Scans docs/ for ```text blocks containing ≥10 box-drawing characters,
calls OpenAI gpt-4o to generate clean SVG XML, saves to docs/assets/,
and replaces the ```text block in-place with a Markdown image reference.

Usage:
  python3 scripts/ascii_to_svg.py --dry-run          # preview, no writes
  python3 scripts/ascii_to_svg.py --limit 5          # first 5 diagrams only
  python3 scripts/ascii_to_svg.py --section vmware   # path substring filter
  python3 scripts/ascii_to_svg.py --force            # overwrite existing SVGs
  python3 scripts/ascii_to_svg.py                    # all diagrams
"""
import argparse
import html.entities
import re
import time
from pathlib import Path
from defusedxml import ElementTree as ET

from openai import OpenAI, OpenAIError, RateLimitError, APIConnectionError, APITimeoutError

REPO   = Path(__file__).parent.parent.resolve()
DOCS   = REPO / 'docs'
ASSETS = REPO / 'docs' / 'assets'

BOX_CHARS   = set('┌┐└┘│─├┤┬┴┼╔╗╚╝║═╠╣╦╩╬▼▲►◄→←↑↓')
BOX_MIN     = 10        # minimum box-drawing chars to treat as diagram
CALL_PAUSE  = 1.2       # seconds between OpenAI calls
RETRY_PAUSE = 30        # seconds before retrying on rate limit

BLOCK_RE = re.compile(r'```text\n(.*?\n)```', re.DOTALL)
H1_RE    = re.compile(r'^# (.+)$', re.MULTILINE)

SYSTEM_PROMPT = """\
You are an expert SVG diagram generator for a technical knowledge base.
Convert ASCII art diagrams into clean, professional SVG XML.

STRICT REQUIREMENTS — violating any will cause the output to be rejected:
1. Output ONLY valid SVG XML. Start with <svg xmlns="http://www.w3.org/2000/svg"
   and end with </svg>. No markdown fences, no explanation, no comments.
2. Width MUST be exactly 820. Height should fit the content (200–700px).
3. Define an arrowhead marker in <defs> and use it on connection lines.
4. Escape ALL special characters in text nodes: & → &amp;  < → &lt;  > → &gt;
5. No JavaScript. No <foreignObject>. No <html>. Pure SVG only.
6. font-family="Arial,Helvetica,sans-serif" on all text elements.

VISUAL STYLE:
- Background: white (#ffffff)
- Header bar at top: fill="#1a2744" with white title text (font-size="14" font-weight="bold")
- Component boxes: rounded corners (rx="6"), light fills, dark borders
  Palette: #e3f2fd/#1565c0  #e8eaf6/#3949ab  #e8f5e9/#2e7d32  #fff8e1/#f57f17  #fce4ec/#c62828
- Arrow/connection lines: stroke="#455a64" stroke-width="1.5"
- Label text: font-size="11" fill="#1a2744"
- Sub-label text: font-size="10" fill="#37474f"
- Footer bar at bottom: fill="#f5f7fa" with small grey text showing the diagram type

CONTENT:
- Reproduce ALL labels, component names, port numbers, and annotations from the ASCII art
- Maintain the same topology/layout (horizontal flow → keep horizontal, vertical stack → keep vertical)
- Group related components visually
"""

client = OpenAI()


def slug_from_path(page: Path, idx: int = 0) -> str:
    """Derive SVG asset filename from page path."""
    rel   = page.relative_to(DOCS)
    parts = list(rel.parts)
    if parts[-1] == 'index.md':
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace('.md', '')
    slug   = '-'.join(p.replace('_', '-') for p in parts) if parts else 'home'
    suffix = f'-d{idx + 1}' if idx > 0 else '-diagram'
    return f'{slug}{suffix}.svg'


def rel_assets(page: Path) -> str:
    """Relative path from page to docs/assets/."""
    depth = len(page.relative_to(DOCS).parts) - 1
    return '../' * depth + 'assets/'


def page_title(content: str, page: Path) -> str:
    m = H1_RE.search(content)
    raw = m.group(1).strip() if m else page.stem.replace('-', ' ').title()
    return raw.replace(']', ')').replace('[', '(')


def is_diagram(block_text: str) -> bool:
    count = sum(1 for c in block_text if c in BOX_CHARS)
    return count >= BOX_MIN


def call_openai(ascii_art: str, title: str, path_hint: str) -> str | None:
    """Return SVG string, or None on unrecoverable error."""
    user_msg = (
        f"Page: {title}\n"
        f"Section: {path_hint}\n\n"
        f"ASCII art to convert:\n```\n{ascii_art.strip()}\n```"
    )
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user',   'content': user_msg},
                ],
                temperature=0.2,
                max_tokens=8192,
            )
            if not resp.choices:
                print(f'    SKIPPED — empty choices (content filtered)', flush=True)
                return None
            content = resp.choices[0].message.content
            if content is None:
                print(f'    SKIPPED — null content in response', flush=True)
                return None
            return content.strip()
        except (RateLimitError, APIConnectionError, APITimeoutError) as e:
            label = 'rate limit' if isinstance(e, RateLimitError) else 'connection error'
            if attempt < 2:
                print(f'    {label} — retrying in {RETRY_PAUSE}s…', flush=True)
                time.sleep(RETRY_PAUSE)
            else:
                print(f'    SKIPPED — {label} after 3 attempts', flush=True)
                return None
        except OpenAIError as e:
            print(f'    SKIPPED — OpenAI error: {e}', flush=True)
            return None


_XML_SAFE_ENTITIES = {'amp', 'lt', 'gt', 'quot', 'apos'}

def _fix_html_entities(s: str) -> str:
    """Replace named HTML entities (not valid in XML) with their Unicode chars."""
    def replace(m: re.Match) -> str:
        name = m.group(1)
        if name in _XML_SAFE_ENTITIES:
            return m.group(0)
        char = html.entities.html5.get(name + ';')
        if char:
            return char
        cp = html.entities.name2codepoint.get(name)
        if cp:
            return chr(cp)
        return m.group(0)
    return re.sub(r'&([a-zA-Z][a-zA-Z0-9]*);', replace, s)


def clean_svg(raw: str) -> str:
    """Strip markdown fences and fix HTML entities so the XML is valid."""
    raw = raw.strip()
    if raw.startswith('```'):
        raw = re.sub(r'^```[a-zA-Z0-9]*\n?', '', raw)
        raw = re.sub(r'\n?```$', '', raw)
    return _fix_html_entities(raw.strip())


def validate_svg(xml_str: str) -> bool:
    try:
        root = ET.fromstring(xml_str)
        tag  = root.tag
        if tag not in ('svg', '{http://www.w3.org/2000/svg}svg'):
            print(f'    SKIPPED — root element is <{tag}>, expected <svg>', flush=True)
            return False
        return True
    except Exception as e:
        print(f'    SKIPPED — XML validation failed: {e}', flush=True)
        return False


def process_page(page: Path, content: str, dry_run: bool, force: bool) -> tuple[int, int]:
    """Return (diagrams_found, diagrams_converted)."""
    blocks   = list(BLOCK_RE.finditer(content))
    diagrams = [(m, m.group(1)) for m in blocks if is_diagram(m.group(1))]

    if not diagrams:
        return 0, 0

    title     = page_title(content, page)
    path_hint = str(page.relative_to(DOCS))
    rel_a     = rel_assets(page)

    found     = len(diagrams)
    converted = 0
    new_content = content

    # Process in reverse order so string offsets stay valid
    for idx, (match, ascii_art) in enumerate(reversed(diagrams)):
        real_idx = found - 1 - idx   # actual diagram index (0-based)
        svg_name = slug_from_path(page, real_idx)
        svg_path = ASSETS / svg_name
        img_ref  = f'![{title} — Diagram]({rel_a}{svg_name})'

        print(f'  [{real_idx + 1}/{found}] {svg_name}', flush=True)

        if svg_path.exists() and not force:
            if dry_run:
                print(f'    dry-run: SVG exists, would replace block', flush=True)
            else:
                new_content = (
                    new_content[:match.start()]
                    + img_ref
                    + new_content[match.end():]
                )
                print(f'    SVG exists — replaced block', flush=True)
            converted += 1
            continue

        if dry_run:
            print(f'    dry-run: would generate SVG ({len(ascii_art)} chars)', flush=True)
            converted += 1
            continue

        print(f'    calling gpt-4o…', flush=True)
        raw = call_openai(ascii_art, title, path_hint)
        if raw is None:
            continue
        svg = clean_svg(raw)

        if not validate_svg(svg):
            continue

        try:
            svg_path.write_text(svg, encoding='utf-8')
        except OSError as e:
            print(f'    ERROR — could not write {svg_path.name}: {e}', flush=True)
            continue
        print(f'    saved {svg_path.name}', flush=True)

        new_content = (
            new_content[:match.start()]
            + img_ref
            + new_content[match.end():]
        )
        converted += 1
        time.sleep(CALL_PAUSE)

    if not dry_run and new_content != content:
        try:
            page.write_text(new_content, encoding='utf-8')
            print(f'    updated {page.relative_to(REPO)}', flush=True)
        except OSError as e:
            print(f'    ERROR — could not write {page.relative_to(REPO)}: {e}', flush=True)

    return found, converted


def main() -> None:
    ap = argparse.ArgumentParser(description='Convert ASCII diagram blocks to SVGs')
    ap.add_argument('--dry-run',  action='store_true', help='Preview only, no writes')
    ap.add_argument('--force',    action='store_true', help='Overwrite existing SVGs')
    ap.add_argument('--limit',    type=int, default=0, help='Stop after ~N diagrams (page-granular; may overshoot)')
    ap.add_argument('--section',  default='',          help='Filter to pages whose path contains this string')
    args = ap.parse_args()

    pages = sorted(DOCS.rglob('*.md'))
    if args.section:
        pages = [p for p in pages if args.section in str(p)]

    total_found = total_converted = 0
    limit_hit   = False

    for page in pages:
        if limit_hit:
            break

        try:
            content = page.read_text(encoding='utf-8')
        except OSError as e:
            print(f'\nWARN — skipping unreadable file {page.relative_to(REPO)}: {e}', flush=True)
            continue
        if '```text' not in content:
            continue

        if not any(is_diagram(m.group(1)) for m in BLOCK_RE.finditer(content)):
            continue

        print(f'\n{page.relative_to(REPO)}', flush=True)

        found, converted = process_page(page, content, args.dry_run, args.force)
        total_found     += found
        total_converted += converted

        if args.limit and total_converted >= args.limit:
            print(f'\n-- limit of {args.limit} diagrams reached --', flush=True)
            limit_hit = True

    print(f'\n{"=" * 60}')
    print(f'Diagrams found:     {total_found}')
    print(f'Diagrams converted: {total_converted}')
    if args.dry_run:
        print('(dry-run — no files written)')
    print(f'{"=" * 60}')


if __name__ == '__main__':
    main()
