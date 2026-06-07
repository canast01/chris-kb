#!/usr/bin/env python3
"""
Track 4 restructuring — execution orchestrator.

Phases:
  1  Pre-flight check (aborts on any error)
  2  Build DB product section stubs (mysql, postgresql, sql-server)
  3  git mv disaster-recovery residual → backup/
  4  git mv performance → monitoring-standards/
  5  git mv project-management/health-checks → monitoring-standards/
  6  Move/merge change-management → tools/servicenow/change-management/
  7  Move/merge inventory + pm/asset-inventory → tools/servicenow/asset-inventory/
  8  Move lifecycle → tools/servicenow/lifecycle/
  9  Move remaining project-management → tools/servicenow/
  10 Seed DB sections from database/ pages
  11 Fix diagram path registrations
  12 Post-check

Run with --dry-run to simulate.
Run with --phase=N to execute only a specific phase.
"""
import re, shutil, subprocess, sys, textwrap
from pathlib import Path

REPO  = Path(__file__).parent.parent
DOCS  = REPO / "docs"
DRY   = "--dry-run" in sys.argv
ONLY  = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--phase=")), None)
ERRORS = []
DONE   = []

def log(msg):  print(f"  {msg}")
def ok(msg):   DONE.append(msg); print(f"  ✓  {msg}")
def err(msg):  ERRORS.append(msg); print(f"  ✗  {msg}")
def skip(msg): print(f"  –  {msg}")

def phase(n, title):
    if ONLY and ONLY != n: return False
    print(f"\n{'='*60}\nPhase {n}: {title}\n{'='*60}")
    return True

def run(cmd):
    if DRY: print(f"  [DRY] {' '.join(str(c) for c in cmd)}"); return True
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    if result.returncode != 0:
        err(f"Command failed: {' '.join(str(c) for c in cmd)}\n{result.stderr.strip()}")
        return False
    return True

def git_mv(src_rel, dst_rel):
    src = DOCS / src_rel
    dst = DOCS / dst_rel
    if not src.exists(): skip(f"git mv {src_rel} (source gone)"); return True
    if dst.exists():     err(f"git mv {src_rel} → {dst_rel}: destination exists"); return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if run(["git", "mv", str(src), str(dst)]):
        ok(f"git mv {src_rel} → {dst_rel}"); return True
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
    if not src.exists(): skip(f"merge {src_rel} (gone)"); return True
    if not dst.exists():
        if not DRY: dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
        ok(f"Copied (new): {src_rel} → {dst_rel}"); return True
    src_secs = h2_sections(src); dst_secs = h2_sections(dst)
    unique = [h for h in src_secs if h not in dst_secs]
    if not unique: skip(f"merge {src_rel} (no unique content)"); return True
    if not DRY:
        additions = '\n'.join(src_secs[h].rstrip('\n') + '\n' for h in unique)
        existing = dst.read_text(errors="replace")
        dst.write_text(existing.rstrip('\n') + '\n\n' + additions)
    ok(f"Merged +{len(unique)} H2s: {src_rel} → {dst_rel}"); return True

def write_file(rel, content):
    p = DOCS / rel
    if p.exists(): skip(f"write {rel} (exists)"); return
    if not DRY:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(textwrap.dedent(content).lstrip())
    ok(f"Created: {rel}")

def extract_engine_sections(src_rel, engine_keywords):
    """Extract H2 sections matching engine_keywords from a multi-engine page."""
    src = DOCS / src_rel
    if not src.exists(): return ""
    content = src.read_text(errors="replace")
    lines = content.splitlines(keepends=True)
    in_fence = False; result = []; capture = False
    for line in lines:
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            if not in_fence: in_fence = True
            elif not m.group(2).strip(): in_fence = False
        if not in_fence and re.match(r'^## ', line):
            capture = any(kw.lower() in line.lower() for kw in engine_keywords)
        if capture: result.append(line)
    return ''.join(result)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 1: Pre-flight
# ─────────────────────────────────────────────────────────────────────────────
if phase(1, "Pre-flight check"):
    result = subprocess.run(["python3", "scripts/track4_precheck.py"],
                            capture_output=True, text=True, cwd=REPO)
    print(result.stdout)
    if result.returncode != 0:
        print("Pre-check FAILED — aborting. Fix errors and re-run.")
        sys.exit(1)
    ok("Pre-check passed")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: Build DB product section stubs
