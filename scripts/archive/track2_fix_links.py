#!/usr/bin/env python3
"""
Track 2 link rewriter.

After all git mv operations complete, run this script to rewrite internal
relative links that point to moved/dissolved sections.

The script:
  1. Resolves each relative link to an absolute docs-root path
  2. Applies the Track 2 path mapping table
  3. Recalculates the correct new relative path from the file's new location
  4. Rewrites the link in-place

Run with --dry-run first to preview all changes.
"""
import re, sys
from pathlib import Path, PurePosixPath

REPO   = Path(__file__).parent.parent
DOCS   = REPO / "docs"
DRY    = "--dry-run" in sys.argv

# ── Path mapping table ────────────────────────────────────────────────────────
# Key   = old docs-root-relative path prefix (no leading slash, no trailing slash)
# Value = new docs-root-relative path prefix
#
# Order matters: more-specific prefixes must come before less-specific ones.

MOVES = [
    # disaster-recovery products → backup/
    ("disaster-recovery/veeam",                 "backup/veeam"),
    ("disaster-recovery/commvault",             "backup/commvault"),
    ("disaster-recovery/netbackup",             "backup/netbackup"),
    ("disaster-recovery/rasr",                  "backup/dell-cyber-recovery"),
    # disaster-recovery storage products → storage/
    ("disaster-recovery/recoverpoint",          "storage/dell/recoverpoint"),
    ("disaster-recovery/srdf-a",                "storage/dell/srdf-a"),
    ("disaster-recovery/srdf-s",                "storage/dell/srdf-s"),
    ("disaster-recovery/superna-eyeglass",      "storage/netapp/superna-eyeglass"),
    # monitoring products → platforms
    ("monitoring/aria-operations",              "virtualization/vmware/aria-operations"),
    ("monitoring/cloudiq",                      "storage/dell/cloudiq"),
    ("monitoring/nexus-dashboard",              "san/cisco/nexus-dashboard"),
    ("monitoring/pure1",                        "storage/pure/pure1"),
    ("monitoring/insightiq",                    "storage/netapp/insightiq"),
    ("monitoring/dell-aiops",                   "storage/dell/dell-aiops"),
    # monitoring cross-cutting → monitoring/ (stays, just renaming clarity)
    # (no path change needed — pages stay under monitoring/)
    # architecture pages → platform sections
    ("architecture/disaster-recovery-design",   "disaster-recovery/disaster-recovery-design"),
    ("architecture/high-availability",          "virtualization/high-availability"),
    ("architecture/network-design",             "networking/network-design"),
    ("architecture/storage-design",             "storage/storage-design"),
    # integration pages → protocols / security / compute / networking
    ("integration/api-connectivity",            "protocols/api-connectivity"),
    ("integration/certificate-trust",           "security/certificate-trust"),
    ("integration/directory-integration",       "compute/linux/directory-integration"),
    ("integration/email-relay",                 "protocols/email-relay"),
    ("integration/external-connectivity",       "networking/external-connectivity"),
    ("integration/service-integrations",        "protocols/service-integrations"),
    ("integration/time-synchronization",        "protocols/ntp"),
    # security
    ("security/active-directory",               "compute/windows-server/active-directory"),
    # data-protection
    ("data-protection/data-classification",     "security/data-classification"),
    ("data-protection/data-encryption",         "security/data-encryption"),
    ("data-protection/key-management",          "security/key-management"),
    ("data-protection/data-governance",         "security/data-governance"),
    ("data-protection/data-retention-policy",   "security/data-retention-policy"),
    ("data-protection/backup-validation",       "backup/backup-validation"),
    ("data-protection/recovery-testing",        "backup/recovery-testing"),
    # runbooks
    ("runbooks/vm-snapshot",                    "virtualization/vmware/operations/runbooks/vm-snapshot"),
    ("runbooks/server-reboot",                  "compute/linux/operations/runbooks/server-reboot"),
    ("runbooks/disk-space-cleanup",             "compute/linux/operations/runbooks/disk-space-cleanup"),
    ("runbooks/service-restart",                "compute/linux/operations/runbooks/service-restart"),
    ("runbooks/storage-volume-expansion",       "storage/operations/runbooks/storage-volume-expansion"),
    ("runbooks/account-unlock",                 "security/operations/runbooks/account-unlock"),
    ("runbooks/certificate-renewal",            "security/operations/runbooks/certificate-renewal"),
    # troubleshooting → platform sections
    ("troubleshooting/vm-performance",          "virtualization/troubleshooting/vm-performance"),
    ("troubleshooting/storage-latency",         "storage/troubleshooting/storage-latency"),
    ("troubleshooting/high-cpu",                "compute/troubleshooting/high-cpu"),
    ("troubleshooting/network-connectivity",    "networking/troubleshooting/network-connectivity"),
    ("troubleshooting/dns-resolution",          "protocols/troubleshooting/dns-resolution"),
    ("troubleshooting/authentication-failures", "security/troubleshooting/authentication-failures"),
    ("troubleshooting/backup-failures",         "backup/troubleshooting/backup-failures"),
    ("troubleshooting/replication-failures",    "storage/troubleshooting/replication-failures"),
    # certifications (stay top-level, vcp-dcv merges into certifications/vmware)
    ("virtualization/reference/certification/vcp-dcv", "certifications/vmware/vcp-dcv"),
    # database → compute platforms
    ("database",                                "compute/databases"),
]


