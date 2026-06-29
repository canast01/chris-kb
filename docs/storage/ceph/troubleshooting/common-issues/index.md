---
tags:
  - ceph
  - troubleshooting
search:
  boost: 1.5
---
# Ceph — Common Issues

<div class="kb-summary">
Troubleshooting guide for frequent Ceph problems: OSD down/out, PG degraded and stuck, slow requests, nearfull/full cluster, clock skew, MON quorum loss, and recovery that won't complete.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

C: "Check OSD log\nsmartctl + journalctl" {shape: rectangle}
D: "Restart OSD or\nreplace disk" {shape: rectangle}
F: "ceph pg dump_stuck\nFind affected OSDs" {shape: rectangle}
G: "Bring OSD back up\nor replace" {shape: rectangle}
A: "Start: ceph -s shows unhealthy" {shape: rectangle}
I: "ceph osd set nofull\nor delete/expand" {shape: rectangle}
K: "SSH to MON hosts\nrestart failed MONs" {shape: rectangle}
M: "ceph osd perf\niostat on OSD host" {shape: rectangle}
N: "Escalate to diagnostics/" {shape: rectangle}

C -> D
F -> G
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
osd_down: "OSD Down" {shape: rectangle}
healtherr_osd_full: "HEALTH_ERR: OSD Full" {shape: rectangle}
slow_ops_high_latency: "Slow Ops / High Latency" {shape: rectangle}
pg_degraded_undersized_stuck: "PG Degraded / Undersized / Stuck" {shape: rectangle}
clock_skew: "Clock Skew" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> osd_down: investigate
symptom -> healtherr_osd_full: investigate
symptom -> slow_ops_high_latency: investigate
symptom -> pg_degraded_undersized_stuck: investigate
symptom -> clock_skew: investigate
diagnostic_flow -> resolution
osd_down -> resolution
healtherr_osd_full -> resolution
slow_ops_high_latency -> resolution
pg_degraded_undersized_stuck -> resolution
clock_skew -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
A: "OSD down / cluster degraded" {shape: rectangle}
B: "PG stuck — active+undersized" {shape: rectangle}
C: "RADOS object not found" {shape: rectangle}
D: "Monitor quorum lost" {shape: rectangle}
E: "Slow requests / high latency" {shape: rectangle}
A1: "A1" {shape: rectangle}
A2: "Replace OSD disk — see OSD Down" {shape: rectangle}
A3: "Restart OSD daemon and check OOM or network issue" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "Bring OSD back up or reweight to 0 — see PG\nDegraded / Undersized / Stuck" {shape: rectangle}
B3: "Run ceph pg repair and check CRUSH map" {shape: rectangle}
C1: "C1" {shape: rectangle}
C2: "Check PG state — may be inactive; resolve OSD\nfirst — see OSD Down" {shape: rectangle}
C3: "Run rados stat on object and check for deletion or\nnaming mismatch" {shape: rectangle}
D1: "D1" {shape: rectangle}
D2: "Restart ceph-mon service — see MON Quorum Lost" {shape: rectangle}
D3: "Check clock skew with ceph time-sync-status — see\nClock Skew" {shape: rectangle}
E1: "E1" {shape: rectangle}
E2: "Check iostat await; disable scrub temporarily —\nsee Slow Ops / High Latency" {shape: rectangle}
E3: "Run iperf3 between nodes; check cluster network path" {shape: rectangle}

S -> A
S -> B
S -> C
S -> D
S -> E
A1 -> A2
A1 -> A3
B1 -> B2
B1 -> B3
C1 -> C2
C1 -> C3
D1 -> D2
D1 -> D3
E1 -> E2
E1 -> E3
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## OSD Down

```bash
# Identify down OSDs
ceph health detail | grep OSD_DOWN
ceph osd tree | grep down

# Check OSD log (most common cause: disk error, kernel issue, or OOM kill)
journalctl -u ceph-osd@5 -n 100 --no-pager
# Or via cephadm:
ceph orch daemon logs osd.5 | tail -100

# Check disk health
smartctl -a /dev/sdb | grep -E "Reallocated|Pending|Offline|Error"

# If disk is healthy but OSD crashed: restart OSD
ceph orch daemon restart osd.5

# If disk has errors: replace the OSD (see Procedures page)

# Check if OSD is timing out due to network
ceph osd perf | grep osd.5   # check commit/apply latency

# Check for OOM kill
dmesg | grep -i oom | tail -20
# If OOM: increase osd_memory_target
ceph config set osd osd_memory_target 6G  # adjust per available RAM
```


