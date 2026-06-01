# Horizon — Scripts


<div class="kb-summary">
Scripts reference covering Get Session Count by Pool, Force Logoff Disconnected Sessions Older Than N Hours, Get All Desktops in Error State, Rebalance Instant Clone Pool, Export Entitlement Report and 3 more sections.
</div>

  Automation via PowerCLI / REST API
```
┌──────────────────────────────────────────────────────────┐
│  Connect-HVServer ──► token/session                      │
│                                                          │
│  Session Management        Pool Management               │
│  ┌──────────────────┐      ┌──────────────────────────┐  │
│  │ Get-HVLocalSession│     │ Get-HVPool               │  │
│  │ Invoke-HVSession  │     │ Get-HVMachine -ErrorState│  │
│  │ Logoff            │     │ Remove-HVDesktop         │  │
│  └──────────────────┘      └──────────────────────────┘  │
│                                                          │
│  Reporting                 REST API (Bearer token)        │
│  ┌──────────────────┐      ┌──────────────────────────┐  │
│  │ Entitlement      │      │ POST /rest/login          │  │
│  │ report CSV       │      │ GET  /inventory/v1/pools  │  │
│  │ Pool availability│      │ POST /action/refresh      │  │
│  │ alert script     │      └──────────────────────────┘  │
│  └──────────────────┘                                    │
└──────────────────────────────────────────────────────────┘
```
```
┌──────────────────────────────── VMware Horizon — Operational Scripts ─────────────────────────────────┐
│                                                                                                       │
│  PowerCLI Horizon View module and REST API scripts automate pool reporting,                           │
│  session management, golden image push, and licence capacity checks.                                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Reporting Scripts               │  │               Session Scripts               │   │
│   │           Get-HVPool | Export-Csv            │  │           Get-HVLocalSession (all)          │   │
│   │          Get-HVMachine | Ft Status           │  │             Disconnect-HVSession            │   │
│   │          Licence usage: API /usage           │  │            Send-HVSessionMessage            │   │
│   │        Pool capacity: available count        │  │          Remove-HVSession (logoff)          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Read-only scripts for reporting; destructive session ops require Horizon admin role.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Maintenance Scripts              │  │              REST API Examples              │   │
│   │        Start-HVMachineRecycle (push)         │  │               POST /rest/login              │   │
│   │           Reset-HVMachine (reboot)           │  │         GET /rest/inventory/v1/pools        │   │
│   │         Set-HVPool -Enable/-Disable          │  │         PUT /rest/config/pools/{id}         │   │
│   │         Rebuild stuck clone: remove          │  │           GET /rest/monitor/pools           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  PowerCLI scripts connect from jump host to Connection Server; REST API on port 443;                  │
│  use service account with minimum Horizon admin privileges.                                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Get-HVPool        = list all Horizon pools and their status                                          │
│  Get-HVMachine     = list desktop VMs and their state                                                 │
│  Get-HVLocalSession= list active and disconnected sessions                                            │
│  Disconnect-HVSession= disconnect user session without logoff                                         │
│  Remove-HVSession  = force logoff of a session                                                        │
│  Send-HVSessionMessage= send popup message to user sessions                                           │
│  Start-HVMachineRecycle= push golden image update to pool                                             │
│  Reset-HVMachine   = force reboot a desktop VM                                                        │
│  POST /rest/login  = obtain Horizon REST API session token                                            │
│  PUT /rest/config/pools= update pool configuration via REST                                           │
│  GET /rest/monitor = health monitor endpoints for CS/pools                                            │
│  Licence /usage    = REST endpoint for licence consumption reporting                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

---

## Force Logoff Disconnected Sessions Older Than N Hours

```powershell
$thresholdHours = 4
$cutoff = (Get-Date).AddHours(-$thresholdHours)

$stale = Get-HVLocalSession | Where-Object {
    $_.SessionData.SessionState -eq "DISCONNECTED" -and
    $_.SessionData.DisconnectTime -lt $cutoff
}

Write-Host "Stale disconnected sessions: $($stale.Count)"

