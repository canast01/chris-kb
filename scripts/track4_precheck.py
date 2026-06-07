#!/usr/bin/env python3
"""
Track 4 pre-flight checks.
Validates all planned moves before execution:
  - Git working tree is clean
  - All source paths exist
  - Destination conflicts and merge candidates
  - Content that would be lost (unique H2s in overlapping pages)
  - Fence integrity on source files
  - Diagram registration inventory (paths that need updating)
"""
import re, subprocess, sys
from pathlib import Path

REPO = Path(__file__).parent.parent
DOCS = REPO / "docs"
ERRORS = []
WARNINGS = []
INFO = []

def err(msg):  ERRORS.append(msg);   print(f"  ERROR: {msg}")
def warn(msg): WARNINGS.append(msg); print(f"  WARN:  {msg}")
def ok(msg):   INFO.append(msg);     print(f"  OK:    {msg}")

def exists(rel): return (DOCS / rel).exists()

def page_count(rel):
    p = DOCS / rel
    return len(list(p.rglob("*.md"))) if p.exists() else 0

def h2_sections(path):
    if not Path(path).exists(): return set()
    content = Path(path).read_text(errors="replace")
    in_fence = False; sections = set()
    for line in content.splitlines():
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            if not in_fence: in_fence = True
            elif not m.group(2).strip(): in_fence = False
        elif not in_fence and re.match(r'^## ', line):
            sections.add(line.strip())
    return sections

def unique_h2s(src_rel, dst_rel):
    src = DOCS / src_rel
    dst = DOCS / dst_rel
    src_secs = h2_sections(src) if src.is_file() else set()
    dst_secs = h2_sections(dst) if dst.is_file() else set()
    return src_secs - dst_secs

def fence_ok(p):
    if not p.exists(): return True
    content = p.read_text(errors="replace")
    in_fence = False
    for line in content.splitlines():
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            if not in_fence: in_fence = True
            elif not m.group(2).strip(): in_fence = False
    return not in_fence


# ── CHECK 1: Git state ────────────────────────────────────────────────────────
print("\n── Git State ──")
result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=REPO)
if result.stdout.strip():
    warn(f"Working tree has uncommitted changes ({len(result.stdout.strip().splitlines())} files) — commit before executing Track 4")
else:
    ok("Working tree clean")


# ── CHECK 2: Source paths exist ───────────────────────────────────────────────
print("\n── Source Existence ──")

