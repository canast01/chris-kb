#!/usr/bin/env python3
"""
KB Restructure — unified pipeline for dissolving cross-cutting sections into platform homes.

This is the single script for all "dissolve section → platform home" work.
Same strategy used for Track 2 (products) and Track 4 (process/ops content).

Phases:
  0  Precheck   — validate sources, detect conflicts, flag stale diagrams
  1  Build      — create new product section stubs (MySQL, PostgreSQL, SQL Server)
  2  Move DR    — disaster-recovery residual → backup/
  3  Move Perf  — performance/ → monitoring-standards/
  4  Move HC    — project-management/health-checks → monitoring-standards/
  5  Move CM    — change-management/ → tools/servicenow/change-management/
  6  Move Inv   — inventory/ + pm/asset-inventory/ → tools/servicenow/asset-inventory/
  7  Move LC    — lifecycle/ → tools/servicenow/lifecycle/
  8  Move PM    — remaining project-management/ → tools/servicenow/
  9  Seed DB    — extract engine sections from database/ → product sections
  10 Fix Diags  — remap @kb_diagram path strings, remove deleted entries
  11 Postcheck  — verify destinations, fence integrity, diagram sync

Usage:
  python3 scripts/kb_restructure.py --dry-run          # simulate all phases
  python3 scripts/kb_restructure.py                    # execute all phases
  python3 scripts/kb_restructure.py --phase=0          # precheck only
  python3 scripts/kb_restructure.py --phase=0,1,2      # specific phases
"""
import re, shutil, subprocess, sys, textwrap
from pathlib import Path

REPO  = Path(__file__).parent.parent
DOCS  = REPO / "docs"
DRY   = "--dry-run" in sys.argv
ONLY  = set()
for a in sys.argv:
    if a.startswith("--phase="):
        ONLY = {int(x) for x in a.split("=")[1].split(",")}

ERRORS = []; WARNINGS = []; DONE = []

def log(msg):  print(f"  {msg}")
def ok(msg):   DONE.append(msg);     print(f"  ✓  {msg}")
def warn(msg): WARNINGS.append(msg); print(f"  !  {msg}")
def err(msg):  ERRORS.append(msg);   print(f"  ✗  {msg}")
def skip(msg): print(f"  –  {msg}")

def phase(n, title):
    if ONLY and n not in ONLY: return False
    print(f"\n{'='*60}\nPhase {n}: {title}\n{'='*60}")
    return True

def run(cmd):
    if DRY: print(f"  [DRY] {' '.join(str(c) for c in cmd)}"); return True
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    if r.returncode != 0: err(f"FAILED: {' '.join(str(c) for c in cmd)}\n{r.stderr.strip()}"); return False
    return True

def exists(rel):     return (DOCS / rel).exists()
def page_count(rel): p = DOCS / rel; return len(list(p.rglob("*.md"))) if p.exists() else 0

def h2_sections(path):
    if not Path(path).exists(): return {}
    content = Path(path).read_text(errors="replace")
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

def fence_ok(p):
    if not Path(p).exists(): return True
    in_fence = False
    for line in Path(p).read_text(errors="replace").splitlines():
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            if not in_fence: in_fence = True
            elif not m.group(2).strip(): in_fence = False
    return not in_fence

def git_mv(src_rel, dst_rel):
    src = DOCS / src_rel; dst = DOCS / dst_rel
    if not src.exists(): skip(f"git mv {src_rel} (source gone)"); return True
    if dst.exists():     err(f"git mv {src_rel} → {dst_rel}: destination exists"); return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if run(["git", "mv", str(src), str(dst)]): ok(f"git mv {src_rel} → {dst_rel}"); return True
    return False

def merge_file(src_rel, dst_rel):
    src = DOCS / src_rel; dst = DOCS / dst_rel
    if not src.exists(): skip(f"merge {src_rel} (gone)"); return True
    if not dst.exists():
        if not DRY: dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
        ok(f"Copied (new): {src_rel} → {dst_rel}"); return True
    unique = [h for h in h2_sections(src) if h not in h2_sections(dst)]
    if not unique: skip(f"merge {src_rel} (no unique content)"); return True
    if not DRY:
        additions = '\n'.join(h2_sections(src)[h].rstrip('\n') + '\n' for h in unique)
        dst.write_text(dst.read_text(errors="replace").rstrip('\n') + '\n\n' + additions)
    ok(f"Merged +{len(unique)} H2s: {src_rel} → {dst_rel}"); return True

