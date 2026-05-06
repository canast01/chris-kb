# RVC Commands (Legacy)

> Part of the [vSAN CLI Reference](../).

RVC (Ruby vSphere Console) was the primary vSAN diagnostic tool before vSAN 6.7. It remains available on vCenter appliances for backwards-compatible diagnostics but most workflows have moved to `esxcli vsan` and the vSAN health service UI.

## Connecting to RVC

```bash
# SSH to vCenter appliance, then launch RVC
rvc <user>@<vcenter_fqdn>

# Example
rvc administrator@vsphere.local@vcenter.corp.local

# Navigate the object tree
ls
cd localhost/
cd localhost/<datacenter>/computers/<cluster>/
```

## Health Checks

```bash
# Full vSAN health check against a cluster
vsan.health.health_check <cluster_path>

# Example path: localhost/dc1/computers/prod-cluster/
vsan.health.health_check localhost/dc1/computers/prod-cluster/

# Quiet mode — only failed checks
vsan.health.health_check <cluster_path> --quiet
```

## Disk and Object Status

```bash
# Disk stats per host in the cluster
vsan.disks_stats <cluster_path>

# Object inventory and compliance state
vsan.obj_status_report <cluster_path>

# Detail for a specific object UUID
vsan.object_info <cluster_path> <object_uuid>
```

## Resync Dashboard

```bash
# Active resync operations (rebuilds, migrations)
vsan.resync_dashboard <cluster_path>

# Refresh every 10 seconds
vsan.resync_dashboard <cluster_path> --refresh-rate 10
```

## Rebalance

```bash
# View current rebalance status
vsan.proactive_rebalance_info <cluster_path>

# Cluster usage summary — per-host disk consumption
vsan.cluster_info <cluster_path>
```

## RVC vs Modern Alternatives

| RVC Command | Modern Equivalent |
|---|---|
| `vsan.health.health_check` | vSAN Health UI / `esxcli vsan health summary get` |
| `vsan.disks_stats` | `esxcli vsan storage stats get` |
| `vsan.resync_dashboard` | `esxcli vsan debug resync list` |
| `vsan.obj_status_report` | `esxcli vsan debug object list` |
| `vsan.cluster_info` | vSAN Skyline Health UI |

RVC is still useful for scripted checks against older vSAN clusters (6.0–6.5) where `esxcli vsan` commands are limited.