MOVES = [
    # disaster-recovery residual → backup/
    ("disaster-recovery/isolated-recovery-environment-ire",   "backup/ire"),
    ("disaster-recovery/failover-procedure",                  "backup/runbooks/failover"),
    ("disaster-recovery/failback-procedure",                  "backup/runbooks/failback"),
    ("disaster-recovery/disaster-recovery-design",            "backup/dr-design"),
    ("disaster-recovery/runbook",                             "backup/runbooks/dr-runbook"),
    # performance → monitoring-standards
    ("performance/capacity-forecasting",      "monitoring-standards/capacity-forecasting"),
    ("performance/failure-testing",           "monitoring-standards/failure-testing"),
    ("performance/performance-baselining",    "monitoring-standards/performance-baselining"),
    ("performance/reliability-engineering",   "monitoring-standards/reliability-engineering"),
    ("performance/resource-optimization",     "monitoring-standards/resource-optimization"),
    ("performance/service-availability",      "monitoring-standards/service-availability"),
    ("performance/service-level-objectives",  "monitoring-standards/service-level-objectives"),
    # project-management/health-checks → monitoring-standards
    ("project-management/health-checks",      "monitoring-standards/health-checks"),
    # change-management → tools/servicenow
    ("change-management/change-approval",     "tools/servicenow/change-management/change-approval"),
    ("change-management/change-communication","tools/servicenow/change-management/change-communication"),
    ("change-management/change-request",      "tools/servicenow/change-management/change-request"),
    ("change-management/change-validation",   "tools/servicenow/change-management/change-validation"),
    ("change-management/deployment-procedure","tools/servicenow/change-management/deployment-procedure"),
    ("change-management/emergency-change",    "tools/servicenow/change-management/emergency-change"),
    ("change-management/release-management",  "tools/servicenow/change-management/release-management"),
    # project-management/change-management → merge into servicenow/change-management
    ("project-management/change-management/approval",   "tools/servicenow/change-management/approval"),
    ("project-management/change-management/backout-plan","tools/servicenow/change-management/backout-plan"),
    ("project-management/change-management/closeout",   "tools/servicenow/change-management/closeout"),
    ("project-management/change-management/risk",       "tools/servicenow/change-management/risk"),
    ("project-management/change-management/validation", "tools/servicenow/change-management/validation"),
    # inventory → servicenow/asset-inventory
    ("inventory/asset-lifecycle",       "tools/servicenow/asset-inventory/asset-lifecycle"),
    ("inventory/asset-tracking",        "tools/servicenow/asset-inventory/asset-tracking"),
    ("inventory/audit",                 "tools/servicenow/asset-inventory/audit"),
    ("inventory/cleanup",               "tools/servicenow/asset-inventory/cleanup"),
    ("inventory/cmdb",                  "tools/servicenow/asset-inventory/cmdb"),
    ("inventory/configuration-management","tools/servicenow/asset-inventory/configuration-management"),
    ("inventory/environment-mapping",   "tools/servicenow/asset-inventory/environment-mapping"),
    ("inventory/hardware-lifecycle",    "tools/servicenow/asset-inventory/hardware-lifecycle"),
    ("inventory/license-management",    "tools/servicenow/asset-inventory/license-management"),
    ("inventory/ownership",             "tools/servicenow/asset-inventory/ownership"),
    ("inventory/support-contracts",     "tools/servicenow/asset-inventory/support-contracts"),
    ("inventory/system-inventory",      "tools/servicenow/asset-inventory/system-inventory"),
    # project-management/asset-inventory → merge into servicenow/asset-inventory
    ("project-management/asset-inventory/audit",     "tools/servicenow/asset-inventory/audit"),
    ("project-management/asset-inventory/cleanup",   "tools/servicenow/asset-inventory/cleanup"),
    ("project-management/asset-inventory/cmdb",      "tools/servicenow/asset-inventory/cmdb"),
    ("project-management/asset-inventory/lifecycle", "tools/servicenow/asset-inventory/asset-lifecycle"),
    ("project-management/asset-inventory/ownership", "tools/servicenow/asset-inventory/ownership"),
    # lifecycle → servicenow
    ("lifecycle/environment-readiness",    "tools/servicenow/lifecycle/environment-readiness"),
    ("lifecycle/migration-procedure",      "tools/servicenow/lifecycle/migration-procedure"),
    ("lifecycle/post-upgrade-validation",  "tools/servicenow/lifecycle/post-upgrade-validation"),
    ("lifecycle/rollback-procedure",       "tools/servicenow/lifecycle/rollback-procedure"),
    ("lifecycle/system-decommission",      "tools/servicenow/lifecycle/system-decommission"),
    ("lifecycle/system-onboarding",        "tools/servicenow/lifecycle/system-onboarding"),
    ("lifecycle/upgrade-readiness",        "tools/servicenow/lifecycle/upgrade-readiness"),
    # project-management remaining → servicenow
    ("project-management/incident-management",  "tools/servicenow/incident-management"),
    ("project-management/maintenance-windows",  "tools/servicenow/maintenance-windows"),
    ("project-management/rca-template",         "tools/servicenow/templates/rca-template"),
    ("project-management/change-plan-template", "tools/servicenow/templates/change-plan-template"),
    # database → compute product sections (destination created by execute script)
    ("database/database-health-check",              "compute/linux/mysql"),
    ("database/database-maintenance",               "compute/linux/postgresql"),
    ("database/database-failover",                  "compute/windows-server/sql-server"),
    ("database/database-backup-validation",         "compute/linux/mysql"),
    ("database/database-capacity-monitoring",       "compute/linux/postgresql"),
    ("database/database-performance-troubleshooting","compute/windows-server/sql-server"),
    ("database/database-replication-check",         "compute/linux/mysql"),
]

for src, dst in MOVES:
    if exists(src):
        ok(f"EXISTS: {src}")
    else:
        err(f"SOURCE MISSING: {src}")


