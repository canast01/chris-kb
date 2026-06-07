#!/usr/bin/env python3
"""
Track 2 post-execution validation and cleanup.
Run after each major operation or at the end.
Checks: fences, duplicate diagrams, diagram sync, orphaned dirs, nav consistency.
"""
import re, subprocess, sys
from pathlib import Path

REPO = Path(__file__).parent.parent
DOCS = REPO / "docs"
ERRORS = []
WARNINGS = []

def err(msg): ERRORS.append(f"  ERROR: {msg}")
def warn(msg): WARNINGS.append(f"  WARN:  {msg}")

# ── 1. Broken fences ──────────────────────────────────────────────────────────
print("\n── Broken Fences ──")
broken = []
for f in sorted(DOCS.rglob("*.md")):
    content = f.read_text(errors="replace")
    in_fence = False
    for line in content.splitlines():
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            lang = m.group(2).strip()
            if not in_fence: in_fence = True
            elif not lang: in_fence = False
    if in_fence:
        broken.append(str(f.relative_to(DOCS)))
if broken:
    for f in broken: err(f"Broken fence: {f}")
else:
    print("  OK: 0 broken fences")

# ── 2. Duplicate diagrams ─────────────────────────────────────────────────────
print("\n── Duplicate Diagrams ──")
dupes = []
for f in sorted(DOCS.rglob("*.md")):
    content = f.read_text(errors="replace")
    blocks = re.findall(r'^```text\n.*?^```$', content, re.MULTILINE | re.DOTALL)
    seen = []
    for b in blocks:
        if b in seen:
            dupes.append(str(f.relative_to(DOCS)))
            break
        seen.append(b)
if dupes:
    for f in dupes: err(f"Duplicate diagram: {f}")
else:
    print("  OK: 0 duplicate diagrams")

# ── 3. Diagram sync ───────────────────────────────────────────────────────────
print("\n── Diagram Sync ──")
result = subprocess.run(
    ["python3", "scripts/ascii_diagram_gen.py", "--check"],
    capture_output=True, text=True, cwd=REPO
)
out_of_sync = [l for l in result.stdout.splitlines() if "OUT OF SYNC" in l or "NO BLOCK" in l]
if out_of_sync:
    for l in out_of_sync[:10]: warn(l.strip())
    if len(out_of_sync) > 10: warn(f"... and {len(out_of_sync)-10} more")
else:
    print("  OK: All diagrams in sync")

# ── 4. Orphaned sections (expected-dissolved still exist) ────────────────────
print("\n── Orphaned Sections ──")
should_be_gone = [
    "change-management", "lifecycle", "inventory", "performance",
    "project-management", "data-protection", "runbooks", "architecture",
    "integration", "database", "monitoring", "certifications",
    "troubleshooting",
]
for s in should_be_gone:
    p = DOCS / s
    if p.exists():
        count = len(list(p.rglob("*.md")))
        warn(f"Still exists: {s}/ ({count} pages)")
    else:
        print(f"  OK: {s}/ dissolved")

# ── 5. Expected new sections exist ───────────────────────────────────────────
print("\n── New Sections Present ──")
should_exist = [
    "backup",
    "backup/veeam",
    "backup/commvault",
    "backup/netbackup",
    "backup/dell-cyber-recovery",
    "storage/dell/recoverpoint",
    "storage/dell/srdf-a",
    "storage/dell/srdf-s",
    "storage/netapp/superna-eyeglass",
    "storage/pure/pure1",
    "storage/netapp/insightiq",
    "storage/dell/dell-aiops",
    "compute/windows-server/active-directory",
    "compute/windows-server/sql-server",
    "compute/linux/postgresql",
    "compute/linux/mysql",
]
for s in should_exist:
    p = DOCS / s
    if p.exists():
        count = len(list(p.rglob("*.md")))
        print(f"  OK: {s}/ ({count} pages)")
    else:
        err(f"MISSING new section: {s}/")

# ── 6. SR M duplicate deleted ────────────────────────────────────────────────
print("\n── Deleted Sections ──")
for s in ["disaster-recovery/srm"]:
    p = DOCS / s
    if p.exists():
        warn(f"Should be deleted: {s}/ (already merged)")
    else:
        print(f"  OK: {s}/ deleted")

# ── 7. H1 check (no pages missing headings) ──────────────────────────────────
print("\n── H1 Coverage ──")
no_h1 = []
for f in sorted(DOCS.rglob("*.md")):
    content = f.read_text(errors="replace")
    if 'kb-grid' in content: continue  # nav pages
    lines = content.splitlines()
    in_fence = False
    h1s = []
    for line in lines:
        m = re.match(r'^(`{3,})(.*)', line.strip())
        if m:
            if not in_fence: in_fence = True
            elif not m.group(2).strip(): in_fence = False
        elif not in_fence and re.match(r'^# ', line):
            h1s.append(line)
    if not h1s:
        no_h1.append(str(f.relative_to(DOCS)))
if no_h1:
    for f in no_h1[:10]: warn(f"No H1: {f}")
    if len(no_h1) > 10: warn(f"... and {len(no_h1)-10} more")
else:
    print("  OK: All pages have H1")

# ── 8. Page count sanity ──────────────────────────────────────────────────────
print("\n── Page Count Sanity ──")
total = len(list(DOCS.rglob("*.md")))
print(f"  Total pages: {total}")
if total < 2000:
    err(f"Page count dropped below 2000 — content may have been lost (was ~2254)")
elif total > 3000:
    warn(f"Page count over 3000 — possible duplication during moves")
else:
    print(f"  OK: Page count in expected range")

# ── SUMMARY ──────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print(f"ERRORS:   {len(ERRORS)}")
print(f"WARNINGS: {len(WARNINGS)}")

if ERRORS:
    print("\nERRORS (fix immediately):")
    for e in ERRORS: print(e)
if WARNINGS:
    print("\nWARNINGS:")
    for w in WARNINGS: print(w)

sys.exit(1 if ERRORS else 0)
