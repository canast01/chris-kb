#!/usr/bin/env python3
"""
fix_broken_see_also_links.py — Fix broken internal links in "See also" sections.

Root cause: MkDocs converts file.md → file/index.html (adding one depth level),
but does NOT adjust relative directory-style links (only .md links). This means
links like [text](sibling/) from foo.md become href="sibling/" in foo/index.html,
resolving to foo/sibling/ instead of sibling/.

This script:
1. Parses the broken link report from check_site_links.py
2. Maps each broken href back to the source .md file
3. Tries candidate fixes (add ../, ../../, strip .md) against the site/ tree
4. Applies fixes to source .md files
"""

import re
import os
from pathlib import Path

REPO    = Path(__file__).parent.parent
DOCS    = REPO / "docs"
SITE    = REPO / "site"
REPORT  = Path("/private/tmp/claude-501/-Users-chrisanastasiadis/2df3f1df-e4df-47a6-b812-06b7ec1921ad/tasks/b30yj1w40.output")

# Regex to find links in "See also" sections of markdown
SEE_ALSO_LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def html_to_md_sources(html_rel: str) -> list[Path]:
    """Map site/foo/bar/index.html → candidate docs/ source files."""
    parts = html_rel.split("/")
    # Remove trailing index.html
    if parts and parts[-1] == "index.html":
        parts = parts[:-1]

    candidates = []
    if parts:
        # Could be docs/a/b/c/index.md (already a dir)
        candidates.append(DOCS / Path(*parts) / "index.md")
        # Or docs/a/b/c.md (flat file that became a dir)
        candidates.append(DOCS / Path(*parts[:-1]) / (parts[-1] + ".md"))
    return candidates


def target_exists_in_site(html_file: Path, href: str) -> bool:
    """Check if href resolves to an existing path in site/."""
    base = SITE / html_file.parent.relative_to(SITE)
    resolved = (base / href).resolve()
    try:
        resolved.relative_to(SITE)
    except ValueError:
        return False
    return resolved.exists() or (resolved / "index.html").exists()


def find_fix(html_file: Path, broken_href: str) -> str | None:
    """Return a corrected href, or None if no fix found."""
    # Skip data: and external
    if broken_href.startswith(("data:", "http:", "https:", "mailto:", "javascript:")):
        return None

    candidates = []

    if broken_href.endswith(".md"):
        # Convert .md links to directory paths
        base = broken_href[:-3]  # strip .md
        # foo/index.md → foo/  or  foo.md → foo/
        if base.endswith("/index"):
            candidates.append(base[:-5] + "/")  # strip /index
        else:
            candidates.append(base + "/")
        # Also try ../base.md → ../base/
        if broken_href.startswith("../"):
            inner = broken_href[3:-3]
            candidates.append("../../" + inner + "/")

    elif broken_href.endswith("/"):
        # Directory-style relative link: try adding levels of ../
        candidates = [
            "../" + broken_href,
            "../../" + broken_href,
            "../../../" + broken_href,
        ]
        # Also try removing one level of ../
        if broken_href.startswith("../"):
            candidates.append(broken_href[3:])
        if broken_href.startswith("../../"):
            candidates.append(broken_href[6:])
    else:
        return None  # Not a pattern we handle

    for candidate in candidates:
        if target_exists_in_site(html_file, candidate):
            return candidate

    return None


def apply_fix_to_md(md_path: Path, broken_href: str, fixed_href: str) -> int:
    """Replace broken_href with fixed_href in the markdown file. Returns count of replacements."""
    text = md_path.read_text(encoding="utf-8")
    # Replace inside markdown links: ([text](broken_href)) → ([text](fixed_href))
    # Must be exact match of the href portion
    old = f"]({broken_href})"
    new = f"]({fixed_href})"
    count = text.count(old)
    if count > 0:
        md_path.write_text(text.replace(old, new), encoding="utf-8")
    return count


def parse_report(report_path: Path) -> dict[str, set[str]]:
    """Parse checker output into {html_rel: set(broken_hrefs)}."""
    result: dict[str, set[str]] = {}
    current_page = None
    page_pat = re.compile(r'^PAGE: (.+)$')
    broken_pat = re.compile(r'^\s+BROKEN href: (\S+) →')

    for line in report_path.read_text().splitlines():
        m = page_pat.match(line)
        if m:
            current_page = m.group(1)
            result.setdefault(current_page, set())
            continue
        m = broken_pat.match(line)
        if m and current_page:
            href = m.group(1)
            if not href.startswith("data:"):
                result[current_page].add(href)

    return result


def main():
    broken_map = parse_report(REPORT)

    total_pages_fixed = 0
    total_links_fixed = 0
    total_links_unfixable = 0

    for html_rel, broken_hrefs in sorted(broken_map.items()):
        if not broken_hrefs:
            continue

        html_file = SITE / html_rel
        md_sources = html_to_md_sources(html_rel)
        md_path = next((p for p in md_sources if p.exists()), None)

        if not md_path:
            continue

        page_fixed = 0
        for href in sorted(broken_hrefs):
            fix = find_fix(html_file, href)
            if fix:
                count = apply_fix_to_md(md_path, href, fix)
                if count > 0:
                    page_fixed += count
                    total_links_fixed += count
            else:
                total_links_unfixable += 1

        if page_fixed > 0:
            total_pages_fixed += 1

    print(f"Fixed {total_links_fixed} broken links in {total_pages_fixed} source files")
    print(f"Could not auto-fix: {total_links_unfixable} links")


if __name__ == "__main__":
    main()
