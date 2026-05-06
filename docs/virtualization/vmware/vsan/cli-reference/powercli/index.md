# PowerCLI — vSAN

> Part of the [vSAN CLI Reference](../).

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