$stale | ForEach-Object {
    Write-Host "Logging off: $($_.NamesData.UserName) on $($_.NamesData.MachineOrRDSServerName)"
    Invoke-HVSessionLogoff -HVSession $_ -Force
}
```

---

## Get All Desktops in Error State

```powershell
$errors = Get-HVDesktop | Where-Object { $_.Base.BasicState -eq "ERROR" }

if ($errors.Count -gt 0) {
    Write-Warning "Desktops in ERROR state: $($errors.Count)"
    $errors | Select-Object -ExpandProperty Base |
        Select-Object Name, BasicState, @{N="Pool";E={$_.DesktopSummaryData.DesktopPoolCN}} |
        Format-Table -AutoSize
} else {
    Write-Host "No desktops in error state."
}
```

---

## Rebalance Instant Clone Pool

Force the pool to reprovision desktops evenly across ESXi hosts:

```powershell
# Get pool
$pool = Get-HVPool -PoolName "pool-win10-float"

# Get all available (unassigned) desktops in the pool
$available = Get-HVDesktop -PoolName "pool-win10-float" |
    Where-Object { $_.Base.BasicState -eq "AVAILABLE" }

# Delete available desktops (pool will reprovision them fresh, spreading across hosts)
$available | ForEach-Object {
    Write-Host "Removing for rebalance: $($_.Base.Name)"
    Remove-HVDesktop -VMName $_.Base.Name -Confirm:$false
}
# Pool provisioning picks up the missing desktops automatically
```

---

## Export Entitlement Report

```powershell
$pools = Get-HVPool
$report = @()

foreach ($pool in $pools) {
    $entitlements = Get-HVEntitlement -ResourceType DESKTOP -ResourceId $pool.Id

    foreach ($ent in $entitlements) {
        $report += [PSCustomObject]@{
            Pool         = $pool.Base.Name
            DisplayName  = $pool.Base.DisplayName
            Principal    = $ent.UserOrGroupData.DisplayName
            PrincipalDN  = $ent.UserOrGroupData.AdDomain + "\" + $ent.UserOrGroupData.LoginName
            Type         = $ent.UserOrGroupData.GroupMembershipData.IsGroup ? "Group" : "User"
        }
    }
}

$report | Export-Csv -Path "horizon-entitlements-$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation
Write-Host "Exported $($report.Count) entitlement records"
```

---

## Bulk-Add AD Group Entitlements

```powershell
# Add multiple AD groups to a pool in one script
$poolName = "pool-win10-float"
$groups = @(
    "CORP\Horizon-Win10-Group1",
    "CORP\Horizon-Win10-Group2",
    "CORP\Horizon-Win10-Group3"
)

$pool = Get-HVPool -PoolName $poolName

foreach ($group in $groups) {
    $domain, $name = $group -split "\\"
    try {
        New-HVEntitlement -UserName $name -Domain $domain -ResourceName $poolName -Type DESKTOP
        Write-Host "Entitled: $group → $poolName"
    } catch {
        Write-Warning "Failed to entitle $group`: $_"
    }
}
```

---

## Get App Volumes Assignment Report

```powershell
# Requires App Volumes Manager REST API
$avmBase = "https://appvol-mgr.example.local"
$headers = @{ "Authorization" = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:<password>")) }

$assignments = Invoke-RestMethod -Uri "$avmBase/cv_api/assignments" -Headers $headers
$assignments | Select-Object computer_name, user_name, appstack_name, status |
    Export-Csv "appvolumes-assignments-$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation
Write-Host "Exported $($assignments.Count) App Volumes assignments"
```

---

## Alert on Pools Below Minimum Available Desktops

```powershell
$minAvailableRatio = 0.10  # alert if less than 10% available

Get-HVPool | ForEach-Object {
    $pool = $_
    $desktops = Get-HVDesktop -PoolName $pool.Base.Name
    $total = $desktops.Count
    $available = ($desktops | Where-Object { $_.Base.BasicState -eq "AVAILABLE" }).Count

    if ($total -gt 0) {
        $ratio = $available / $total
        if ($ratio -lt $minAvailableRatio) {
            Write-Warning "LOW AVAILABILITY: Pool $($pool.Base.Name) — $available/$total available ($([math]::Round($ratio*100,1))%)"
        }
    }
}
```
