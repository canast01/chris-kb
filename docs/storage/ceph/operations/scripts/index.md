---
tags:
  - ceph
  - operations
---
# Ceph — Scripts

<div class="kb-summary">
Operational scripts for Ceph: daily health check, OSD replacement workflow, capacity report, cluster health snapshot, OSD utilization report, and RBD snapshot rotation.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

S: "S" {shape: rectangle}
HS: "ceph-health-check.sh · daily cluster health" {shape: rectangle}
OR: "osd-replace.sh · safe OSD replacement" {shape: rectangle}
CR: "capacity-report.sh · pool usage report" {shape: rectangle}
SS: "ceph-health-snapshot.sh · full state capture" {shape: rectangle}
UR: "osd-utilization-report.sh · OSD over-threshold check" {shape: rectangle}
RS: "rbd-snapshot-rotate.sh · daily snap + 7-day retention" {shape: rectangle}
O1: "exit 0 = HEALTH_OK · exit 1 = degraded" {shape: rectangle}
O2: "exit 0 = all within bounds · exit 1 = OSD over threshold" {shape: rectangle}
O3: "creates daily snap · removes snaps older than 7 days" {shape: rectangle}
O4: "/tmp/ceph-snapshot-DATE.txt · full cluster state dump" {shape: rectangle}

S -> HS
S -> OR
S -> CR
S -> SS
S -> UR
S -> RS
HS -> O1
UR -> O2
RS -> O3
SS -> O4
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


```text title="Expected output"
=== Ceph Health Check 2024-01-15-1447 ===
  [OK]   Overall: HEALTH_OK
  [OK]   OSDs up: 12/12
  [OK]   OSDs in: 12/12
  [OK]   PGs: no unclean
  [OK]   PGs: no inactive
  [WARN] Capacity: 78% warning
  [OK]   MON quorum: 3 mons

=== PASS=6  WARN=1  FAIL=0 ===
```

!!! warning "Common errors"
    **`command not found: ceph`** — Ensure Ceph CLI tools are installed and the ceph-common package is available on the monitoring host.
    **`Error initializing cluster client: ('error connecting to the cluster', -2)`** — Verify the Ceph cluster is running, the monitor nodes are reachable, and /etc/ceph/ceph.conf is properly configured.
    **`grep: invalid option -- 'P'`** — Replace `grep -oP` with `grep -oE` if using a system without PCRE support in grep (e.g., macOS or older Linux distributions).
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


```text title="Expected output"
Replacing OSD 3 on ceph-node-02 device /dev/sdd
[1] Marking OSD out
marked out osd.3
[2] Waiting for PGs to recover...
  Still recovering — waiting 30s...
  Still recovering — waiting 30s...
  Recovery complete.
[3] Removing daemon
Removed osd.3
[4] Purging OSD from cluster
purged osd.3
[5] (Replace physical disk now — press Enter when done)

[6] Adding new OSD
Created osd(s) 3 on host ceph-node-02
[7] Verifying new OSD is up+in
 3   hdd   10.0  1.00000  10.0G  9.8G  200M  1 up
Done. Monitor: ceph -s
```

!!! warning "Common errors"
    **`Error EINVAL: invalid osd id 3`** — Verify the OSD ID exists with `ceph osd ls` before running the script.
    **`Error: No orchestrator backend configured`** — Ensure Ceph Orchestrator (cephadm) is deployed with `ceph orch status`.
    **`Error: device /dev/sdd is already in use`** — Wipe the disk with `ceph-volume lvm zap /dev/sdd --destroy` before re-adding the OSD.
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


```text title="Expected output"
=== Ceph Capacity Report 2024-01-15 ===

[Cluster Summary]
GLOBAL:
    SIZE       AVAIL      RAW USED     %RAW USED
    450 GiB    312 GiB     138 GiB         30.67
POOLS:
    NAME                 ID     USED       %USED     MAX AVAIL     OBJECTS
    rbd                  1      45 GiB     10.00      156 GiB      11523
    cephfs_data          2      67 GiB     14.89      156 GiB      234891
    cephfs_metadata      3      2.1 GiB    0.47       156 GiB      1847392

[Pool Detail]
  rbd                            45 GiB /      450 GiB (10.00%)
  cephfs_data                    67 GiB /      450 GiB (14.89%)
  cephfs_metadata                2.1 GiB /     450 GiB (0.47%)

[OSD Utilization]
  OSD 0     156/450  (34.67%)
  OSD 1     142/450  (31.56%)
  OSD 2     138/450  (30.67%)
  OSD 3     151/450  (33.56%)
  OSD 4     145/450  (32.22%)
```

!!! warning "Common errors"
    **`Error: error connecting to the cluster`** — Verify the Ceph cluster is running with `ceph status` and check `/etc/ceph/ceph.conf` connectivity settings.
    **`awk: syntax error in pattern near line 1`** — Ensure the Ceph output format hasn't changed; run `ceph df` manually to verify column alignment matches the awk field references.
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


