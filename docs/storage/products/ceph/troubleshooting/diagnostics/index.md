---
tags:
  - ceph
  - troubleshooting
search:
  boost: 1.5
description: "Diagnostic tools for Ceph: health code reference, OSD log analysis, crash dump review, network and latency diagnostics, PG deep dives, and gathering data..."
---
# Ceph — Diagnostics

<div class="kb-summary">
Diagnostic tools for Ceph: health code reference, OSD log analysis, crash dump review, network and latency diagnostics, PG deep dives, and gathering data for support cases.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

A: "ceph -s — top-level status" {shape: rectangle}
B: "Drill into daemons\nceph daemon osd.id ..." {shape: rectangle}
C: "Collect crash data\nceph crash ls / info" {shape: rectangle}
D: "Collect logs\njournalctl / ceph orch daemon logs" {shape: rectangle}
E: "Run sos report\nfor RHCS cases" {shape: rectangle}
F: "Open support case\nescalation/" {shape: rectangle}
G: "PG deep dive\nceph pg query / rados list-inconsistent" {shape: rectangle}

A -> B
B -> C
C -> D
D -> E
E -> F
B -> G
G -> D
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
health_code_reference: "Health Code Reference" {shape: rectangle}
crash_collection: "Crash Collection" {shape: rectangle}
osd_daemon_diagnostics: "OSD Daemon Diagnostics" {shape: rectangle}
osd_log_analysis: "OSD Log Analysis" {shape: rectangle}
log_levels_debugging: "Log Levels (Debugging)" {shape: rectangle}
crash_dump_analysis: "Crash Dump Analysis" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> health_code_reference: investigate
symptom -> crash_collection: investigate
symptom -> osd_daemon_diagnostics: investigate
symptom -> osd_log_analysis: investigate
symptom -> log_levels_debugging: investigate
symptom -> crash_dump_analysis: investigate
health_code_reference -> resolution
crash_collection -> resolution
osd_daemon_diagnostics -> resolution
osd_log_analysis -> resolution
log_levels_debugging -> resolution
crash_dump_analysis -> resolution
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Health Code Reference

```bash
# Get full health detail with error codes
ceph health detail

# Common health codes and meanings:
# OSD_DOWN           = OSD not responding; check disk and daemon log
# OSD_OUT            = OSD marked out manually; data migrating
# OSD_NEARFULL       = OSD disk > nearfull ratio (per-OSD)
# OSD_FULL           = All writes blocked; free space immediately
# PG_DEGRADED        = PG has fewer than desired replicas
# PG_INACTIVE        = PG can't serve I/O; check which OSD primary is down
# PG_BACKFILL_TOOFULL= OSD too full to receive backfill; add capacity
# SLOW_OPS           = Ops queued > 30s; check disk I/O or network
# CLOCK_SKEW         = MON node NTP drift > 50ms; fix NTP
# MON_DOWN           = MON daemon down; quorum may be at risk
# POOL_NEAR_FULL     = Pool quota nearly exceeded
# AUTH_INSECURE_GLOBAL_ID_RECLAIM = msgr2 security issue; patch required
```


```text title="Expected output"
HEALTH_WARN 1 nearfull osd(s); 2 pool(s) near full
    OSD_NEARFULL 1 osd(s) at 85% capacity
        osd.7 is at 85%, near full threshold 90%
    POOL_NEAR_FULL 2 pool(s) near full
        pool 'rbd' is at 87% of quota
        pool 'cephfs_data' is at 92% of quota
    SLOW_OPS 12 slow ops, oldest blocked for 45 sec
        osd.3: 8 ops blocked > 30s
        osd.7: 4 ops blocked > 30s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error initializing cluster client: ('error calling remote procedure server', -5)` | Verify ceph.conf exists in /etc/ceph/ and cluster name matches; run `ceph --version` to confirm connectivity. |
    | `HEALTH_ERR: 3 osds down; 24 pg degraded` | Check OSD daemon status with `systemctl status ceph-osd@*` and OSD logs at `/var/log/ceph/ceph-osd.*.log` to identify disk or network failures. |
    | `HEALTH_CRITICAL: 1 mon down; quorum lost` | Restart the downed monitor daemon with `systemctl restart ceph-mon@<hostname>` and verify NTP sync across all monitor nodes with `chronyc sources`. |
## Crash Collection

