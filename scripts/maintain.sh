#!/usr/bin/env bash
# KB maintenance — run from anywhere, safe to run anytime.
# Steps: generate missing SVGs → audit → commit+push if changed.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓${NC} $*"; }
info() { echo -e "${YELLOW}→${NC} $*"; }
fail() { echo -e "${RED}❌${NC} $*"; exit 1; }

echo "=== KB Maintenance $(date '+%Y-%m-%d %H:%M') ==="

# ── 1. Generate missing content SVGs ─────────────────────────────────────────
PENDING=$(python3 scripts/generate_svgs_content.py --dry-run 2>&1 | grep -oE '[0-9]+ SVGs' | grep -oE '[0-9]+' || echo 0)
if [ "${PENDING:-0}" -gt 0 ]; then
    info "Generating $PENDING missing content SVGs..."
    python3 scripts/generate_svgs_content.py
    ok "SVGs generated"
else
    ok "SVGs up to date"
fi

# ── 2. Site audit ─────────────────────────────────────────────────────────────
info "Running site audit..."
AUDIT_OUT=$(python3 scripts/site_audit.py 2>&1)
SUMMARY=$(echo "$AUDIT_OUT" | grep "SUMMARY:")
echo "  $SUMMARY"
if ! echo "$SUMMARY" | grep -q "37/37"; then
    echo "$AUDIT_OUT" | grep -E "❌|⚠️"
    fail "Audit has failures — fix before pushing"
fi
ok "Audit clean"

# ── 3. Incremental semantic search re-index ──────────────────────────────────
if [ -d ".kb-search" ] && command -v python3 &>/dev/null; then
    info "Re-indexing changed pages for semantic search..."
    python3 scripts/kb_embed.py && ok "Search index updated" || echo "  ⚠️  Search index skipped (check OPENAI_API_KEY)"
fi

# ── 4. Commit + push if anything changed ─────────────────────────────────────
CHANGES=$(git status --short | wc -l | tr -d ' ')
if [ "${CHANGES}" -gt 0 ]; then
    info "$CHANGES file(s) changed — committing..."
    git add -A
    DATE=$(date '+%Y-%m-%d')
    git commit -m "chore: KB maintenance ${DATE} — SVGs, admin pages

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    git push
    ok "Pushed to GitHub"
else
    ok "Nothing to commit"
fi

echo "=== Done ==="
