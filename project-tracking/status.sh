#!/usr/bin/env bash
# Quick morning check on the Certification-Grade KB daily automation.
cd "$(dirname "$0")/.." || exit 1

echo "=== Certification-Grade KB — daily automation status ==="
echo
echo "Job installed: $(launchctl list | grep -q chriskb && echo 'yes, scheduled' || echo 'NOT LOADED')"
echo
DONE=$(grep -c '\[x\]' project-tracking/cert_kb_queue.md)
TOTAL=$(grep -cE '\[x\]|\[ \]' project-tracking/cert_kb_queue.md)
echo "Progress: $DONE / $TOTAL Phase A sections done"
echo
echo "--- Last run (tail of daily_run.log) ---"
tail -30 project-tracking/daily_run.log 2>/dev/null || echo "(no runs yet)"
echo
echo "--- Most recently checked-off item ---"
grep '\[x\]' project-tracking/cert_kb_queue.md | tail -1
