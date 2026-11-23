#!/usr/bin/env bash
# Full daily pipeline: precheck -> run -> verify -> notify on failure.
# Invoked by the launchd job; also safe to run manually.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

# launchd runs with a minimal PATH (/usr/bin:/bin:...) that lacks ~/.local/bin,
# so `claude` was "command not found" and every failure alert was silently lost
# from 2026-07-17 to 2026-11-22. Set PATH explicitly.
export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

# Alert that cannot be silently lost: try Claude's PushNotification, and if
# that fails for any reason, fall back to a native macOS notification.
notify() {
    local msg="$1"
    if ! claude -p "Call the PushNotification tool now with this exact message: '$msg'" \
            --dangerously-skip-permissions >> "$LOG" 2>&1; then
        echo "notify: claude alert failed, using osascript fallback" >> "$LOG"
        osascript -e "display notification \"$msg\" with title \"chris-kb daily job\"" >> "$LOG" 2>&1
    fi
}

DATE=$(date +%Y-%m-%d)
LOG=project-tracking/daily_run.log
mkdir -p project-tracking/runs

echo "=== $DATE run starting ===" >> "$LOG"

if ! ./project-tracking/precheck.sh >> "$LOG" 2>&1; then
    echo "$DATE: precheck failed, skipping today (see log above)" >> "$LOG"
    notify "chris-kb daily job: precheck failed on $DATE, see project-tracking/daily_run.log"
    exit 1
fi

BEFORE_SHA=$(git rev-parse HEAD)

claude -p "$(cat project-tracking/daily_prompt.txt)" \
    --dangerously-skip-permissions --output-format json \
    > "project-tracking/runs/$DATE.json" 2>> "$LOG"

if python3 project-tracking/verify_daily_run.py "project-tracking/runs/$DATE.json" "$BEFORE_SHA" >> "$LOG" 2>&1; then
    echo "$DATE: verified OK" >> "$LOG"
else
    echo "$DATE: VERIFICATION FAILED" >> "$LOG"
    notify "chris-kb daily job: $DATE run failed verification, check project-tracking/daily_run.log before trusting the commit"
fi

echo "=== $DATE run finished ===" >> "$LOG"