# ─────────────────────────────────────────────────────────────────────────────
if phase(2, "Build MySQL, PostgreSQL, SQL Server product sections"):

    DB_SECTIONS = {
        "compute/linux/mysql": {
            "title": "MySQL / MariaDB",
            "summary": "MySQL and MariaDB — relational database management for Linux environments. "
                       "Covers InnoDB storage engine, replication topologies, backup strategies, "
                       "performance tuning, and high-availability with Group Replication or Galera.",
            "engine_keywords": ["mysql", "mariadb"],
        },
        "compute/linux/postgresql": {
            "title": "PostgreSQL",
            "summary": "PostgreSQL — open-source object-relational database for Linux. "
                       "Covers MVCC architecture, streaming replication, logical replication, "
                       "pg_basebackup, autovacuum tuning, and extension management.",
            "engine_keywords": ["postgresql", "postgres"],
        },
        "compute/windows-server/sql-server": {
            "title": "SQL Server",
            "summary": "Microsoft SQL Server — relational database platform for Windows Server. "
                       "Covers Always On Availability Groups, failover clustering, backup/restore, "
                       "index maintenance, DMV-based diagnostics, and SQL Agent jobs.",
            "engine_keywords": ["sql server", "mssql", "sqlserver"],
        },
    }

    TILES = ["architecture", "deploy", "operations", "security", "troubleshooting"]
    ARCH_SUBS  = ["how-it-works", "design-standards", "integrations"]
    OPS_SUBS   = ["health-checks", "procedures", "cli-reference",
                  "backup-restore", "install-upgrade", "scripts"]
    SEC_SUBS   = ["access-control", "authentication", "encryption", "hardening"]
    TRBL_SUBS  = ["common-issues", "diagnostics", "escalation"]

    for base, meta in DB_SECTIONS.items():
        title = meta["title"]
        summary = meta["summary"]

        # Landing page
        write_file(f"{base}/index.md", f"""\
# {title}

<div class="kb-summary">
{summary}
</div>

<div class="kb-grid kb-grid-5">
  <a class="kb-card" href="architecture/">Architecture</a>
  <a class="kb-card" href="deploy/">Deploy</a>
  <a class="kb-card" href="operations/">Operations</a>
  <a class="kb-card" href="security/">Security</a>
  <a class="kb-card" href="troubleshooting/">Troubleshooting</a>
</div>
""")

        # Architecture
        write_file(f"{base}/architecture/index.md", f"""\
# {title} — Architecture

<div class="kb-summary">
{title} architecture: component overview, design standards, and integrations.
</div>

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">How It Works</a>
  <a class="kb-card" href="design-standards/">Design Standards</a>
  <a class="kb-card" href="integrations/">Integrations</a>
</div>
""")
        for sub in ARCH_SUBS:
            write_file(f"{base}/architecture/{sub}/index.md",
                       f"# {title} — {sub.replace('-', ' ').title()}\n\n<div class=\"kb-summary\">\n{title} {sub.replace('-', ' ')} reference.\n</div>\n")

        # Deploy
        write_file(f"{base}/deploy/index.md", f"""\
# {title} — Initial Deployment

<div class="kb-summary">
{title} deployment: installation, initial configuration, and first-run validation.
</div>
""")

        # Operations
        write_file(f"{base}/operations/index.md", f"""\
# {title} — Operations

<div class="kb-summary">
{title} day-to-day operations: health checks, procedures, CLI reference, scripts, backup/restore, and upgrades.
</div>

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="health-checks/">Health Checks</a>
  <a class="kb-card" href="procedures/">Procedures</a>
  <a class="kb-card" href="cli-reference/">CLI Reference</a>
  <a class="kb-card" href="backup-restore/">Backup & Restore</a>
  <a class="kb-card" href="install-upgrade/">Install & Upgrade</a>
  <a class="kb-card" href="scripts/">Scripts</a>
</div>
""")
        for sub in OPS_SUBS:
            write_file(f"{base}/operations/{sub}/index.md",
                       f"# {title} — {sub.replace('-', ' ').title()}\n\n<div class=\"kb-summary\">\n{title} {sub.replace('-', ' ')} reference.\n</div>\n")

        # Security
        write_file(f"{base}/security/index.md", f"""\
# {title} — Security

<div class="kb-summary">
{title} security: access control, authentication, encryption, and hardening.
</div>

<div class="kb-grid kb-grid-4">
  <a class="kb-card" href="access-control/">Access Control</a>
  <a class="kb-card" href="authentication/">Authentication</a>
  <a class="kb-card" href="encryption/">Encryption</a>
  <a class="kb-card" href="hardening/">Hardening</a>
</div>
""")
        for sub in SEC_SUBS:
            write_file(f"{base}/security/{sub}/index.md",
                       f"# {title} — {sub.replace('-', ' ').title()}\n\n<div class=\"kb-summary\">\n{title} {sub.replace('-', ' ')} reference.\n</div>\n")

        # Troubleshooting
        write_file(f"{base}/troubleshooting/index.md", f"""\
# {title} — Troubleshooting

<div class="kb-summary">
{title} troubleshooting: common issues, diagnostics, and escalation.
</div>

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="common-issues/">Common Issues</a>
  <a class="kb-card" href="diagnostics/">Diagnostics</a>
  <a class="kb-card" href="escalation/">Escalation</a>
</div>
""")
        for sub in TRBL_SUBS:
            write_file(f"{base}/troubleshooting/{sub}/index.md",
                       f"# {title} — {sub.replace('-', ' ').title()}\n\n<div class=\"kb-summary\">\n{title} {sub.replace('-', ' ')} reference.\n</div>\n")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 3: Disaster-recovery residual → backup/
