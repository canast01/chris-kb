# ONTAP — Components

## Core Components

| Component | Description |
|---|---|
| Cluster | The top-level administrative domain; 2–24 nodes sharing a common namespace and management interface |
| Node | An individual controller (AFF/FAS/ONTAP Select) running ONTAP; each node owns aggregates and serves data |
| HA Pair | Two nodes configured as an active-active pair sharing disk shelves; each node can take over the other's storage |
| Aggregate | A collection of RAID groups built from physical disks or SSDs; the raw storage pool owned by a node |
| SVM (Storage VM) | A logical tenant with its own namespace, network interfaces, protocols, and security domain; equivalent to a vFiler |
| Volume | A FlexVol (or FlexGroup) within an SVM; the unit of storage presented to hosts and clients |
| LUN | A block device within a volume, mapped to hosts via iSCSI or FC using igroups |
| LIF (Logical Interface) | A virtual IP or WWN endpoint on a node port; SVMs have data LIFs, the cluster has a cluster-management LIF |
| WAFL | Write Anywhere File Layout — ONTAP's internal filesystem that handles all I/O, snapshots, and deduplication |
| ONTAP Mediator | An external Linux VM used to provide a quorum witness for SnapMirror Business Continuity (SMBC) automatic failover |

## Aggregates

Aggregates are ONTAP's physical storage pools, built from disks or SSDs. Volumes reside within aggregates.

### List Aggregates

```bash
storage aggregate show
storage aggregate show -fields size,used,percent-used,state
```

### Check Aggregate Health

```bash
storage aggregate show -state !online
# Any aggregate not online requires immediate investigation

storage aggregate show-status
```

### Capacity Monitoring

```bash
# Show used/available per aggregate
storage aggregate show -fields size,used,available,percent-used

# Identify aggregates over 80% full
storage aggregate show -fields percent-used | awk '$2 > 80'
```

Alert thresholds (standard practice):
- **80%** — warning
- **90%** — critical; investigate and plan expansion

### RAID Status

```bash
storage aggregate show-status -aggregate <aggr_name>
```

RAID states:
- `normal` — healthy
- `degraded` — one or more disks failed; not yet broken
- `broken` — aggregate offline due to disk failures

### Disk Assignment

```bash
# Show unassigned disks
storage disk show -container-type unassigned

# Assign disk to node
storage disk assign -disk <disk_id> -owner <node_name>
```

### Add Disks to an Aggregate

```bash
storage aggregate add-disks -aggregate <aggr_name> -diskcount <n>
```

### Relocation (HA Pairs)

```bash
# Move aggregate ownership to partner node (planned maintenance)
storage aggregate relocation start -node <source_node> -destination <dest_node> -aggregates <aggr_name>

# Check relocation status
storage aggregate relocation show
```

### Common Issues

| Issue | Check | Action |
|---|---|---|
| Aggregate degraded | Disk failure | Check `storage disk show -broken` |
| Over 80% capacity | Volume growth | Add disks or move volumes |
| Aggregate offline | RAID broken | Engage NetApp support immediately |
| No space for new volumes | Fragmentation | Run `aggr efficiency` or add disks |