def write_file(rel, content):
    p = DOCS / rel
    if p.exists(): skip(f"exists: {rel}"); return
    if not DRY: p.parent.mkdir(parents=True, exist_ok=True); p.write_text(textwrap.dedent(content).lstrip())
    ok(f"Created: {rel}")

def extract_engine_sections(src_rel, keywords):
    src = DOCS / src_rel
    if not src.exists(): return ""
    in_fence = False; result = []; capture = False
    for line in src.read_text(errors="replace").splitlines(keepends=True):
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            if not in_fence: in_fence = True
            elif not m.group(2).strip(): in_fence = False
        if not in_fence and re.match(r'^## ', line):
            capture = any(kw.lower() in line.lower() for kw in keywords)
        if capture: result.append(line)
    return ''.join(result)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 0: Precheck
# ─────────────────────────────────────────────────────────────────────────────
if phase(0, "Precheck — validate before executing"):

    print("\n  [Git state]")
    r = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=REPO)
    if r.stdout.strip(): warn(f"Uncommitted changes ({len(r.stdout.strip().splitlines())} files) — commit first")
    else: ok("Working tree clean")

    print("\n  [Source existence]")
    SOURCES = [
        "disaster-recovery/isolated-recovery-environment-ire",
        "disaster-recovery/failover-procedure", "disaster-recovery/failback-procedure",
        "disaster-recovery/disaster-recovery-design", "disaster-recovery/runbook",
        "performance/capacity-forecasting", "performance/failure-testing",
        "performance/performance-baselining", "performance/reliability-engineering",
        "performance/resource-optimization", "performance/service-availability",
        "performance/service-level-objectives",
        "project-management/health-checks",
        "change-management/change-approval", "change-management/change-communication",
        "change-management/change-request", "change-management/change-validation",
        "change-management/deployment-procedure", "change-management/emergency-change",
        "change-management/release-management",
        "project-management/change-management",
        "inventory/asset-lifecycle", "inventory/asset-tracking", "inventory/audit",
        "inventory/cleanup", "inventory/cmdb", "inventory/configuration-management",
        "inventory/environment-mapping", "inventory/hardware-lifecycle",
        "inventory/license-management", "inventory/ownership",
        "inventory/support-contracts", "inventory/system-inventory",
        "project-management/asset-inventory",
        "lifecycle/environment-readiness", "lifecycle/migration-procedure",
        "lifecycle/post-upgrade-validation", "lifecycle/rollback-procedure",
        "lifecycle/system-decommission", "lifecycle/system-onboarding",
        "lifecycle/upgrade-readiness",
        "project-management/incident-management", "project-management/maintenance-windows",
        "project-management/rca-template", "project-management/change-plan-template",
        "database/database-health-check", "database/database-maintenance",
        "database/database-failover", "database/database-backup-validation",
        "database/database-capacity-monitoring",
        "database/database-performance-troubleshooting",
        "database/database-replication-check",
    ]
    for s in SOURCES:
        (ok if exists(s) else err)(f"{'EXISTS' if exists(s) else 'MISSING'}: {s}")

    print("\n  [Merge conflict check]")
    OVERLAPS = [
        ("project-management/asset-inventory/audit/index.md",     "inventory/audit/index.md"),
        ("project-management/asset-inventory/cleanup/index.md",   "inventory/cleanup/index.md"),
        ("project-management/asset-inventory/cmdb/index.md",      "inventory/cmdb/index.md"),
        ("project-management/asset-inventory/ownership/index.md", "inventory/ownership/index.md"),
        ("project-management/change-management/approval/index.md","change-management/change-approval/index.md"),
        ("project-management/change-management/validation/index.md","change-management/change-validation/index.md"),
    ]
    for src_rel, dst_rel in OVERLAPS:
        if exists(src_rel) and exists(dst_rel):
            lost = {h for h in h2_sections(DOCS / src_rel) if h not in h2_sections(DOCS / dst_rel)}
            if lost: warn(f"MERGE NEEDED ({len(lost)} unique H2s): {src_rel}")
            else: ok(f"No content loss: {src_rel}")

    print("\n  [Fence integrity]")
    broken = sum(1 for d in ["disaster-recovery","performance","change-management",
                              "inventory","lifecycle","project-management","database"]
                 for f in (DOCS/d).rglob("*.md") if (DOCS/d).exists() and not fence_ok(f)
                 and not err(f"BROKEN FENCE: {f.relative_to(DOCS)}"))
    if not broken: ok("All source fences clean")

    print("\n  [Diagram registrations to update]")
    prefixes = ["docs/disaster-recovery/","docs/performance/","docs/change-management/",
                "docs/inventory/","docs/lifecycle/","docs/project-management/",
                "docs/database/","docs/backup/dell-cyber-recovery/"]
    total = 0
    for py in sorted((REPO/"scripts"/"diagrams").glob("*.py")):
        content = py.read_text(errors="replace")
        count = sum(content.count(p) for p in prefixes)
        if count: warn(f"  {py.name}: {count} entries need path updates"); total += count
    if not total: ok("No stale diagram registrations")

    print(f"\n  PRECHECK: {len(ERRORS)} errors, {len(WARNINGS)} warnings")
    if ERRORS: [print(f"  ✗  {e}") for e in ERRORS]; sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 1: Build MySQL, PostgreSQL, SQL Server product sections
