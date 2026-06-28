---
tags:
  - pure
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

## Common Performance Issues

| Symptom | Probable cause | Investigation |
|---|---|---|
| High write latency only | Snapshot tree overhead, or full array cache | Check snapshot usage; check array load |
| Latency spikes at regular intervals | Host-side I/O scheduling (e.g., backup jobs) | Correlate spike times with backup schedule |
| Low throughput on iSCSI | MTU mismatch (jumbo frames) | Verify MTU 9000 end-to-end |
| Low throughput on FC | Single path only (multipath not configured) | `pureport list --performance` — check per-port balance |
| High queue depth | HBA driver issue or host CPU saturation | Check host `iostat -x` and HBA error counters |
| Array load > 80% sustained | Over-provisioned workload or snapshot amplification | Review workload profile; consider adding shelves |
