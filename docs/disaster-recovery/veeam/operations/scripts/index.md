# Veeam — Scripts

PowerShell scripts for Veeam automation use the Veeam PowerShell snap-in and should be scheduled via Windows Task Scheduler on the Backup Server. Scripts must load the snap-in and connect to VBR at the start of each execution, and disconnect cleanly at the end. Output should be written to a dated log file and emailed or pushed to a monitoring system.

| Script | Language | Purpose |
|---|---|---|
| `veeam_job_summary.ps1` | PowerShell | Queries all job sessions from last 24 hours; emails pass/warn/fail counts |
| `veeam_restore_point_age.ps1` | PowerShell | Reports oldest restore point per protected VM; alerts on stale restore points |
| `veeam_sobr_capacity.ps1` | PowerShell | Iterates SOBR extents; alerts when any extent exceeds 80% usage |
| `veeam_surebackup_trigger.ps1` | PowerShell | Triggers SureBackup job for critical group; parses result and posts to ticketing system |
| `veeam_backup_copy_health.ps1` | PowerShell | Confirms backup copy jobs have run within expected window; alerts on missed runs |

**Script conventions**

```powershell
Add-PSSnapin VeeamPSSnapIn -ErrorAction SilentlyContinue
Connect-VBRServer -Server "localhost"
# ... script logic ...
Disconnect-VBRServer
```

- Store VBR credentials using Windows Credential Manager or retrieve from CyberArk at runtime.
- Use `Try/Catch/Finally` blocks to ensure `Disconnect-VBRServer` is called even on error.