# ─────────────────────────────────────────────────────────────────────────────
if phase(1, "Build DB product sections (MySQL, PostgreSQL, SQL Server)"):

    DB = {
        "compute/linux/mysql": ("MySQL / MariaDB",
            "MySQL and MariaDB relational database for Linux — InnoDB, replication, backup, HA.",
            ["mysql","mariadb"]),
        "compute/linux/postgresql": ("PostgreSQL",
            "PostgreSQL open-source object-relational database — MVCC, streaming replication, autovacuum.",
            ["postgresql","postgres"]),
        "compute/windows-server/sql-server": ("SQL Server",
            "Microsoft SQL Server for Windows Server — Always On AG, failover clustering, backup/restore.",
            ["sql server","mssql","sqlserver"]),
    }
    OPS  = ["health-checks","procedures","cli-reference","backup-restore","install-upgrade","scripts"]
    SEC  = ["access-control","authentication","encryption","hardening"]
    TRBL = ["common-issues","diagnostics","escalation"]
    ARCH = ["how-it-works","design-standards","integrations"]

    for base, (title, summary, _) in DB.items():
        write_file(f"{base}/index.md",
            f"# {title}\n\n<div class=\"kb-summary\">\n{summary}\n</div>\n\n"
            "<div class=\"kb-grid kb-grid-5\">\n"
            "  <a class=\"kb-card\" href=\"architecture/\">Architecture</a>\n"
            "  <a class=\"kb-card\" href=\"deploy/\">Deploy</a>\n"
            "  <a class=\"kb-card\" href=\"operations/\">Operations</a>\n"
            "  <a class=\"kb-card\" href=\"security/\">Security</a>\n"
            "  <a class=\"kb-card\" href=\"troubleshooting/\">Troubleshooting</a>\n"
            "</div>\n")
        write_file(f"{base}/architecture/index.md",
            f"# {title} — Architecture\n\n<div class=\"kb-summary\">\nArchitecture overview, design standards, and integrations.\n</div>\n\n"
            "<div class=\"kb-grid kb-grid-3\">\n"
            "  <a class=\"kb-card\" href=\"how-it-works/\">How It Works</a>\n"
            "  <a class=\"kb-card\" href=\"design-standards/\">Design Standards</a>\n"
            "  <a class=\"kb-card\" href=\"integrations/\">Integrations</a>\n"
            "</div>\n")
        for s in ARCH:
            write_file(f"{base}/architecture/{s}/index.md",
                f"# {title} — {s.replace('-',' ').title()}\n\n<div class=\"kb-summary\">\n{title} {s.replace('-',' ')} reference.\n</div>\n")
        write_file(f"{base}/deploy/index.md",
            f"# {title} — Initial Deployment\n\n<div class=\"kb-summary\">\nInstallation, initial configuration, and first-run validation.\n</div>\n")
        write_file(f"{base}/operations/index.md",
            f"# {title} — Operations\n\n<div class=\"kb-summary\">\nHealth checks, procedures, CLI, backup/restore, upgrades, and scripts.\n</div>\n\n"
            "<div class=\"kb-grid kb-grid-3\">\n"
            + "".join(f"  <a class=\"kb-card\" href=\"{s}/\">{s.replace('-',' ').title()}</a>\n" for s in OPS)
            + "</div>\n")
        for s in OPS:
            write_file(f"{base}/operations/{s}/index.md",
                f"# {title} — {s.replace('-',' ').title()}\n\n<div class=\"kb-summary\">\n{title} {s.replace('-',' ')} reference.\n</div>\n")
        write_file(f"{base}/security/index.md",
            f"# {title} — Security\n\n<div class=\"kb-summary\">\nAccess control, authentication, encryption, and hardening.\n</div>\n\n"
            "<div class=\"kb-grid kb-grid-4\">\n"
            + "".join(f"  <a class=\"kb-card\" href=\"{s}/\">{s.replace('-',' ').title()}</a>\n" for s in SEC)
            + "</div>\n")
        for s in SEC:
            write_file(f"{base}/security/{s}/index.md",
                f"# {title} — {s.replace('-',' ').title()}\n\n<div class=\"kb-summary\">\n{title} {s.replace('-',' ')} reference.\n</div>\n")
        write_file(f"{base}/troubleshooting/index.md",
            f"# {title} — Troubleshooting\n\n<div class=\"kb-summary\">\nCommon issues, diagnostics, and escalation.\n</div>\n\n"
            "<div class=\"kb-grid kb-grid-3\">\n"
            + "".join(f"  <a class=\"kb-card\" href=\"{s}/\">{s.replace('-',' ').title()}</a>\n" for s in TRBL)
            + "</div>\n")
        for s in TRBL:
            write_file(f"{base}/troubleshooting/{s}/index.md",
                f"# {title} — {s.replace('-',' ').title()}\n\n<div class=\"kb-summary\">\n{title} {s.replace('-',' ')} reference.\n</div>\n")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: Disaster-recovery residual → backup/
