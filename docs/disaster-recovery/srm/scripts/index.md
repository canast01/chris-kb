# SRM Scripts

SRM automation scripts use PowerCLI and the VMware.VimAutomation.Srm module. Scripts requiring elevated permissions (test failover, plan execution) must authenticate with a dedicated DR-operator service account, not a shared admin credential. All scripts write structured output to a log file for audit trail purposes.

**Available scripts:**

| Script | Language | Purpose |
|---|---|---|
| `srm_pg_status.ps1` | PowerCLI | List all protection groups and current RPO/status |
| `srm_test_failover.ps1` | PowerCLI | Run test failover on a named recovery plan and verify cleanup |
| `srm_recovery_report.ps1` | PowerCLI | Generate HTML recovery readiness report for all plans |
| `srm_replication_lag.ps1` | PowerCLI | Check vSphere Replication lag for all protected VMs |

**Script pattern — protection group status:**
```powershell
Connect-SrmServer -SrmServerAddress $SrmFqdn -Credential $Cred
Get-SRMProtectionGroup | Select-Object Name, State, ProtectionState |
  Format-Table -AutoSize
Disconnect-SrmServer -Confirm:$false
```
