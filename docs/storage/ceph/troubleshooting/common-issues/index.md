# Ceph — Common Issues

<div class="kb-summary">
Troubleshooting guide for frequent Ceph problems: OSD down/out, PG degraded and stuck, slow requests, nearfull/full cluster, clock skew, and recovery that won't complete.
</div>

```text
┌──────────────────────────────────────── Ceph — Common Issues ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   First: ceph health detail — every health warning has a code (e.g. OSD_DOWN, SLOW_OPS)      │    │
│   │   OSD down: check disk health (smartctl), network, and OSD log before concluding hardware     │   │
│   │   Nearfull/Full: add capacity or delete data; full cluster stops ALL writes including repair  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HEALTH_ERR    = Critical cluster condition requiring immediate action; may block all writes          │
│  OSD_DOWN      = Health code: one or more OSDs not responding; check disk and network first           │
│  PG_DEGRADED   = Health code: PGs have fewer replicas than required; data still accessible            │
│  PG_INACTIVE   = Health code: PG cannot serve I/O; primary OSD down; investigate immediately          │
│  SLOW_OPS      = Health code: operations queued more than 30s; indicates disk or network saturation   │
│  OSD_NEARFULL  = Health code: OSD disk usage approaching full ratio; add capacity soon                │
│  OSD_FULL      = All I/O including recovery halted; must free space or add capacity immediately       │
│  clock skew    = NTP drift exceeding 0.05s between MON nodes; triggers HEALTH_WARN                    │
│  ceph health detail = Lists all active health codes with per-OSD/PG explanation and context           │
│  BytesToResync = Remaining bytes to replicate after OSD change; wait for 0 before disk replacement    │
│  CRUSH         = Data placement algorithm; incorrect CRUSH map causes PG stuck states                 │
│  noout flag    = Prevents OSDs being marked out during maintenance; set before host reboot            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## OSD Down

```bash
# Identify down OSD
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

## PG Degraded / Stuck

```bash
# Check PG status
ceph pg stat
ceph pg dump_stuck   # all stuck PGs

# PG states requiring action:
# active+degraded   = Some replicas missing; cluster recovering; usually self-resolves
# inactive          = No primary OSD; I/O blocked; urgent — check which OSD is down
# stale             = Primary OSD hasn't reported in; check MON-OSD connectivity
# incomplete        = Not enough OSDs to form a quorum for the PG; data at risk

# Find which OSDs are mapped to a specific PG
ceph pg map 1.5a    # shows: osd.[primary] [osd.secondary, ...]

# Force recovery on a specific PG
ceph pg repair 1.5a

# If PG is stuck active+undersized (not enough OSDs to meet min_size):
# Check if any OSDs are down and bring them back, OR
# Temporarily reduce min_size (risky — only for emergency)
# ceph osd pool set rbd min_size 1   # DANGEROUS — data loss risk; temporary only
```

## Slow Requests

```bash
# Symptoms: HEALTH_WARN "X requests are blocked"
ceph health detail | grep SLOW_OPS
ceph osd perf | sort -k2 -n -r | head -10  # highest commit latency

# Common causes:
# 1. Disk I/O saturation on specific OSDs → check iostat on OSD nodes
iostat -x 1 5 | grep -E "^sd|Device"

# 2. Network congestion on cluster network → check throughput
iperf3 -c ceph-node2 -t 10 -P 4   # between OSD nodes

# 3. OSD journal/WAL full → check BlueStore WAL usage
ceph daemon osd.5 perf dump | grep -i "wal\|db\|commit"

# 4. Scrubbing causing latency → temporarily disable
ceph osd set noscrub
# Re-enable during maintenance: ceph osd unset noscrub

# 5. Recovery consuming I/O bandwidth → limit recovery speed
ceph config set osd osd_max_backfills 1
ceph config set osd osd_recovery_max_active_hdd 2
```

## Nearfull / Full Cluster

```bash
# Check thresholds and current usage
ceph df
ceph health detail | grep -E "NEARFULL|FULL"

# Default thresholds:
# nearfull ratio: 0.85 (85%) → HEALTH_WARN
# backfillfull ratio: 0.90 (90%) → stops backfill
# full ratio: 0.95 (95%) → stops ALL writes

# Emergency: increase full ratio temporarily (buy time)
ceph osd set-full-ratio 0.97   # temporary only
ceph osd set-nearfull-ratio 0.90

# Permanent fix options:
# 1. Add more nodes/OSDs
# 2. Delete data or expired snapshots
# 3. Move data to another pool/cluster

# Find large RBD images consuming space
rbd ls rbd | while read img; do
    SIZE=$(rbd info rbd/$img | grep disk_usage | awk '{print $2}')
    echo "$SIZE $img"
done | sort -h -r | head -20
```

## Clock Skew

```bash
# Ceph MONs require clock sync within 0.05 seconds
# Clock skew > 50ms triggers HEALTH_WARN; > 1s can cause MON election failures

ceph health detail | grep CLOCK_SKEW

# Check NTP on affected nodes
chronyc tracking
chronyc sources -v

# Fix: ensure NTP is configured and syncing
systemctl status chronyd
systemctl restart chronyd

# Check clock difference between MON nodes
for host in $(ceph mon dump | awk '/^[0-9]/{print $3}' | cut -d: -f1); do
    echo -n "$host: "; ssh $host date -u +%T
done
```