# ─────────────────────────────────────────────────────────────────────────────
if phase(3, "Move disaster-recovery residual → backup/"):
    DR_MOVES = [
        ("disaster-recovery/isolated-recovery-environment-ire", "backup/ire"),
        ("disaster-recovery/failover-procedure",                "backup/runbooks/failover"),
        ("disaster-recovery/failback-procedure",                "backup/runbooks/failback"),
        ("disaster-recovery/disaster-recovery-design",          "backup/dr-design"),
        ("disaster-recovery/runbook",                           "backup/runbooks/dr-runbook"),
    ]
    for src, dst in DR_MOVES:
        git_mv(src, dst)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 4: Performance → monitoring-standards/
# ─────────────────────────────────────────────────────────────────────────────
if phase(4, "Move performance → monitoring-standards/"):
    PERF_PAGES = [
        "capacity-forecasting", "failure-testing", "performance-baselining",
        "reliability-engineering", "resource-optimization",
        "service-availability", "service-level-objectives",
    ]
    for page in PERF_PAGES:
        git_mv(f"performance/{page}", f"monitoring-standards/{page}")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 5: project-management/health-checks → monitoring-standards/
# ─────────────────────────────────────────────────────────────────────────────
if phase(5, "Move project-management/health-checks → monitoring-standards/"):
    git_mv("project-management/health-checks", "monitoring-standards/health-checks")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 6: change-management → tools/servicenow/change-management/
# ─────────────────────────────────────────────────────────────────────────────
if phase(6, "Move/merge change-management → tools/servicenow/change-management/"):
    CM_PAGES = [
        "change-approval", "change-communication", "change-request",
        "change-validation", "deployment-procedure", "emergency-change", "release-management",
    ]
    for page in CM_PAGES:
        git_mv(f"change-management/{page}", f"tools/servicenow/change-management/{page}")

    # project-management/change-management sub-pages (merge where overlap)
    PM_CM_PAGES = [
        ("approval",    "change-approval"),   # merge into change-approval
        ("backout-plan","backout-plan"),       # new
        ("closeout",    "closeout"),           # new
        ("risk",        "risk"),               # new
        ("validation",  "change-validation"),  # merge into change-validation
    ]
    for pm_sub, sn_sub in PM_CM_PAGES:
        src = f"project-management/change-management/{pm_sub}/index.md"
        dst = f"tools/servicenow/change-management/{sn_sub}/index.md"
        merge_file(src, dst)

    # move remaining pm/change-management sub-pages that are new
    for pm_sub, sn_sub in PM_CM_PAGES:
        pm_dir  = f"project-management/change-management/{pm_sub}"
        sn_dir  = f"tools/servicenow/change-management/{sn_sub}"
        src = DOCS / pm_dir
        dst = DOCS / sn_dir
        if src.exists() and not dst.exists():
            git_mv(pm_dir, sn_dir)
        elif src.exists() and dst.exists():
            skip(f"pm/change-management/{pm_sub} already merged or exists at dst")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 7: inventory + pm/asset-inventory → tools/servicenow/asset-inventory/
