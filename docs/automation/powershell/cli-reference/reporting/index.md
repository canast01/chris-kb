# Reporting

> Part of the PowerShell CLI Reference.

---

```powershell
# Export VM inventory to CSV
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB, @{N="Datastore";E={($_ | Get-Datastore).Name}} | Export-Csv -Path vm_inventory.csv -NoTypeInformation

# Host summary
Get-VMHost | Select-Object Name, Version, @{N="CPU%";E={[math]::Round($_.CpuUsageMhz / $_.CpuTotalMhz * 100, 1)}}, @{N="Mem%";E={[math]::Round($_.MemoryUsageGB / $_.MemoryTotalGB * 100, 1)}} | Format-Table

# Snapshot report
Get-VM | Get-Snapshot | Select-Object VM, Name, Created, @{N="SizeGB";E={[math]::Round($_.SizeGB, 2)}} | Sort-Object SizeGB -Descending
```
