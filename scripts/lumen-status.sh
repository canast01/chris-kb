#!/usr/bin/env bash
# Check lumen indexing status for chris-kb from the debug log.
set -euo pipefail

LOG="$HOME/.local/share/lumen/debug.log"

if [ ! -f "$LOG" ]; then
    echo "No lumen debug log found at $LOG"
    exit 1
fi

echo "=== Lumen Index Status (chris-kb) ==="

# Parse log in Python so we correctly track only the MOST RECENT session
python3 - "$LOG" <<'PYEOF'
import sys, json

log_path = sys.argv[1]
session = {}  # state of the most recent chris-kb session

with open(log_path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        proj = d.get("project", "") + d.get("effective_root", "")
        if "chris-kb" not in proj:
            continue
        msg = d.get("msg", "")
        if msg == "indexing started":
            # New session — reset state
            session = {"started": d["time"][:19].replace("T", " "), "status": "in_progress"}
        elif msg == "indexing plan" and session:
            session["total"] = d.get("total_files", "?")
            session["to_add"] = d.get("files_to_add", "?")
            session["to_modify"] = d.get("files_to_modify", "?")
        elif msg == "indexing complete" and session:
            session["status"] = "complete"
            session["indexed"] = d.get("indexed_files", "?")
            session["chunks"] = d.get("chunks_created", "?")
            session["elapsed"] = d.get("elapsed", "?")
        elif msg == "indexing failed" and session:
            session["status"] = "failed"
            session["error"] = d.get("err", "unknown")

if not session:
    print("No indexing session found for chris-kb")
    sys.exit(0)

print(f"Started:  {session.get('started', '?')}")
if "total" in session:
    print(f"Plan:     {session['total']} files ({session['to_add']} to add, {session['to_modify']} to modify)")

status = session.get("status")
if status == "complete":
    print(f"Status:   ✅ COMPLETE")
    print(f"Indexed:  {session['indexed']} files → {session['chunks']} chunks in {session['elapsed']}")
elif status == "failed":
    print(f"Status:   ❌ FAILED — {session['error']}")
else:
    print(f"Status:   ⏳ IN PROGRESS")
    print(f"Watch:    tail -f {log_path} | grep chris-kb")
PYEOF

# Show WAL size as a progress proxy (grows as chunks are written)
WAL=$(find "$HOME/.local/share/lumen" -name "index.db-wal" 2>/dev/null | xargs ls -lh 2>/dev/null | awk '{print $5}' | sort -h | tail -1 || true)
[ -n "$WAL" ] && echo "WAL size: $WAL (grows as chunks are written)"
