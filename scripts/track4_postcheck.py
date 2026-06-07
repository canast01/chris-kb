#!/usr/bin/env python3
"""
Track 4 post-execution validation.
Run after track4_execute.py completes.
Checks:
  - Old sections gone (dissolved)
  - New destinations exist with content
  - No broken fences introduced
  - ascii_diagram_gen --check passes
  - No orphaned section index.md shells
  - backup/dell-cyber-recovery still present (was NOT deleted — confirm manually)
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

def exists(rel):     return (DOCS / rel).exists()
def page_count(rel):
    p = DOCS / rel
    return len(list(p.rglob("*.md"))) if p.exists() else 0


# ── CHECK 1: Old section sources are gone ─────────────────────────────────────
print("\n── Old Sections Dissolved ──")
# Only top-level sub-pages should be gone; index.md shells may still exist
SHOULD_BE_GONE = [
    # disaster-recovery sub-pages (moved to backup/)
    "disaster-recovery/isolated-recovery-environment-ire",
    "disaster-recovery/failover-procedure",
    "disaster-recovery/failback-procedure",
    "disaster-recovery/disaster-recovery-design",
    "disaster-recovery/runbook",
    # performance sub-pages (moved to monitoring-standards/)
    "performance/capacity-forecasting",
    "performance/failure-testing",
    "performance/performance-baselining",
    "performance/reliability-engineering",
    "performance/resource-optimization",
    "performance/service-availability",
    "performance/service-level-objectives",
    # change-management (moved to servicenow)
    "change-management/change-approval",
    "change-management/change-communication",
    "change-management/change-request",
    "change-management/change-validation",
    "change-management/deployment-procedure",
    "change-management/emergency-change",
    "change-management/release-management",
    # inventory (moved to servicenow)
    "inventory/asset-lifecycle",
    "inventory/asset-tracking",
    "inventory/audit",
    "inventory/cleanup",
    "inventory/cmdb",
    "inventory/configuration-management",
    "inventory/environment-mapping",
    "inventory/hardware-lifecycle",
    "inventory/license-management",
    "inventory/ownership",
    "inventory/support-contracts",
    "inventory/system-inventory",
    # lifecycle (moved to servicenow)
    "lifecycle/environment-readiness",
    "lifecycle/migration-procedure",
    "lifecycle/post-upgrade-validation",
    "lifecycle/rollback-procedure",
    "lifecycle/system-decommission",
    "lifecycle/system-onboarding",
    "lifecycle/upgrade-readiness",
    # project-management sub-sections (distributed)
    "project-management/health-checks",
    "project-management/incident-management",
    "project-management/maintenance-windows",
    "project-management/rca-template",
    "project-management/change-plan-template",
    "project-management/asset-inventory",
    "project-management/change-management",
]
for path in SHOULD_BE_GONE:
    if exists(path):
        err(f"STILL EXISTS (should have moved): {path}")
    else:
        ok(f"Gone: {path}")


# ── CHECK 2: New destinations exist ───────────────────────────────────────────
print("\n── New Destinations Exist ──")
SHOULD_EXIST = [
    # backup/ gains
    ("backup/ire",                  5),
    ("backup/runbooks/failover",    1),
    ("backup/runbooks/failback",    1),
    ("backup/runbooks/dr-runbook",  1),
    ("backup/dr-design",            1),
    # monitoring-standards/ gains
    ("monitoring-standards/capacity-forecasting",   1),
    ("monitoring-standards/failure-testing",        1),
    ("monitoring-standards/performance-baselining", 1),
    ("monitoring-standards/reliability-engineering",1),
    ("monitoring-standards/resource-optimization",  1),
    ("monitoring-standards/service-availability",   1),
    ("monitoring-standards/service-level-objectives",1),
    ("monitoring-standards/health-checks",          5),
    # tools/servicenow/ gains
    ("tools/servicenow/change-management",          7),
    ("tools/servicenow/asset-inventory",            10),
    ("tools/servicenow/lifecycle",                  7),
    ("tools/servicenow/incident-management",        5),
    ("tools/servicenow/maintenance-windows",        5),
    ("tools/servicenow/templates",                  2),
    # new DB product sections
    ("compute/linux/mysql",             15),
    ("compute/linux/postgresql",        15),
    ("compute/windows-server/sql-server",15),
]
for path, min_pages in SHOULD_EXIST:
    if not exists(path):
        err(f"MISSING destination: {path}")
    else:
        actual = page_count(path)
        if actual < min_pages:
            warn(f"Low page count ({actual} < {min_pages} expected): {path}")
        else:
            ok(f"EXISTS ({actual} pages): {path}")


# ── CHECK 3: Section shells — warn if top-level dirs still have content ───────
print("\n── Empty Section Shells (pending manual cleanup) ──")
SHELL_DIRS = [
    "disaster-recovery", "performance", "change-management",
    "inventory", "lifecycle", "project-management", "database",
]
for d in SHELL_DIRS:
    p = DOCS / d
    if not p.exists():
        ok(f"Fully gone: {d}")
        continue
    pages = list(p.rglob("*.md"))
    if len(pages) == 1 and pages[0].name == "index.md":
        warn(f"Shell remains (index.md only — safe to delete): {d}/")
    elif len(pages) == 0:
        warn(f"Empty dir remains — safe to delete: {d}/")
    else:
        err(f"CONTENT REMAINS in {d}/ ({len(pages)} pages) — moves incomplete")


# ── CHECK 4: Broken fences in moved content ────────────────────────────────────
print("\n── Fence Integrity (new destinations) ──")
check_dirs = [
    "backup/ire", "backup/runbooks", "backup/dr-design",
    "monitoring-standards",
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
broken = 0
for d in check_dirs:
    p = DOCS / d
    if not p.exists(): continue
    for f in sorted(p.rglob("*.md")):
        content = f.read_text(errors="replace")
        in_fence = False
        for line in content.splitlines():
            m = re.match(r'^(`{3,})(.*)', line.strip())
            if m:
                if not in_fence: in_fence = True
                elif not m.group(2).strip(): in_fence = False
        if in_fence:
            err(f"BROKEN FENCE: {f.relative_to(DOCS)}")
            broken += 1
if broken == 0:
    ok("No broken fences in new destinations")


# ── CHECK 5: Diagram sync ──────────────────────────────────────────────────────
print("\n── Diagram Registration Check ──")
result = subprocess.run(
    ["python3", "scripts/ascii_diagram_gen.py", "--check"],
    capture_output=True, text=True, cwd=REPO
)
output = result.stdout + result.stderr
no_block = output.count("NO BLOCK")
if no_block > 0:
    err(f"ascii_diagram_gen --check: {no_block} NO BLOCK errors")
    print(output[-3000:])
else:
    ok("ascii_diagram_gen --check: 0 issues")


# ── CHECK 6: backup/dell-cyber-recovery still present (confirm delete manually) ──
print("\n── Manual Delete Confirmation ──")
if exists("backup/dell-cyber-recovery"):
    warn("backup/dell-cyber-recovery/ still exists — delete manually after confirming with user:\n"
         "    git rm -r docs/backup/dell-cyber-recovery/")
else:
    ok("backup/dell-cyber-recovery/ already removed")

for shell_idx in ["disaster-recovery/index.md", "performance/index.md",
                   "change-management/index.md", "inventory/index.md",
                   "lifecycle/index.md", "project-management/index.md",
                   "database/index.md"]:
    if exists(shell_idx):
        warn(f"Shell index remains — delete after confirming: {shell_idx}")


# ── SUMMARY ───────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"ERRORS:   {len(ERRORS)}")
print(f"WARNINGS: {len(WARNINGS)}")
print(f"OK:       {len(INFO)}")

if ERRORS:
    print("\nERRORS:")
    for e in ERRORS: print(f"  ✗  {e}")

if WARNINGS:
    print("\nWARNINGS:")
    for w in WARNINGS: print(f"  !  {w}")

sys.exit(1 if ERRORS else 0)