```text title="Expected output"
HEALTH_WARN 1 osds down
osd.5                down weight 1.0
   host ceph-node-02
        osd.5            down weight 1.0
Dec 15 14:32:18 ceph-node-02 ceph-osd[8924]: 2024-12-15T14:32:18.456+0000 7f8a2c3d5600 -1 osd.5 0 log_channel(audit) log [WRN] : slow request 30.245s
Dec 15 14:32:45 ceph-node-02 ceph-osd[8924]: 2024-12-15T14:32:45.123+0000 7f8a2c3d5600 -1 osd.5 0 log_channel(default) log [ERR] : EIO: error reading /var/lib/ceph/osd/ceph-5/current
Dec 15 14:33:02 ceph-node-02 ceph-osd[8924]: 2024-12-15T14:33:02.789+0000 7f8a2c3d5600 -1 osd.5 0 log_channel(default) log [ERR] : mark_down_peers: osd.5 down
SMART Health Status: PASSED
Reallocated_Sector_Ct   0x0033   100   100   036    Pre-fail  Never       0
Pending_Sector_Ct       0x0022   100   100   030    Old_age   Never       0
Offline_Uncorrectable   0x0010   100   100   097    Offline   Never       0
Restarting daemon osd.5 on host ceph-node-02
osd.5: commit_latency_ms 45.2 apply_latency_ms 127.8
osd.6: commit_latency_ms 12.1 apply_latency_ms 34.5
[  245.123] Out of memory: Kill process 8924 (ceph-osd) score 612 or sacrifice child
[  245.456] Killed process 8924 (ceph-osd) total-vm:8192456kB, anon-rss:7856320kB, file-rss:0kB, shmem-rss:0kB
```

!!! warning "Common errors"
    **`error: unable to get daemon logs: No such container for osd.5`** — Verify the OSD exists with `ceph osd ls` and use correct daemon name format `osd.N`.
    **`Error: DEVICE FAILED [90%] Reallocated_Sector_Ct`** — Replace the disk immediately following the OSD replacement procedure, as sector reallocation indicates imminent disk failure.
    **`command not found: smartctl`** — Install smartmontools package with `apt install smartmontools` (Debian/Ubuntu) or `yum install smartmontools` (RHEL/CentOS).
## HEALTH_ERR: OSD Full

When the cluster hits the `full ratio` (default 95%), all writes are blocked including replication and recovery.

```bash
# Confirm full state
ceph health detail | grep -E "OSD_FULL|FULL"
ceph osd df | sort -k8 -rn | head -20  # find highest-utilisation OSDs

# Immediate override — allows writes past 100% temporarily (DANGEROUS)
# Only use to free space, then unset immediately
ceph osd set nofull

# Buy time by raising the full threshold
ceph osd set-full-ratio 0.97          # temporary; reset after fix
ceph osd set-nearfull-ratio 0.92

# Find large objects contributing to usage
rados df | sort -k2 -rn | head -20

# Find large RBD images
rbd ls rbd | while read img; do
  SIZE=$(rbd info rbd/$img | grep disk_usage | awk '{print $2}')
  echo "$SIZE $img"
done | sort -h -r | head -20

# Permanent fix options:
# 1. Delete data or expired snapshots
# 2. Add more OSDs (see Procedures)
# 3. Increase pool min_size temporarily only in genuine emergency

# After freeing space: unset override flags
ceph osd unset nofull
ceph osd set-full-ratio 0.95   # reset to default
```


```text title="Expected output"
HEALTH_WARN [WRN] OSD_FULL: 1 osds have reached or exceeded full threshold
    osd.7 is full at 100.5%

HEALTH_WARN [WRN] OSD_NEARFULL: 2 osds are approaching full
    osd.5 is near full at 94.2%
    osd.9 is near full at 91.8%

 id  weight  reweight  size   raw use  %RAW_USE  %USED  %AVAIL
  7   1.00000  1.00000  10.0T   10.1T  100.50   100.50    0.00
  5   1.00000  1.00000  10.0T    9.4T   94.20    94.20    5.80
  9   1.00000  1.00000  10.0T    9.2T   91.80    91.80    8.20
  3   1.00000  1.00000  10.0T    8.7T   87.10    87.10   12.90
  1   1.00000  1.00000  10.0T    7.2T   72.10    72.10   27.90

set nofull
set-full-ratio 0.97
set-nearfull-ratio 0.92

pool name                 KB
rbd                  5242880000
cinder-volumes       3145728000
images               1048576000
...

2684354560 prod-vm-disk-001
1610612736 backup-archive-image
805306368 test-snapshot-v2
536870912 old-export-vol
268435456 temp-workspace
...

unset nofull
set-full-ratio 0.95
```