```bash
ceph crash ls                          # list crashes with timestamp and ID
ceph crash info <crash-id>             # full crash detail: backtrace, daemon version, message
ceph crash archive <crash-id>          # acknowledge crash after review
ceph crash archive-all                 # acknowledge all pending crashes

# Crash minidumps stored on disk at:
ls /var/lib/ceph/crash/
# Each crash directory contains: metadata JSON, backtrace, and OSD log at time of crash

# Count crashes by daemon type
ceph crash stat
```


```text title="Expected output"
2024-01-15T09:42:33.456789+0000 osd.12
2024-01-15T08:17:22.123456+0000 mon.0
2024-01-14T23:55:11.789012+0000 osd.8

COMPONENT       osd
HOST            ceph-node-03
TIMESTAMP       2024-01-15T09:42:33.456789+0000
UTIME           1705318953.456789
VERSION         18.2.1
BACKTRACE       [<core>] /usr/bin/ceph-osd(_ZN3OSD4initEv+0x4a2) [0x55d8c2f1a8b2]
                [<core>] /usr/bin/ceph-osd(main+0x1c3) [0x55d8c2f1a5e1]
CRASH_ID        20240115t094233z-osd-12-abc123def456

total 3
drwxr-x--- 2 ceph ceph 4096 Jan 15 09:42 20240115t094233z-osd-12-abc123def456
drwxr-x--- 2 ceph ceph 4096 Jan 15 08:17 20240115t081722z-mon-0-xyz789uvw012
drwxr-x--- 2 ceph ceph 4096 Jan 14 23:55 20240114t235511z-osd-8-pqr345stu678

     DAEMON TYPE     COUNT
            osd        2
            mon        1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: crash id not found` | Verify the crash ID exists with `ceph crash ls` and ensure you're using the exact ID from the output. |
    | `Error: EACCES: permission denied, open '/var/lib/ceph/crash/'` | Run the command with `sudo` or ensure your user is in the `ceph` group with `sudo usermod -aG ceph $USER`. |
## OSD Daemon Diagnostics

```bash
# Performance counters (all metrics the OSD tracks internally)
ceph daemon osd.<id> perf dump

# Show active configuration for messaging and OSD parameters
ceph daemon osd.<id> config show | grep -E "ms_|osd_max"

# Recent slow ops — shows ops that exceeded slow_op threshold
ceph daemon osd.<id> dump_historic_ops

# Current in-flight ops — shows what is actively being processed
ceph daemon osd.<id> dump_ops_in_flight

# BlueStore internal stats (fragmentation, read/write latency breakdown)
ceph daemon osd.<id> perf dump | python3 -m json.tool | grep -A5 "bluestore"

# Cache stats for BlueStore buffer cache
ceph daemon osd.<id> perf dump | python3 -m json.tool | grep -E "cache_|throttle"
```


```text title="Expected output"
{
  "osd": {
    "op_latency": {
      "avgcount": 45821,
      "sum": 2847.392841
    },
    "op_w_rlat": {
      "avgcount": 12043,
      "sum": 1203.847291
    }
  },
  "bluestore": {
    "kv_commit_lat": {
      "avgcount": 8932,
      "sum": 892.123456
    },
    "kv_sync_lat": {
      "avgcount": 8932,
      "sum": 1204.567890
    },
    "compress_success_count": 45821,
    "compress_rejected_count": 2104
  },
  "throttle-msgr_dispatch_throttler-osd": {
    "val": 0,
    "max": 131072,
    "get_sum": 892341,
    "get_or_fail_fail": 0,
    "put_sum": 892341,
    "take_sum": 892341,
    "take_or_fail_fail": 0
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error connecting to daemon: (2) No such file or directory` | Verify the OSD is running with `systemctl status ceph-osd@<id>` and confirm the correct socket path exists in `/var/run/ceph/`. |
    | `command not found: python3` | Install Python 3 with `apt install python3` or `yum install python3`, or pipe to `jq` instead if available. |
    | `No such file or directory` | Replace `<id>` with an actual OSD number (e.g., `osd.0`) and verify it exists with `ceph osd tree`. |
## OSD Log Analysis

