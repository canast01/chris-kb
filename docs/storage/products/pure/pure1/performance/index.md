---
tags:
  - pure
description: "Performance reference covering Performance via Pure1 API, Latency Investigation, Performance Benchmarking (fio), Common Performance Issues."
---
# Pure1 — Performance

<div class="kb-summary">
Performance reference covering Performance via Pure1 API, Latency Investigation, Performance Benchmarking (fio), Common Performance Issues.

*Applies to: Pure1*
</div>

```d2
direction: down

latency_investigation: "Latency Investigation" {shape: rectangle}
performance_benchmarking_fio: "Performance Benchmarking (fio)" {shape: rectangle}
common_performance_issues: "Common Performance Issues" {shape: rectangle}

latency_investigation -> performance_benchmarking_fio: uses
performance_benchmarking_fio -> common_performance_issues: uses
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


```text title="Expected output"
seqread: (g=0): rw=read, bs=(R) 1024KiB-1024KiB, (W) 1024KiB-1024KiB, bs=1024KiB-1024KiB, bs_is_seq=on, ioengine=libaio, iodepth=32
...
seqread: Laying out IO file (1 file / 10240MiB)
seqread: Starting 4 processes
seqread: Jobs: 4 (f=4): [R(4)][100.0%][1247MiB/s][1247 IOPS][eta 00m:00s]
seqread: (groupid=0, jobs=4): io=40960MiB, aggrb=1247.3MiB/s, minb=311.8MiB/s, maxb=311.9MiB/s, mint=32827ms, maxt=32827ms
  read: IOPS=1247, BW=1247MiB/s (1308MB/s), aggrb=1247.3MiB/s
  lat (msec): min=25.4, max=156.2, avg=102.3, stdev=18.7
  percentiles (msec):
     |  1.00th=[  28.3],  5.00th=[  45.2], 10.00th=[  62.1], 20.00th=[  78.4],
     | 50.00th=[ 102.1], 90.00th=[ 128.6], 99.00th=[ 148.9], 99.90th=[ 155.3]

randread_lat: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, bs=4096B-4096B, ioengine=libaio, iodepth=1
...
randread_lat: Starting 1 process
randread_lat: Jobs: 1 (f=1): [r(1)][100.0%][2847 IOPS][11.4MiB/s][eta 00m:00s]
randread_lat: (groupid=0, jobs=1): io=10240MiB, aggrb=170.7MiB/s, minb=170.7MiB/s, maxb=170.7MiB/s, mint=59968ms, maxt=59968ms
  read: IOPS=43700, BW=170.7MiB/s (179MB/s), aggrb=170.7MiB/s
  lat (usec): min=18, max=8942, avg=22.8, stdev=156.3
  percentiles (usec):
     | 50.00th=[   21], 90.00th=[   24], 99.00th=[   31], 99.90th=[  187]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fio: filename=/dev/sdX: No such file or directory` | Replace `/dev/sdX` with the actual device path (e.g., `/dev/sda`, `/dev/nvme0n1`, or |
## Common Performance Issues

| Symptom | Probable cause | Investigation |
|---|---|---|
| High write latency only | Snapshot tree overhead, or full array cache | Check snapshot usage; check array load |
| Latency spikes at regular intervals | Host-side I/O scheduling (e.g., backup jobs) | Correlate spike times with backup schedule |
| Low throughput on iSCSI | MTU mismatch (jumbo frames) | Verify MTU 9000 end-to-end |
| Low throughput on FC | Single path only (multipath not configured) | `pureport list --performance` — check per-port balance |
| High queue depth | HBA driver issue or host CPU saturation | Check host `iostat -x` and HBA error counters |
| Array load > 80% sustained | Over-provisioned workload or snapshot amplification | Review workload profile; consider adding shelves |