!!! warning "Common errors"
    **`Error ENOSPC: no space left on device`** — Run `ceph osd set nofull` immediately to allow writes, then delete data or add OSDs urgently.
    **`Error: pool 'rbd' does not exist`** — Replace `rbd` with the correct pool name from `ceph osd pool ls`.
    **`Error EINVAL: invalid full ratio 0.97: must be between 0.0 and 1.0`** — Use decimal notation (0.97) not percentage; ensure the value is less than set-full-ratio.
## Slow Ops / High Latency

```bash
# Symptoms: HEALTH_WARN "X requests are blocked"
ceph health detail | grep SLOW_OPS
ceph osd perf | sort -k3 -rn | head -10  # sort by commit_latency; high value = disk issue

# Check disk I/O on OSD host (await > 50 ms = disk saturated)
iostat -dx 5 3 | grep -E "^sd|Device"

# Test cluster network bandwidth (expect ≥ 10 Gbps on 10 GbE)
iperf3 -c ceph-node2 -t 10 -P 4

# Check BlueStore WAL/DB usage
ceph daemon osd.5 perf dump | grep -E "wal|db|commit"

# Temporarily disable scrubbing if it is contributing to latency
ceph osd set noscrub
ceph osd set nodeep-scrub
# Re-enable after resolving: ceph osd unset noscrub

# Limit recovery I/O to reduce impact on client ops
ceph config set osd osd_max_backfills 1
ceph config set osd osd_recovery_max_active_hdd 2

# Check slow op details (shows which object and which client)
ceph daemon osd.5 dump_ops_in_flight
ceph daemon osd.5 dump_historic_ops
```


```text title="Expected output"
SLOW_OPS 12 slow ops, oldest one blocked for 157 sec, osd.5 has slow ops
     osd.5       3.45 GiB / 1.82 TiB   0.19  [SLOW_OPS]
     osd.3       2.91 GiB / 1.82 TiB   0.16  
     osd.7       2.12 GiB / 1.82 TiB   0.14  
     osd.1       1.89 GiB / 1.82 TiB   0.11  
     osd.2       1.56 GiB / 1.82 TiB   0.09  
...

Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await  svctm  %util
sda              0.00    12.40   156.20  89.50   312.45   178.90   128.5     8.42   67.3   3.2   78.5
sdb              0.00     8.10   142.10  76.30   284.20   152.10   125.2     7.15   62.1   2.9   71.2
sdc              0.00     5.20    98.50  45.20   196.80   90.40    120.1     4.23   45.8   2.1   48.3

Connecting to host ceph-node2, port 5201
[  5]   0.00-10.00  sec  12.8 GBytes  11.0 Gbps                  sender
[  5]   0.00-10.00  sec  12.7 GBytes  10.9 Gbps                  receiver

{
  "bluestore_wal_total_bytes": 2147483648,
  "bluestore_wal_used_bytes": 1678901248,
  "bluestore_db_total_bytes": 10737418240,
  "bluestore_db_used_bytes": 8589934592,
  "commit_latency_ms": 245
}

noscrub,nodeep-scrub set
set osd_max_backfills to 1
set osd_recovery_max_active_hdd to 2

{
  "ops": [
    {
      "description": "osd_op(client.12345.0:1 rbd_data.1a2b3c4d5e6f7g8h9i0j_0000000000000001 [write 0~4194304] 0x1, snapid=0, op_flags=0, mtime=2024-01-15T10:23:45.123456+0000)",
      "initiated_at": "2024-01-15T10:23:42.987654+0000",
      "age": 2.135802,
      "duration": 2.135802
    }
  ]
}

Historic ops (last 20):
  osd_op(client.12346.0:2 rbd_data.1a2b3c4d5e6f7
```
## PG Degraded / Undersized / Stuck

```bash
# Check PG status
ceph pg stat
ceph pg dump_stuck                    # all stuck PGs
ceph pg dump_stuck unclean | head -20  # identify PGs and their OSDs

# PG states requiring action:
# active+degraded   = Some replicas missing; cluster recovering; usually self-resolves
# inactive          = No primary OSD; I/O blocked; urgent — check which OSD is down
# stale             = Primary OSD hasn't reported in; check MON-OSD connectivity
# incomplete        = Not enough OSDs to form a quorum for the PG; data at risk
# active+undersized = Replica count below min_size (one or more OSDs down)

# Find which OSDs are mapped to a specific PG
ceph pg map 1.5a    # shows: osd.[primary] [osd.secondary, ...]

# Force repair on a specific PG
ceph pg repair 1.5a

# Identify which OSDs are down causing undersized PGs
ceph osd tree | grep -E "down|out"

# If one OSD is permanently lost: reweight to 0 and let cluster rebalance
ceph osd reweight osd.5 0

# Emergency only: temporarily reduce min_size (DANGEROUS — data loss risk)
# ceph osd pool set rbd min_size 1   # use only if you have no other option, unset immediately
```


