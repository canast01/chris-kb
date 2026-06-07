#!/usr/bin/env python3
"""
Track 2 restructuring pre-flight checks.
Verifies every planned operation before execution:
  - Source paths exist
  - Destination conflicts
  - Content that would be lost (unique H2s in source not in destination)
  - Git working tree is clean
  - No broken fences in files being touched
  - Duplicate detection for merge targets
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
DOCS = REPO / "docs"
ERRORS = []
WARNINGS = []
INFO = []

def err(msg): ERRORS.append(f"  ERROR: {msg}"); print(f"  ERROR: {msg}")
def warn(msg): WARNINGS.append(f"  WARN:  {msg}"); print(f"  WARN:  {msg}")
def ok(msg): INFO.append(f"  OK:    {msg}"); print(f"  OK:    {msg}")

# ── helpers ──────────────────────────────────────────────────────────────────

def exists(rel): return (DOCS / rel).exists()

def page_count(rel):
    p = DOCS / rel
    return len(list(p.rglob("*.md"))) if p.exists() else 0

def h2_sections(rel):
    p = DOCS / rel
    if not p.exists(): return set()
    content = p.read_text(errors="replace")
    in_fence = False
    sections = set()
    for line in content.splitlines():
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            if not in_fence: in_fence = True
            elif not m.group(2).strip(): in_fence = False
        elif not in_fence and re.match(r'^## ', line):
            sections.add(line.strip())
    return sections

def unique_h2s(src_rel, dst_rel):
    """H2 sections in src that don't exist in dst."""
    return h2_sections(src_rel) - h2_sections(dst_rel)

def fence_ok(rel):
    """Returns True if file has no broken fences."""
    p = DOCS / rel
    if not p.exists(): return True
    content = p.read_text(errors="replace")
    in_fence = False
    for line in content.splitlines():
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            lang = m.group(2).strip()
            if not in_fence: in_fence = True
            elif not lang: in_fence = False
    return not in_fence

def subdir_count(rel):
    p = DOCS / rel
    if not p.exists(): return 0
    return len([d for d in p.iterdir() if d.is_dir()])

# ── CHECK 1: Git state ────────────────────────────────────────────────────────
print("\n── Git State ──")
result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=REPO)
if result.stdout.strip():
    warn(f"Working tree has uncommitted changes ({len(result.stdout.strip().splitlines())} files) — commit before executing Track 2")
else:
    ok("Working tree clean")

