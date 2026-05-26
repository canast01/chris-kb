# Pure1 — Performance

```text
Performance Data Flow — Pure1
┌──────────────────────────┐
│  Array (FlashArray/FB)   │
│  metrics collected every │
│  30s via phone-home      │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│   Pure1 Time-Series DB   │
│   (up to 1 year history) │
└────────────┬─────────────┘
             ▼
┌─────────────────────────────────────────┐
│         Dashboard Charts                │
├─────────────┬──────────────┬────────────┤
│    IOPS     │   Latency    │ Throughput │
│  ▲          │  ▲           │  ▲         │
│  │ ╭╮  ╭╮  │  │   ╭──╮   │  │  ╭──╮  │
│  │╭╯╰╮╭╯╰╮ │  │───╯  ╰── │  │──╯  ╰─ │
│  └──────────│  └──────────│  └─────────│
│  read/write │  µs avg     │  MB/s      │
└─────────────┴──────────────┴────────────┘
```
┌──────────────────────────────────── Pure1 — Performance Analysis ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Performance Metrics              │  │            Workload Intelligence            │   │
│   │               IOPS read/write                │  │               Workload ID (AI)              │   │
│   │               Latency p50/p99                │  │               IO size profile               │   │
│   │                Bandwidth MB/s                │  │               Read/write ratio              │   │
│   │                 Queue depth                  │  │               Fleet benchmark               │   │
│   │               Per-volume stats               │  │              Custom time range              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Metrics from Purity OS via phonehome · Pure1 aggregates and visualises                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IOPS = Input/Output Operations per Second; primary performance metric                                │
│  p50 latency = Median latency; 50% of operations faster than this value                               │
│  p99 latency = 99th percentile; 1% of operations slower; shows tail latency                           │
│  Bandwidth = Throughput in MB/s; saturates at network limit before IOPS typically                     │
│  Queue depth = Outstanding IO requests; high queue depth may indicate saturation                      │
│  Per-volume = Pure1 showing IOPS/latency per volume for workload isolation                            │
│  Workload ID = Pure1 AI classifying application type from IO signature                                │
│  IO size = Average IO request size in KB; small random vs large sequential                            │
│  Read/write ratio = Proportion of reads vs writes; impacts cache effectiveness                        │
│  Fleet benchmark = Pure1 comparing array performance to anonymised peer group                         │
│  Custom range = Pure1 UI allows selecting arbitrary time window for analysis                          │
│  Anomaly = Pure1 ML detecting performance deviation from established baseline                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```bash
ssh pureuser@<flashblade-ip>

# Array performance
purearray list --performance

# File system performance
purefs list --performance | sort -k3 -rn | head -20

# NFS/SMB protocol stats
pureprotocol list
```

## Performance via Pure1 API

```bash
TOKEN="<pure1-token>"

# Array performance metrics (last hour)
curl -s "https://api.pure1.purestorage.com/api/1.latest/metrics/history?names=array_performance&resource_names=<array-name>&resolution=30000&start_time=$(date -d '1 hour ago' +%s)000" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Volume performance
curl -s "https://api.pure1.purestorage.com/api/1.latest/metrics/history?names=volume_performance&resource_names=<array-name>%3A<vol-name>&resolution=30000" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

## Latency Investigation

High latency on a Pure FlashArray usually originates from the host side, not the array. Investigate in this order:

```text
1. Check array latency: purearray list --performance
   → If array latency OK (< 1ms) → problem is host-side or network

2. Check volume-level latency: purevol list --performance
   → Identify which volumes are slow

3. Check host queue depth: purehost list --performance
   → High queue depth on a specific host → host HBA or multipath issue

4. Check network path (iSCSI/FC port errors):
   pureport list --performance
   purehw list | grep -i "FC\|eth"

5. Check for snapshot overhead:
   puresnapshot list --space | sort -k5 -rh | head -5
   → Large snapshot trees add read amplification
```

## Performance Benchmarking (fio)

Run from the host after verifying the issue is host-observable:

```bash
# Sequential read (throughput baseline)
fio --name=seqread --ioengine=libaio --iodepth=32 --rw=read \
  --bs=1m --direct=1 --numjobs=4 --size=10g \
  --filename=/dev/sdX --runtime=60 --time_based

# Random read latency (latency baseline)
fio --name=randread_lat --ioengine=libaio --iodepth=1 --rw=randread \
  --bs=4k --direct=1 --numjobs=1 --size=10g \
  --filename=/dev/sdX --runtime=60 --time_based --lat_percentiles=1 \
  --percentile_list=50,90,99,99.9
```

## Common Performance Issues

| Symptom | Probable cause | Investigation |
|---|---|---|
| High write latency only | Snapshot tree overhead, or full array cache | Check snapshot usage; check array load |
| Latency spikes at regular intervals | Host-side I/O scheduling (e.g., backup jobs) | Correlate spike times with backup schedule |
| Low throughput on iSCSI | MTU mismatch (jumbo frames) | Verify MTU 9000 end-to-end |
| Low throughput on FC | Single path only (multipath not configured) | `pureport list --performance` — check per-port balance |
| High queue depth | HBA driver issue or host CPU saturation | Check host `iostat -x` and HBA error counters |
| Array load > 80% sustained | Over-provisioned workload or snapshot amplification | Review workload profile; consider adding shelves |