# ─────────────────────────────────────────────────────────────────────────────
if phase(2, "Move disaster-recovery residual → backup/"):
    for src, dst in [
        ("disaster-recovery/isolated-recovery-environment-ire", "backup/ire"),
        ("disaster-recovery/failover-procedure",                "backup/runbooks/failover"),
        ("disaster-recovery/failback-procedure",                "backup/runbooks/failback"),
        ("disaster-recovery/disaster-recovery-design",          "backup/dr-design"),
        ("disaster-recovery/runbook",                           "backup/runbooks/dr-runbook"),
    ]:
        git_mv(src, dst)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 3: Performance → monitoring-standards/
# ─────────────────────────────────────────────────────────────────────────────
if phase(3, "Move performance/ → monitoring-standards/"):
    for p in ["capacity-forecasting","failure-testing","performance-baselining",
              "reliability-engineering","resource-optimization",
              "service-availability","service-level-objectives"]:
        git_mv(f"performance/{p}", f"monitoring-standards/{p}")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 4: project-management/health-checks → monitoring-standards/
# ─────────────────────────────────────────────────────────────────────────────
if phase(4, "Move project-management/health-checks → monitoring-standards/"):
    git_mv("project-management/health-checks", "monitoring-standards/health-checks")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 5: change-management → tools/servicenow/change-management/