# ── CHECK 2: Sources exist ────────────────────────────────────────────────────
print("\n── Source Existence ──")
moves = [
    # disaster-recovery splits
    ("disaster-recovery/veeam",                "backup/veeam"),
    ("disaster-recovery/commvault",            "backup/commvault"),
    ("disaster-recovery/netbackup",            "backup/netbackup"),
    ("disaster-recovery/recoverpoint",         "storage/dell/recoverpoint"),
    ("disaster-recovery/srdf-a",               "storage/dell/srdf-a"),
    ("disaster-recovery/srdf-s",               "storage/dell/srdf-s"),
    ("disaster-recovery/superna-eyeglass",     "storage/netapp/superna-eyeglass"),
    ("disaster-recovery/rasr",                 "backup/dell-cyber-recovery"),
    # monitoring moves (simple — destination doesn't exist)
    ("monitoring/pure1",                       "storage/pure/pure1"),
    ("monitoring/insightiq",                   "storage/netapp/insightiq"),
    ("monitoring/dell-aiops",                  "storage/dell/dell-aiops"),
    # monitoring cross-cutting
    ("monitoring/alert-management",            "monitoring-standards/alert-management"),
    ("monitoring/dashboard-standards",         "monitoring-standards/dashboard-standards"),
    ("monitoring/event-correlation",           "monitoring-standards/event-correlation"),
    ("monitoring/health-monitoring",           "monitoring-standards/health-monitoring"),
    ("monitoring/log-retention",               "monitoring-standards/log-retention"),
    ("monitoring/metrics-baseline",            "monitoring-standards/metrics-baseline"),
    ("monitoring/syslog",                      "monitoring-standards/syslog"),
    # security
    ("security/active-directory",              "compute/windows-server/active-directory"),
    # architecture dissolve
    ("architecture/disaster-recovery-design",  "disaster-recovery"),
    ("architecture/high-availability",         "virtualization"),
    ("architecture/network-design",            "networking"),
    ("architecture/storage-design",            "storage"),
    # integration dissolve
    ("integration/api-connectivity",           "protocols"),
    ("integration/certificate-trust",          "security"),
    ("integration/directory-integration",      "compute/linux"),
    ("integration/email-relay",                "protocols"),
    ("integration/external-connectivity",      "networking"),
    ("integration/service-integrations",       "protocols"),
    ("integration/time-synchronization",       "protocols/ntp"),   # merge, not new
    # certifications
    ("certifications/vmware",                  "virtualization/certifications"),
    ("certifications/aws",                     "cloud/aws/certifications"),
    ("certifications/azure",                   "cloud/azure/certifications"),
    ("certifications/san",                     "san/certifications"),
    ("certifications/storage",                 "storage/certifications"),
    ("certifications/ai",                      "ai/certifications"),
    # troubleshooting distribute
    ("troubleshooting/vm-performance",         "virtualization/troubleshooting/vm-performance"),
    ("troubleshooting/storage-latency",        "storage/troubleshooting/storage-latency"),
    ("troubleshooting/high-cpu",               "compute/troubleshooting/high-cpu"),
    ("troubleshooting/network-connectivity",   "networking/troubleshooting/network-connectivity"),
    ("troubleshooting/dns-resolution",         "protocols/troubleshooting/dns-resolution"),
    ("troubleshooting/authentication-failures","security/troubleshooting/authentication-failures"),
    ("troubleshooting/backup-failures",        "backup/troubleshooting/backup-failures"),
    ("troubleshooting/replication-failures",   "storage/troubleshooting/replication-failures"),
    # runbooks distribute
    ("runbooks/vm-snapshot",                   "virtualization/vmware/operations/runbooks/vm-snapshot"),
    ("runbooks/server-reboot",                 "compute/linux/operations/runbooks/server-reboot"),
    ("runbooks/disk-space-cleanup",            "compute/linux/operations/runbooks/disk-space-cleanup"),
    ("runbooks/service-restart",               "compute/linux/operations/runbooks/service-restart"),
    ("runbooks/storage-volume-expansion",      "storage/operations/runbooks/storage-volume-expansion"),
    ("runbooks/account-unlock",                "security/operations/runbooks/account-unlock"),
    ("runbooks/certificate-renewal",           "security/operations/runbooks/certificate-renewal"),
    # data-protection dissolve
    ("data-protection/data-classification",    "security"),
    ("data-protection/data-encryption",        "security"),
    ("data-protection/key-management",         "security"),
    ("data-protection/data-governance",        "security"),
    ("data-protection/data-retention-policy",  "security"),
    ("data-protection/backup-validation",      "backup"),
    ("data-protection/recovery-testing",       "backup"),   # has Commvault content
]

for src, dst in moves:
    if exists(src):
        ok(f"{src}")
    else:
        err(f"SOURCE MISSING: {src}")

# ── CHECK 3: Destination conflicts ───────────────────────────────────────────
print("\n── Destination Conflicts ──")
for src, dst in moves:
    src_name = Path(src).name
    dst_exact = Path(dst) / src_name if not dst.endswith(src_name) else Path(dst)
    # Real conflict = the exact destination sub-path already exists
    if exists(str(dst_exact)) and exists(src):
        src_pages = page_count(src)
        dst_pages = page_count(str(dst_exact))
        warn(f"MERGE NEEDED: {dst_exact} ({dst_pages}p) already exists — check content vs {src} ({src_pages}p)")
    elif exists(dst) and not exists(str(dst_exact)):
        ok(f"Parent exists, sub-path free: {dst}/{src_name}")
    elif not exists(dst):
        ok(f"Clean new destination: {dst}")

