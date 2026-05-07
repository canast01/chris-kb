# VPLEX Consistency Groups

Consistency groups (CGs) in VPLEX ensure that a set of virtual volumes is treated as a crash-consistent unit during failover and recovery operations.
## List Consistency Groups

```bash
VPlexcli:/> ll /clusters/cluster-1/consistency-groups/
VPlexcli:/> ll /clusters/cluster-2/consistency-groups/
```

## View CG Details

```bash
VPlexcli:/> ll /clusters/cluster-1/consistency-groups/<cg_name>/
```

Key attributes:
- `operational-status` — should be `ok`
- `type` — `local` or `distributed`
- `virtual-volumes` — list of member volumes

## Create a Consistency Group

```bash
VPlexcli:/> consistency-group create --name <cg_name> --cluster-name cluster-1
```

## Add Volumes to a CG

```bash
VPlexcli:/> consistency-group add-virtual-volume \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg_name> \
    --virtual-volume /clusters/cluster-1/virtual-volumes/<vol_name>
```

## Remove a Volume from a CG

```bash
VPlexcli:/> consistency-group remove-virtual-volume \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg_name> \
    --virtual-volume /clusters/cluster-1/virtual-volumes/<vol_name>
```

## Distributed Consistency Groups

For Metro configurations, CGs span both clusters:

```bash
VPlexcli:/> ll /clusters/cluster-1/consistency-groups/<cg_name>/
# Check: type = distributed
# Check: operational-status = ok on both clusters
```

## Detach / Re-attach CG (Metro Failover)

```bash
# Detach from cluster-2 (planned maintenance or failover)
VPlexcli:/> consistency-group detach \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg_name>

# Re-attach after recovery
VPlexcli:/> consistency-group attach \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg_name>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| CG degraded | Check cluster connectivity | Investigate inter-cluster link |
| CG detached | Planned or unplanned detach | Re-attach after recovery |
| Volume not in CG | Missed during provisioning | Add via `add-virtual-volume` |
