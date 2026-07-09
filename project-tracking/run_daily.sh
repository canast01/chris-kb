#!/usr/bin/env bash
# Full daily pipeline: precheck -> run -> verify -> notify on failure.
# Invoked by the launchd job; also safe to run manually.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

DATE=$(date +%Y-%m-%d)
LOG=project-tracking/daily_run.log
mkdir -p project-tracking/runs

echo "=== $DATE run starting ===" >> "$LOG"

if ! ./project-tracking/precheck.sh >> "$LOG" 2>&1; then
    echo "$DATE: precheck failed, skipping today (see log above)" >> "$LOG"
    claude -p "Call the PushNotification tool now with this exact message: 'chris-kb daily job: precheck failed on $DATE, see project-tracking/daily_run.log'" \
        --dangerously-skip-permissions >> "$LOG" 2>&1
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
    claude -p "Call the PushNotification tool now with this exact message: 'chris-kb daily job: $DATE run failed verification, check project-tracking/daily_run.log before trusting today'\''s commit'" \
        --dangerously-skip-permissions >> "$LOG" 2>&1
fi

echo "=== $DATE run finished ===" >> "$LOG"
