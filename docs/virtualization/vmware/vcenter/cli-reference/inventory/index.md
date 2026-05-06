# Inventory & Reporting

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

---

## Inventory & Reporting

```powershell
# VM inventory to CSV
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB,
  @{N="VMHost";E={$_.VMHost.Name}},
  @{N="Cluster";E={$_.VMHost.Parent.Name}},
  @{N="Datastore";E={($_ | Get-Datastore).Name -join ";"}},
  @{N="GuestOS";E={$_.Guest.OSFullName}},
  @{N="IP";E={$_.Guest.IPAddress -join ";"}} |
  Export-Csv -Path vm_inventory.csv -NoTypeInformation

# Host inventory
Get-VMHost | Select-Object Name, Version, Build, Manufacturer, Model,
  @{N="CPUModel";E={$_.ProcessorType}},
  @{N="NumCPU";E={$_.NumCpu}},
  @{N="MemGB";E={[math]::Round($_.MemoryTotalGB,0)}},
  ConnectionState, PowerState |
  Export-Csv -Path host_inventory.csv -NoTypeInformation
```
