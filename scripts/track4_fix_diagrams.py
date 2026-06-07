#!/usr/bin/env python3
"""
Track 4 — fix diagram path registrations after section moves.

Updates all @kb_diagram path strings in scripts/diagrams/*.py to reflect
new locations. Also removes entries for backup/dell-cyber-recovery/ which
is being deleted.

Run with --dry-run to preview changes without writing.
"""
import re, sys
from pathlib import Path

REPO = Path(__file__).parent.parent
DRY  = "--dry-run" in sys.argv

DIAGRAM_DIR = REPO / "scripts" / "diagrams"

ERRORS   = []
CHANGES  = []
REMOVALS = []

def log(msg):  print(f"  {msg}")
def ok(msg):   CHANGES.append(msg); print(f"  ✓  {msg}")
def removed(msg): REMOVALS.append(msg); print(f"  –  REMOVED: {msg}")
def err(msg):  ERRORS.append(msg); print(f"  ✗  {msg}")


# Path remaps: (old_prefix, new_prefix)
# Order matters — more specific prefixes first
PATH_REMAPS = [
    # disaster-recovery residual → backup/
    ("docs/disaster-recovery/isolated-recovery-environment-ire/", "docs/backup/ire/"),
    ("docs/disaster-recovery/failover-procedure/",                "docs/backup/runbooks/failover/"),
    ("docs/disaster-recovery/failback-procedure/",                "docs/backup/runbooks/failback/"),
    ("docs/disaster-recovery/disaster-recovery-design/",          "docs/backup/dr-design/"),
    ("docs/disaster-recovery/runbook/",                           "docs/backup/runbooks/dr-runbook/"),

    # performance → monitoring-standards
    ("docs/performance/capacity-forecasting/",      "docs/monitoring-standards/capacity-forecasting/"),
    ("docs/performance/failure-testing/",           "docs/monitoring-standards/failure-testing/"),
    ("docs/performance/performance-baselining/",    "docs/monitoring-standards/performance-baselining/"),
    ("docs/performance/reliability-engineering/",   "docs/monitoring-standards/reliability-engineering/"),
    ("docs/performance/resource-optimization/",     "docs/monitoring-standards/resource-optimization/"),
    ("docs/performance/service-availability/",      "docs/monitoring-standards/service-availability/"),
    ("docs/performance/service-level-objectives/",  "docs/monitoring-standards/service-level-objectives/"),

    # project-management/health-checks → monitoring-standards
    ("docs/project-management/health-checks/",      "docs/monitoring-standards/health-checks/"),

    # change-management → tools/servicenow/change-management
    ("docs/change-management/change-approval/",     "docs/tools/servicenow/change-management/change-approval/"),
    ("docs/change-management/change-communication/","docs/tools/servicenow/change-management/change-communication/"),
    ("docs/change-management/change-request/",      "docs/tools/servicenow/change-management/change-request/"),
    ("docs/change-management/change-validation/",   "docs/tools/servicenow/change-management/change-validation/"),
    ("docs/change-management/deployment-procedure/","docs/tools/servicenow/change-management/deployment-procedure/"),
    ("docs/change-management/emergency-change/",    "docs/tools/servicenow/change-management/emergency-change/"),
    ("docs/change-management/release-management/",  "docs/tools/servicenow/change-management/release-management/"),

    # project-management/change-management → tools/servicenow/change-management
    ("docs/project-management/change-management/approval/",    "docs/tools/servicenow/change-management/approval/"),
    ("docs/project-management/change-management/backout-plan/","docs/tools/servicenow/change-management/backout-plan/"),
    ("docs/project-management/change-management/closeout/",    "docs/tools/servicenow/change-management/closeout/"),
    ("docs/project-management/change-management/risk/",        "docs/tools/servicenow/change-management/risk/"),
    ("docs/project-management/change-management/validation/",  "docs/tools/servicenow/change-management/validation/"),

    # inventory → tools/servicenow/asset-inventory
    ("docs/inventory/",                             "docs/tools/servicenow/asset-inventory/"),

    # project-management/asset-inventory → tools/servicenow/asset-inventory
    ("docs/project-management/asset-inventory/",   "docs/tools/servicenow/asset-inventory/"),

    # lifecycle → tools/servicenow/lifecycle
    ("docs/lifecycle/",                             "docs/tools/servicenow/lifecycle/"),

    # project-management remaining → tools/servicenow
    ("docs/project-management/incident-management/",  "docs/tools/servicenow/incident-management/"),
    ("docs/project-management/maintenance-windows/",  "docs/tools/servicenow/maintenance-windows/"),
    ("docs/project-management/rca-template/",         "docs/tools/servicenow/templates/rca-template/"),
    ("docs/project-management/change-plan-template/", "docs/tools/servicenow/templates/change-plan-template/"),

    # database → compute product sections (generic remaps for the database/ section)
    # these are handled as removals since content was split; new registrations added separately
]

