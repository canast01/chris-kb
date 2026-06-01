# PowerShell — Script Reference


<div class="kb-summary">
Script Reference reference covering VM Health Report, Datastore Utilization Alert.
</div>

## VM Health Report

Generates a per-cluster VM health report: power state, CPU/memory, snapshot age, and datastore utilization. Outputs to CSV and console.

```powershell
# vm-health-report.ps1
# Usage: .\vm-health-report.ps1 -vCenter <hostname> -OutputPath .\report.csv

param(
    [Parameter(Mandatory)] [string] $vCenter,
    [string] $OutputPath = ".\vm-health-$(Get-Date -Format 'yyyyMMdd').csv"
)

Connect-VIServer -Server $vCenter -Credential (Get-Credential) | Out-Null

$report = Get-VM | ForEach-Object {
    $vm = $_
    $snaps = Get-Snapshot -VM $vm
    $oldestSnap = if ($snaps) { ($snaps | Sort-Object Created | Select-Object -First 1).Created } else { $null }

    [PSCustomObject]@{
        Name         = $vm.Name
        Cluster      = (Get-Cluster -VM $vm).Name
        PowerState   = $vm.PowerState
        vCPU         = $vm.NumCpu
        MemGB        = $vm.MemoryGB
        Snapshots    = $snaps.Count
        OldestSnap   = $oldestSnap
        Datastore    = ($vm | Get-Datastore | Select-Object -First 1).Name
    }
}

$report | Export-Csv -Path $OutputPath -NoTypeInformation
$report | Format-Table -AutoSize
Write-Host "`nReport saved: $OutputPath" -ForegroundColor Green
Disconnect-VIServer -Confirm:$false
```
```powershell
┌────────────────────────────────── PowerShell — Scripts (Operations) ──────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Operational PowerShell scripts for common infrastructure management tasks           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Windows Admin Scripts             │  │              Reporting Scripts              │   │
│   │              Get-DiskHealth.ps1              │  │           Get-ServerInventory.ps1           │   │
│   │          Set-LocalAdminPassword.ps1          │  │            Get-EventLogErrors.ps1           │   │
│   │            Enable-WinRMHTTPS.ps1             │  │           Export-ADUserReport.ps1           │   │
│   │         Install-RequiredModules.ps1          │  │             Check-CertExpiry.ps1            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Script header = always include #Requires, help block, param block with ValidateSet/Mandatory │   │
│   │       Logging       = use Write-Verbose for debug; Start-Transcript for full session log      │   │
│   │     Return values = output objects not strings; allows caller to filter with Where-Object     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
