# Datastores

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

## List Datastores

```powershell
# All datastores
Get-Datastore

# Datastores with capacity and free space
Get-Datastore | Select-Object Name, CapacityGB, FreeSpaceGB,
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpaceGB / $_.CapacityGB) * 100, 1)}} |
    Sort-Object UsedPct -Descending

# Datastores below 20% free
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.2 } |
    Select-Object Name, @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}}, @{N="CapGB";E={[math]::Round($_.CapacityGB,1)}}
```

## Datastore Clusters (SDRS)

```powershell
# List datastore clusters
Get-DatastoreCluster

# Datastores within a cluster
Get-DatastoreCluster -Name "<name>" | Get-Datastore

# Cluster capacity summary
Get-DatastoreCluster | Select-Object Name, CapacityGB, FreeSpaceGB,
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpaceGB / $_.CapacityGB) * 100, 1)}}
```

## Datastore to VM Mapping

```powershell
# VMs on a specific datastore
Get-Datastore -Name "<datastore_name>" | Get-VM | Select-Object Name, PowerState

# Datastore per VM
Get-VM | ForEach-Object {
    $vm = $_
    $vm | Get-Datastore | ForEach-Object {
        [PSCustomObject]@{ VM = $vm.Name; Datastore = $_.Name }
    }
}
```

## Datastore Hosts

```powershell
# Hosts that mount a specific datastore
Get-Datastore -Name "<datastore_name>" | Get-VMHost | Select-Object Name, ConnectionState
```

## Export Datastore Report

```powershell
Get-Datastore | Select-Object Name,
    @{N="Type";E={$_.Type}},
    @{N="CapacityGB";E={[math]::Round($_.CapacityGB,1)}},
    @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}},
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpaceGB / $_.CapacityGB) * 100, 1)}} |
    Sort-Object UsedPct -Descending |
    Export-Csv -Path datastores.csv -NoTypeInformation
```

## Datastore Maintenance

```powershell
# Enter maintenance mode (SDRS must be configured, or migrate VMs first)
$ds = Get-Datastore "<datastore_name>"
$storMgr = Get-View StorageResourceManager
$storMgr.DatastoreEnterMaintenanceMode($ds.ExtensionData.MoRef)

# Refresh datastore space info
Get-Datastore "<datastore_name>" | Update-Datastore
```

## Capacity Thresholds

| Free Space | Action |
|---|---|
| > 30% | Healthy |
| 20–30% | Monitor closely |
| 10–20% | Alert — plan expansion or migration |
| < 10% | Emergency — VMs may power off or suspend |
