from pathlib import Path
import re
import sys

docs = Path("docs")
errors = []

def links_from(text):
    links = re.findall(r'href="([^"]+)"', text)
    links += re.findall(r'\[[^\]]+\]\(([^)]+)\)', text)
    return sorted(set(links))

for md in docs.rglob("*.md"):
    if "assets" in md.parts:
        continue

    text = md.read_text()

    if md.stat().st_size == 0:
        errors.append(f"EMPTY FILE: {md}")

    if 'href="#"' in text:
        errors.append(f"PLACEHOLDER LINK: {md}")

    for link in links_from(text):
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue

        base = link.split("#", 1)[0]
        if not base:
            continue

        if base.endswith(".md") or base.endswith(".html"):
            errors.append(f"RAW FILE LINK: {md} -> {link}")

        if base.endswith("/"):
            target = (md.parent / base / "index.md").resolve()
        elif base.endswith(".md"):
            target = (md.parent / base).resolve()
        else:
            target = (md.parent / base).resolve()

        if not target.exists():
            errors.append(f"MISSING LINK: {md} -> {link}")

if errors:
    for e in errors:
        print(e)
    sys.exit(1)

print("OK: site checks passed")
