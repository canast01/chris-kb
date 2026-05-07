# Veeam CLI Reference

Veeam is managed via the `Veeam.Backup.PowerShell` module, loaded automatically in the Veeam PowerShell Console on the Backup Server. For remote execution, load it with `Add-PSSnapin VeeamPSSnapIn` then `Connect-VBRServer -Server <backup_server>`.

---

## Connection

```powershell
# Load the Veeam snap-in (if not already loaded)
Add-PSSnapin VeeamPSSnapIn

# Connect to local Backup Server
Connect-VBRServer -Server localhost

# Connect to a remote Backup Server
Connect-VBRServer -Server <hostname> -User <domain\user> -Password <pass>

# Disconnect
Disconnect-VBRServer
```

---

## Jobs

Jobs are the primary operational unit in Veeam.

```powershell
# List all backup jobs with last result
Get-VBRJob | Select Name, JobType, LastResult, NextRun

# Find failed jobs
Get-VBRJob | Where-Object { $_.LastResult -eq "Failed" }

# Start a job manually
Start-VBRJob -Job (Get-VBRJob -Name "prod-vm-daily")

# Stop a running job
Stop-VBRJob -Job (Get-VBRJob -Name "prod-vm-daily")
```

---

## Sessions & History

```powershell
# List recent sessions, newest first
Get-VBRBackupSession | Sort-Object CreationTime -Descending | Select -First 20

# Show session result and duration for a job
Get-VBRBackupSession | Where-Object { $_.JobName -eq "prod-vm-daily" } |
  Select JobName, State, Result, CreationTime, EndTime
```

---

## Restore Points

```powershell
# List restore points for a VM
Get-VBRRestorePoint -Name "vm01" | Select Name, CreationTime, IsCorrupted

# Find latest restore point for a VM
Get-VBRRestorePoint -Name "vm01" | Sort-Object CreationTime -Descending | Select -First 1

# Find restore points for all VMs in a job
Get-VBRBackup -Name "prod-vm-daily" | Get-VBRRestorePoint
```

---

## VM Restore

```powershell
# Instant VM recovery to original location
$rp = Get-VBRRestorePoint -Name "vm01" | Sort-Object CreationTime -Descending | Select -First 1
Start-VBRRestoreVM -RestorePoint $rp -Reason "DR test"

# Full VM restore
Start-VBRVMFLRRestore -RestorePoint $rp

# File-level restore (Windows)
Start-VBRWindowsFileRestore -RestorePoint $rp
```

---

## Infrastructure

```powershell
# List repositories with free/total space
Get-VBRRepository | Select Name,
  @{N="FreeTB"; E={[math]::Round($_.FreeSpace/1TB,2)}},
  @{N="TotalTB"; E={[math]::Round($_.TotalSpace/1TB,2)}}

# List proxies
Get-VBRViProxy

# List protected VMs
Get-VBRProtectedVM
```

---

## Configuration Backup

```powershell
# Export configuration backup
Export-VBRConfiguration -Path "C:\vbr-config-backup.xml"

# Check last config backup
Get-VBRConfigurationDatabaseBackup
```
