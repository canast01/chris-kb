# Veeam — Diagnostics

## Log Locations

- VBR service log: `C:\ProgramData\Veeam\Backup\Svc.VeeamBackup.log`
- Job session logs: `C:\ProgramData\Veeam\Backup\Job_<JobName>\`
- Proxy logs: `C:\ProgramData\Veeam\Backup\` on each proxy server
- Linux agent logs: `/var/log/veeam/`
- Audit log: `C:\ProgramData\Veeam\Backup\Audit.log`

## Diagnostic Commands

```powershell
# Quick PowerShell view of last result per job
Get-VBRJob | Select-Object Name, LastResult, LastRun | Sort-Object LastResult

# List jobs with a non-success last result
Get-VBRJob | Where-Object { $_.LastResult -ne "Success" -and $_.LastResult -ne "None" } |
    Select-Object Name, LastResult, LastRun

# Check repository free space
Get-VBRBackupRepository | Select Name, FriendlyPath, Path,
  @{N="FreeMB";E={[math]::Round($_.GetContainer().CachedFreeSpace / 1MB)}}

# Check proxy status
Get-VBRViProxy | Select Name, Host, MaxTasksCount, IsDisabled

# Check Veeam service log (last 100 lines)
Get-Content "C:\ProgramData\Veeam\Backup\Svc.VeeamBackup.log" -Tail 100
```

## Support Bundle Collection

1. In the VBR console: Main Menu > Help > Support Information
2. Click "Export Logs" — select the job or time range relevant to the issue
3. The wizard packages logs from the Backup Server and relevant proxies into a single ZIP archive
