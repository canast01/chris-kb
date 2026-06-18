#!/usr/bin/env python3
"""
Track 2 restructuring — execution orchestrator.

Phases:
  1  Pre-flight check (aborts on any error)
  2  Merge monitoring unique sub-sections into platform sections
  3  git mv — move product sections to their new homes
  4  Merge overlapping sections (architecture, deploy, operations, security, troubleshooting)
  5  Rewrite internal links
  6  Rewrite section index pages (backup/, monitoring/, disaster-recovery/)
  7  Delete already-merged duplicates (disaster-recovery/srm/)
  8  Post-check

Run with --dry-run to simulate without writing anything.
Run with --phase=N to execute only a specific phase (for recovery).
"""
import re, shutil, subprocess, sys
from pathlib import Path

REPO   = Path(__file__).parent.parent
DOCS   = REPO / "docs"
DRY    = "--dry-run" in sys.argv
ONLY   = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--phase=")), None)

ERRORS = []
DONE   = []


def log(msg):   print(f"  {msg}")
def ok(msg):    DONE.append(msg); print(f"  ✓  {msg}")
def err(msg):   ERRORS.append(msg); print(f"  ✗  {msg}")
def skip(msg):  print(f"  –  {msg} (already done)")
def phase(n, title):
    if ONLY and ONLY != n:
        return False
    print(f"\n{'='*60}\nPhase {n}: {title}\n{'='*60}")
    return True


# ── helpers ──────────────────────────────────────────────────────────────────

def run(cmd, **kw):
    if DRY:
        print(f"  [DRY] {' '.join(str(c) for c in cmd)}")
        return True
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO, **kw)
    if result.returncode != 0:
        err(f"Command failed: {' '.join(str(c) for c in cmd)}\n{result.stderr.strip()}")
        return False
    return True


def git_mv(src_rel, dst_rel):
    src = DOCS / src_rel
    dst = DOCS / dst_rel
    if not src.exists():
        skip(f"git mv {src_rel} (source gone)")
        return True
    if dst.exists():
        err(f"git mv {src_rel} → {dst_rel}: destination already exists — merge manually first")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if run(["git", "mv", str(src), str(dst)]):
        ok(f"git mv {src_rel} → {dst_rel}")
        return True
    return False


def h2_sections(path):
    if not path.exists(): return {}
    content = path.read_text(errors="replace")
    in_fence = False; sections = {}; current = None; buf = []
    for line in content.splitlines(keepends=True):
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            if not in_fence: in_fence = True
            elif not m.group(2).strip(): in_fence = False
        elif not in_fence and re.match(r'^## ', line):
            if current: sections[current] = ''.join(buf)
            current = line.rstrip('\n'); buf = [line]
        else:
            if current: buf.append(line)
    if current: sections[current] = ''.join(buf)
    return sections


def merge_file(src_rel, dst_rel):
    src = DOCS / src_rel
    dst = DOCS / dst_rel
    if not src.exists():
        skip(f"merge {src_rel} (source gone)")
        return True
    if not dst.exists():
        # Just copy
        if not DRY:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        ok(f"Copied (new): {src_rel} → {dst_rel}")
        return True
    src_secs = h2_sections(src)
    dst_secs = h2_sections(dst)
    unique = [h for h in src_secs if h not in dst_secs]
    if not unique:
        skip(f"merge {src_rel} (no unique content)")
        return True
    additions = '\n'.join(src_secs[h].rstrip('\n') + '\n' for h in unique)
    if not DRY:
        existing = dst.read_text(errors="replace")
        dst.write_text(existing.rstrip('\n') + '\n\n' + additions)
    ok(f"Merged +{len(unique)} H2s: {src_rel} → {dst_rel}")
    return True


# ── Phase 1: Pre-flight ───────────────────────────────────────────────────────

if phase(1, "Pre-flight check"):
    result = subprocess.run(["python3", "scripts/track2_precheck.py"],
                            capture_output=True, text=True, cwd=REPO)
    print(result.stdout)
    if result.returncode != 0:
        print("Pre-check FAILED — aborting. Fix errors and re-run.")
        sys.exit(1)
    ok("Pre-check passed")


# ── Phase 2: Monitoring absorption ───────────────────────────────────────────