# ─────────────────────────────────────────────────────────────────────────────
if phase(5, "Move/merge change-management → tools/servicenow/change-management/"):
    for p in ["change-approval","change-communication","change-request","change-validation",
              "deployment-procedure","emergency-change","release-management"]:
        git_mv(f"change-management/{p}", f"tools/servicenow/change-management/{p}")

    PM_CM = [("approval","change-approval"),("backout-plan","backout-plan"),
             ("closeout","closeout"),("risk","risk"),("validation","change-validation")]
    for pm_sub, sn_sub in PM_CM:
        merge_file(f"project-management/change-management/{pm_sub}/index.md",
                   f"tools/servicenow/change-management/{sn_sub}/index.md")
        src_dir = f"project-management/change-management/{pm_sub}"
        dst_dir = f"tools/servicenow/change-management/{sn_sub}"
        if exists(src_dir) and not exists(dst_dir):
            git_mv(src_dir, dst_dir)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 6: inventory + pm/asset-inventory → tools/servicenow/asset-inventory/
# ─────────────────────────────────────────────────────────────────────────────
if phase(6, "Move/merge inventory → tools/servicenow/asset-inventory/"):
    for p in ["asset-lifecycle","asset-tracking","audit","cleanup","cmdb",
              "configuration-management","environment-mapping","hardware-lifecycle",
              "license-management","ownership","support-contracts","system-inventory"]:
        git_mv(f"inventory/{p}", f"tools/servicenow/asset-inventory/{p}")

    for pm_sub, sn_sub in [("audit","audit"),("cleanup","cleanup"),("cmdb","cmdb"),
                            ("lifecycle","asset-lifecycle"),("ownership","ownership")]:
        merge_file(f"project-management/asset-inventory/{pm_sub}/index.md",
                   f"tools/servicenow/asset-inventory/{sn_sub}/index.md")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 7: lifecycle → tools/servicenow/lifecycle/
# ─────────────────────────────────────────────────────────────────────────────
if phase(7, "Move lifecycle/ → tools/servicenow/lifecycle/"):
    for p in ["environment-readiness","migration-procedure","post-upgrade-validation",
              "rollback-procedure","system-decommission","system-onboarding","upgrade-readiness"]:
        git_mv(f"lifecycle/{p}", f"tools/servicenow/lifecycle/{p}")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 8: Remaining project-management → tools/servicenow/
# ─────────────────────────────────────────────────────────────────────────────
if phase(8, "Move remaining project-management → tools/servicenow/"):
    git_mv("project-management/incident-management",  "tools/servicenow/incident-management")
    git_mv("project-management/maintenance-windows",  "tools/servicenow/maintenance-windows")
    git_mv("project-management/rca-template",         "tools/servicenow/templates/rca-template")
    git_mv("project-management/change-plan-template", "tools/servicenow/templates/change-plan-template")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 9: Seed DB sections from database/ multi-engine pages