```text title="Expected output"
=== Ceph Health Snapshot 2024-01-15-1430 ===

--- ceph -s ---
  cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_OK
  services:
    mon: 3 daemons, quorum ceph-mon01,ceph-mon02,ceph-mon03 (age 2d)
    mgr: ceph-mgr01(active, since 8d), standbys: ceph-mgr02
    osd: 12 osds: 12 up (since 2d), 12 in (since 2d)
    rgw: 2 daemons active (ceph-rgw01, ceph-rgw02)
  data:
    pools:   8 pools, 256 pgs
    objects: 1.24M objects, 4.5 TiB
    usage:   9.2 TiB used, 18.8 TiB / 28 TiB avail
    pgs:     256 active+clean

--- ceph health detail ---
HEALTH_OK

--- ceph osd tree ---
ID  CLASS WEIGHT   TYPE NAME          STATUS REWEIGHT PRI-AFF
-1       28.00000 root default
-3       14.00000   host ceph-osd01
 0   ssd  1.75000     osd.0              up  1.00000 1.00000
 1   ssd  1.75000     osd.1              up  1.00000 1.00000
 2   ssd  1.75000     osd.2              up  1.00000 1.00000
 3   ssd  1.75000     osd.3              up  1.00000 1.00000
...

--- ceph df ---
RAW STORAGE USAGE:
    CLASS     SIZE       AVAIL      USED       RAW USED %RAW USED
    ssd       28 TiB     18.8 TiB   9.2 TiB    9.2 TiB     32.86
    TOTAL     28 TiB     18.8 TiB   9.2 TiB    9.2 TiB     32.86

--- ceph pg stat ---
256 pgs: 256 active+clean; 0 B data, 9.2 TiB used, 18.8 TiB / 28 TiB avail

--- ceph osd perf ---
osd.0: commit_latency_ms: 2.341, apply_latency_ms: 3.127
osd.1: commit_latency_ms: 2.156, apply_latency_ms: 2.998
osd.2: commit_latency_ms: 2.489, apply_latency_ms: 3.245
osd.3: commit_latency_ms: 2.203, apply_latency_ms: 3.089
...

Snapshot written to: /tmp/ceph-snapshot-2024-01-15-1430.txt
```

!!! warning "Common errors"
    **`Error: error connecting to the cluster`** — Verify C
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


```text title="Expected output"
=== OSD Utilization Report 2024-01-15 — threshold: 80% ===

  HOST         OSD      USE%     STATUS
  --------------------------------------------------
  ceph-node-03 osd.7     82%  [OVER THRESHOLD]
  ceph-node-01 osd.12    85%  [OVER THRESHOLD]
  ceph-node-02 osd.19    81%  [OVER THRESHOLD]

RESULT: 3 OSD(s) above 80% utilization
```

!!! warning "Common errors"
    **`command not found: ceph`** — Ensure the Ceph CLI tools are installed and the user has access to the Ceph cluster configuration files in /etc/ceph/.
    **`jq: command not found`** — Replace the `python3 -m json.tool` pipeline with `jq -r '.host'` or install python3 if JSON parsing is required.
    **`error: osd.X does not exist`** — Verify the OSD IDs in `ceph osd df` output are valid; if OSDs have been removed, run `ceph osd purge-new` to clean up stale entries.
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


```text title="Expected output"
=== RBD Snapshot Rotate: backups/vm-disk-01 ===
Creating snapshot: @daily-2024-01-15
  Created: backups/vm-disk-01@daily-2024-01-15
Checking for snapshots older than 7 days (before 2024-01-08)...
  Removing: backups/vm-disk-01@daily-2024-01-07
  Removing: backups/vm-disk-01@daily-2024-01-06
Done. Current snapshots:
SNAPID                                 NAME                 SIZE   PROTECTED TIMESTAMP
     4 daily-2024-01-15                 2048 MB        false      Mon Jan 15 09:42:31 2024
     3 daily-2024-01-14                 2048 MB        false      Sun Jan 14 09:41:22 2024
     2 daily-2024-01-13                 2048 MB        false      Sat Jan 13 09:40:15 2024
     1 daily-2024-01-12                 2048 MB        false      Fri Jan 12 09:39:08 2024
```

!!! warning "Common errors"
    **`error: image not found`** — Verify the pool and image name exist with `rbd ls <pool>` and check for typos.
    **`error: snapshot already exists`** — The script ran twice on the same day; either wait until tomorrow or manually remove the duplicate snapshot with `rbd snap rm`.
    **`date: invalid date 'now'`** — Use GNU date syntax (`date -d`) on Linux or BSD date syntax (`date -v`) on macOS; the script attempts both but may fail if neither is available.
---

## See also

- [Ceph — CLI Reference](../cli-reference/)
- [Ceph — Procedures](../procedures/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
