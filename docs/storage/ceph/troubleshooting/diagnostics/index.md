# Ceph — Diagnostics

```text
┌───────────────────────────────────── Ceph — Diagnostic Overview ──────────────────────────────────────┐
│                                                                                                       │
│  Diagnostic Layers                                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐                │
│  │  Health Codes           │  │  OSD / PG Analysis      │  │  Network & Latency      │                │
│  │  ceph health detail     │  │  ceph osd tree          │  │  ceph osd perf          │                │
│  │  OSD_DOWN, PG_DEGRADED  │  │  ceph pg dump           │  │  iperf3 between nodes   │                │
│  │  SLOW_OPS, NEARFULL     │  │  osd log analysis       │  │  messenger v2 stats     │                │
│  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘                │
│                                                                                                       │
│  Diagnostic Sequence — Cluster Unhealthy                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  1. ceph -s — get top-level health, OSD count, PG summary, active I/O rate                            │
│  2. ceph health detail — enumerate all active health codes with explanations                          │
│  3. ceph osd tree — identify which OSDs are down/out; cross-reference to host names                   │
│  4. ceph pg dump_stuck — list inactive/degraded/unclean PGs with primary OSD                          │
│  5. journalctl -u ceph-osd@<id> — last 100 lines of OSD log for crash or error context                │
│  6. ceph osd perf — per-OSD commit/apply latency; outliers indicate disk I/O issues                   │
│                                                                                                       │
│  Crash Dump and Support Data Collection                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  ceph crash ls — list recent daemon crashes                                                           │
│  ceph crash info <crash-id> — full crash report with traceback                                        │
│  ceph crash archive <crash-id> — acknowledge and archive crash after review                           │
│  Support bundle: sosreport + ceph report > ceph-report.json — attach to vendor support case           │
│                                                                                                       │
│  GLOSSARY                                                                                             │
│  OSD_DOWN      — OSD not responding; check disk status and OSD daemon journal                         │
│  PG_DEGRADED   — PG has fewer replicas than desired; data still available but unprotected             │
│  PG_INACTIVE   — PG cannot serve I/O; primary OSD is down; check OSD and network                      │
│  SLOW_OPS      — Operations queued > 30s; indicates disk or network saturation                        │
│  OSD_NEARFULL  — OSD disk usage exceeds nearfull ratio; add capacity before OSD_FULL                  │
│  ceph report   — full cluster state snapshot for support analysis and case submission                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-summary">
Diagnostic tools for Ceph: health code reference, OSD log analysis, crash dump review, network and latency diagnostics, and gathering data for support cases.
</div>

## Health Code Reference

```bash
# Get full health detail with error codes
ceph health detail

# Common health codes and meanings:
# OSD_DOWN           = OSD not responding; check disk and daemon log
# OSD_OUT            = OSD marked out manually; data migrating
# OSD_NEARFULL       = OSD disk > nearfull ratio (per-OSD)
# PG_DEGRADED        = PG has fewer than desired replicas
# PG_INACTIVE        = PG can't serve I/O; check which OSD primary is down
# PG_BACKFILL_TOOFULL= OSD too full to receive backfill; add capacity
# SLOW_OPS           = Ops queued > 30s; check disk I/O or network
# CLOCK_SKEW         = MON node NTP drift; fix NTP
# MON_DOWN           = MON daemon down; quorum may be at risk
# POOL_NEAR_FULL     = Pool quota nearly exceeded
# AUTH_INSECURE_GLOBAL_ID_RECLAIM = msgr2 security issue; patch required
```

## OSD Log Analysis

```bash
# Ceph OSD logs (cephadm-managed clusters use container logs)
ceph orch daemon logs osd.5            # recent container logs
ceph orch daemon logs osd.5 --follow   # live tail

# On OSD node directly
journalctl -u ceph-osd@5 -n 200 --no-pager

# Common OSD log messages:
# "slow request" → latency issue (disk or network)
# "wrongly marked me down" → network partition between OSD and MON
# "bluestore osd ... fsck failed" → disk corruption; run: ceph-osd --osd-id 5 --repair
# "FAILED assert" followed by crash → OSD bug or disk error
# "heartbeat_check: no reply from osd.X" → OSD-to-OSD network issue

# Get OSD perf dump (runtime metrics)
ceph daemon osd.5 perf dump | python3 -m json.tool | grep -A3 "commit_latency\|apply_latency"
```

## Crash Dump Analysis

```bash
# Ceph saves crash dumps when daemons crash unexpectedly
ceph crash ls               # list all crash dumps
ceph crash stat             # summary of crash counts

# View specific crash
ceph crash info <crash-id>   # shows backtrace, OSD version, message

# Archive crash (acknowledge it)
ceph crash archive <crash-id>
ceph crash archive-all       # archive all

# Crash logs on disk
ls /var/lib/ceph/crash/
# Each crash has a directory with: metadata, backtrace, and log
```

## Network Diagnostics

```bash
# Test cluster network bandwidth between OSD nodes
# Run on both endpoints simultaneously:
# Node 1 (receiver):
iperf3 -s

# Node 2 (sender):
iperf3 -c 10.0.2.11 -t 30 -P 4 -i 5
# Expected: near line rate (9+ Gbps for 10G, 23+ Gbps for 25G)

# Check OSD heartbeat timeouts (indicates network issues)
ceph config show-with-defaults osd.0 | grep -E "heartbeat|timeout"

# Measure round-trip latency between OSD nodes
ping -c 20 10.0.2.11   # cluster network
# Expected: < 0.5 ms on local network

# Check for packet loss (can cause OSD down events)
mtr --report --report-cycles 100 10.0.2.11
```

## Gather Support Data

```bash
# For support cases, collect:

# 1. Full cluster status
ceph status > /tmp/ceph-status.txt
ceph health detail > /tmp/ceph-health-detail.txt
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

# 5. MON log (last 1000 lines per MON)
for mon in $(ceph mon dump | awk '/^[0-9]/{print $3}' | cut -d: -f1); do
    ssh $mon "journalctl -u ceph-mon@$(hostname) -n 1000 --no-pager" > /tmp/mon-${mon}.log
done

# 6. OSD logs from affected OSDs
ceph orch daemon logs osd.5 > /tmp/osd5.log

# Compress all
tar czf ceph-support-$(date +%F).tar.gz /tmp/ceph-*.txt /tmp/osd*.log /tmp/mon-*.log
```
