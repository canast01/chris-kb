# SRM — CLI Reference

```
  SRM CLI / API Access
┌──────────────────────────────────────────────────────────────┐
│  SRM REST API (vCenter SSO token)                            │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ POST /rest/com/vmware/cis/session → session token    │    │
│  │ GET  /api/vcenter/dr/recovery/plans                  │    │
│  │ POST /api/vcenter/dr/recovery/plans/<id>/start       │    │
│  │      { "recovery_type": "TEST" | "FAILOVER" }        │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  PowerCLI (VMware.VimAutomation.Srm)                         │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Connect-SrmServer -SrmServerAddress <fqdn>           │    │
│  │ $srm.ExtensionData.Recovery.ListPlans()              │    │
│  │ $srm.ExtensionData.Protection.ListProtectionGroups() │    │
│  │ $srm.ExtensionData.Recovery.Start($plan, "TEST")     │    │
│  │ $srm.ExtensionData.Recovery.Start($plan, "CLEANUP")  │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## SRM REST API Authentication

```bash
# SRM REST API uses vCenter SSO session tokens
# Authenticate against vCenter SSO first:
TOKEN=$(curl -sk -X POST \
  "https://vcenter-protected.example.local/rest/com/vmware/cis/session" \
  -u "administrator@vsphere.local:<password>" \
  -H "Content-Type: application/json" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['value'])")

# SRM REST API base: https://srm-server.example.local/api/vcenter/dr/recovery
```

---

## SRM REST API — Recovery Plans

```bash
# List all Recovery Plans
curl -sk -H "vmware-api-session-id: $TOKEN" \
  "https://vcenter-protected.example.local/api/vcenter/dr/recovery/plans" | \
  python3 -m json.tool

# Get Recovery Plan status
PLAN_ID="<recovery-plan-moref>"
curl -sk -H "vmware-api-session-id: $TOKEN" \
  "https://vcenter-protected.example.local/api/vcenter/dr/recovery/plans/$PLAN_ID" | \
  python3 -m json.tool

# Start a test recovery
curl -sk -X POST -H "vmware-api-session-id: $TOKEN" \
  "https://vcenter-protected.example.local/api/vcenter/dr/recovery/plans/$PLAN_ID/start" \
  -H "Content-Type: application/json" \
  -d '{"recovery_type": "TEST"}'

# Start a real recovery (DR failover)
curl -sk -X POST -H "vmware-api-session-id: $TOKEN" \
  "https://vcenter-protected.example.local/api/vcenter/dr/recovery/plans/$PLAN_ID/start" \
  -H "Content-Type: application/json" \
  -d '{"recovery_type": "FAILOVER"}'

# Cancel a running recovery
curl -sk -X POST -H "vmware-api-session-id: $TOKEN" \
  "https://vcenter-protected.example.local/api/vcenter/dr/recovery/plans/$PLAN_ID/cancel"
```

---

## PowerCLI for SRM

```powershell
# Connect to vCenter (SRM operations run through vCenter)
Connect-VIServer -Server vcenter-protected.example.local
$srm = Connect-SrmServer -SrmServerAddress srm-protected.example.local `
  -Credential (Get-Credential)

# List all Recovery Plans
$plans = $srm.ExtensionData.Recovery.ListPlans()
$plans | Select-Object MoRef, Name

# Get Recovery Plan details
$plan = $plans | Where-Object { $_.Name -eq "SQL-DR-Plan" }
$planDetails = $srm.ExtensionData.Recovery.GetPlan($plan)

# Get Protection Groups
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
$pgs | Select-Object MoRef, Name

# Get VMs in a Protection Group
$pg = $pgs | Where-Object { $_.Name -eq "SQL-PG" }
$pgInfo = $srm.ExtensionData.Protection.QueryReplicationState($pg)

# Run a test recovery
$planRef = $plan.MoRef
$srm.ExtensionData.Recovery.Start($planRef, "TEST")

# Monitor recovery task status
$history = $srm.ExtensionData.Recovery.GetHistory($planRef)
$history | Select-Object StartTime, EndTime, ResultState, Percent

# Clean up after test
$srm.ExtensionData.Recovery.Start($planRef, "CLEANUP")
```

---

## Get Protected VM List

```powershell
# List all protected VMs and their replication state
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()

foreach ($pg in $pgs) {
    $pgInfo = $srm.ExtensionData.Protection.ListProtectedVms($pg)
    foreach ($vm in $pgInfo) {
        [PSCustomObject]@{
            ProtectionGroup = $pg.Name
            VM              = $vm.Vm.Name
            State           = $vm.State
            ReplicationState = $vm.ReplicationState
        }
    }
} | Format-Table -AutoSize
```

---

## Get Recovery Plan History

```powershell
$plans = $srm.ExtensionData.Recovery.ListPlans()

foreach ($plan in $plans) {
    $history = $srm.ExtensionData.Recovery.GetHistory($plan)
    foreach ($h in $history) {
        [PSCustomObject]@{
            Plan        = $plan.Name
            StartTime   = $h.StartTime
            EndTime     = $h.EndTime
            Type        = $h.RecoveryType
            Result      = $h.ResultState
        }
    }
} | Sort-Object StartTime | Format-Table -AutoSize
```

---

## Disconnect SRM Session

```powershell
Disconnect-SrmServer -SrmServer $srm -Confirm:$false
Disconnect-VIServer -Server * -Confirm:$false
```
