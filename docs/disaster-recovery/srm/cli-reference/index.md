# SRM CLI Reference

SRM management is primarily performed via the `VMware.VimAutomation.Srm` PowerCLI module. Connect to the SRM server with `Connect-SrmServer` before running any cmdlets. The SRM REST API (available from SRM 8.3+) provides equivalent functionality for automation pipelines.

---

## Connection

Establish a session to both vCenter and SRM before running any operations.

```powershell
# Connect to vCenter first
Connect-VIServer -Server <vcenter_fqdn> -User administrator@vsphere.local -Password <pass>

# Connect to SRM server
Connect-SrmServer -SrmServerAddress <srm_fqdn> -User administrator@vsphere.local -Password <pass>

# Verify connection
$defaultSrmServer

# Disconnect when done
Disconnect-SrmServer
Disconnect-VIServer
```

---

## Protection Groups

Protection groups define which VMs are protected and how they map to the recovery site.

```powershell
# List all protection groups
Get-SRMProtectionGroup

# Get detail for a specific protection group
Get-SRMProtectionGroup -Name <group_name>

# List VMs in a protection group
Get-SRMProtectionGroup -Name <group_name> | Get-SRMProtectedVM

# Check protection group status
Get-SRMProtectionGroup | Select Name, State, ProtectionState
```

---

## Recovery Plans

Recovery plans define the failover sequence and IP customisation rules.

```powershell
# List all recovery plans
Get-SRMRecoveryPlan

# Show recovery plan details
Get-SRMRecoveryPlan -Name <plan_name> | Format-List

# List steps in a recovery plan
Get-SRMRecoveryPlan -Name <plan_name> | Get-SRMRecoveryPlanStep
```

---

## Test Failover

Test failover runs in an isolated network bubble and does not affect production. Always run a test before a real recovery.

```powershell
# Start a test failover
$plan = Get-SRMRecoveryPlan -Name <plan_name>
$plan.RecoveryPlanService.Start($plan.MoRef, (New-Object VMware.VimAutomation.Srm.Types.V1.RecoveryPlanRecoveryMode))

# Check test status
Get-SRMRecoveryPlan -Name <plan_name> | Select State, ActiveHistoryTask

# Clean up (remove test snapshot, restore network)
$plan.RecoveryPlanService.Cancel($plan.MoRef)
```

---

## Recovery (Planned Migration / Failover)

Real recovery — run only during a DR event or planned migration.

```powershell
# Execute planned migration (graceful, bidirectional)
Start-SRMRecoveryPlan -RecoveryPlan (Get-SRMRecoveryPlan -Name <plan_name>) -RecoveryMode Planned

# Execute emergency failover (one-way, no replication cleanup)
Start-SRMRecoveryPlan -RecoveryPlan (Get-SRMRecoveryPlan -Name <plan_name>) -RecoveryMode Failover

# Stop an in-progress plan
Stop-SRMRecoveryPlan -RecoveryPlan (Get-SRMRecoveryPlan -Name <plan_name>)
```

---

## REST API

SRM 8.3+ exposes a REST API at `https://<srm_fqdn>/api`.

```bash
# Authenticate
curl -k -X POST https://<srm_fqdn>/api/sessions   -H "Content-Type: application/json"   -d '{"username":"administrator@vsphere.local","password":"<pass>"}'

# List protection groups
curl -k -X GET https://<srm_fqdn>/api/groups   -H "Authorization: <token>"

# List recovery plans
curl -k -X GET https://<srm_fqdn>/api/plans   -H "Authorization: <token>"

# Trigger test failover
curl -k -X POST "https://<srm_fqdn>/api/plans/<plan_id>/actions/test"   -H "Authorization: <token>"
```
