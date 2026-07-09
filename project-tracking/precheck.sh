#!/usr/bin/env bash
# Environment health precheck, run before each daily cert-kb invocation.
# Exit 0 = safe to proceed. Exit 1 = do not run today, something's wrong.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

fail() { echo "PRECHECK FAIL: $1"; exit 1; }

# 1. Git must be clean -- a dirty tree means a previous run crashed mid-way
#    and left uncommitted state; don't pile more work on top of that.
if [ -n "$(git status --porcelain)" ]; then
    fail "working tree is not clean (leftover state from a previous run?)"
fi

# 2. Must be able to reach GitHub (push will fail otherwise, and we don't
#    want to do an hour of research work that can't be saved).
if ! curl -s -o /dev/null -m 10 https://github.com; then
    fail "cannot reach github.com"
fi

# 3. Queue file must exist and have at least one unchecked Phase A item.
if [ ! -f project-tracking/cert_kb_queue.md ]; then
    fail "cert_kb_queue.md is missing"
fi
REMAINING=$(grep -cE '^- \[ \] ' project-tracking/cert_kb_queue.md)
if [ "$REMAINING" -eq 0 ]; then
    fail "no unchecked Phase A items remain -- Phase A is complete, needs a human decision on Phase B, not another automated run"
fi

echo "PRECHECK OK: $REMAINING items remaining, tree clean, network reachable"
exit 0
