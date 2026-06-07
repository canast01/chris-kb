# PowerCLI — Diagnostics

<div class="kb-summary">
PowerCLI diagnostic techniques: verbose/debug output, API call tracing via ExtensionData, performance profiling for large inventories, and log collection for VMware support escalations.
</div>

## Enable Verbose and Debug Output

```powershell
# Enable verbose logging for a session
$VerbosePreference = "Continue"
$DebugPreference   = "Continue"

# Or per-command
Connect-VIServer -Server vcenter.example.com -Verbose -Debug

# Reset
$VerbosePreference = "SilentlyContinue"
$DebugPreference   = "SilentlyContinue"
```

## Trace API Calls via ExtensionData

When a high-level cmdlet doesn't expose what you need, drop to the vSphere API via `.ExtensionData`:

```powershell
# Access raw vSphere API for a VM
$vm = Get-VM -Name "web01"
$vmView = $vm | Get-View

# Show all raw properties
$vmView | Get-Member -MemberType Properties

# Access config directly
$vmView.Config.Hardware
$vmView.Config.ExtraConfig

# Call API methods directly
$vmView.RefreshStorageInfo()
```

## Check Error Detail

```powershell
# Full exception detail
try {
    Connect-VIServer -Server vcenter.example.com -Credential $cred
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Inner: $($_.Exception.InnerException?.Message)" -ForegroundColor Yellow
    Write-Host "Stack: $($_.ScriptStackTrace)" -ForegroundColor Gray
}
```

## Performance Profiling for Large Inventories

```powershell
# Measure cmdlet execution time
Measure-Command { Get-VM | Get-Snapshot } | Select-Object TotalSeconds

# Speed up with targeted queries instead of piped filtering
# SLOW: get all VMs then filter
Get-VM | Where-Object { $_.PowerState -eq 'PoweredOff' }

# FAST: filter at source via Get-View (direct API, no wrappers)
Get-View -ViewType VirtualMachine -Filter @{ "Runtime.PowerState" = "poweredOff" } |
    Select-Object Name, @{N="State";E={$_.Runtime.PowerState}}

# Use -Location to scope expensive queries
Get-VM -Location (Get-Cluster -Name "Production")
```

## Check vCenter API Version

```powershell
$si = Get-View ServiceInstance
$si.Content.About | Select-Object ApiVersion, Version, Build, OsType

# Check if a specific API feature is available
$si.Capability | Select-Object ProvisioningSupported, MultiHostSupported, UserShellAccessSupported
```

## Collect Logs for Escalation

```powershell
# Collect PowerCLI version info
Get-Module -Name VMware.* -ListAvailable | Select-Object Name, Version | Export-Csv -Path .\powercli-modules.csv

# Collect vCenter and API version
$si = Get-View ServiceInstance
$si.Content.About | Export-Csv -Path .\vcenter-version.csv

# Export event log (last 24h) for support
Get-VIEvent -Start (Get-Date).AddHours(-24) | Export-Csv -Path .\vcenter-events.csv

# Capture a command with full output and error stream
& {
    $VerbosePreference = "Continue"
    $DebugPreference = "Continue"
    Get-VM -Name "problem-vm"
} 2>&1 | Out-File -Path .\debug-output.txt
```

## Test Connection Health

```powershell
# Verify vCenter API is responding
$uri = "https://vcenter.example.com/sdk"
try {
    $resp = Invoke-WebRequest -Uri $uri -Method Get -SkipCertificateCheck -TimeoutSec 10
    Write-Host "vCenter API reachable. Status: $($resp.StatusCode)"
} catch {
    Write-Host "vCenter API unreachable: $($_.Exception.Message)" -ForegroundColor Red
}

# Check active sessions
Get-View SessionManager | ForEach-Object {
    $_.SessionList | Select-Object UserName, LoginTime, IpAddress, UserAgent
}
```