if phase(2, "Monitoring product absorption into platform sections"):

    # Sub-section mapping: monitoring sub-dir → platform tile sub-dir
    # For each product: (monitoring_product, platform_dest, sub-section_map)
    ABSORPTIONS = [
        (
            "monitoring/aria-operations",
            "virtualization/vmware/aria-operations",
            {
                "alerts":         "operations/alerts",
                "capacity":       "operations/capacity",
                "cli-reference":  "operations/cli-reference",   # merge
                "dashboards":     "operations/dashboards",
                "design-standards":"architecture/design-standards", # merge
                "integration":    "architecture/integrations",   # merge
                "lifecycle":      "operations/install-upgrade",  # merge
                "reports":        "operations/reports",
                "scripts":        "operations/scripts",          # merge
                "vendor-support": "troubleshooting/escalation",  # merge
            }
        ),
        (
            "monitoring/cloudiq",
            "storage/dell/cloudiq",
            {
                "alerts":         "operations/alerts",
                "capacity":       "operations/capacity",
                "cli-reference":  "operations/cli-reference",   # merge
                "deploy":         "deploy",                      # merge
                "design-standards":"architecture/design-standards", # merge
                "health":         "operations/health-checks",   # merge
                "integration":    "architecture/integrations",   # merge
                "lifecycle":      "operations/install-upgrade",  # merge
                "recommendations":"operations/recommendations",
                "reporting":      "operations/reports",
                "scripts":        "operations/scripts",          # merge
                "vendor-support": "troubleshooting/escalation",  # merge
            }
        ),
        (
            "monitoring/nexus-dashboard",
            "san/cisco/nexus-dashboard",
            {
                "alerts":         "operations/alerts",
                "cli-reference":  "operations/cli-reference",   # merge
                "design-standards":"architecture/design-standards", # merge
                "fabric-health":  "operations/fabric-health",
                "integration":    "architecture/integrations",   # merge
                "integrations":   "architecture/integrations",   # merge (alias)
                "lifecycle":      "operations/install-upgrade",  # merge
                "scripts":        "operations/scripts",          # merge
                "vendor-support": "troubleshooting/escalation",  # merge
                "visibility":     "operations/visibility",
            }
        ),
    ]

    for mon_base, plat_base, mapping in ABSORPTIONS:
        mon_path = DOCS / mon_base
        if not mon_path.exists():
            skip(f"{mon_base} (already moved)")
            continue
        for sub, tile in mapping.items():
            src_idx = f"{mon_base}/{sub}/index.md"
            dst_idx = f"{plat_base}/{tile}/index.md"
            merge_file(src_idx, dst_idx)


# ── Phase 3: git mv — simple section moves ───────────────────────────────────

if phase(3, "git mv — move sections to new homes"):

    MOVES = [
        # disaster-recovery → backup/
        ("disaster-recovery/veeam",              "backup/veeam"),
        ("disaster-recovery/commvault",          "backup/commvault"),
        ("disaster-recovery/netbackup",          "backup/netbackup"),
        ("disaster-recovery/rasr",               "backup/dell-cyber-recovery"),
        # disaster-recovery → storage/
        ("disaster-recovery/recoverpoint",       "storage/dell/recoverpoint"),
        ("disaster-recovery/srdf-a",             "storage/dell/srdf-a"),
        ("disaster-recovery/srdf-s",             "storage/dell/srdf-s"),
        ("disaster-recovery/superna-eyeglass",   "storage/netapp/superna-eyeglass"),
        # monitoring products → platforms (cross-cutting stays)
        ("monitoring/pure1",                     "storage/pure/pure1"),
        ("monitoring/insightiq",                 "storage/netapp/insightiq"),
        ("monitoring/dell-aiops",                "storage/dell/dell-aiops"),
        # security
        ("security/active-directory",            "compute/windows-server/active-directory"),
        # architecture → platforms
        ("architecture/disaster-recovery-design","disaster-recovery/disaster-recovery-design"),
        ("architecture/high-availability",       "virtualization/high-availability"),
        ("architecture/network-design",          "networking/network-design"),
        ("architecture/storage-design",          "storage/storage-design"),
        # integration → protocols / security / compute / networking
        ("integration/api-connectivity",         "protocols/api-connectivity"),
        ("integration/certificate-trust",        "security/certificate-trust"),
        ("integration/directory-integration",    "compute/linux/directory-integration"),
        ("integration/email-relay",              "protocols/email-relay"),
        ("integration/external-connectivity",    "networking/external-connectivity"),
        ("integration/service-integrations",     "protocols/service-integrations"),
        # data-protection → security / backup
        ("data-protection/data-classification",  "security/data-classification"),
        ("data-protection/data-encryption",      "security/data-encryption"),
        ("data-protection/key-management",       "security/key-management"),
        ("data-protection/data-governance",      "security/data-governance"),
        ("data-protection/data-retention-policy","security/data-retention-policy"),
        ("data-protection/backup-validation",    "backup/backup-validation"),
        ("data-protection/recovery-testing",     "backup/recovery-testing"),
        # runbooks → platforms
        ("runbooks/vm-snapshot",                 "virtualization/vmware/operations/runbooks/vm-snapshot"),
        ("runbooks/server-reboot",               "compute/linux/operations/runbooks/server-reboot"),
        ("runbooks/disk-space-cleanup",          "compute/linux/operations/runbooks/disk-space-cleanup"),
        ("runbooks/service-restart",             "compute/linux/operations/runbooks/service-restart"),
        ("runbooks/storage-volume-expansion",    "storage/operations/runbooks/storage-volume-expansion"),
        ("runbooks/account-unlock",              "security/operations/runbooks/account-unlock"),
        ("runbooks/certificate-renewal",         "security/operations/runbooks/certificate-renewal"),
        # troubleshooting → platform sections
        ("troubleshooting/vm-performance",       "virtualization/troubleshooting/vm-performance"),
        ("troubleshooting/storage-latency",      "storage/troubleshooting/storage-latency"),
        ("troubleshooting/high-cpu",             "compute/troubleshooting/high-cpu"),
        ("troubleshooting/network-connectivity", "networking/troubleshooting/network-connectivity"),
        ("troubleshooting/dns-resolution",       "protocols/troubleshooting/dns-resolution"),
        ("troubleshooting/authentication-failures","security/troubleshooting/authentication-failures"),
        ("troubleshooting/backup-failures",      "backup/troubleshooting/backup-failures"),
        ("troubleshooting/replication-failures", "storage/troubleshooting/replication-failures"),
        # certifications — vcp-dcv merge
        ("virtualization/reference/certification/vcp-dcv", "certifications/vmware/vcp-dcv"),
        # monitoring products that were absorbed (now safe to move remaining shell)
        ("monitoring/aria-operations",           "virtualization/vmware/aria-operations-monitoring"),
        ("monitoring/cloudiq",                   "storage/dell/cloudiq-monitoring"),
        ("monitoring/nexus-dashboard",           "san/cisco/nexus-dashboard-monitoring"),
    ]

    for src, dst in MOVES:
        git_mv(src, dst)


