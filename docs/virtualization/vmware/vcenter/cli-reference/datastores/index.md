# Datastores

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

---

## Datastores

```powershell
Get-Datastore
Get-Datastore | Select-Object Name, CapacityGB, FreeSpaceGB, @{N="UsedPct";E={[math]::Round((1-$_.FreeSpaceGB/$_.CapacityGB)*100,1)}} | Sort-Object UsedPct -Descending

# Datastores below threshold
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.2 } | Select-Object Name, FreeSpaceGB

# Datastore cluster
Get-DatastoreCluster
Get-DatastoreCluster | Get-Datastore
```
