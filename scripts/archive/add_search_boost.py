#!/usr/bin/env python3
"""Add search.boost: 2 to front matter of top KB pages."""

import re
from pathlib import Path

DOCS = Path("docs")

# Top pages most likely to be the target of user searches
TOP_PAGES = [
    # VMware core troubleshooting
    "virtualization/vmware/vcenter/troubleshooting/common-issues/index.md",
    "virtualization/vmware/esxi/troubleshooting/common-issues/index.md",
    "virtualization/vmware/vsan/troubleshooting/common-issues/index.md",
    "virtualization/vmware/nsx/troubleshooting/common-issues/index.md",
    # Health check runbook
    "virtualization/vmware/operations/morning-health-check/index.md",
    # VMware deploy guides
    "virtualization/vmware/vcenter/deploy/index.md",
    "virtualization/vmware/esxi/deploy/index.md",
    "virtualization/vmware/vsan/deploy/index.md",
    "virtualization/vmware/nsx/deploy/index.md",
    # VMware operations
    "virtualization/vmware/vcenter/operations/index.md",
    "virtualization/vmware/vsan/operations/index.md",
    # Section landing pages
    "virtualization/vmware/index.md",
    "storage/dell/powermax/index.md",
    "storage/netapp/ontap/index.md",
    "backup/veeam/index.md",
    # Key troubleshooting pages across products
    "storage/dell/powermax/troubleshooting/common-issues/index.md",
    "storage/netapp/ontap/troubleshooting/common-issues/index.md",
    "backup/veeam/troubleshooting/common-issues/index.md",
    "compute/linux/troubleshooting/common-issues/index.md",
    "compute/windows-server/active-directory/troubleshooting/common-issues/index.md",
]

FRONT_MATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)


def add_boost(rel: str) -> bool:
    path = DOCS / rel
    if not path.exists():
        print(f"  SKIP (not found): {rel}")
        return False
    content = path.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(content)
    if not m:
        print(f"  SKIP (no front matter): {rel}")
        return False
    fm = m.group(1)
    if "search:" in fm:
        print(f"  SKIP (already has search:): {rel}")
        return False
    new_fm = fm + "\nsearch:\n  boost: 2"
    new_content = f"---\n{new_fm}\n---\n" + content[m.end():]
    path.write_text(new_content, encoding="utf-8")
    print(f"  OK: {rel}")
    return True


def main():
    updated = 0
    for rel in TOP_PAGES:
        if add_boost(rel):
            updated += 1
    print(f"\n{updated}/{len(TOP_PAGES)} pages boosted.")


if __name__ == "__main__":
    main()
