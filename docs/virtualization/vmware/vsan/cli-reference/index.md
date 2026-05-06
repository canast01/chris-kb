# vSAN CLI Reference

Commonly used ESXi shell and PowerCLI commands for managing and troubleshooting vSAN clusters.

---

## Cluster Status

```bash
# From ESXi host shell
esxcli vsan cluster get
esxcli vsan storage list
esxcli vsan storage list | grep -i ssd
esxcli vsan storage list | grep -i hdd

# Disk groups
esxcli vsan storage list | grep -E "Display Name|Type|UUID"

# Network
esxcli vsan network list
esxcli vsan network ipconfig list
```

---

## Health & Diagnostics

```bash
# Summary health
esxcli vsan health cluster get
esxcli vsan health summary get

# Trace
esxcli vsan trace get

# VM objects
esxcli vsan debug object list
esxcli vsan debug object list | grep -i unhealthy
esxcli vsan debug object list | grep -i absent

# Resync
esxcli vsan debug resync list
esxcli vsan debug resync summary get

# Component status
esxcli vsan debug component list
```

---

## Disk Groups

```bash
# List disk groups
esxcli vsan storage list

# Per-disk stats
esxcli vsan storage stats get

# Evacuate disk group (before removal)
esxcli vsan storage evacuate -d <device_naa>

# Add disk to disk group
esxcli vsan storage add -s <ssd_naa> -d <capacity_naa>

# Remove disk group
esxcli vsan storage remove -s <ssd_naa>
```

---

## Capacity & Objects

```bash
# Datastore info
esxcli vsan datastore list

# Object count
esxcli vsan debug object list | wc -l

# Inaccessible objects
esxcli vsan debug object list | grep -v "Healthy"
```

---

## Networking (vSAN VMkernel)

```bash
# vSAN network adapters
esxcli vsan network list

# Validate unicast agent
esxcli vsan network ipconfig list

# Test connectivity between hosts
esxcli vsan debug network test
```

---

## PowerCLI — vSAN

```powershell
# Connect
Connect-VIServer <vcenter>

# Cluster config
Get-VsanClusterConfiguration -Cluster <cluster>

# Health check
Test-VsanClusterHealth -Cluster <cluster>

# Disk groups
Get-VsanDiskGroup -VMHost <host>
Get-VsanDisk -VMHost <host>

# Object health
Get-VsanView -Id VsanObjectSystem-vsan-object-system | ForEach-Object { $_.QueryObjectIdentities() }

# Resync status
Get-VsanResyncStatus -Cluster <cluster>

# Capacity
Get-VsanSpaceUsage -Cluster <cluster>

# Witness
Get-VsanFaultDomainConfiguration -Cluster <cluster>

# vSAN health service
$vhs = Get-VsanView -Id VsanVcClusterHealthSystem-vsan-cluster-health-system
$vhs.VsanQueryVcClusterHealthSummary((Get-Cluster <cluster>).ExtensionData.MoRef, $null, $null, $true, $null, $null, 'defaultView')
```

---

## Skyline Health (vSphere Client Context)

Accessed in vSphere Client → Cluster → Monitor → vSAN → Skyline Health

```bash
# From ESXi — equivalent checks
esxcli vsan health cluster get | grep -i fail
esxcli vsan health cluster get | grep -i warning

# vSAN performance service status
esxcli vsan perf get
```

---

## RVC Commands (Ruby vSphere Console — legacy)

```bash
# Connect to vSAN cluster via RVC
rvc <user>@<vcenter>

# vSAN summary
vsan.health.health_check <cluster_path>
vsan.disks_stats <cluster_path>
vsan.resync_dashboard <cluster_path>
vsan.obj_status_report <cluster_path>
vsan.object_info <cluster_path> <object_uuid>
vsan.proactive_rebalance_info <cluster_path>
vsan.cluster_info <cluster_path>
```
