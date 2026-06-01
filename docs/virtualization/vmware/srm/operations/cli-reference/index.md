# SRM — CLI Reference


<div class="kb-summary">
CLI Reference reference covering SRM REST API — Recovery Plans, PowerCLI for SRM, Get Protected VM List, Get Recovery Plan History, Disconnect SRM Session.
</div>

  SRM CLI / API Access
```
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
┌───────────────────────────────────── VMware SRM — CLI Reference ──────────────────────────────────────┐
│                                                                                                       │
│  SRM is managed primarily via the vSphere Client plugin; srm-util.exe and the SRM                     │
│  REST API provide CLI automation for plan management and testing.                                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              srm-util Commands               │  │                 SRM REST API                │   │
│   │          srm-util srmcli list-plans          │  │             POST /api/rest/login            │   │
│   │          srm-util srmcli test-plan           │  │             GET /api/rest/plans             │   │
│   │           srm-util srmcli run-plan           │  │         POST /api/rest/plans/{}/run         │   │
│   │               srm-util showvms               │  │        GET /api/rest/plans/{}/status        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  srm-util.exe runs on SRM Server; REST API is accessible from any host on port 443.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             PowerCLI SRM Module              │  │             Diagnostic Commands             │   │
│   │              Connect-SrmServer               │  │             Get-SrmRecoveryPlan             │   │
│   │            Get-SrmProtectionGroup            │  │               srm-util history              │   │
│   │            Start-SrmRecoveryPlan             │  │                srm-util plans               │   │
│   │           Get-SrmReplicationGroup            │  │            Check replication lag            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  srm-util.exe runs on Windows SRM Server; PowerCLI module connects from jump host;                    │
│  REST API on port 443 of SRM Server FQDN.                                                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  srm-util      = SRM command-line utility on the SRM Server VM                                        │
│  srmcli        = sub-command for recovery plan operations                                             │
│  list-plans    = show all configured recovery plans                                                   │
│  test-plan     = run plan in test mode (bubble network)                                               │
│  run-plan      = trigger actual failover (use with caution)                                           │
│  showvms       = list VMs in protection group with replication status                                 │
│  history       = show previous plan run results and timestamps                                        │
│  Connect-SrmServer= PowerCLI; authenticate to SRM                                                     │
│  Start-SrmRecoveryPlan= PowerCLI; trigger plan test or failover                                       │
│  GET /api/rest/plans= list all recovery plans via REST                                                │
│  POST /api/rest/plans/{}/run= trigger plan execution via REST                                         │
│  Replication lag= time delta between protected and recovery replica                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```powershell

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