def resolve_link(source_file: Path, link: str) -> str | None:
    """Resolve a relative link from source_file to an absolute docs-root path."""
    if link.startswith(("http://", "https://", "mailto:", "#", "/")):
        return None  # external or absolute — skip
    try:
        src_dir   = source_file.parent
        abs_link  = (src_dir / link).resolve()
        # Make relative to docs root
        rel = abs_link.relative_to(DOCS.resolve())
        return str(PurePosixPath(rel))
    except (ValueError, OSError):
        return None


def apply_mapping(abs_path: str) -> str | None:
    """Return new abs_path if the old path matches any move, else None."""
    for old_prefix, new_prefix in MOVES:
        if abs_path == old_prefix or abs_path.startswith(old_prefix + "/"):
            return new_prefix + abs_path[len(old_prefix):]
    return None


def new_relative(source_file: Path, new_abs: str) -> str:
    """Calculate relative link from source_file's new location to new_abs."""
    src_dir  = source_file.parent.resolve()
    tgt_path = (DOCS / new_abs).resolve()
    try:
        rel = tgt_path.relative_to(src_dir)
        return str(PurePosixPath(rel))
    except ValueError:
        # Use ../ climbing
        parts_src = src_dir.parts
        parts_tgt = tgt_path.parts
        common = 0
        for a, b in zip(parts_src, parts_tgt):
            if a == b:
                common += 1
            else:
                break
        ups    = len(parts_src) - common
        downs  = parts_tgt[common:]
        return "/".join([".."] * ups + list(downs))


def rewrite_file(f: Path) -> int:
    content  = f.read_text(errors="replace")
    original = content
    count    = 0

    def replace_link(match):
        nonlocal count
        prefix, link, suffix = match.group(1), match.group(2), match.group(3)
        abs_old = resolve_link(f, link)
        if abs_old is None:
            return match.group(0)
        abs_new = apply_mapping(abs_old)
        if abs_new is None:
            return match.group(0)
        new_link = new_relative(f, abs_new)
        # Preserve trailing slash / fragment
        if link.endswith("/") and not new_link.endswith("/"):
            new_link += "/"
        count += 1
        return f"{prefix}{new_link}{suffix}"

    # Rewrite markdown links: [text](link)
    content = re.sub(
        r'(\[(?:[^\]]*)\]\()(\.\.?/[^)#\s]+)([^)]*\))',
        replace_link, content
    )
    # Rewrite href attributes: href="link"
    content = re.sub(
        r'(href=")(\.\.?/[^"#]+)(")',
        replace_link, content
    )

    if content != original:
        if not DRY:
            f.write_text(content)
        return count
    return 0


def main():
    files_changed = 0
    links_rewritten = 0

    for f in sorted(DOCS.rglob("*.md")):
        n = rewrite_file(f)
        if n:
            files_changed += 1
            links_rewritten += n
            print(f"  {'[DRY] ' if DRY else ''}Rewrote {n} link(s): {f.relative_to(DOCS)}")

    print(f"\n{'DRY RUN — ' if DRY else ''}Files changed: {files_changed}")
    print(f"{'DRY RUN — ' if DRY else ''}Links rewritten: {links_rewritten}")


if __name__ == "__main__":
    main()
