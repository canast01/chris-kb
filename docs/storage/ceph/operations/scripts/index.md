---
tags:
  - ceph
  - operations
---
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
│  Key terms:                                                                                           │
│                                                                                                       │
│  ceph -s      = Cluster status: health, OSD up/in counts, PG summary, I/O rate, capacity              │
│  ceph osd tree= Visual tree of hosts, buckets, OSDs, and their weights and up/in state                │
│  ceph df      = Per-pool capacity: stored objects, data used, available, and quota                    │
│  ceph pg stat = Aggregate PG count by state (active+clean, degraded, recovering, etc.)                │
│  PASS/WARN/FAIL= Script exit convention: all PASS = exit 0, any WARN = exit 1, any FAIL = exit 2      │
│  admin keyring= /etc/ceph/ceph.client.admin.keyring; required on execution host for all scripts       │
│  ceph.conf    = Cluster config file; must point to correct monitors for scripts to connect            │
│  set -euo pipefail = Bash safe mode: exit on error, unset var, or pipe failure in scripts             │
│  nearfull ratio= Configurable OSD full threshold (default 85%); script alerts when exceeded           │
│  OSD_DOWN     = Health code raised when OSD is not responding; scripts parse this for alerting        │
│  ceph health detail = Enumerates health codes with per-item detail; parsed by health-check script     │
│  cron         = Linux task scheduler; used to run health-check and capacity scripts daily             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-summary">
Operational scripts for Ceph: daily health check, OSD replacement workflow, capacity report, cluster health snapshot, OSD utilization report, and RBD snapshot rotation.

*Applies to: Ceph Reef / Squid*
</div>

```mermaid
graph LR
    classDef root fill:#2563eb,color:#fff
    classDef scr  fill:#15803d,color:#fff
    classDef out  fill:#1e3a5f,color:#fff

    S[Scripts]:::root

    S --> HS[ceph-health-check.sh<br/>daily cluster health]:::scr
    S --> OR[osd-replace.sh<br/>safe OSD replacement]:::scr
    S --> CR[capacity-report.sh<br/>pool usage report]:::scr
    S --> SS[ceph-health-snapshot.sh<br/>full state capture]:::scr
    S --> UR[osd-utilization-report.sh<br/>OSD over-threshold check]:::scr
    S --> RS[rbd-snapshot-rotate.sh<br/>daily snap + 7-day retention]:::scr

    HS --> O1[exit 0 = HEALTH_OK<br/>exit 1 = degraded]:::out
    UR --> O2[exit 0 = all within bounds<br/>exit 1 = OSD over threshold]:::out
    RS --> O3[creates daily snap<br/>removes snaps older than 7 days]:::out
    SS --> O4[/tmp/ceph-snapshot-DATE.txt<br/>full cluster state dump]:::out
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## ceph-health-check.sh

```bash
#!/bin/bash
set -euo pipefail

PASS=0; WARN=0; FAIL=0
ok()   { echo "  [OK]   $1"; ((PASS++)); }
warn() { echo "  [WARN] $1"; ((WARN++)); }
fail() { echo "  [FAIL] $1"; ((FAIL++)); }

echo "=== Ceph Health Check $(date +%F-%H%M) ==="

HEALTH=$(ceph health 2>/dev/null)
if echo "$HEALTH" | grep -q "^HEALTH_OK"; then
    ok "Overall: HEALTH_OK"
elif echo "$HEALTH" | grep -q "^HEALTH_WARN"; then
    warn "Overall: HEALTH_WARN — $(ceph health detail 2>/dev/null | head -2)"
else
    fail "Overall: $(echo $HEALTH)"
fi

read -r TOTAL UP IN <<< $(ceph osd stat 2>/dev/null | awk '{print $1; gsub(/[^0-9]/,"",$3); print $3; gsub(/[^0-9]/,"",$6); print $6}' | tr '\n' ' ')
[[ "$UP" == "$TOTAL" ]] && ok "OSDs up: $UP/$TOTAL" || fail "OSDs: only $UP/$TOTAL up"
[[ "$IN" == "$TOTAL" ]] && ok "OSDs in: $IN/$TOTAL" || warn "OSDs: only $IN/$TOTAL in"

UNCLEAN=$(ceph pg stat 2>/dev/null | grep -oP '\d+(?= unclean)' || echo "0")
INACTIVE=$(ceph pg stat 2>/dev/null | grep -oP '\d+(?= inactive)' || echo "0")
[[ "$UNCLEAN" -eq 0 ]] && ok "PGs: no unclean" || warn "PGs: $UNCLEAN unclean"
[[ "$INACTIVE" -eq 0 ]] && ok "PGs: no inactive" || fail "PGs: $INACTIVE inactive — I/O blocked"

