from pathlib import Path
import re
import sys

docs = Path("docs")
errors = []


def strip_fences(text):
    """Return text with code-fence content blanked (preserves line count)."""
    out = []
    in_fence = False
    fence_char = None
    for line in text.splitlines(keepends=True):
        s = line.strip()
        if not in_fence:
            if s.startswith("```") or s.startswith("~~~"):
                in_fence = True
                fence_char = s[:3]
                out.append("\n")
            else:
                out.append(line)
        else:
            if s == fence_char:
                in_fence = False
            out.append("\n")
    return "".join(out)


def links_from(text):
    links = re.findall(r'href="([^"]+)"', text)
    links += re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    return sorted(set(links))


def resolve_link(md_path, link):
    """Return the resolved Path for a relative or absolute link, or None."""
    base = link.split("#", 1)[0]
    if not base:
        return None

    if base.startswith("/"):
        # Absolute — resolve relative to docs root
        rel = base.lstrip("/").rstrip("/")
        for candidate in [
            docs / rel,
            docs / (rel + ".md"),
            docs / rel / "index.md",
        ]:
            if candidate.exists():
                return candidate
        return docs / rel  # return non-existent path so caller flags it

    if base.endswith("/"):
        slug = base.rstrip("/")
        # MkDocs accepts both slug/index.md and slug.md
        as_dir = (md_path.parent / slug / "index.md").resolve()
        as_file = (md_path.parent / (slug + ".md")).resolve()
        return as_dir if as_dir.exists() else as_file
    if base.endswith(".md"):
        return (md_path.parent / base).resolve()
    # bare path — could be a directory (section) or file without extension
    candidate = (md_path.parent / base).resolve()
    if candidate.is_dir():
        return candidate / "index.md"
    return candidate


for md in docs.rglob("*.md"):
    if "assets" in md.parts:
        continue

    raw = md.read_text()

    if md.stat().st_size == 0:
        errors.append(f"EMPTY FILE: {md}")

    if 'href="#"' in raw:
        errors.append(f"PLACEHOLDER LINK: {md}")

    # Strip fences before link extraction so PowerShell [Type](expr) casts
    # and other code constructs are not mistaken for markdown links.
    text = strip_fences(raw)

    for link in links_from(text):
        if link.startswith(("http://", "https://", "mailto://", "mailto:", "#")):
            continue

        base = link.split("#", 1)[0]
        if not base:
            continue

        # Raw .html links in markdown source are unusual — flag them
        if base.endswith(".html") and not base.startswith("/"):
            errors.append(f"RAW HTML LINK: {md} -> {link}")

        target = resolve_link(md, link)
        if target is not None and not target.exists():
            errors.append(f"MISSING LINK: {md} -> {link}")


if errors:
    for e in errors:
        print(e)
    sys.exit(1)

print("OK: site checks passed")