```bash
# Ceph OSD logs (cephadm-managed clusters use container logs)
ceph orch daemon logs osd.5            # recent container logs
ceph orch daemon logs osd.5 --follow   # live tail

# On OSD node directly
journalctl -u ceph-osd@5 -n 200 --no-pager

# Common OSD log messages and their meaning:
# "slow request"                       → latency issue (disk or network)
# "wrongly marked me down"             → network partition between OSD and MON
# "bluestore osd ... fsck failed"      → disk corruption; run: ceph-osd --osd-id 5 --repair
# "FAILED assert" followed by crash    → OSD bug or disk error
# "heartbeat_check: no reply from osd.X" → OSD-to-OSD network issue

# Get OSD perf dump (runtime metrics)
ceph daemon osd.5 perf dump | python3 -m json.tool | grep -A3 "commit_latency\|apply_latency"
```


```text title="Expected output"
2024-11-15T09:42:33.847+0000 osd.5 [WRN] slow request 30.045 seconds old, received at 2024-11-15T09:42:03.802+0000:
2024-11-15T09:42:33.847+0000 osd.5 [WRN] client.4567 osd5 [0x560d2a8f4700] 0x560d2a8f5c00 queued for 29.234s, latency 0.811s
2024-11-15T09:42:33.847+0000 osd.5 [INF] 73 slow requests, 1 included below; oldest blocked for 45.123s, new request blocked for 1.234s, 0 ops in flight
2024-11-15T09:42:33.847+0000 osd.5 [ERR] wrongly marked me down
2024-11-15T09:42:33.847+0000 osd.5 [ERR] heartbeat_check: no reply from osd.3 after 40.000s
Nov 15 09:42:33 ceph-node-02 ceph-osd[4521]: 2024-11-15T09:42:33.847+0000 osd.5 [WRN] slow request 30.045 seconds old
Nov 15 09:42:33 ceph-node-02 ceph-osd[4521]: 2024-11-15T09:42:33.847+0000 osd.5 [INF] 73 slow requests, 1 included below
Nov 15 09:42:33 ceph-node-02 ceph-osd[4521]: 2024-11-15T09:42:33.847+0000 osd.5 [ERR] wrongly marked me down
    "commit_latency": {
      "avgcount": 1847,
      "sum": 2345.678
    },
    "apply_latency": {
      "avgcount": 1847,
      "sum": 5678.234
    }
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: No such daemon osd.5` | Verify the OSD exists with `ceph osd tree` and confirm the correct OSD ID. |
    | `error: unable to connect to the cluster` | Ensure you have valid Ceph credentials in `/etc/ceph/ceph.client.admin.keyring` and the monitor addresses are reachable. |
    | `jq: command not found` | Install `jq` with `apt install jq` or `yum install jq`, or use `python3 -m json.tool` instead for pretty-printing JSON. |
## Log Levels (Debugging)

```bash
# Increase OSD log verbosity for debugging (reset after use — very verbose)
ceph config set osd debug_osd 10       # verbose OSD log
ceph config set osd debug_ms 1         # message layer debug
ceph config set osd debug_bluestore 10 # BlueStore internals

# Reset after debugging (do not leave elevated in production)
ceph config rm osd debug_osd
ceph config rm osd debug_ms
ceph config rm osd debug_bluestore

# Via cephadm orchestrator log tailing
ceph orch daemon logs osd.<id>         # tail daemon log via orchestrator

# Journald query on OSD host
journalctl -u ceph-osd@<id> --since "1 hour ago"
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
=== osd.42 ===
2024-01-15T14:23:47.892+0000 7f8c3a2b1234 10 osd.42 pg_epoch 1847 pg[11.4r1847] handle_activate_map: Not primary, not in up_set
2024-01-15T14:23:48.103+0000 7f8c3a2b5678 10 osd.42 bluestore(db_path /var/lib/ceph/osd/ceph-42/db) _do_alloc_write: allocating 4096 bytes
2024-01-15T14:23:48.456+0000 7f8c3a2b9abc 10 osd.42 ms(simplemessenger) ms_deliver_fast: delivering to osd.41 v1:192.168.1.105:6802/1847
2024-01-15T14:23:49.234+0000 7f8c3a2b2def 10 osd.42 pg_epoch 1848 pg[11.4r1848] activate: pg now active+clean
-- Logs begin at Mon 2024-01-15 13:15:22 UTC, end at Mon 2024-01-15 14:25:10 UTC. --
Jan 15 14:23:47 ceph-node-03 ceph-osd[4521]: 2024-01-15T14:23:47.892+0000 7f8c3a2b1234 10 osd.42 pg_epoch 1847 pg[11.4r1847] handle_activate_map: Not primary
Jan 15 14:23:48 ceph-node-03 ceph-osd[4521]: 2024-01-15T14:23:48.103+0000 7f8c3a2b5678 10 osd.42 bluestore(db_path /var/lib/ceph/osd/ceph-42/db) _do_alloc_write
Jan 15 14:23:49 ceph-node-03 ceph-osd[4521]: 2024-01-15T14:23:49.234+0000 7f8c3a2b2def 10 osd.42 pg_epoch 1848 pg[11.4r1847] activate: pg now active+clean
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: osd not found` | Verify the OSD ID exists with `ceph osd tree` and use the correct numeric ID in place of `<id>`. |
    | `Error: EACCES: permission denied` | Run journalctl commands with `sudo` or as root, or add your user to the `systemd-journal` group. |
    | `Error: unrecognized config option 'debug_osd'` | Ensure you are running a compatible Ceph version; use `ceph config help osd` |
