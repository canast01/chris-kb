# SRM CLI Reference

SRM management is primarily performed via PowerCLI cmdlets from the `VMware.VimAutomation.Srm` module. Connect to the SRM server using `Connect-SrmServer` before running any cmdlets. The SRM REST API (available from SRM 8.3+) provides equivalent functionality for automation pipelines that prefer HTTP over PowerCLI.

| Cmdlet / Endpoint | Purpose |
|---|---|
| `Connect-SrmServer -SrmServerAddress <fqdn>` | Authenticate to SRM server |
| `Get-SRMProtectionGroup` | List all protection groups and their status |
| `Get-SRMRecoveryPlan` | List all recovery plans |
| `Test-SRMRecoveryPlan -RecoveryPlan <plan>` | Initiate a test failover |
| `Start-SRMRecoveryPlan -RecoveryPlan <plan>` | Execute a real recovery (failover/migration) |
| `Stop-SRMRecoveryPlan -RecoveryPlan <plan>` | Stop an in-progress recovery plan |
| `GET /api/vms` | SRM REST API: list protected VMs |
| `GET /api/protection-groups` | SRM REST API: list protection groups and status |
| `POST /api/recovery-plans/{id}/actions/test` | SRM REST API: trigger test failover |
