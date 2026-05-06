# PowerShell CLI Reference

Commonly used PowerShell commands and VMware PowerCLI for infrastructure management.

---

## PowerShell — Core

```powershell
# Version and environment
$PSVersionTable
Get-Host

# Help
Get-Help <cmdlet>
Get-Help <cmdlet> -Full
Get-Help <cmdlet> -Examples
Update-Help

# Commands and modules
Get-Command
Get-Command -Noun VM
Get-Module
Get-Module -ListAvailable
Import-Module <module>
Remove-Module <module>
Install-Module <module> -Scope CurrentUser
```

---

## Variables & Output

```powershell
# Variables
$myVar = "value"
$myArray = @(1, 2, 3)
$myHash = @{ key = "value" }

# Output
Write-Output "message"
Write-Host "message" -ForegroundColor Green
Write-Error "error message"
Write-Verbose "verbose" -Verbose

# Null check
if ($null -eq $var) { "null" }

# String formatting
"Server: $($server.Name)"
```

---

## Pipeline & Filtering

```powershell
# Common filters
Get-Service | Where-Object { $_.Status -eq "Running" }
Get-Process | Where-Object { $_.CPU -gt 10 }
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Select properties
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB

# Measure
Get-VM | Measure-Object MemoryGB -Sum -Average

# ForEach
Get-VM | ForEach-Object { Write-Host $_.Name }
1..10 | ForEach-Object { "Item $_" }
```

---

## Files & Filesystem

```powershell
# Navigation
Get-Location
Set-Location C:\scripts
Get-ChildItem
Get-ChildItem -Recurse -Filter "*.ps1"

# File operations
New-Item -Path ".\file.txt" -ItemType File
Copy-Item source.txt dest.txt
Move-Item source.txt dest\
Remove-Item file.txt
Get-Content file.txt
Set-Content file.txt "content"
Add-Content file.txt "new line"

# CSV / JSON
Import-Csv data.csv
Export-Csv -Path output.csv -NoTypeInformation
$obj | ConvertTo-Json
$json | ConvertFrom-Json

# Test path
Test-Path "C:\scripts\file.ps1"
```

---

## Remoting (PSSession)

```powershell
# Connect to remote host
Enter-PSSession -ComputerName <host>
Exit-PSSession

# Persistent session
$session = New-PSSession -ComputerName <host>
Invoke-Command -Session $session -ScriptBlock { Get-Service }
Remove-PSSession $session

# Run command on multiple hosts
$servers = @("srv1", "srv2")
Invoke-Command -ComputerName $servers -ScriptBlock { hostname }
```

---

## Services & Processes

```powershell
# Services
Get-Service
Get-Service -Name <name>
Start-Service <name>
Stop-Service <name>
Restart-Service <name>
Set-Service -Name <name> -StartupType Automatic

# Processes
Get-Process
Get-Process -Name <name>
Stop-Process -Name <name>
Stop-Process -Id <pid> -Force
```

---

## Error Handling

```powershell
# Try/catch
try {
    Get-VM -Name "nonexistent" -ErrorAction Stop
} catch {
    Write-Error "Failed: $_"
}

# Error preference
$ErrorActionPreference = "Stop"     # Terminate on error
$ErrorActionPreference = "Continue" # Default

# -ErrorAction
Get-VM -Name "test" -ErrorAction SilentlyContinue
```

---

## VMware PowerCLI

```powershell
# Install / connect
Install-Module VMware.PowerCLI -Scope CurrentUser
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false
Connect-VIServer -Server <vcenter> -Credential (Get-Credential)
Disconnect-VIServer -Confirm:$false

# VMs
Get-VM
Get-VM -Name <name>
Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" }
Start-VM -VM <name>
Stop-VM -VM <name> -Confirm:$false
Restart-VM -VM <name> -Confirm:$false
Suspend-VM -VM <name>

# VM config
Get-VM <name> | Get-HardDisk
Get-VM <name> | Get-NetworkAdapter
Set-VM -VM <name> -NumCpu 4 -MemoryGB 16 -Confirm:$false

# Snapshots
Get-Snapshot -VM <name>
New-Snapshot -VM <name> -Name "pre-patch" -Memory:$false -Quiesce:$false
Remove-Snapshot -Snapshot <snap> -Confirm:$false
Set-VM -VM <name> -Snapshot <snap> -Confirm:$false  # Revert

# Hosts
Get-VMHost
Get-VMHost -Name <hostname>
Get-VMHost | Select-Object Name, PowerState, ConnectionState, Version
Set-VMHost -VMHost <host> -State Maintenance

# Clusters
Get-Cluster
Get-Cluster <name> | Get-VMHost
Get-Cluster | Get-VM

# Datastores
Get-Datastore
Get-Datastore | Select-Object Name, CapacityGB, FreeSpaceGB
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.2 }

# vSAN
Get-VsanView
Get-VsanClusterConfiguration -Cluster <cluster>

# Resource pools
Get-ResourcePool
Get-ResourcePool -Name <name> | Get-VM

# vCenter events
Get-VIEvent -MaxSamples 100
Get-VIEvent -Start (Get-Date).AddHours(-24)

# Tags
Get-Tag
Get-TagCategory
New-Tag -Name <tag> -Category <category>
Get-VM <name> | Get-TagAssignment
New-TagAssignment -Tag <tag> -Entity (Get-VM <name>)
```

---

## Reporting

```powershell
# Export VM inventory to CSV
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB, @{N="Datastore";E={($_ | Get-Datastore).Name}} | Export-Csv -Path vm_inventory.csv -NoTypeInformation

# Host summary
Get-VMHost | Select-Object Name, Version, @{N="CPU%";E={[math]::Round($_.CpuUsageMhz / $_.CpuTotalMhz * 100, 1)}}, @{N="Mem%";E={[math]::Round($_.MemoryUsageGB / $_.MemoryTotalGB * 100, 1)}} | Format-Table

# Snapshot report
Get-VM | Get-Snapshot | Select-Object VM, Name, Created, @{N="SizeGB";E={[math]::Round($_.SizeGB, 2)}} | Sort-Object SizeGB -Descending
```