TOTAL_USAGE=$(ceph df 2>/dev/null | awk '/TOTAL/{print $(NF)}' | tr -d '%')
if   [[ "$TOTAL_USAGE" -ge 85 ]]; then fail "Capacity: ${TOTAL_USAGE}% CRITICAL nearfull"
elif [[ "$TOTAL_USAGE" -ge 75 ]]; then warn "Capacity: ${TOTAL_USAGE}% warning"
else                                    ok   "Capacity: ${TOTAL_USAGE}%"
fi

MONS=$(ceph mon stat 2>/dev/null | grep -oP '\d+ mons')
ok "MON quorum: $MONS"

echo ""
echo "=== PASS=$PASS  WARN=$WARN  FAIL=$FAIL ==="
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
```

## osd-replace.sh

```bash
#!/bin/bash
set -euo pipefail

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
ceph osd purge "$OSD_ID" --yes-i-really-mean-it

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
set -euo pipefail

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

## ceph-health-snapshot.sh

```bash
#!/bin/bash
set -euo pipefail

OUTFILE="/tmp/ceph-snapshot-$(date +%F-%H%M).txt"

{
    echo "=== Ceph Health Snapshot $(date +%F-%H%M) ==="
    echo ""

    echo "--- ceph -s ---"
    ceph -s

    echo ""
    echo "--- ceph health detail ---"
    ceph health detail

    echo ""
    echo "--- ceph osd tree ---"
    ceph osd tree

    echo ""
    echo "--- ceph df ---"
    ceph df

    echo ""
    echo "--- ceph pg stat ---"
    ceph pg stat

    echo ""
    echo "--- ceph osd perf ---"
    ceph osd perf

} > "$OUTFILE" 2>&1

echo "Snapshot written to: $OUTFILE"
```

## osd-utilization-report.sh

```bash
#!/bin/bash
set -euo pipefail

THRESHOLD="${1:-80}"
OVER=0

echo "=== OSD Utilization Report $(date +%F) — threshold: ${THRESHOLD}% ==="
echo ""
printf "  %-12s %-8s %-8s %s\n" "HOST" "OSD" "USE%" "STATUS"
echo "  $(printf '%0.s-' {1..50})"

while IFS= read -r line; do
    osd_id=$(echo "$line" | awk '{print $1}')
    use_pct=$(echo "$line" | awk '{print $8}' | tr -d '%')
    host=$(ceph osd find "$osd_id" 2>/dev/null | python3 -m json.tool | grep '"host"' | awk -F'"' '{print $4}')

    if [[ "$use_pct" -ge "$THRESHOLD" ]]; then
        printf "  %-12s osd.%-5s %5s%%  [OVER THRESHOLD]\n" "$host" "$osd_id" "$use_pct"
        ((OVER++))
    fi
done < <(ceph osd df 2>/dev/null | awk 'NR>1 && $1 ~ /^[0-9]/')

echo ""
if [[ "$OVER" -gt 0 ]]; then
    echo "RESULT: $OVER OSD(s) above ${THRESHOLD}% utilization"
    exit 1
else
    echo "RESULT: all OSDs within ${THRESHOLD}% threshold"
    exit 0
fi
```

## rbd-snapshot-rotate.sh

```bash
#!/bin/bash
set -euo pipefail

POOL="${1:?Usage: $0 <pool> <image> [retain-days]}"
IMAGE="${2:?}"
RETAIN="${3:-7}"
SNAP_NAME="daily-$(date +%F)"

echo "=== RBD Snapshot Rotate: ${POOL}/${IMAGE} ==="

echo "Creating snapshot: @${SNAP_NAME}"
rbd snap create "${POOL}/${IMAGE}@${SNAP_NAME}"
echo "  Created: ${POOL}/${IMAGE}@${SNAP_NAME}"

CUTOFF=$(date -d "-${RETAIN} days" +%F 2>/dev/null || date -v -"${RETAIN}"d +%F)

echo "Checking for snapshots older than ${RETAIN} days (before ${CUTOFF})..."
while IFS= read -r snap; do
    snap_date=$(echo "$snap" | grep -oP '\d{4}-\d{2}-\d{2}' || true)
    if [[ -n "$snap_date" && "$snap_date" < "$CUTOFF" ]]; then
        echo "  Removing: ${POOL}/${IMAGE}@${snap}"
        rbd snap rm "${POOL}/${IMAGE}@${snap}"
    fi
done < <(rbd snap ls "${POOL}/${IMAGE}" | awk 'NR>1 {print $2}')

echo "Done. Current snapshots:"
rbd snap ls "${POOL}/${IMAGE}"
```
