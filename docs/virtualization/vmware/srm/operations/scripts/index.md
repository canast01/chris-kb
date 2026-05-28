# SRM — Scripts

```text
  SRM Automation via PowerCLI + REST API
┌──────────────────────────────────────────────────────────────┐
│  Connect-SrmServer ──► $srm.ExtensionData.*                  │
│                                                              │
│  Reporting Scripts             Operational Scripts           │
│  ┌──────────────────────┐      ┌──────────────────────────┐  │
│  │ Protected VMs +      │      │ Run test recovery         │  │
│  │  RPO compliance CSV  │      │ Monitor request state    │  │
│  │ Last test date +     │      │ Alert: plans not tested  │  │
│  │  result per plan     │      │  in 30 days              │  │
│  │ Recovery plan        │      │ Check placeholder VMs    │  │
│  │  summary export      │      │  missing at recov. site  │  │
│  └──────────────────────┘      └──────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────── VMware SRM — Operational Scripts ───────────────────────────────────┐
│                                                                                                       │
│  SRM operational scripts use PowerCLI, srm-util, and the REST API to automate                         │
│  DR test scheduling, plan reporting, replication status, and compliance tracking.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Replication Status Scripts          │  │              Compliance Scripts             │   │
│   │           Get-SrmReplicationGroup            │  │            Get plan last-run date           │   │
│   │               Check lag per VM               │  │              Alert if >90 days              │   │
│   │            Report: RPO compliance            │  │            Export plan status CSV           │   │
│   │             srm-util showvms lag             │  │            RTO achieved vs target           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Replication lag and test compliance are the two key SRM health metrics to track.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Plan Management Scripts            │  │             REST API Automation             │   │
│   │             Get-SrmRecoveryPlan              │  │             GET /api/rest/plans             │   │
│   │         Start-SrmRecoveryPlan -Test          │  │         GET /api/rest/plans/{}/runs         │   │
│   │          Get plan history: all runs          │  │         GET /api/rest/vms (prot VMs)        │   │
│   │          Export to HTML/CSV report           │  │         POST /api/rest/plans/{}/test        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  PowerCLI connects from jump host to SRM Server; REST API on port 443;                                │
│  scripts need SRM administrator role to trigger plan tests.                                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Get-SrmReplicationGroup= PowerCLI; list replication groups and status                                │
│  Get-SrmRecoveryPlan  = PowerCLI; list recovery plans                                                 │
│  Start-SrmRecoveryPlan= PowerCLI; trigger test or failover                                            │
│  -Test flag    = run in test mode; no production impact                                               │
│  srm-util showvms= show protected VM list and replication lag                                         │
│  GET /api/rest/plans/{}/runs= list all plan run history                                               │
│  POST /api/rest/plans/{}/test= trigger test via REST                                                  │
│  RPO compliance= lag < RPO target for each protected VM                                               │
│  90-day alert  = compliance: test within 90 days of last run                                          │
│  CSV report    = export plan status for DR governance reporting                                       │
│  RTO vs target = compare achieved vs agreed RTO                                                       │
│  Plan run date = stored in SRM DB; queryable via REST API                                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Get All Protected VMs and RPO Compliance

```powershell
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
$results = @()

foreach ($pg in $pgs) {
    $vms = $srm.ExtensionData.Protection.ListProtectedVms($pg)
    foreach ($vm in $vms) {
        # Get last replication time from vSphere Replication if applicable
        $vrState = $vm.ReplicationState

        $results += [PSCustomObject]@{
            ProtectionGroup  = $pg.Name
            VMName           = $vm.Vm.Name
            State            = $vm.State
            ReplicationState = $vrState
        }
    }
}

$results | Export-Csv "srm-protected-vms-$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation
Write-Host "Exported $($results.Count) protected VMs"
```

---

## Get Last Test Failover Date and Result

```powershell
$plans = $srm.ExtensionData.Recovery.ListPlans()
$testResults = @()

foreach ($plan in $plans) {
    $history = $srm.ExtensionData.Recovery.GetHistory($plan)
    $lastTest = $history | 
        Where-Object { $_.RecoveryType -eq "TEST" } | 
        Sort-Object StartTime -Descending | 
        Select-Object -First 1
    
    $testResults += [PSCustomObject]@{
        Plan          = $plan.Name
        LastTestDate  = if ($lastTest) { $lastTest.StartTime } else { "Never" }
        Result        = if ($lastTest) { $lastTest.ResultState } else { "None" }
        Duration      = if ($lastTest -and $lastTest.EndTime) { 
                          ($lastTest.EndTime - $lastTest.StartTime).TotalMinutes
                        } else { "N/A" }
    }
}

$testResults | Format-Table -AutoSize
$testResults | Export-Csv "srm-test-history-$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation
```

---

## Alert on Plans Not Tested in 30 Days

```powershell
$plans = $srm.ExtensionData.Recovery.ListPlans()
$threshold = (Get-Date).AddDays(-30)

foreach ($plan in $plans) {
    $history = $srm.ExtensionData.Recovery.GetHistory($plan)
    $lastTest = $history | 
        Where-Object { $_.RecoveryType -eq "TEST" } | 
        Sort-Object StartTime -Descending | 
        Select-Object -First 1

    if (-not $lastTest -or $lastTest.StartTime -lt $threshold) {
        $lastDate = if ($lastTest) { $lastTest.StartTime } else { "Never" }
        Write-Warning "OVERDUE: Recovery Plan '$($plan.Name)' — last test: $lastDate"
    }
}
```

---

## Check Placeholder VMs Exist at Recovery Site

```powershell
# Connect to recovery site vCenter
$recoveryVC = Connect-VIServer -Server vcenter-recovery.example.local

$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
$missingPlaceholders = @()

foreach ($pg in $pgs) {
    $vms = $srm.ExtensionData.Protection.ListProtectedVms($pg)
    foreach ($vm in $vms) {
        # Check if placeholder exists at recovery site
        $placeholder = Get-VM -Server $recoveryVC -Name $vm.Vm.Name -ErrorAction SilentlyContinue
        if (-not $placeholder) {
            $missingPlaceholders += $vm.Vm.Name
        }
    }
}

if ($missingPlaceholders.Count -gt 0) {
    Write-Warning "Missing placeholder VMs at recovery site:"
    $missingPlaceholders | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "All placeholder VMs present at recovery site."
}
```

---

## Export Recovery Plan Summary

```powershell
$plans = $srm.ExtensionData.Recovery.ListPlans()
$summary = @()

foreach ($plan in $plans) {
    $details = $srm.ExtensionData.Recovery.GetPlan($plan)
    $pgs = $srm.ExtensionData.Recovery.GetProtectionGroups($plan)
    $vmCount = ($pgs | ForEach-Object { 
        $srm.ExtensionData.Protection.ListProtectedVms($_) 
    }).Count

    $summary += [PSCustomObject]@{
        PlanName   = $plan.Name
        State      = $details.Info.State
        VMCount    = $vmCount
        ProtectionGroups = ($pgs | Select-Object -ExpandProperty Name) -join "; "
    }
}

$summary | Export-Csv "srm-plan-summary.csv" -NoTypeInformation
$summary | Format-Table -AutoSize
```
