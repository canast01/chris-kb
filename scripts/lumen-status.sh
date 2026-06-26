#!/usr/bin/env bash
# Check lumen indexing status for chris-kb.
# Detects completion, failure, dead process, and stuck (no WAL growth).
# Writes WAL size to .lumen-wal-prev for stuck detection between runs.
set -euo pipefail

LOG="$HOME/.local/share/lumen/debug.log"
LUMEN_BIN="$HOME/.claude/plugins/cache/claude-plugins-official/lumen/0.0.41/bin/lumen-darwin-amd64"
LUMEN_MODEL="nomic-embed-text"
KB="$HOME/chris-kb"
WAL_PREV="$KB/.lumen-wal-prev"   # format: "<size>:<unchanged_count>"

if [ ! -f "$LOG" ]; then
    echo "No lumen debug log found at $LOG"
    exit 1
fi

echo "=== Lumen Index Status (chris-kb) — $(date '+%Y-%m-%d %H:%M') ==="

# ── Parse most recent chris-kb session from log ───────────────────────────────
STATUS=$(python3 - "$LOG" <<'PYEOF'
import sys, json

log_path = sys.argv[1]
session = {}

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
    print("NO_SESSION")
    sys.exit(0)

def q(v): return f"'{v}'"
print(f"started={q(session.get('started','?'))}")
print(f"total={q(session.get('total','?'))}")
print(f"to_add={q(session.get('to_add','?'))}")
print(f"to_modify={q(session.get('to_modify','?'))}")
print(f"status={q(session.get('status','?'))}")
print(f"indexed={q(session.get('indexed',''))}")
print(f"chunks={q(session.get('chunks',''))}")
print(f"elapsed={q(session.get('elapsed',''))}")
print(f"error={q(session.get('error',''))}")
PYEOF
)

if [ "$STATUS" = "NO_SESSION" ]; then
    echo "No indexing session found for chris-kb"
    exit 0
fi

eval "$STATUS"

echo "Started:  $started"
[ -n "${total:-}" ] && echo "Plan:     $total files ($to_add to add, $to_modify to modify)"

# ── COMPLETE ──────────────────────────────────────────────────────────────────
if [ "$status" = "complete" ]; then
    echo "Status:   ✅ COMPLETE"
    echo "Indexed:  $indexed files → $chunks chunks in $elapsed"
    rm -f "$WAL_PREV"
    osascript -e 'display notification "Lumen index complete — semantic search is ready." with title "chris-kb" sound name "Glass"' 2>/dev/null || true
    # Self-unload so launchd doesn't keep firing after completion
    PLIST="$HOME/Library/LaunchAgents/com.chrisanastasiadis.lumen-status.plist"
    [ -f "$PLIST" ] && launchctl unload "$PLIST" 2>/dev/null || true
    exit 0
fi

# ── FAILED (log says so) ──────────────────────────────────────────────────────
if [ "$status" = "failed" ]; then
    echo "Status:   ❌ FAILED — $error"
    echo "Action:   Restarting indexer..."
    pkill -f "lumen-darwin.*index" 2>/dev/null || true
    nohup "$LUMEN_BIN" index "$KB" -m "$LUMEN_MODEL" >> "$KB/lumen-status.log" 2>&1 &
    echo "          Restarted (PID $!)"
    rm -f "$WAL_PREV"
    exit 0
fi

# ── IN PROGRESS — check liveness and WAL growth ───────────────────────────────
PROC=$(pgrep -f "lumen-darwin.*index" || true)
WAL_SIZE=$(find "$HOME/.local/share/lumen" -name "index.db-wal" 2>/dev/null \
    | xargs ls -l 2>/dev/null | awk '{print $5}' | sort -n | tail -1 || echo 0)

# Check if process is alive
if [ -z "$PROC" ]; then
    echo "Status:   ❌ PROCESS DEAD (no lumen-darwin index process found)"
    echo "Action:   Restarting indexer..."
    nohup "$LUMEN_BIN" index "$KB" -m "$LUMEN_MODEL" >> "$KB/lumen-status.log" 2>&1 &
    echo "          Restarted (PID $!)"
    rm -f "$WAL_PREV"
    exit 0
fi

# Check WAL growth (stuck detection — requires 2 consecutive unchanged readings)
# WAL_PREV file format: "<size>:<unchanged_count>"
PREV_WAL=0
PREV_COUNT=0
if [ -f "$WAL_PREV" ]; then
    RAW=$(cat "$WAL_PREV")
    PREV_WAL="${RAW%%:*}"
    PREV_COUNT="${RAW##*:}"
fi

PIDS_DISPLAY=$(echo "$PROC" | tr '\n' ' ' | sed 's/ $//')
echo "Status:   ⏳ IN PROGRESS (PID $PIDS_DISPLAY)"
echo "WAL size: ${WAL_SIZE} bytes (prev: ${PREV_WAL} bytes)"

if [ "${PREV_WAL}" -gt 0 ] && [ "${WAL_SIZE}" -le "${PREV_WAL}" ]; then
    NEW_COUNT=$(( PREV_COUNT + 1 ))
    if [ "${NEW_COUNT}" -ge 3 ]; then
        echo "Action:   ⚠️  WAL unchanged for 3 checks — indexer stuck. Restarting..."
        echo "$PROC" | xargs -r kill 2>/dev/null || true
        sleep 2
        nohup "$LUMEN_BIN" index "$KB" -m "$LUMEN_MODEL" >> "$KB/lumen-status.log" 2>&1 &
        echo "          Restarted (PID $!)"
        rm -f "$WAL_PREV"
    else
        echo "          WAL unchanged (check ${NEW_COUNT}/3) — monitoring..."
        echo "${WAL_SIZE}:${NEW_COUNT}" > "$WAL_PREV"
    fi
else
    echo "          WAL growing ✓ — indexer healthy"
    echo "${WAL_SIZE}:0" > "$WAL_PREV"
fi