# ─────────────────────────────────────────────────────────────────────────────
if phase(9, "Seed DB product sections from database/ pages"):
    SEEDS = []
    for db_page, title_prefix, kws, dst_base, ops_page in [
        ("database-health-check",               "Health Checks",              ["mysql","mariadb"],            "compute/linux/mysql",              "operations/health-checks"),
        ("database-maintenance",                "Maintenance",                ["mysql","mariadb"],            "compute/linux/mysql",              "operations/procedures"),
        ("database-backup-validation",          "Backup & Restore",           ["mysql","mariadb"],            "compute/linux/mysql",              "operations/backup-restore"),
        ("database-failover",                   "Failover",                   ["mysql","mariadb"],            "compute/linux/mysql",              "operations/procedures"),
        ("database-capacity-monitoring",        "Capacity Monitoring",        ["mysql","mariadb"],            "compute/linux/mysql",              "operations/health-checks"),
        ("database-performance-troubleshooting","Performance Troubleshooting",["mysql","mariadb"],            "compute/linux/mysql",              "troubleshooting/common-issues"),
        ("database-replication-check",          "Replication Check",          ["mysql","mariadb"],            "compute/linux/mysql",              "operations/health-checks"),
        ("database-health-check",               "Health Checks",              ["postgresql","postgres"],      "compute/linux/postgresql",         "operations/health-checks"),
        ("database-maintenance",                "Maintenance",                ["postgresql","postgres"],      "compute/linux/postgresql",         "operations/procedures"),
        ("database-backup-validation",          "Backup & Restore",           ["postgresql","postgres"],      "compute/linux/postgresql",         "operations/backup-restore"),
        ("database-failover",                   "Failover",                   ["postgresql","postgres"],      "compute/linux/postgresql",         "operations/procedures"),
        ("database-capacity-monitoring",        "Capacity Monitoring",        ["postgresql","postgres"],      "compute/linux/postgresql",         "operations/health-checks"),
        ("database-performance-troubleshooting","Performance Troubleshooting",["postgresql","postgres"],      "compute/linux/postgresql",         "troubleshooting/common-issues"),
        ("database-replication-check",          "Replication Check",          ["postgresql","postgres"],      "compute/linux/postgresql",         "operations/health-checks"),
        ("database-health-check",               "Health Checks",              ["sql server","mssql"],        "compute/windows-server/sql-server","operations/health-checks"),
        ("database-maintenance",                "Maintenance",                ["sql server","mssql"],        "compute/windows-server/sql-server","operations/procedures"),
        ("database-backup-validation",          "Backup & Restore",           ["sql server","mssql"],        "compute/windows-server/sql-server","operations/backup-restore"),
        ("database-failover",                   "Failover",                   ["sql server","mssql"],        "compute/windows-server/sql-server","operations/procedures"),
        ("database-capacity-monitoring",        "Capacity Monitoring",        ["sql server","mssql"],        "compute/windows-server/sql-server","operations/health-checks"),
        ("database-performance-troubleshooting","Performance Troubleshooting",["sql server","mssql"],        "compute/windows-server/sql-server","troubleshooting/common-issues"),
        ("database-replication-check",          "Replication Check",          ["sql server","mssql"],        "compute/windows-server/sql-server","operations/health-checks"),
    ]:
        extracted = extract_engine_sections(f"database/{db_page}/index.md", kws)
        if not extracted: skip(f"No {kws[0]} content in database/{db_page}/"); continue
        dst_rel = f"{dst_base}/{ops_page}/index.md"
        dst = DOCS / dst_rel
        if dst.exists():
            existing = dst.read_text(errors="replace")
            if extracted.strip() in existing: skip(f"Already seeded: {dst_rel}"); continue
            if not DRY: dst.write_text(existing.rstrip('\n') + '\n\n' + extracted)
            ok(f"Seeded {kws[0]} → {dst_rel}")
        else:
            if not DRY:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(f"# {dst_base.split('/')[-1].replace('-',' ').title()} — {title_prefix}\n\n"
                               f"<div class=\"kb-summary\">\n{title_prefix} reference.\n</div>\n\n" + extracted)
            ok(f"Created with seed: {dst_rel}")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 10: Fix diagram path registrations
