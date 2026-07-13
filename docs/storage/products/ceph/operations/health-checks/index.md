---
tags:
  - ceph
  - operations
description: "Ceph health check routine: cluster status, OSD up/in counts, PG state verification, MON quorum, capacity thresholds, and recovery progress monitoring."
---
# Ceph — Health Checks

<div class="kb-summary">
Ceph health check routine: cluster status, OSD up/in counts, PG state verification, MON quorum, capacity thresholds, and recovery progress monitoring.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
comprehensive_manual_checks: "Comprehensive Manual Checks" {shape: rectangle}
healthwarn_triage: "HEALTH_WARN Triage" {shape: rectangle}
osdspecific_checks: "OSD-Specific Checks" {shape: rectangle}
recovery_monitoring: "Recovery Monitoring" {shape: rectangle}
capacity_thresholds: "Capacity Thresholds" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> comprehensive_manual_checks
comprehensive_manual_checks -> healthwarn_triage
healthwarn_triage -> osdspecific_checks
osdspecific_checks -> recovery_monitoring
recovery_monitoring -> capacity_thresholds
capacity_thresholds -> generate_report
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

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


```text title="Expected output"
=== Ceph Health Check 2024-01-15 ===

[Overall Status]
  [OK]  Cluster health: HEALTH_OK

[OSD Status]
  [OK]  OSDs up: 12/12
  [OK]  OSDs in: 12/12

[PG Status]
  [OK]  No unclean PGs
  [OK]  No inactive PGs

[Capacity]
  [WARN] Total usage: 78% — approaching nearfull

[MON Quorum]
  [OK]  MON quorum: 3 mons

[Recovery Progress]
  [OK]  No recovery in progress

=== Summary: PASS=7 WARN=1 FAIL=0 ===
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `command not found: ceph` | Ensure the Ceph CLI tools are installed and the `ceph` command is in your PATH, or run the script on a Ceph admin node. |
    | `Error: error connecting to the cluster` | Verify your Ceph cluster is running and `/etc/ceph/ceph.conf` exists with correct permissions, or set `CEPH_ARGS` environment variable. |
    | `grep: (standard input) is empty` | Some `ceph` commands may return empty output if the cluster is severely degraded; add error handling with `|| true` to prevent script failure on edge cases. |
## Comprehensive Manual Checks

```bash
# 1. Overall cluster health — always start here
ceph -s
ceph health detail

# 2. OSD status — all should be up and in
ceph osd stat
ceph osd tree | grep -E "down|out"
# Any "down" or "out" entry requires immediate investigation

# 3. PG summary — look for non active+clean states
ceph pg stat
ceph pg dump_stuck | head -20    # show stuck PGs (inactive/unclean/undersized)
ceph pg dump_stuck inactive      # detail on PGs that cannot service I/O
ceph pg dump_stuck unclean       # PGs with incorrect replica count

# 4. MON quorum — all MONs must be in quorum
ceph mon stat
ceph quorum_status --format json | python3 -m json.tool | \
  grep -E "quorum_leader_name|quorum\b"

# 5. Capacity — check per-pool and per-OSD utilisation
ceph df
ceph df detail                              # per-pool usage with quota info
ceph osd df tree | sort -k8 -rn | head -10 # top OSDs by usage %

# 6. Recovery progress (if any)
ceph -s | grep -i recover
watch -n5 "ceph -s | grep -E 'health|pgs|recover'"

# 7. Recent errors in cluster log
ceph log last 20 | grep -iE "error|warn|failed"
```


```text title="Expected output"
cluster:
    id:     a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
    health: HEALTH_OK
    
mon: 3 mons at {mon01=10.0.1.10:6789/0,mon02=10.0.1.11:6789/0,mon03=10.0.1.12:6789/0}
        election epoch 156, quorum 0,1,2 [mon01,mon02,mon03], out of quorum: none
    mgr: mgr01(active, since 8d), standbys: mgr02, mgr03
    mds: cephfs:1 {0=mds01=up:active} 2 up:standby
    osd: 12 osds: 12 up (since 3d), 12 in (since 3d); flags sortbitwise,require_jewel_osds,require_kraken_osds

  pools:   4 pools, 256 pgs
  objects: 2.34M objects, 4.56 TiB
  usage:   6.78 TiB used, 18.22 TiB / 25 TiB avail
  pgs:     256 active+clean

 +++ HEALTH DETAIL +++
