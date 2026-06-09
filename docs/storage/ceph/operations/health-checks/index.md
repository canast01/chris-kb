# Ceph — Health Checks

<div class="kb-summary">
Ceph health check routine: cluster status, OSD up/in counts, PG state verification, MON quorum, capacity thresholds, and recovery progress monitoring.
</div>

```text
┌──────────────────────────────────────── Ceph — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Health baseline: HEALTH_OK + all OSDs up+in + all PGs active+clean + MON quorum             │   │
│   │   HEALTH_WARN acceptable if clock skew (fix NTP) or nearfull (add capacity)                   │   │
│   │   HEALTH_ERR: investigate immediately; OSDs down or PGs inactive blocks client I/O            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Run This Routine

```bash
#!/bin/bash
# Ceph Daily Health Check
# Usage: ./ceph-health-check.sh

PASS=0; FAIL=0; WARN=0

check_ok() { echo "  [OK]  $1"; ((PASS++)); }
check_warn() { echo "  [WARN] $1"; ((WARN++)); }
check_fail() { echo "  [FAIL] $1"; ((FAIL++)); }

echo "=== Ceph Health Check $(date +%F) ==="

echo ""
echo "[Overall Status]"
HEALTH=$(ceph health)
if echo "$HEALTH" | grep -q "^HEALTH_OK"; then
    check_ok "Cluster health: HEALTH_OK"
elif echo "$HEALTH" | grep -q "^HEALTH_WARN"; then
    check_warn "Cluster health: HEALTH_WARN → $(ceph health detail | head -3)"
else
    check_fail "Cluster health: $(echo $HEALTH | head -1)"
fi

echo ""
echo "[OSD Status]"
TOTAL=$(ceph osd stat | awk '{print $1}')
UP=$(ceph osd stat | grep -oP '\d+ up' | awk '{print $1}')
IN=$(ceph osd stat | grep -oP '\d+ in' | awk '{print $1}')
[[ "$UP" == "$TOTAL" ]] && check_ok "OSDs up: $UP/$TOTAL" || check_fail "OSDs not all up: $UP/$TOTAL"
[[ "$IN" == "$TOTAL" ]] && check_ok "OSDs in: $IN/$TOTAL" || check_warn "OSDs not all in: $IN/$TOTAL"

echo ""
echo "[PG Status]"
UNCLEAN=$(ceph pg stat | grep -oP '\d+ unclean')
INACTIVE=$(ceph pg stat | grep -oP '\d+ inactive')
[[ -z "$UNCLEAN" ]] && check_ok "No unclean PGs" || check_warn "PGs unclean: $UNCLEAN"
[[ -z "$INACTIVE" ]] && check_ok "No inactive PGs" || check_fail "PGs inactive: $INACTIVE — I/O may be impacted"

echo ""
echo "[Capacity]"
USAGE=$(ceph df | awk '/TOTAL/{print $NF}' | tr -d '%')
[[ "$USAGE" -lt 75 ]] && check_ok "Total usage: ${USAGE}%" \
  || ([[ "$USAGE" -lt 85 ]] && check_warn "Total usage: ${USAGE}% — approaching nearfull" \
  || check_fail "Total usage: ${USAGE}% — NEARFULL or FULL; writes may stop")

echo ""
echo "[MON Quorum]"
QUORUM=$(ceph mon stat | grep -oP '\d+ mons')
check_ok "MON quorum: $QUORUM"

echo ""
echo "[Recovery Progress]"
RECOVERING=$(ceph -s | grep -c "recovering" || true)
[[ "$RECOVERING" -eq 0 ]] && check_ok "No recovery in progress" \
  || check_warn "Recovery in progress — $(ceph -s | grep recovering)"

echo ""
echo "=== Summary: PASS=$PASS WARN=$WARN FAIL=$FAIL ==="
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
```

## Manual Spot Checks

```bash
# Cluster I/O rates
ceph -s | grep "client:"   # real-time read/write rates

# Slow OSD requests (> 30s default)
ceph health detail | grep -i slow

# Clock skew check
ceph time-sync-status

# Scrub progress (background data integrity check)
ceph pg dump | grep -c scrubbing
ceph osd scrub osd.5   # trigger scrub on specific OSD

# Backfill/recovery progress
ceph -s | grep -E "degraded|recovering|backfilling"
ceph pg dump_stuck degraded  # show degraded PG details
```