# Paths to REMOVE entirely (section being deleted)
PATHS_TO_REMOVE = [
    "docs/backup/dell-cyber-recovery/",
    "docs/disaster-recovery/index.md",
    "docs/performance/index.md",
    "docs/change-management/index.md",
    "docs/inventory/index.md",
    "docs/lifecycle/index.md",
    "docs/project-management/index.md",
    "docs/database/",
]


def remove_kb_diagram_block(content, path_fragment):
    """Remove all @kb_diagram decorated functions whose path contains path_fragment."""
    pattern = re.compile(
        r'@kb_diagram\([^)]*?' + re.escape(path_fragment) + r'[^)]*?\)\s*\ndef \w+\([^)]*\):\s*\n(?:    [^\n]*\n)*',
        re.MULTILINE
    )
    new_content, count = pattern.subn('', content)
    return new_content, count


for py_file in sorted(DIAGRAM_DIR.glob("*.py")):
    original = py_file.read_text(errors="replace")
    updated  = original

    # Apply path remaps
    for old_prefix, new_prefix in PATH_REMAPS:
        if old_prefix in updated:
            new_text = updated.replace(old_prefix, new_prefix)
            count = updated.count(old_prefix)
            if new_text != updated:
                ok(f"{py_file.name}: replaced {count}× '{old_prefix}' → '{new_prefix}'")
                updated = new_text

    # Remove entries for deleted paths
    for dead_path in PATHS_TO_REMOVE:
        if dead_path in updated:
            # Count occurrences before attempting block removal
            occurrences = updated.count(dead_path)
            # Remove entire @kb_diagram blocks containing this path
            new_text, removed_blocks = remove_kb_diagram_block(updated, dead_path)
            if removed_blocks:
                removed(f"{py_file.name}: removed {removed_blocks} @kb_diagram block(s) for '{dead_path}'")
                updated = new_text
            elif occurrences > 0:
                # Path appears but not in a block we can auto-remove — flag it
                err(f"{py_file.name}: '{dead_path}' found {occurrences}× but could not auto-remove — fix manually")

    if updated != original:
        if not DRY:
            py_file.write_text(updated)
        else:
            log(f"[DRY] Would update: {py_file.name}")
    else:
        if any(old in original for old, _ in PATH_REMAPS) or \
           any(d in original for d in PATHS_TO_REMOVE):
            pass  # already logged
        else:
            log(f"No changes needed: {py_file.name}")


# Validate: run ascii_diagram_gen --check
if not DRY:
    print("\n── Running ascii_diagram_gen --check ──")
    result = subprocess.run(
        ["python3", "scripts/ascii_diagram_gen.py", "--check"],
        capture_output=True, text=True, cwd=REPO
    ) if False else type('obj', (object,), {'returncode': 0, 'stdout': '', 'stderr': ''})()

    # Import subprocess at top
    import subprocess
    result = subprocess.run(
        ["python3", "scripts/ascii_diagram_gen.py", "--check"],
        capture_output=True, text=True, cwd=REPO
    )
    if result.returncode != 0:
        err(f"ascii_diagram_gen --check failed:\n{result.stdout[-2000:]}")
    else:
        ok("ascii_diagram_gen --check: 0 issues")
else:
    log("[DRY] Would run ascii_diagram_gen --check")


# ── Summary ───────────────────────────────────────────────────────────────────
import subprocess  # noqa (already imported above but keep for standalone runs)

print(f"\n{'='*60}")
print(f"Path remaps applied:    {len(CHANGES)}")
print(f"Blocks removed:         {len(REMOVALS)}")
print(f"Errors:                 {len(ERRORS)}")

if ERRORS:
    print("\nErrors (fix manually):")
    for e in ERRORS: print(f"  ✗  {e}")
    sys.exit(1)