HEALTH_OK

 +++ OSD STAT +++
12 osds: 12 up, 12 in

 +++ PG STAT +++
256 pgs: 256 active+clean; 0 B data, 6.78 TiB used, 18.22 TiB / 25 TiB avail

 +++ MON STAT +++
e3: 3 mons at {mon01=10.0.1.10:6789/0,mon02=10.0.1.11:6789/0,mon03=10.0.1.12:6789/0}, election epoch 156, quorum 0,1,2 [mon01,mon02,mon03], out of quorum: none

 +++ CAPACITY (ceph df) +++
CLASS     SIZE       AVAIL      USED       RAW USED   %RAW USED
all       25 TiB     18.22 TiB  6.78 TiB   6.78 TiB       27.12
ssd       25 TiB     18.22 TiB  6.78 TiB   6.78 TiB       27.12

--- Per-Pool Usage ---
POOL                 ID     USED      %USED     MAX AVAIL     OBJECTS
rbd-pool             1      2.34 TiB   9.36     18.22 TiB     1.2M
cephfs_data          2      1.89 TiB   7.56     18.22 TiB     890K
cephfs_metadata      3      45 GiB    0.18     18.22 TiB     234K
rgw.buckets.data     4      2.10 TiB   8.40     18.22 TiB     567K

--- Top 10 OSDs by Usage ---
ID  CLASS
```
## HEALTH_WARN Triage

| Warning Code | Cause | Remediation |
|---|---|---|
| `OSD_NEARFULL` | OSD disk > 85% used | Add OSDs; or `ceph osd reweight-by-utilization` |
| `OSD_FULL` | OSD disk > 95% used | Stop writes, add OSDs immediately |
| `CLOCK_SKEW_DETECTED` | NTP drift > 0.05 s between hosts | `chronyc makestep` on offending host; verify with `ceph time-sync-status` |
| `TOO_FEW_PGS` / `TOO_MANY_PGS` | Pool PG count not optimised | `ceph osd pool set <pool> pg_autoscale_mode on` |
| `LARGE_OMAP_OBJECTS` | RGW/RBD index objects oversized | Run `radosgw-admin bucket check` and compact with `radosgw-admin gc process` |
| `MON_DISK_LOW` | MON host disk < 30% free | Expand disk or clean old logs under `/var/lib/ceph/mon/` |
| `POOL_NO_REDUNDANCY` | Pool replicated with size=1 | `ceph osd pool set <pool> size 3` |
| `SLOW_OPS` | OSD or MON slow request latency | Check OSD disk health; see OSD-specific checks below |
| `PG_NOT_SCRUBBED` | PG has not been scrubbed in >2 weeks | `ceph osd pool set <pool> noscrub false` then trigger manually |
| `AUTH_INSECURE_GLOBAL_ID_RECLAIM` | Clients using old auth protocol | Upgrade clients; then `ceph config set mon auth_allow_insecure_global_id_reclaim false` |

## OSD-Specific Checks

```bash
# Check slow ops — OSD latency issues
# Sort by commit latency (column 3); highest values = slowest OSDs
ceph osd perf | sort -k3 -rn | head -10

# Dump in-flight ops on a specific OSD (useful when SLOW_OPS warning is active)
ceph daemon osd.<id> dump_ops_in_flight
# Look for ops with age > 30 s; indicates slow disk or network

# Check OSD configuration at runtime
ceph daemon osd.<id> config show | grep -E "osd_op_timeout|osd_disk_threads"

# Check OSD disk device health (if smartmontools installed)
ceph device get-health-metrics <device-id>
ceph device ls    # list device IDs known to the cluster

# Mark an OSD out manually before replacing it
ceph osd out osd.<id>
# Wait for rebalance to complete, then:
ceph osd down osd.<id>
ceph osd purge osd.<id> --yes-i-really-mean-it
```


```text title="Expected output"
osd  commit_latency  apply_latency  commit_latency_ns  apply_latency_ns
       5        0.045821       0.031245          45821000         31245000
       2        0.038912       0.027654          38912000         27654000
       8        0.032156       0.024891          32156000         24891000
       1        0.028743       0.021567          28743000         21567000
       7        0.019234       0.015432          19234000         15432000
       4        0.015678       0.012345          15678000         12345000
       3        0.012456       0.009876          12456000          9876000
       6        0.008932       0.007123           8932000          7123000