# ── CHECK 4: Unique content that would be lost ───────────────────────────────
print("\n── Content Loss Check (merge targets) ──")
merges = [
    ("monitoring/aria-operations/operations/index.md",      "virtualization/vmware/aria-operations/operations/index.md"),
    ("monitoring/aria-operations/architecture/index.md",    "virtualization/vmware/aria-operations/architecture/index.md"),
    ("monitoring/cloudiq/operations/index.md",              "storage/dell/cloudiq/operations/index.md"),
    ("monitoring/nexus-dashboard/operations/index.md",      "san/cisco/nexus-dashboard/operations/index.md"),
    ("integration/time-synchronization/index.md",           "protocols/ntp/index.md"),
]
for src, dst in merges:
    unique = unique_h2s(src, dst)
    if unique:
        warn(f"{len(unique)} unique H2s in {src} not in {dst}:")
        for h in sorted(unique):
            print(f"         {h}")
    else:
        ok(f"No unique H2s lost: {src}")

# ── CHECK 5: Fence integrity on key files ────────────────────────────────────
print("\n── Fence Integrity (sample of files being touched) ──")
sample = [
    "disaster-recovery/veeam/operations/procedures/index.md",
    "disaster-recovery/commvault/operations/procedures/index.md",
    "monitoring/aria-operations/operations/index.md",
    "monitoring/cloudiq/operations/index.md",
    "security/active-directory/operations/procedures/index.md",
]
for f in sample:
    if exists(f):
        if fence_ok(f):
            ok(f"Clean fences: {f}")
        else:
            err(f"BROKEN FENCE: {f}")

# ── CHECK 6: Deletes — verify already merged ─────────────────────────────────
print("\n── Delete Safety (verify merged before delete) ──")
deletes = [
    ("disaster-recovery/srm", "virtualization/vmware/srm"),
]
for src, merged_into in deletes:
    if not exists(src):
        ok(f"Already gone: {src}")
        continue
    # Spot-check: do key files exist in merged_into?
    src_pages = list((DOCS / src).rglob("*.md"))
    dst_pages = set(str(p.relative_to(DOCS / src)) for p in src_pages)
    missing = [p for p in dst_pages if not exists(f"{merged_into}/{p}")]
    if missing:
        warn(f"{src} has {len(missing)} files not found in {merged_into} — verify merge before delete")
    else:
        ok(f"All files accounted for in {merged_into}: safe to delete {src}")

# ── CHECK 7: NTP collision ────────────────────────────────────────────────────
print("\n── Protocol Collision Check ──")
if exists("protocols/ntp") and exists("integration/time-synchronization"):
    ntp_lines = len((DOCS / "protocols/ntp/index.md").read_text().splitlines()) if exists("protocols/ntp/index.md") else 0
    ts_lines  = len((DOCS / "integration/time-synchronization/index.md").read_text().splitlines()) if exists("integration/time-synchronization/index.md") else 0
    warn(f"NTP collision: protocols/ntp ({ntp_lines}L) + integration/time-synchronization ({ts_lines}L) — merge before moving")
else:
    ok("No NTP collision")

# ── SUMMARY ──────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print(f"ERRORS:   {len(ERRORS)}")
print(f"WARNINGS: {len(WARNINGS)}")
print(f"OK:       {len(INFO)}")

if ERRORS:
    print("\nERRORS (must fix before executing):")
    for e in ERRORS: print(e)

if WARNINGS:
    print("\nWARNINGS (review before executing):")
    for w in WARNINGS: print(w)

sys.exit(1 if ERRORS else 0)
