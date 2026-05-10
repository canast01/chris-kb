# Pure1 — Performance

Pure1 retains performance data for all registered arrays — IOPS, bandwidth, latency, and queue depth — with up to 1 year of history and anomaly detection via AI-powered analytics.

## Key Metrics

| Metric | Definition | Healthy range |
|---|---|---|
| **Read/Write IOPS** | I/O operations per second | Array-dependent; see model spec |
| **Read/Write Bandwidth** | MB/s throughput | Array-dependent |
| **Read/Write Latency** | Average response time in µs | < 1ms read, < 1ms write (FlashArray//XL) |
| **Queue Depth** | Outstanding I/O in flight | < 32 sustained; spikes are normal |
| **Load** | % of array processing capacity used | < 80% sustained |
| **Data Reduction** | Combined dedup + compression ratio | Workload-dependent |

## Viewing Performance in Pure1

**Pure1 → Arrays → select array → Performance tab**

- Toggle between Read / Write / Combined
- Zoom to specific time windows (1h, 6h, 24h, 7d, 30d, 1y)
- Compare multiple arrays side-by-side
- AI-powered anomaly highlights shown as orange bands

**Pure1 → Analytics → Workload Planner** — capacity and performance forecasting.

## Performance via CLI

```bash
ssh pureuser@<flasharray-ip>

# Current array-level IOPS, bandwidth, latency
purearray list --performance

# Per-volume performance
purevol list --performance | sort -k3 -rn | head -20   # sort by read IOPS

# Host-level performance
purehost list --performance

# Historical stats for a volume (last 24h)
purevol list VOL_NAME --historical 1d

# Protocol-level stats (FC vs iSCSI)
pureport list --performance
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

```
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