## Crash Dump Analysis

```bash
# View specific crash detail
ceph crash info <crash-id>   # shows backtrace, OSD version, message

# Archive crash (acknowledge it after review)
ceph crash archive <crash-id>
ceph crash archive-all       # archive all

# Crash logs on disk: one directory per crash
ls /var/lib/ceph/crash/
# Each crash has: metadata, backtrace, and log at time of crash
```


```text title="Expected output"
$ ceph crash info 2024-01-15T09:42:33.847291Z_a1b2c3d4-e5f6-4a7b-9c8d-1e2f3a4b5c6d

{
  "crash_id": "2024-01-15T09:42:33.847291Z_a1b2c3d4-e5f6-4a7b-9c8d-1e2f3a4b5c6d",
  "timestamp": "2024-01-15T09:42:33.847291Z",
  "process_name": "osd.7",
  "entity_name": "osd.7",
  "ceph_version": "18.2.1",
  "os_version": "Ubuntu 22.04.3 LTS",
  "backtrace": [
    "0x00007f8a2c1e4d20 in /usr/lib/ceph/librados.so.2",
    "0x00007f8a2c1e4e15 in /usr/lib/ceph/librados.so.2",
    "0x00007f8a2c1f2a0c in /usr/lib/ceph/librados.so.2"
  ],
  "message": "Assertion `!m_filestore_queue_high_delay_ms' failed"
}

$ ceph crash archive 2024-01-15T09:42:33.847291Z_a1b2c3d4-e5f6-4a7b-9c8d-1e2f3a4b5c6d
Archived crash dump.

$ ceph crash archive-all
Archived 3 crash dumps.

$ ls /var/lib/ceph/crash/
2024-01-15T09:42:33.847291Z_a1b2c3d4-e5f6-4a7b-9c8d-1e2f3a4b5c6d
2024-01-14T16:18:22.512047Z_f7e6d5c4-b3a2-9f8e-7d6c-5b4a3f2e1d0c
2024-01-13T11:05:47.293156Z_9c8b7a69-5e4d-3c2b-1a09-f8e7d6c5b4a3
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: crash_id not found` | Verify the crash ID exists with `ceph crash ls` before attempting to archive. |
    | `Error: EACCES: permission denied, open '/var/lib/ceph/crash/'` | Run the command with appropriate privileges (sudo) or ensure your user is in the ceph group. |
## Network Diagnostics

```bash
# Test cluster network bandwidth between OSD nodes
# Node 1 (receiver):
iperf3 -s

# Node 2 (sender):
iperf3 -c 10.0.1.11 -t 30 -P 4 -i 5
# Expected: near line rate (9+ Gbps for 10 GbE, 23+ Gbps for 25 GbE)

# Check OSD heartbeat timeouts (indicates network issues)
ceph config show-with-defaults osd.0 | grep -E "heartbeat|timeout"