# ── Phase 4: Merge NTP collision ─────────────────────────────────────────────

if phase(4, "Content merges"):
    merge_file("integration/time-synchronization/index.md", "protocols/ntp/index.md")
    merge_file("project-management/asset-inventory/audit/index.md",    "inventory/audit/index.md")
    merge_file("project-management/asset-inventory/cleanup/index.md",  "inventory/cleanup/index.md")
    merge_file("project-management/asset-inventory/cmdb/index.md",     "inventory/cmdb/index.md")
    merge_file("project-management/asset-inventory/lifecycle/index.md","inventory/asset-lifecycle/index.md")
    merge_file("project-management/asset-inventory/ownership/index.md","inventory/ownership/index.md")


# ── Phase 5: Rewrite internal links ──────────────────────────────────────────

if phase(5, "Rewrite internal links"):
    cmd = ["python3", "scripts/track2_fix_links.py"]
    if DRY: cmd.append("--dry-run")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    print(result.stdout)
    ok("Links rewritten")


# ── Phase 6: Delete already-merged duplicates ────────────────────────────────

if phase(6, "Delete already-merged duplicates"):
    deletes = [
        "disaster-recovery/srm",    # merged into virtualization/vmware/srm/
    ]
    for d in deletes:
        p = DOCS / d
        if not p.exists():
            skip(f"rm {d} (already gone)")
            continue
        if DRY:
            log(f"[DRY] Would remove: {d}")
        else:
            run(["git", "rm", "-r", str(p)])
            ok(f"Deleted: {d}")


# ── Phase 7: Stage and commit ─────────────────────────────────────────────────

if phase(7, "Stage and commit"):
    if not DRY:
        run(["git", "add", "-A"])
        run(["git", "commit", "-m",
             "Track 2: restructure KB — move products to platforms, dissolve thin sections\n\n"
             "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"])
        ok("Committed")
    else:
        log("[DRY] Would commit all staged changes")


# ── Phase 8: Post-check ───────────────────────────────────────────────────────

if phase(8, "Post-check"):
    result = subprocess.run(["python3", "scripts/track2_postcheck.py"],
                            capture_output=True, text=True, cwd=REPO)
    print(result.stdout)
    if result.returncode != 0:
        err("Post-check found issues — review before pushing")
    else:
        ok("Post-check passed")


# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print(f"Completed: {len(DONE)} operations")
if ERRORS:
    print(f"Errors:    {len(ERRORS)}")
    for e in ERRORS:
        print(f"  ✗  {e}")
    sys.exit(1)
