# Performance & Statistics

> Part of the Dell PowerScale (Isilon) CLI Reference.
## Cluster-Level Stats

```bash
# Live cluster-wide stats
isi statistics system list

# Per-client breakdown
isi statistics client list

# Protocol-level stats
isi statistics protocol list

# Filter by specific protocol
isi statistics protocol list --protocol nfs3
isi statistics protocol list --protocol smb2
```

## Node-Level Stats

```bash
# Stats per node
isi statistics node list
isi statistics node list --node-id <node_id>
```

## Drive & Disk Stats

```bash
isi statistics drive list
```

## Throughput & IOPS

```bash
# Active NFS client stats
isi statistics query current --stats node.clientstats.active.nfs

# Active SMB client stats
isi statistics query current --stats node.clientstats.active.smb2
```

## Historical Performance

```bash
isi statistics history list
```

## Performance Thresholds

| Metric | Normal | Action if Exceeded |
|---|---|---|
| Node CPU utilization | < 70% | Investigate top protocol clients |
| Disk latency | < 10 ms | Check drives; consider SSD tier |
| Network throughput | < 80% link capacity | Review top clients |

## InsightIQ / CloudPools Analysis

Dell PowerScale integrates with InsightIQ for historical performance trending and capacity forecasting. If InsightIQ is deployed:
- Access via the InsightIQ web UI
- Reports available: protocol throughput, latency, client activity, node utilization

## Common Issues

| Symptom | Check | Action |
|---|---|---|
| High latency on NFS | `isi statistics protocol list --protocol nfs3` | Identify top clients |
| One node overloaded | Node stats | Review SmartConnect zone policy |
| Drive latency high | `isi statistics drive list` | Check for failing drives |
| Protocol stats unavailable | OneFS version | Verify stats collection enabled |
