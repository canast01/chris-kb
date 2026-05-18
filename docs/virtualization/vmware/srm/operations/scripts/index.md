# SRM — Scripts

```
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

Requires: VMware.VimAutomation.Srm PowerShell module (installed with PowerCLI)

---

## Connect to SRM

```powershell
Import-Module VMware.VimAutomation.Srm
Connect-VIServer -Server vcenter-protected.corp.local
$srm = Connect-SrmServer -SrmServerAddress srm-protected.corp.local `
  -Credential (Get-Credential)
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
$recoveryVC = Connect-VIServer -Server vcenter-recovery.corp.local

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