```text title="Expected output"
PG stat v 1234567: 2048 pgs: 2000 active+clean; 48 active+degraded
PG summary: 2000 active+clean, 48 active+degraded

stuck pg query returned 48 results:
1.5a ( [osd.2,osd.7,osd.11] ) [2,7,11] 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1.8c ( [osd.4,osd.9] ) [4,9] 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2.1f ( [osd.3,osd.6,osd.10] ) [3,6,10] 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3.2b ( [osd.1,osd.8] ) [1,8] 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
...

osd.2 [osd.2,osd.7,osd.11] l lb 0 0.04999 1.0 up
osd.7 [osd.2,osd.7,osd.11] l lb 0 0.04999 1.0 up
osd.11 [osd.2,osd.7,osd.11] l lb 0 0.04999 1.0 down

instructing pg 1.5a on osd.2 to repair

 -1 root default
  -3 host ceph-node-01
   2 osd.2 up 1.0 1.0
   7 osd.7 up 1.0 1.0
  -5 host ceph-node-02
   4 osd.4 down 0.0 1.0
   9 osd.9 down 0.0 1.0
  -7 host ceph-node-03
   3 osd.3 out 0.0 1.0
   6 osd.6 up 1.0 1.0
  11 osd.11 down 0.0 1.0

reweighted osd.5 to 0.0
```

!!! warning "Common errors"
    **`Error ENOENT: pg 1.5a not found`** — Verify the PG ID exists with `ceph pg stat` and use the correct hexadecimal format (e.g., `1.5a` not `1.90`).
    **`Error EPERM: you do not have permission to perform this operation`** — Run the command with appropriate Ceph admin privileges or use `sudo` if the client is not in the ceph group.
    **`Error EINVAL: invalid min_size
## Clock Skew

```bash
# MONs require clock sync within 0.05 s (50 ms); > 1 s can cause MON election failures
ceph health detail | grep CLOCK_SKEW

# Show per-MON skew values
ceph time-sync-status

# Check NTP on affected nodes
chronyc tracking
chronyc sources -v

# Fix: restart chrony if drifted
systemctl status chronyd
systemctl restart chronyd

# Check clock difference between MON nodes
for host in $(ceph mon dump | awk '/^[0-9]/{print $3}' | cut -d: -f1); do
  echo -n "$host: "; ssh $host date -u +%T
done

# Verify MON clock skew after fix
ceph health detail | grep -E "CLOCK|TIME"
```


```text title="Expected output"
HEALTH_WARN Monitors are allowing insecure connections
    CLOCK_SKEW clock skew detected on mon.ceph-mon-02
      mon.ceph-mon-01 addr 10.0.1.45:6789/0 clock skew 0.012s
      mon.ceph-mon-02 addr 10.0.1.46:6789/0 clock skew 0.847s
      mon.ceph-mon-03 addr 10.0.1.47:6789/0 clock skew 0.003s

ceph-mon-01: 14:32:18
ceph-mon-02: 14:32:19
ceph-mon-03: 14:32:18

Reference ID    : 91.1234.5678 (ntp.ubuntu.com)
Stratum         : 2
Ref time (UTC)  : Fri Jan 17 14:32:18 2025
System time     : 0.000847123 seconds fast of NTP time
Frequency       : -12.456 ppm
Residual freq   : +1.234 ppm
Residual skew   : 0.847 ppm
Root delay      : 0.045123 seconds
Root dispersion : 0.062456 seconds
Update interval : 64.2 seconds
Leap status     : Normal

Active   : Yes
Leap      : Normal
Stratum   : 2
Address          : 91.190.216.51         Leap  Status     Spike  Raw offset
===============================================================================
^+ ntp.ubuntu.com                          0  Leap  Normal      -    -0.847ms
^- time.cloudflare.com                     3  Leap  Normal      -    +1.234ms
^- 91.189.89.198                           2  Leap  Normal      -    -0.456ms