# Measure round-trip latency between OSD nodes
ping -c 20 10.0.1.11   # cluster network; expected < 0.5 ms
# Check for packet loss (can cause OSD down events)
mtr --report --report-cycles 100 10.0.1.11
```


```text title="Expected output"
---
Server listening on 5201
---
[ ID] Interval           Transfer     Bitrate         Retr
[  4]   0.00-5.00   sec  5.62 GBytes  9.65 Gbps     0             sender
[  4]   5.00-10.00  sec  5.71 GBytes  9.82 Gbps     0             sender
[  4]  10.00-15.00  sec  5.68 GBytes  9.76 Gbps     2             sender
[  4]  15.00-20.00  sec  5.74 GBytes  9.88 Gbps     1             sender
[  4]  20.00-25.00  sec  5.69 GBytes  9.79 Gbps     0             sender
[  4]  25.00-30.00  sec  5.66 GBytes  9.71 Gbps     0             sender
[ SUM]   0.00-30.00  sec  34.1 GBytes  9.78 Gbps     3             sender

osd_heartbeat_interval = 6
osd_heartbeat_timeout = 20
osd_heartbeat_grace = 21
osd_heartbeat_min_peers = 10

PING 10.0.1.11 (10.0.1.11) 56(84) bytes of data.
64 bytes from 10.0.1.11: icmp_seq=1 time=0.312 ms
64 bytes from 10.0.1.11: icmp_seq=2 time=0.298 ms
64 bytes from 10.0.1.11: icmp_seq=3 time=0.325 ms
...
64 bytes from 10.0.1.11: icmp_seq=20 time=0.301 ms
--- 10.0.1.11 statistics ---
20 packets transmitted, 20 received, 0% packet loss, time 19ms
rtt min/avg/max/stddev = 0.298/0.309/0.325/0.008 ms

Start: 2024-01-15T14:32:18+0000
Best:   0.298
Avg:    0.309
Worst:  0.325
StdDev: 0.008
Loss%:  0.000
Snt:    100
Rcv:    100
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `iperf3: error - unable to connect to server` | Verify the receiver is listening on the correct interface with `iperf3 -s -B 10.0.1.11` and check firewall rules allow port 5201. |
    | `connect: Network is unreachable` | Confirm both nodes are on the same cluster network subnet and routing is configured with `ip route show`. |
    | `ping: sendmsg: No route to host` | Verify the cluster network interface is up with `ip link show` and check that 10.0.1.11 is reachable from the sender's network segment. |
## PG Inconsistency Deep Dive

```bash
# Full PG state JSON (useful for support cases)
ceph pg <pgid> query | python3 -m json.tool

# Find which pools have inconsistent PGs
rados list-inconsistent-pg <pool>

# Find which objects are inconsistent within a specific PG
rados list-inconsistent-obj <pgid> <pool>

# Force a PG repair (Ceph will attempt to fix the inconsistency)
ceph pg repair <pgid>

# Check PG states across all pools
ceph pg dump_stuck inconsistent
ceph pg dump | awk '$1 ~ /^[0-9]+\.[0-9a-f]+/ && $9 != "active+clean" {print $1, $9}'
```


```text title="Expected output"
{
  "state": "inconsistent",
  "snap_trimq": "[]",
  "epoch": 2847,
  "up": [
    3,
    1,
    2
  ],
  "acting": [
    3,
    1,
    2
  ],
  "info": {
    "pgid": "12.4a",
    "last_update": "2847'45821",
    "last_complete": "2847'45821",
    "log_tail": "2840'0"
  }
}

pool: rbd
12.4a inconsistent
15.2c inconsistent

12.4a [3,1,2] 12 objects, 0 B, 0 B, 0 B, 0 B
  shard 1: [3,1,2] 12 objects, 0 B, 0 B, 0 B, 0 B
  shard 2: [3,1,2] 11 objects, 0 B, 0 B, 0 B, 0 B

instructing pg 12.4a on osd.3 to repair

12.4a inconsistent
15.2c inconsistent
18.1f peering
24.ab active+clean

12.4a active+clean
15.2c active+clean
18.1f peering
24.ab active+clean
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: pg 12.4a not found` | Verify the PG ID format is correct (e.g., `12.4a`) and the pool exists with `ceph osd pool ls`. |
    | `Error ENOENT: error code 2` | Ensure the pool name is valid and contains data by running `rados ls -p <pool>` first. |
## sosreport for Red Hat Ceph Storage

```bash
# Collect sos report on any RHCS node (includes all Ceph-specific diagnostics)
sos report -e ceph -k ceph.all=true

# Output tarball written to:
ls /var/tmp/sosreport-*.tar.xz

# Collect on all MON hosts and affected OSD hosts before opening a case
# Transfer to admin workstation for upload to access.redhat.com
```


