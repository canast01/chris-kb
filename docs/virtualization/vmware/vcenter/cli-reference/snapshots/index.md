# Snapshots

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

---

## Snapshots

```powershell
Get-Snapshot -VM <name>
Get-VM | Get-Snapshot | Select-Object VM, Name, Created, @{N="SizeGB";E={[math]::Round($_.SizeGB,2)}} | Sort-Object SizeGB -Descending

New-Snapshot -VM <name> -Name "pre-patch-$(Get-Date -Format yyyy-MM-dd)" -Memory:$false -Quiesce:$false
Remove-Snapshot -Snapshot (Get-Snapshot -VM <name> -Name <snap_name>) -Confirm:$false
Remove-Snapshot -VM <name> -RemoveChildren -Confirm:$false

# Revert
Set-VM -VM <name> -Snapshot (Get-Snapshot -VM <name> -Name <snap_name>) -Confirm:$false
```