# ─────────────────────────────────────────────────────────────────────────────
if phase(7, "Move/merge inventory + pm/asset-inventory → tools/servicenow/asset-inventory/"):
    INV_PAGES = [
        "asset-lifecycle", "asset-tracking", "audit", "cleanup", "cmdb",
        "configuration-management", "environment-mapping", "hardware-lifecycle",
        "license-management", "ownership", "support-contracts", "system-inventory",
    ]
    for page in INV_PAGES:
        git_mv(f"inventory/{page}", f"tools/servicenow/asset-inventory/{page}")

    # project-management/asset-inventory — merge unique content then discard
    PM_INV_MAP = [
        ("audit",     "audit"),
        ("cleanup",   "cleanup"),
        ("cmdb",      "cmdb"),
        ("lifecycle", "asset-lifecycle"),
        ("ownership", "ownership"),
    ]
    for pm_sub, sn_sub in PM_INV_MAP:
        merge_file(
            f"project-management/asset-inventory/{pm_sub}/index.md",
            f"tools/servicenow/asset-inventory/{sn_sub}/index.md",
        )


# ─────────────────────────────────────────────────────────────────────────────
# Phase 8: lifecycle → tools/servicenow/lifecycle/
# ─────────────────────────────────────────────────────────────────────────────
if phase(8, "Move lifecycle → tools/servicenow/lifecycle/"):
    LC_PAGES = [
        "environment-readiness", "migration-procedure", "post-upgrade-validation",
        "rollback-procedure", "system-decommission", "system-onboarding", "upgrade-readiness",
    ]
    for page in LC_PAGES:
        git_mv(f"lifecycle/{page}", f"tools/servicenow/lifecycle/{page}")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 9: Remaining project-management → tools/servicenow/
# ─────────────────────────────────────────────────────────────────────────────
if phase(9, "Move remaining project-management → tools/servicenow/"):
    git_mv("project-management/incident-management",  "tools/servicenow/incident-management")
    git_mv("project-management/maintenance-windows",  "tools/servicenow/maintenance-windows")
    git_mv("project-management/rca-template",         "tools/servicenow/templates/rca-template")
    git_mv("project-management/change-plan-template", "tools/servicenow/templates/change-plan-template")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 10: Seed DB product sections from database/ pages
# ─────────────────────────────────────────────────────────────────────────────
if phase(10, "Seed DB product sections from database/ pages"):

    # Map: (database source page, engine keywords, destination operations sub-page, section title)
    SEEDS = [
        # MySQL seeds
        ("database/database-health-check/index.md",
         ["mysql", "mariadb"],
         "compute/linux/mysql/operations/health-checks/index.md",
         "MySQL — Health Checks"),
        ("database/database-maintenance/index.md",
         ["mysql", "mariadb"],
         "compute/linux/mysql/operations/procedures/index.md",
         "MySQL — Maintenance Procedures"),
        ("database/database-backup-validation/index.md",
         ["mysql", "mariadb"],
         "compute/linux/mysql/operations/backup-restore/index.md",
         "MySQL — Backup & Restore"),
        ("database/database-failover/index.md",
         ["mysql", "mariadb"],
         "compute/linux/mysql/operations/procedures/index.md",
         "MySQL — Failover Procedure"),
        ("database/database-capacity-monitoring/index.md",
         ["mysql", "mariadb"],
         "compute/linux/mysql/operations/health-checks/index.md",
         "MySQL — Capacity Monitoring"),
        ("database/database-performance-troubleshooting/index.md",
         ["mysql", "mariadb"],
         "compute/linux/mysql/troubleshooting/common-issues/index.md",
         "MySQL — Performance Troubleshooting"),
        ("database/database-replication-check/index.md",
         ["mysql", "mariadb"],
         "compute/linux/mysql/operations/health-checks/index.md",
         "MySQL — Replication Check"),
        # PostgreSQL seeds
        ("database/database-health-check/index.md",
         ["postgresql", "postgres"],
         "compute/linux/postgresql/operations/health-checks/index.md",
         "PostgreSQL — Health Checks"),
        ("database/database-maintenance/index.md",
         ["postgresql", "postgres"],
         "compute/linux/postgresql/operations/procedures/index.md",
         "PostgreSQL — Maintenance Procedures"),
        ("database/database-backup-validation/index.md",
         ["postgresql", "postgres"],
         "compute/linux/postgresql/operations/backup-restore/index.md",
         "PostgreSQL — Backup & Restore"),
        ("database/database-failover/index.md",
         ["postgresql", "postgres"],
         "compute/linux/postgresql/operations/procedures/index.md",
         "PostgreSQL — Failover Procedure"),
        ("database/database-capacity-monitoring/index.md",
         ["postgresql", "postgres"],
         "compute/linux/postgresql/operations/health-checks/index.md",
         "PostgreSQL — Capacity Monitoring"),
        ("database/database-performance-troubleshooting/index.md",
         ["postgresql", "postgres"],
         "compute/linux/postgresql/troubleshooting/common-issues/index.md",
         "PostgreSQL — Performance Troubleshooting"),
        ("database/database-replication-check/index.md",
         ["postgresql", "postgres"],
         "compute/linux/postgresql/operations/health-checks/index.md",
         "PostgreSQL — Replication Check"),
        # SQL Server seeds
        ("database/database-health-check/index.md",
         ["sql server", "mssql", "sqlserver"],
         "compute/windows-server/sql-server/operations/health-checks/index.md",
         "SQL Server — Health Checks"),
        ("database/database-maintenance/index.md",
         ["sql server", "mssql", "sqlserver"],
         "compute/windows-server/sql-server/operations/procedures/index.md",
         "SQL Server — Maintenance Procedures"),
        ("database/database-backup-validation/index.md",
         ["sql server", "mssql", "sqlserver"],
         "compute/windows-server/sql-server/operations/backup-restore/index.md",
         "SQL Server — Backup & Restore"),
        ("database/database-failover/index.md",
         ["sql server", "mssql", "sqlserver"],
         "compute/windows-server/sql-server/operations/procedures/index.md",
         "SQL Server — Failover Procedure"),
        ("database/database-capacity-monitoring/index.md",
         ["sql server", "mssql", "sqlserver"],
         "compute/windows-server/sql-server/operations/health-checks/index.md",
         "SQL Server — Capacity Monitoring"),
        ("database/database-performance-troubleshooting/index.md",
         ["sql server", "mssql", "sqlserver"],
         "compute/windows-server/sql-server/troubleshooting/common-issues/index.md",
         "SQL Server — Performance Troubleshooting"),
        ("database/database-replication-check/index.md",
         ["sql server", "mssql", "sqlserver"],
         "compute/windows-server/sql-server/operations/health-checks/index.md",
         "SQL Server — Replication Check"),
    ]

    for src_rel, keywords, dst_rel, section_title in SEEDS:
        extracted = extract_engine_sections(src_rel, keywords)
        if not extracted:
            skip(f"No {keywords[0]} content in {src_rel}")
            continue
        dst = DOCS / dst_rel
        if dst.exists():
            existing = dst.read_text(errors="replace")
            if extracted.strip() in existing:
                skip(f"Content already seeded: {dst_rel}"); continue
            if not DRY:
                dst.write_text(existing.rstrip('\n') + '\n\n' + extracted)
            ok(f"Seeded {keywords[0]} content → {dst_rel}")
        else:
            if not DRY:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(f"# {section_title}\n\n<div class=\"kb-summary\">\n{section_title} reference.\n</div>\n\n" + extracted)
            ok(f"Created with seed: {dst_rel}")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 11: Fix diagram registrations
