# Ceph — Scripts

```text
┌─────────────────────────────────────── Ceph — Scripts Overview ───────────────────────────────────────┐
│                                                                                                       │
│  Script Categories                                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐                │
│  │  Health Check           │  │  OSD Replacement        │  │  Reporting              │                │
│  │  ceph-health-check.sh   │  │  osd-replace.sh         │  │  capacity-report.sh     │                │
│  │  HEALTH_OK / WARN / ERR │  │  safe sequence: out →   │  │  per-pool usage         │                │
│  │  OSD state, PG status   │  │  wait heal → purge →    │  │  PG distribution table  │                │
│  │  capacity, slow ops     │  │  create, verify done    │  │  latency per OSD        │                │
│  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘                │
│                                                                                                       │
│  Script Usage Patterns                                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Health check: run daily via cron on a monitor node; exit 0 = HEALTH_OK, exit 1 = degraded            │
│  OSD replacement: interactive; prompts at each step; confirms data migration complete before swap     │
│  Capacity report: tabular output (pool, used, available, %full); alert if > 80% threshold             │
│  PG summary: counts PGs per state (active+clean, degraded, backfilling, inactive); flags issues       │
│                                                                                                       │
│  Operational Conventions                                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  All scripts require Ceph admin keyring (/etc/ceph/ceph.client.admin.keyring) on execution host       │
│  Run from a monitor node or any host with ceph.conf pointing at the correct cluster                   │
│  Scripts use set -euo pipefail for safe error propagation; non-zero exit = check required             │
│  Output format: [OK] / [WARN] / [FAIL] prefixed lines + summary count at bottom                       │
│                                                                                                       │
│  GLOSSARY                                                                                             │
│  ceph -s      — cluster status: health, OSD count, PG summary, I/O rate, capacity                     │
│  ceph osd tree— visual tree of hosts, buckets, OSDs, and their weights                                │
│  ceph df      — per-pool capacity: stored, objects, used, available, quota                            │
│  ceph pg stat — aggregate PG count by state (active+clean, degraded, etc.)                            │
│  PASS/WARN/FAIL— script exit convention: all PASS = 0, any WARN = 1, any FAIL = 2                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-summary">
Operational scripts for Ceph: daily health check, OSD replacement workflow, capacity report, and PG status summary.
</div>

## ceph-health-check.sh

```bash
#!/bin/bash
# Ceph Cluster Health Check — outputs summary with pass/warn/fail counts
set -euo pipefail

PASS=0; WARN=0; FAIL=0
ok()   { echo "  [OK]   $1"; ((PASS++)); }
warn() { echo "  [WARN] $1"; ((WARN++)); }
fail() { echo "  [FAIL] $1"; ((FAIL++)); }

echo "=== Ceph Health Check $(date +%F-%H%M) ==="

# Overall health
HEALTH=$(ceph health 2>/dev/null)
if echo "$HEALTH" | grep -q "^HEALTH_OK"; then
    ok "Overall: HEALTH_OK"
elif echo "$HEALTH" | grep -q "^HEALTH_WARN"; then
    warn "Overall: HEALTH_WARN — $(ceph health detail 2>/dev/null | head -2)"
else
    fail "Overall: $(echo $HEALTH)"
fi

# OSD counts
read -r TOTAL UP IN <<< $(ceph osd stat 2>/dev/null | awk '{print $1; gsub(/[^0-9]/,"",$3); print $3; gsub(/[^0-9]/,"",$6); print $6}' | tr '\n' ' ')
[[ "$UP" == "$TOTAL" ]] && ok "OSDs up: $UP/$TOTAL" || fail "OSDs: only $UP/$TOTAL up"
[[ "$IN" == "$TOTAL" ]] && ok "OSDs in: $IN/$TOTAL" || warn "OSDs: only $IN/$TOTAL in"

# PG health
UNCLEAN=$(ceph pg stat 2>/dev/null | grep -oP '\d+(?= unclean)' || echo "0")
INACTIVE=$(ceph pg stat 2>/dev/null | grep -oP '\d+(?= inactive)' || echo "0")
[[ "$UNCLEAN" -eq 0 ]] && ok "PGs: no unclean" || warn "PGs: $UNCLEAN unclean"
[[ "$INACTIVE" -eq 0 ]] && ok "PGs: no inactive" || fail "PGs: $INACTIVE inactive — I/O blocked"

# Capacity
TOTAL_USAGE=$(ceph df 2>/dev/null | awk '/TOTAL/{print $(NF)}' | tr -d '%')
if   [[ "$TOTAL_USAGE" -ge 85 ]]; then fail "Capacity: ${TOTAL_USAGE}% CRITICAL nearfull"
elif [[ "$TOTAL_USAGE" -ge 75 ]]; then warn "Capacity: ${TOTAL_USAGE}% warning"
else                                    ok   "Capacity: ${TOTAL_USAGE}%"
fi

# MON quorum
MONS=$(ceph mon stat 2>/dev/null | grep -oP '\d+ mons')
ok "MON quorum: $MONS"

echo ""
echo "=== PASS=$PASS  WARN=$WARN  FAIL=$FAIL ==="
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
```

## osd-replace.sh

```bash
#!/bin/bash
# Safe OSD replacement workflow
# Usage: ./osd-replace.sh <osd-id> <host> <device>
# Example: ./osd-replace.sh 5 ceph-node2 /dev/sdc

OSD_ID="${1:?Usage: $0 <osd-id> <host> <device>}"
HOST="${2:?}"
DEVICE="${3:?}"

echo "Replacing OSD $OSD_ID on $HOST device $DEVICE"

echo "[1] Marking OSD out"
ceph osd out "osd.$OSD_ID"

echo "[2] Waiting for PGs to recover..."
while ceph -s | grep -qE "degraded|recovering|backfilling"; do
    echo "  Still recovering — waiting 30s..."
    sleep 30
done
echo "  Recovery complete."

echo "[3] Removing daemon"
ceph orch daemon rm "osd.$OSD_ID" --force

echo "[4] Purging OSD from cluster"
ceph osd crush rm "osd.$OSD_ID"
ceph auth del "osd.$OSD_ID"
ceph osd rm "$OSD_ID"

echo "[5] (Replace physical disk now — press Enter when done)"
read -r

echo "[6] Adding new OSD"
ceph orch daemon add osd "$HOST:$DEVICE"

echo "[7] Verifying new OSD is up+in"
sleep 30
ceph osd tree | grep "$HOST"
echo "Done. Monitor: ceph -s"
```

## capacity-report.sh

```bash
#!/bin/bash
# Ceph Capacity Report — per-pool usage

echo "=== Ceph Capacity Report $(date +%F) ==="
echo ""
echo "[Cluster Summary]"
ceph df

echo ""
echo "[Pool Detail]"
ceph df detail | awk 'NR>2 {printf "  %-30s %8s / %-8s (%s)\n", $1, $2, $4, $6}'

echo ""
echo "[OSD Utilization]"
ceph osd df | awk 'NR>1 && NF>0 {printf "  OSD %-3s  %5s/%5s  (%s%%)\n", $1, $7, $8, $9}' | head -20
```
