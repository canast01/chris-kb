# SnapMirror — Components

> Part of the [SnapMirror Architecture](../) reference.

---

## Components

- **Source volume** — read/write volume on the source cluster; the origin of replicated data
- **Destination volume** — DP (data protection) type, read-only; managed by the replication engine
- **SnapMirror policy** — defines rules, schedule, and retention for the relationship
- **Cluster peer relationship** — trust relationship between two ONTAP clusters; prerequisite for all SnapMirror
- **SVM peer relationship** — required for cross-SVM replication; establishes peer trust at the data SVM layer
- **Intercluster LIFs** — dedicated network interfaces used exclusively for SnapMirror replication traffic

## Sizing Guidelines

Estimate required replication bandwidth using:

```
Required bandwidth = (Daily change rate × source volume size) / replication window (seconds)
```

| Replication Type | Latency Requirement | Bandwidth Requirement |
|---|---|---|
| SnapMirror Async | No strict requirement | Based on change rate and schedule window |
| SnapMirror Sync | <5ms RTT (sustained) | Write throughput of source workload |
| SMBC | <5ms RTT (sustained) | Write throughput of consistency group |

For SnapMirror Sync and SMBC, sustained inter-site latency above 10ms will cause automatic demotion to async mode.