{
  "ops": [
    {
      "description": "osd_op(client.12345.0:1 rbd_data.1a2b3c4d5e6f7g8h9i0j_0000000000000001 [write 0~4194304] snapc 0=[] ack+commit e12345:1234 0.000000)",
      "initiated_at": "2024-01-15T14:32:18.456789+0000",
      "age": 2.345,
      "type": "write"
    }
  ]
}

osd_op_timeout = 30
osd_disk_threads = 4

Health metrics for device nvme-SAMSUNG_PM1735_S6XNNS0R700000_1:
  life_expectancy_min: 100
  predicted_life_expectancy_min: 100
  wear_level: 5

DEVICE                                                                DAEMONS  SIZE
nvme-SAMSUNG_PM1735_S6XNNS0R700000_1                                 osd.5    1.7T
nvme-SAMSUNG_PM1735_S6XNNS0R700000_2                                 osd.2    1.7T
sda                                                                   osd.8    2.0T
...

osd.5 marked out.
osd.5 marked down.
purged osd.5
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error ENOENT: osd.<id> does not exist` | Verify the OSD ID exists with `ceph osd tree` before running daemon commands. |
    | `Error: unable to get device health metrics: (22) Invalid argument` | Ensure smartmontools is installed on the OSD host and the device ID matches output from `ceph device ls`. |
    | `Error EBUSY: osd.<id> is still in use` | Wait for the rebalance to fully complete after `ceph osd out` using `ceph -w` before attempting `ceph osd purge`. |
## Recovery Monitoring

```bash
# Live recovery progress — updates every 5 s
watch -n5 "ceph -s | grep -E 'health|pgs|recover|backfill'"

# Detailed stuck PG information
ceph pg dump_stuck degraded
ceph pg dump_stuck unclean
ceph pg dump_stuck inactive

# Force recovery priority (speeds up recovery at cost of client I/O)
ceph osd set nobackfill        # pause backfill, keep recovery
ceph osd recovery_priority 10  # increase (default 5)

# Throttle recovery if impacting client I/O
ceph tell osd.* injectargs '--osd-max-backfills 1'
ceph tell osd.* injectargs '--osd-recovery-max-active 1'

# Watch bytes remaining
watch -n10 "ceph -s | grep -E 'misplaced|degraded|recovering'"
```


```text title="Expected output"
Every 5.0s: ceph -s | grep -E 'health|pgs|recover|backfill'                                    Mon Dec 18 14:32:47 2023

    health: HEALTH_WARN 1 pg degraded; 1 pg stuck degraded
    pgs:     1 active+degraded
    recovery io 12 MB/s, 847 GB/s avg, 2.3 GB remaining
    backfill io 0 B/s, 0 B/s avg

PG_STUCK DEGRADED
PG             STATE           UP      ACTING  OBJECTS  BYTES
1.a2           active+degraded [0,2]   [0,2]   4521     18 GB

PG_STUCK UNCLEAN
(no unclean PGs)

PG_STUCK INACTIVE
(no inactive PGs)

(no output — command completes silently)
(no output — command completes silently)
osd.0: injectargs: osd-max-backfills = '1'
osd.1: injectargs: osd-max-backfills = '1'
osd.2: injectargs: osd-max-backfills = '1'

Every 10.0s: ceph -s | grep -E 'misplaced|degraded|recovering'                                 Mon Dec 18 14:33:02 2023

    1 pg degraded
    847 GB/s avg, 1.9 GB remaining
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error ENOENT: pg dump_stuck: unknown command` | Verify Ceph version supports `pg dump_stuck` (added in Luminous); use `ceph pg stat` as fallback on older versions. |
    | `Error: HEALTH_ERR: 1 pg stuck degraded; recovery blocked` | Check for full OSDs with `ceph df` and delete non-essential data, or add capacity before recovery can proceed. |
    | `Error: osd.X: injectargs: unknown option 'osd-max-backfills'` | Confirm the OSD daemon version matches your Ceph cluster version, as option names vary between releases. |
## Capacity Thresholds

| Threshold | Default % | Flag Name | Effect |
|---|---|---|---|
| Nearfull | 85% | `osd_nearfull_ratio` | `HEALTH_WARN OSD_NEARFULL`; writes continue |
| Backfillfull | 90% | `osd_backfillfull_ratio` | New backfill operations blocked to this OSD |
| Full | 95% | `osd_full_ratio` | `HEALTH_ERR OSD_FULL`; writes to this OSD stopped |

```bash
# Check current threshold settings
ceph osd dump | grep -E "nearfull|full_ratio|backfillfull"