● chronyd.service - chrony, an NTP client/server
     Loaded: loaded (/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2025-01-17 14:25:33 UTC; 6min ago
     Process: 2847 ExecStartPost=/usr/libexec/chrony-helper update-daemon (code=exited, status=0/SUCCESS)
   Main PID: 2841 (chronyd)
      Tasks: 1 (limit: 4915)
     Memory: 2.1M
        CPU: 145ms
     CGroup: /system.slice/chronyd.service
             └─2841 /usr/sbin/chronyd -F -1

HEALTH_OK
```

!!! warning "Common errors"
    **`CLOCK_SKEW clock skew detected on mon.ceph-mon-02`** — Restart chronyd on the affected MON node and verify NTP synchronization with `chronyc tracking` shows skew under 50ms.
    **`Connection refused when running ssh $host date`** — Ensure passwordless SSH is configured between MON nodes or use explicit credentials; verify SSH keys are in place with `ssh-keyscan`.
    **`chronyd.service is not running`** — Enable and start the service with `systemctl enable chronyd && systemctl start chronyd`, then verify with `systemctl status chronyd`.
## MON Quorum Lost

A MON quorum loss blocks all writes and most reads. Minimum 2 of 3 MONs (or 3 of 5) must be up.

```bash
# Symptoms: ceph -s hangs or returns Error ENOENT
# All writes blocked

# 1. SSH to each MON host and check daemon status
systemctl status ceph-mon@<id>

# 2. Restart failed MONs
systemctl restart ceph-mon@<id>
# Or via cephadm:
ceph orch daemon restart mon.<hostname>

# 3. Verify quorum restored
ceph quorum_status
# Output shows: "quorum_names" containing all expected MON hostnames

# 4. If one MON host permanently failed:
ceph mon rm <id>    # run from a healthy MON host
# Then deploy a replacement MON:
ceph orch apply mon --placement="host1,host2,host3-new"

# 5. Check MON log for split-brain or election issues
journalctl -u ceph-mon@<id> -n 200 | grep -E "election|quorum|paxos"
```


```text title="Expected output"
● ceph-mon@mon0.service - Ceph monitor daemon
     Loaded: loaded (/lib/systemd/ceph-mon@.service; enabled; vendor preset: enabled)
     Active: failed (Result: exit-code) since Thu 2024-01-18 14:32:15 UTC; 2min 43s ago
     Process: 8421 ExecStart=/usr/bin/ceph-mon -f --cluster ${CLUSTER} --id %i --setuser ceph --setgroup ceph (code=exited, status=1)

Jan 18 14:32:15 ceph-mon1 systemd[1]: ceph-mon@mon0.service: Main process exited, code=exited, status=1/FAILURE

{
  "election_epoch": 156,
  "quorum": [
    1,
    2
  ],
  "quorum_names": [
    "mon1",
    "mon2"
  ],
  "quorum_leader_name": "mon1",
  "monmap": {
    "epoch": 3,
    "fsid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "modified": "2024-01-18T14:15:22.123456+0000",
    "created": "2024-01-17T09:42:10.987654+0000",
    "mons": [
      {
        "rank": 0,
        "name": "mon0",
        "public_addr": "10.20.30.41:6789/0"
      },
      {
        "rank": 1,
        "name": "mon1",
        "public_addr": "10.20.30.42:6789/0"
      },
      {
        "rank": 2,
        "name": "mon2",
        "public_addr": "10.20.30.43:6789/0"
      }
    ]
  }
}

Jan 18 14:35:22 ceph-mon1 ceph-mon[8901]: election(156): mon.mon1 is new leader
Jan 18 14:35:23 ceph-mon1 ceph-mon[8902]: paxos(paxos): commit 12456 at 156
Jan 18 14:35:24 ceph-mon1 ceph-mon[8903]: quorum 1,2 quorum_names mon1,mon2
Jan 18 14:35:25 ceph-mon1 ceph-mon[8904]: WARNING: mon0 not responding to heartbeat
```

!!! warning "Common errors"
    **`Error ENOENT: error calling conf_read_file`** — Verify the MON's data directory exists at `/var/lib/ceph/mon/ceph-<id>` and has correct ownership (`chown -R ceph:ceph /var/lib/ceph/mon/ceph-<id>`).
    **`unable to bind monitor socket: Address already in use`** — Kill any orphaned ceph-mon processes with `pkill -9 ceph-mon` before restarting, or check if port 6789 is blocked by a firewall rule.
    **`mon.X is down (
---

## See also

- [Ceph — Diagnostics](../diagnostics/)
- [Ceph — Escalation](../escalation/)
- [Ceph — Health Checks](../../operations/health-checks/)

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