# ─────────────────────────────────────────────────────────────────────────────
if phase(10, "Fix diagram path registrations"):
    DIAG_DIR = REPO / "scripts" / "diagrams"

    REMAPS = [
        ("docs/disaster-recovery/isolated-recovery-environment-ire/", "docs/backup/ire/"),
        ("docs/disaster-recovery/failover-procedure/",  "docs/backup/runbooks/failover/"),
        ("docs/disaster-recovery/failback-procedure/",  "docs/backup/runbooks/failback/"),
        ("docs/disaster-recovery/disaster-recovery-design/", "docs/backup/dr-design/"),
        ("docs/disaster-recovery/runbook/",             "docs/backup/runbooks/dr-runbook/"),
        ("docs/performance/capacity-forecasting/",      "docs/monitoring-standards/capacity-forecasting/"),
        ("docs/performance/failure-testing/",           "docs/monitoring-standards/failure-testing/"),
        ("docs/performance/performance-baselining/",    "docs/monitoring-standards/performance-baselining/"),
        ("docs/performance/reliability-engineering/",   "docs/monitoring-standards/reliability-engineering/"),
        ("docs/performance/resource-optimization/",     "docs/monitoring-standards/resource-optimization/"),
        ("docs/performance/service-availability/",      "docs/monitoring-standards/service-availability/"),
        ("docs/performance/service-level-objectives/",  "docs/monitoring-standards/service-level-objectives/"),
        ("docs/project-management/health-checks/",      "docs/monitoring-standards/health-checks/"),
        ("docs/change-management/change-approval/",     "docs/tools/servicenow/change-management/change-approval/"),
        ("docs/change-management/change-communication/","docs/tools/servicenow/change-management/change-communication/"),
        ("docs/change-management/change-request/",      "docs/tools/servicenow/change-management/change-request/"),
        ("docs/change-management/change-validation/",   "docs/tools/servicenow/change-management/change-validation/"),
        ("docs/change-management/deployment-procedure/","docs/tools/servicenow/change-management/deployment-procedure/"),
        ("docs/change-management/emergency-change/",    "docs/tools/servicenow/change-management/emergency-change/"),
        ("docs/change-management/release-management/",  "docs/tools/servicenow/change-management/release-management/"),
        ("docs/project-management/change-management/",  "docs/tools/servicenow/change-management/"),
        ("docs/inventory/",                             "docs/tools/servicenow/asset-inventory/"),
        ("docs/project-management/asset-inventory/",    "docs/tools/servicenow/asset-inventory/"),
        ("docs/lifecycle/",                             "docs/tools/servicenow/lifecycle/"),
        ("docs/project-management/incident-management/","docs/tools/servicenow/incident-management/"),
        ("docs/project-management/maintenance-windows/","docs/tools/servicenow/maintenance-windows/"),
        ("docs/project-management/rca-template/",       "docs/tools/servicenow/templates/rca-template/"),
        ("docs/project-management/change-plan-template/","docs/tools/servicenow/templates/change-plan-template/"),
    ]
    DEAD = ["docs/backup/dell-cyber-recovery/","docs/database/","docs/disaster-recovery/index",
            "docs/performance/index","docs/change-management/index","docs/inventory/index",
            "docs/lifecycle/index","docs/project-management/index","docs/database/index"]

    def remove_block(content, fragment):
        pat = re.compile(
            r'@kb_diagram\([^)]*?' + re.escape(fragment) + r'[^)]*?\)\s*\ndef \w+\([^)]*\):\s*\n(?:    [^\n]*\n)*',
            re.MULTILINE)
        return pat.subn('', content)

    for py in sorted(DIAG_DIR.glob("*.py")):
        orig = py.read_text(errors="replace"); updated = orig
        for old, new in REMAPS:
            if old in updated:
                count = updated.count(old)
                updated = updated.replace(old, new)
                ok(f"{py.name}: {count}× {old.split('/')[-2]} → {new.split('/')[-2]}")
        for dead in DEAD:
            if dead in updated:
                new_text, n = remove_block(updated, dead)
                if n: removed_msg = f"{py.name}: removed {n} @kb_diagram block(s) for {dead}"; print(f"  –  {removed_msg}"); updated = new_text
                elif updated.count(dead): err(f"{py.name}: '{dead}' found but cannot auto-remove")
        if updated != orig and not DRY:
            py.write_text(updated)

    if not DRY:
        r = subprocess.run(["python3","scripts/ascii_diagram_gen.py","--check"],
                           capture_output=True, text=True, cwd=REPO)
        no_block = (r.stdout+r.stderr).count("NO BLOCK")
        (ok if no_block == 0 else err)(f"ascii_diagram_gen --check: {no_block} issues")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 11: Postcheck