# Adjust nearfull threshold (example: lower to 80% for earlier warning)
ceph osd set-nearfull-ratio 0.80
ceph osd set-full-ratio 0.90
ceph osd set-backfillfull-ratio 0.85

# View per-OSD utilisation sorted by % used
ceph osd df | sort -k7 -rn | head -20
# Column 7 = % used; top entries are the fullest OSDs
```


```text title="Expected output"
nearfull_ratio 0.85
full_ratio 0.95
backfillfill_ratio 0.90
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
ID  CLASS WEIGHT  REWEIGHT SIZE    RAW USE %USE  %AVAIL PG_NUM STATUS
 0   ssd  1.00000  1.00000 1099.5G 879.6G 80.0  20.0   256   up
 1   ssd  1.00000  1.00000 1099.5G 912.3G 82.9  17.1   256   up
 2   ssd  1.00000  1.00000 1099.5G 845.2G 76.8  23.2   256   up
 3   hdd  3.00000  1.00000 3298.6G 2847.1G 86.3  13.7   512   up
 4   hdd  3.00000  1.00000 3298.6G 2756.4G 83.5  16.5   512   up
 5   hdd  3.00000  1.00000 3298.6G 2934.8G 89.0  11.0   512   up
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error EACCES: insufficient capabilities to set osd options` | Run the command with appropriate admin privileges or ensure your keyring has `osd` capability. |
    | `Error: invalid value '0.80': must be between 0.0 and 1.0` | Use decimal ratios between 0 and 1 (e.g., 0.80 for 80%), not percentages. |
## Manual Spot Checks

```bash
# Cluster I/O rates — real-time read/write throughput
ceph -s | grep "client:"

# Slow OSD requests (> 30 s default threshold)
ceph health detail | grep -i slow

# Clock skew check
ceph time-sync-status

# Scrub progress (background data integrity check)
ceph pg dump | grep -c scrubbing
ceph osd scrub osd.5    # trigger scrub on specific OSD
ceph osd deep-scrub osd.5   # trigger deep scrub (checksums)

# Backfill/recovery progress
ceph -s | grep -E "degraded|recovering|backfilling"
ceph pg dump_stuck degraded   # show degraded PG details
```


```text title="Expected output"
client: 512 MiB/s rd, 256 MiB/s wr, 1.2k op/s
HEALTH_WARN Slow OSD requests 12
  OSD_SLOW_PING_TIME_FRONT Host osd.3 is slow to respond on front network
  OSD_SLOW_PING_TIME_BACK Host osd.7 is slow to respond on back network
osd.0: SYNCHRONIZED, age 47s, last updated 2024-01-15T09:23:15.847392+00:00
osd.1: SYNCHRONIZED, age 48s, last updated 2024-01-15T09:23:14.921847+00:00
osd.2: SYNCHRONIZED, age 46s, last updated 2024-01-15T09:23:16.102561+00:00
12
instructing osd.5 to scrub
instructing osd.5 to deep-scrub
degraded+peering, 24 pg degraded, 18 pg recovering
PG_STAT OBJECTS MISSING_ON_PRIMARY DEGRADED MISPLACED UNDERSIZE PEERING STATE
1.a4        512         0           8         0         0 [3,7,2]p8 degraded+peering
1.b2        768         2          16         4         0 [5,1,4]p5 degraded+peering
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error ENOENT: error calling ceph_mon_command` | Ensure the Ceph cluster is running and the admin keyring is properly configured in `/etc/ceph/ceph.client.admin.keyring`. |
    | `HEALTH_ERR: [WRN] SLOW_OSD_REQUESTS` | Investigate slow OSDs with `ceph osd perf` and check network latency, disk I/O, or CPU contention on affected nodes. |
---

## See also

- [Ceph — Common Issues](../../troubleshooting/common-issues/)
- [Ceph — Procedures](../procedures/)
- [Ceph — CLI Reference](../cli-reference/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
