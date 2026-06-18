from pathlib import Path
import re
import sys

docs = Path("docs")
missing = []

for md in docs.rglob("*.md"):
    if "assets" in md.parts:
        continue

    text = md.read_text()

    links = re.findall(r'href="([^"]+)"', text)
    links += re.findall(r'\[[^\]]+\]\(([^)]+)\)', text)

    for link in sorted(set(links)):
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue

        base = link.split("#", 1)[0]

        if not base:
            continue

        if base.endswith("/"):
            target = (md.parent / base / "index.md").resolve()
        elif base.endswith(".md"):
            target = (md.parent / base).resolve()
        else:
            target = (md.parent / base).resolve()

        if not target.exists():
            missing.append((str(md), link))

if missing:
    for src, link in missing:
        print(f"MISSING: {src} -> {link}")
    sys.exit(1)

print("OK: all internal links resolve")