# ─────────────────────────────────────────────────────────────────────────────
if phase(11, "Fix diagram path registrations"):
    cmd = ["python3", "scripts/track4_fix_diagrams.py"]
    if DRY: cmd.append("--dry-run")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    print(result.stdout)
    if result.returncode != 0:
        err("Diagram fix script failed")
    else:
        ok("Diagram registrations updated")


# ─────────────────────────────────────────────────────────────────────────────
# Phase 12: Commit and post-check
# ─────────────────────────────────────────────────────────────────────────────
if phase(12, "Stage, commit, and post-check"):
    if not DRY:
        run(["git", "add", "-A"])
        run(["git", "commit", "-m",
             "Track 4: dissolve cross-cutting sections into platform homes\n\n"
             "- DR residual → backup/ (IRE, failover, failback, DR design, runbook)\n"
             "- performance/ → monitoring-standards/\n"
             "- change-management/ → tools/servicenow/change-management/\n"
             "- inventory/ → tools/servicenow/asset-inventory/\n"
             "- lifecycle/ → tools/servicenow/lifecycle/\n"
             "- project-management/ → monitoring-standards/ + tools/servicenow/\n"
             "- database/ → compute/linux/mysql/, postgresql/, windows-server/sql-server/\n\n"
             "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"])
        ok("Committed")
    else:
        log("[DRY] Would commit all staged changes")

    result = subprocess.run(["python3", "scripts/track4_postcheck.py"],
                            capture_output=True, text=True, cwd=REPO)
    print(result.stdout)
    if result.returncode != 0:
        err("Post-check found issues — review before pushing")
    else:
        ok("Post-check passed")


# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"Completed: {len(DONE)} operations")
if ERRORS:
    print(f"Errors:    {len(ERRORS)}")
    for e in ERRORS: print(f"  ✗  {e}")
    sys.exit(1)
