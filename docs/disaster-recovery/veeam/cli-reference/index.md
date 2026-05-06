# Veeam CLI Reference

Veeam is managed via the Veeam PowerShell module (`Veeam.Backup.PowerShell`), loaded automatically in the Veeam PowerShell Console on the Backup Server. For remote execution, import the snap-in with `Add-PSSnapin VeeamPSSnapIn`. All cmdlets require a connection established with `Connect-VBRServer -Server localhost` (or remote server name).

| Cmdlet | Purpose | Example |
|---|---|---|
| `Get-VBRJob` | List all jobs | `Get-VBRJob | Select Name, JobType, LastResult` |
| `Get-VBRBackupSession` | List recent sessions | `Get-VBRBackupSession | Sort CreationTime -Desc | Select -First 20` |
| `Start-VBRJob` | Start a job manually | `Start-VBRJob -Job (Get-VBRJob -Name "prod-vm-daily")` |
| `Get-VBRRestorePoint` | List restore points | `Get-VBRRestorePoint -Name "vm01"` |
| `Get-VBRBackup` | List backup chains | `Get-VBRBackup | Select JobName, Id` |
| `Get-VBRRepository` | List repositories | `Get-VBRRepository | Select Name, FreeSpace, TotalSpace` |
| `Add-VBRViProxy` | Add vSphere proxy | `Add-VBRViProxy -Server "proxy01" -Type Vi` |
| `Get-VBRSANIntegration` | List SAN integrations | `Get-VBRSANIntegration` |
| `Get-VBRJob` (filter) | Find failed jobs | `Get-VBRJob | Where {$_.LastResult -eq "Failed"}` |
| `Export-VBRConfiguration` | Export config backup | `Export-VBRConfiguration -Path C:\vbr-config-backup.xml` |
