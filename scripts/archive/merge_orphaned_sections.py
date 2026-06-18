#!/usr/bin/env python3
"""
Merge three orphaned virtualization/ sections into vmware/.

For each file:
- If no equivalent in target: move it
- If equivalent exists: keep the longer one
"""

import os, shutil
from pathlib import Path

DOCS = Path("docs")

def count_lines(p):
    try:
        return len(p.read_text(encoding="utf-8").splitlines())
    except Exception:
        return 0


def merge_dir(src: Path, dst: Path, label: str):
    """Recursively merge src into dst. Returns (moved, replaced, skipped)."""
    moved = replaced = skipped = 0
    dst.mkdir(parents=True, exist_ok=True)

    for item in sorted(src.rglob("*")):
        if not item.is_file():
            continue
        rel = item.relative_to(src)
        target = dst / rel

        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(item), str(target))
            print(f"  MOVE  {label}/{rel}")
            moved += 1
        else:
            src_lines = count_lines(item)
            dst_lines = count_lines(target)
            if src_lines > dst_lines:
                shutil.copy2(str(item), str(target))
                print(f"  REPLACE (src {src_lines}L > dst {dst_lines}L)  {label}/{rel}")
                replaced += 1
            else:
                print(f"  SKIP (dst {dst_lines}L >= src {src_lines}L)  {label}/{rel}")
                skipped += 1

    return moved, replaced, skipped


total_moved = total_replaced = total_skipped = 0

# ── 1. virtualization/operations/ → vmware/operations/ ───────────────────────
src = DOCS / "virtualization/operations"
dst = DOCS / "virtualization/vmware/operations"
print(f"\n=== Merging {src.relative_to(DOCS)} → {dst.relative_to(DOCS)} ===")
m, r, s = merge_dir(src, dst, "operations")
total_moved += m; total_replaced += r; total_skipped += s
shutil.rmtree(str(src))
print(f"  Deleted {src.relative_to(DOCS)}/")

# ── 2. virtualization/reference/ → vmware/reference/ ─────────────────────────
src = DOCS / "virtualization/reference"
dst = DOCS / "virtualization/vmware/reference"
print(f"\n=== Merging {src.relative_to(DOCS)} → {dst.relative_to(DOCS)} ===")
m, r, s = merge_dir(src, dst, "reference")
total_moved += m; total_replaced += r; total_skipped += s
shutil.rmtree(str(src))
print(f"  Deleted {src.relative_to(DOCS)}/")

# ── 3. virtualization/vxrail/ → vmware/vxrail/ ───────────────────────────────
src = DOCS / "virtualization/vxrail"
dst = DOCS / "virtualization/vmware/vxrail"
print(f"\n=== Merging {src.relative_to(DOCS)} → {dst.relative_to(DOCS)} ===")
m, r, s = merge_dir(src, dst, "vxrail")
total_moved += m; total_replaced += r; total_skipped += s
shutil.rmtree(str(src))
print(f"  Deleted {src.relative_to(DOCS)}/")

print(f"\nTotal: moved={total_moved}  replaced={total_replaced}  skipped={total_skipped}")