# ─────────────────────────────────────────────────────────────────────────────
if phase(11, "Postcheck — verify moves complete"):

    print("\n  [Old sections gone]")
    GONE = [
        "disaster-recovery/isolated-recovery-environment-ire","disaster-recovery/failover-procedure",
        "disaster-recovery/failback-procedure","disaster-recovery/disaster-recovery-design",
        "disaster-recovery/runbook","performance/capacity-forecasting","performance/failure-testing",
        "performance/performance-baselining","performance/reliability-engineering",
        "performance/resource-optimization","performance/service-availability",
        "performance/service-level-objectives","project-management/health-checks",
        "change-management/change-approval","change-management/change-communication",
        "change-management/change-request","change-management/change-validation",
        "change-management/deployment-procedure","change-management/emergency-change",
        "change-management/release-management","inventory/asset-lifecycle","inventory/asset-tracking",
        "inventory/audit","inventory/cleanup","inventory/cmdb","inventory/configuration-management",
        "inventory/environment-mapping","inventory/hardware-lifecycle","inventory/license-management",
        "inventory/ownership","inventory/support-contracts","inventory/system-inventory",
        "lifecycle/environment-readiness","lifecycle/migration-procedure","lifecycle/post-upgrade-validation",
        "lifecycle/rollback-procedure","lifecycle/system-decommission","lifecycle/system-onboarding",
        "lifecycle/upgrade-readiness","project-management/incident-management",
        "project-management/maintenance-windows","project-management/rca-template",
        "project-management/change-plan-template","project-management/asset-inventory",
        "project-management/change-management",
    ]
    for p in GONE: (err if exists(p) else ok)(f"{'STILL EXISTS' if exists(p) else 'Gone'}: {p}")

    print("\n  [New destinations exist]")
    NEW = [
        ("backup/ire",4), ("backup/runbooks/failover",1), ("backup/runbooks/failback",1),
        ("backup/dr-design",1), ("backup/runbooks/dr-runbook",1),
        ("monitoring-standards/capacity-forecasting",1), ("monitoring-standards/health-checks",5),
        ("tools/servicenow/change-management",7), ("tools/servicenow/asset-inventory",10),
        ("tools/servicenow/lifecycle",7), ("tools/servicenow/incident-management",5),
        ("tools/servicenow/maintenance-windows",5), ("tools/servicenow/templates",2),
        ("compute/linux/mysql",15), ("compute/linux/postgresql",15),
        ("compute/windows-server/sql-server",15),
    ]
    for path, min_p in NEW:
        actual = page_count(path)
        if not exists(path): err(f"MISSING: {path}")
        elif actual < min_p: warn(f"Low count ({actual}<{min_p}): {path}")
        else: ok(f"EXISTS ({actual}p): {path}")

    print("\n  [Section shells pending manual cleanup]")
    for d in ["disaster-recovery","performance","change-management","inventory",
              "lifecycle","project-management","database"]:
        pages = list((DOCS/d).rglob("*.md")) if exists(d) else []
        if not exists(d): ok(f"Fully gone: {d}")
        elif len(pages) <= 1: warn(f"Shell only (safe to delete): {d}/")
        else: err(f"CONTENT REMAINS ({len(pages)}p): {d}/")

    print("\n  [Diagram check]")
    r = subprocess.run(["python3","scripts/ascii_diagram_gen.py","--check"],
                       capture_output=True, text=True, cwd=REPO)
    n = (r.stdout+r.stderr).count("NO BLOCK")
    (ok if n == 0 else err)(f"ascii_diagram_gen --check: {n} issues")

    print("\n  [Manual deletes still needed]")
    for d in ["backup/dell-cyber-recovery","disaster-recovery","performance",
              "change-management","inventory","lifecycle","project-management","database"]:
        if exists(d):
            pages = page_count(d)
            warn(f"Pending delete (confirm with user): {d}/ ({pages} pages)")


# ─────────────────────────────────────────────────────────────────────────────
# Commit (runs when no --phase filter or when phase 11 included)
# ─────────────────────────────────────────────────────────────────────────────
if not ONLY or 11 in ONLY:
    if not DRY and not ERRORS:
        run(["git", "add", "-A"])
        run(["git", "commit", "-m",
             "Dissolve cross-cutting sections into platform homes\n\n"
             "- disaster-recovery/ residual → backup/\n"
             "- performance/ → monitoring-standards/\n"
             "- change-management/ → tools/servicenow/change-management/\n"
             "- inventory/ → tools/servicenow/asset-inventory/\n"
             "- lifecycle/ → tools/servicenow/lifecycle/\n"
             "- project-management/ → monitoring-standards/ + tools/servicenow/\n"
             "- database/ → compute/linux/mysql|postgresql, windows-server/sql-server\n\n"
             "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"])
        ok("Committed")


print(f"\n{'='*60}")
print(f"Done: {len(DONE)}  Warnings: {len(WARNINGS)}  Errors: {len(ERRORS)}")
if ERRORS: [print(f"  ✗  {e}") for e in ERRORS]; sys.exit(1)
