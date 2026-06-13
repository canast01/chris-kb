#!/usr/bin/env python3
"""
Add '## See also' to KB leaf pages using section-type rules.
Covers pages not handled by the specific add_see_also.py XREF_MAP.
"""
import os

DOCS = "docs"

COMPANIONS = {
    "deploy": [
        "architecture/how-it-works",
        "operations/health-checks",
        "troubleshooting/common-issues",
    ],
    "operations/health-checks": [
        "troubleshooting/common-issues",
        "operations/procedures",
        "operations/cli-reference",
    ],
    "operations/procedures": [
        "operations/health-checks",
        "troubleshooting/common-issues",
        "operations/cli-reference",
    ],
    "operations/cli-reference": [
        "operations/procedures",
        "operations/scripts",
        "operations/health-checks",
    ],
    "operations/scripts": [
        "operations/cli-reference",
        "operations/procedures",
    ],
    "operations/backup-restore": [
        "operations/procedures",
        "troubleshooting/common-issues",
        "operations/health-checks",
    ],
    "operations/install-upgrade": [
        "operations/health-checks",
        "troubleshooting/common-issues",
        "operations/procedures",
    ],
    "troubleshooting/common-issues": [
        "troubleshooting/diagnostics",
        "troubleshooting/escalation",
        "operations/health-checks",
    ],
    "troubleshooting/diagnostics": [
        "troubleshooting/common-issues",
        "troubleshooting/escalation",
    ],
    "troubleshooting/escalation": [
        "troubleshooting/diagnostics",
        "troubleshooting/common-issues",
    ],
    "security/hardening": [
        "security/access-control",
        "security/authentication",
        "operations/health-checks",
    ],
    "security/authentication": [
        "security/access-control",
        "security/hardening",
    ],
    "security/access-control": [
        "security/authentication",
        "security/hardening",
    ],
    "security/encryption": [
        "security/hardening",
        "operations/health-checks",
    ],
    "architecture/how-it-works": [
        "architecture/design-standards",
        "deploy",
        "architecture/integrations",
    ],
    "architecture/design-standards": [
        "architecture/how-it-works",
        "deploy",
    ],
    "architecture/integrations": [
        "architecture/how-it-works",
        "deploy",
    ],
}


def get_title(path):
    try:
        for line in open(path, encoding="utf-8"):
            if line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return None


def find_companion(product_root, companion_key):
    for p in (
        os.path.join(product_root, companion_key + ".md"),
        os.path.join(product_root, companion_key, "index.md"),
    ):
        if os.path.isfile(p):
            title = get_title(p)
            if title:
                return title
    return None


def make_link(source_path, product_root, companion_key, title):
    source_dir = os.path.dirname(source_path)
    target = os.path.join(product_root, companion_key)
    rel = os.path.relpath(target, source_dir).replace("\\", "/") + "/"
    return f"- [{title}]({rel})"


def get_product_roots():
    roots = []
    vmware = os.path.join(DOCS, "virtualization", "vmware")
    if os.path.isdir(vmware):
        for d in sorted(os.listdir(vmware)):
            p = os.path.join(vmware, d)
            if os.path.isdir(p):
                roots.append(p)
    for extra in ["cloud/aws/evs", "storage/ceph",
                  "virtualization/openshift", "virtualization/nutanix"]:
        p = os.path.join(DOCS, *extra.split("/"))
        if os.path.isdir(p):
            roots.append(p)
    return roots


def get_section_key(path, product_root):
    rel = os.path.relpath(path, product_root).replace("\\", "/")
    if rel.endswith("/index.md"):
        rel = rel[:-9]
    elif rel.endswith(".md"):
        rel = rel[:-3]
    return rel


added = skipped = 0

for product_root in get_product_roots():
    for root, dirs, files in os.walk(product_root):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            content = open(path, encoding="utf-8").read()

            if "## See also" in content:
                skipped += 1
                continue
            if '<div class="kb-grid' in content:
                skipped += 1
                continue

            key = get_section_key(path, product_root)
            if key not in COMPANIONS:
                continue

            links = []
            for ck in COMPANIONS[key]:
                title = find_companion(product_root, ck)
                if title:
                    links.append(make_link(path, product_root, ck, title))

            if len(links) < 2:
                continue

            see_also = "\n## See also\n\n" + "\n".join(links) + "\n"

            if "\n## Verify" in content:
                new_content = content.replace("\n## Verify", see_also + "\n## Verify", 1)
            else:
                new_content = content.rstrip() + "\n" + see_also

            open(path, "w", encoding="utf-8").write(new_content)
            print(f"  ADDED  {os.path.relpath(path, DOCS)}")
            added += 1

print(f"\nAdded: {added}   Skipped: {skipped}")