```text title="Expected output"
sosreport (version 4.3)

This command will collect system information and diagnostic data from this
Linux system. An HTML report will be generated in addition to the compressed
archive containing the collected data.

Running plugins. This may take a while ...

  Running 90/90: ceph...                                                   [100%]

sosreport completed successfully (runtime 2m 34s)

The following archive has been created and saved in /var/tmp:

  sosreport-ceph-node01-20240215-kxvj4wd.tar.xz (487 MB)

The checksum with the filename is added to the manifest file:
  /var/tmp/sosreport-ceph-node01-20240215-kxvj4wd.tar.xz.md5

sosreport-ceph-node01-20240215-kxvj4wd.tar.xz
sosreport-ceph-node01-20240215-kxvj4wd.tar.xz.md5
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sosreport: command not found` | Install sos package with `yum install sos` or `dnf install sos`. |
    | `ERROR: insufficient permissions to run sosreport, root access is required` | Run the command with `sudo` or as the root user. |
    | `ERROR: plugin ceph not found` | Install ceph-common package with `yum install ceph-common` to enable Ceph plugin support. |
## Gather Support Data

```bash
# 1. Full cluster status
ceph status > /tmp/ceph-status.txt
ceph health detail >> /tmp/ceph-status.txt
ceph -s >> /tmp/ceph-status.txt

# 2. OSD map and tree
ceph osd dump > /tmp/osd-dump.txt
ceph osd tree > /tmp/osd-tree.txt
ceph osd df > /tmp/osd-df.txt

# 3. PG dump
ceph pg dump > /tmp/pg-dump.txt
ceph pg dump_stuck > /tmp/pg-stuck.txt

# 4. Config
ceph config dump > /tmp/ceph-config.txt

# 5. MON logs (last 1000 lines per MON)
for mon in $(ceph mon dump | awk '/^[0-9]/{print $3}' | cut -d: -f1); do
  ssh $mon "journalctl -u ceph-mon@$(hostname) -n 1000 --no-pager" > /tmp/mon-${mon}.log
done

# 6. OSD logs from affected OSDs
ceph orch daemon logs osd.5 > /tmp/osd5.log

# Compress all for upload
tar czf ceph-support-$(date +%F).tar.gz /tmp/ceph-*.txt /tmp/osd*.log /tmp/mon-*.log
```


```text title="Expected output"
cluster:
    id:     a1b2c3d4-e5f6-4789-abcd-ef1234567890
    health: HEALTH_WARN
            1 pg inactive
            2 osds down

monmap e3: 3 mons at {mon0=10.0.1.10:6789/0,mon1=10.0.1.11:6789/0,mon2=10.0.1.12:6789/0}
           election epoch 42, quorum 0,1,2, out of quorum: none
           leader: mon0
           have v2 addresses

osdmap e1847: 24 osds: 22 up, 2 down; 11 replicas
             flags sortbitwise,recovery_deletes,purged_snapdirs,pglog_hardlimit

pgmap v4521847h2847: 256 pgs, 8 pools, 847 GB data, 2.1 TB used, 18 TB / 20 TB avail
       -1/3 objects degraded (33.3%)
       2 pg peering
       1 pg stuck inactive

osd.0  10.0.2.5   10.0.3.5  up   1.0  1.0T  847G
osd.1  10.0.2.6   10.0.3.6  up   1.0  1.0T  923G
osd.5  10.0.2.10  10.0.3.10 down 1.0  1.0T      0
osd.12 10.0.2.15  10.0.3.15 down 1.0  1.0T      0

pg_stat objects byte_used
1.0       1024    512M
1.1       2048    1.2G
...

ceph-support-2024-01-15.tar.gz created successfully (847 MB)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: error connecting to the cluster` | Verify CEPH_CONF environment variable points to a valid ceph.conf and the user has read permissions on /etc/ceph/ceph.client.admin.keyring. |
    | `ssh: Could not resolve hostname mon0: Name or service not known` | Replace the hostname extraction logic with explicit mon hostnames: `for mon in mon0 mon1 mon2; do` instead of parsing `ceph mon dump`. |
    | `ceph orch daemon logs osd.5: No such daemon` | Verify the OSD exists and is registered with ceph-orch by running `ceph orch ps | grep osd.5` first. |
---

## See also

- [Ceph — Common Issues](../common-issues/)
- [Ceph — Escalation](../escalation/)

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