# ── CHECK 3: Destination conflicts ───────────────────────────────────────────
print("\n── Destination Conflicts ──")
MERGE_CANDIDATES = [
    # project-management/asset-inventory overlaps with inventory/
    ("project-management/asset-inventory/audit/index.md",     "inventory/audit/index.md"),
    ("project-management/asset-inventory/cleanup/index.md",   "inventory/cleanup/index.md"),
    ("project-management/asset-inventory/cmdb/index.md",      "inventory/cmdb/index.md"),
    ("project-management/asset-inventory/ownership/index.md", "inventory/ownership/index.md"),
    # project-management/change-management overlaps with change-management/
    ("project-management/change-management/approval/index.md","change-management/change-approval/index.md"),
    ("project-management/change-management/validation/index.md","change-management/change-validation/index.md"),
]
for src_rel, dst_rel in MERGE_CANDIDATES:
    if exists(src_rel) and exists(dst_rel):
        lost = unique_h2s(src_rel, dst_rel)
        if lost:
            warn(f"MERGE NEEDED — {len(lost)} unique H2 (src not in dst): {src_rel}")
            for h in sorted(lost):
                print(f"         {h}")
        else:
            ok(f"No unique content lost: {src_rel}")
    elif exists(src_rel):
        ok(f"Clean move (dst free): {src_rel}")


# ── CHECK 4: Destinations that will be created ───────────────────────────────
print("\n── New Destinations to Create ──")
NEW_DIRS = [
    "backup/runbooks",
    "backup/runbooks/failover",
    "backup/runbooks/failback",
    "backup/runbooks/dr-runbook",
    "backup/dr-design",
    "backup/ire",
    "tools/servicenow/change-management",
    "tools/servicenow/asset-inventory",
    "tools/servicenow/lifecycle",
    "tools/servicenow/incident-management",
    "tools/servicenow/maintenance-windows",
    "tools/servicenow/templates",
    "compute/linux/mysql",
    "compute/linux/postgresql",
    "compute/windows-server/sql-server",
]
for d in NEW_DIRS:
    if exists(d):
        warn(f"Already exists — check for conflicts: {d}")
    else:
        ok(f"Will be created: {d}")


# ── CHECK 5: Fence integrity ──────────────────────────────────────────────────
print("\n── Fence Integrity ──")
broken = 0
check_dirs = [
    "disaster-recovery", "performance", "change-management",
    "inventory", "lifecycle", "project-management", "database",
]
for d in check_dirs:
    p = DOCS / d
    if not p.exists(): continue
    for f in sorted(p.rglob("*.md")):
        if not fence_ok(f):
            err(f"BROKEN FENCE: {f.relative_to(DOCS)}")
            broken += 1
if broken == 0:
    ok("All fences clean in source sections")


# ── CHECK 6: Diagram registrations to update ─────────────────────────────────
print("\n── Diagram Registration Coverage ──")
diagram_dir = REPO / "scripts" / "diagrams"
path_prefixes_moving = [
    "docs/disaster-recovery/",
    "docs/performance/",
    "docs/change-management/",
    "docs/inventory/",
    "docs/lifecycle/",
    "docs/project-management/",
    "docs/database/",
    "docs/backup/dell-cyber-recovery/",
]
registrations_to_update = []
for py_file in sorted(diagram_dir.glob("*.py")):
    content = py_file.read_text(errors="replace")
    for prefix in path_prefixes_moving:
        matches = re.findall(rf'@kb_diagram\([^)]*?(?:{re.escape(prefix)}[^"\']*)[^)]*\)', content)
        for m in matches:
            path_match = re.search(r'"(docs/[^"]+)"', m)
            if path_match:
                registrations_to_update.append((py_file.name, path_match.group(1)))

if registrations_to_update:
    warn(f"{len(registrations_to_update)} diagram registrations need path updates after moves:")
    by_file = {}
    for fname, path in registrations_to_update:
        by_file.setdefault(fname, []).append(path)
    for fname, paths in sorted(by_file.items()):
        print(f"    {fname}: {len(paths)} entries")
else:
    ok("No diagram registrations in moving sections")


# ── CHECK 7: Sections to be dissolved exist ───────────────────────────────────
print("\n── Sections Being Dissolved ──")
dissolve_sections = [
    "disaster-recovery", "performance", "change-management",
    "inventory", "lifecycle", "project-management", "database",
    "backup/dell-cyber-recovery",
]
for s in dissolve_sections:
    if exists(s):
        p = page_count(s)
        ok(f"EXISTS ({p} pages): {s}")
    else:
        warn(f"Already gone: {s}")


# ── SUMMARY ───────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"ERRORS:   {len(ERRORS)}")
print(f"WARNINGS: {len(WARNINGS)}")
print(f"OK:       {len(INFO)}")

if ERRORS:
    print("\nERRORS (fix before executing):")
    for e in ERRORS: print(f"  ✗  {e}")

if WARNINGS:
    print("\nWARNINGS (review before executing):")
    for w in WARNINGS: print(f"  !  {w}")

sys.exit(1 if ERRORS else 0)
