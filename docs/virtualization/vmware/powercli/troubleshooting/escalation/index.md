---
tags:
  - powercli
  - troubleshooting
  - vmware
---
# PowerCLI — Escalation

<div class="kb-summary">
PowerCLI escalation — collecting diagnostic information, engaging VMware support for PowerCLI and vSphere API issues, module version compatibility matrix, and community resources for advanced troubleshooting.
</div>

```text
┌────────────────────────────────── PowerCLI — Escalation Procedures ───────────────────────────────────┐
│                                                                                                       │
│   Escalate when the issue persists after checking module version, cert config, and API compatibility  │
│   Collect a minimal reproduction script before escalating; reduces resolution time significantly      │
│   Check community resources first — most PowerCLI issues have a known solution without a support case │
│                                                                                                       │
│   When to escalate                                                                                    │
│   vSphere API returns an undocumented error code not found in the vSphere API Reference               │
│   A PowerCLI cmdlet produces inconsistent results across identical vCenter versions                   │
│   A module installs successfully but throws unexpected exceptions on import                           │
│   Performance regression after a PowerCLI or vCenter upgrade that cannot be explained by workload     │
│                                                                                                       │
│   Information to collect                                                                              │
│   PowerCLI module versions: Get-Module VMware.* | Select-Object Name, Version                         │
│   vCenter version: $global:DefaultVIServer | Select-Object Name, Version, Build                       │
│   Full error message: $Error[0] | Format-List * -Force                                                │
│   Minimal repro: smallest script that triggers the issue (no proprietary data)                        │
│   vCenter support bundle from VAMI (for API-layer issues affecting multiple clients)                  │
│                                                                                                       │
│   Escalation path                                                                                     │
│   Step 1: VMware PowerCLI Community (community.vmware.com) — check existing threads                   │
│   Step 2: PowerCLI GitHub (github.com/vmware/PowerCLI) — check issues tab for known bugs              │
│   Step 3: VMware GSS support case — attach collected data; include reproduction steps                 │
│   Step 4: VMware Product Team via GSS (if confirmed product defect)                                   │
│                                                                                                       │
│   Key terms:                                                                                          │
│   GSS           = Global Support Services; Broadcom/VMware support case portal                        │
│   vSphere API Ref = API reference documentation; documents all managed object types and methods       │
│   Minimal repro  = smallest possible script that reproduces the issue; no credentials or env details  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## When to Escalate

Escalate to VMware support (or the community) when:

| Scenario | Escalation Path |
|---|---|
| PowerCLI cmdlet returns unexpected API error (not a permission issue) | VMware Support case |
| Cmdlet behaviour changed after a vCenter upgrade | VMware Support case |
| Module install fails from PowerShell Gallery with non-network errors | VMware Support case |
| Cmdlet parameter documented in help but not accepted by API | VMware Support case |
| Performance issue — API response time increased after vCenter upgrade | VMware Support case |
| General "how do I do X" questions | VMware {code} Community, vCommunity Slack |
| Cross-vendor PowerCLI integration questions | Community forums |

---

## Diagnostic Collection

Collect this information before opening a support case.

```powershell
# 1. PowerCLI and PowerShell version
$psVersion = $PSVersionTable | Select-Object PSVersion, PSEdition, OS
$vmwareModules = Get-Module -ListAvailable | Where-Object { $_.Name -like 'VMware*' } |
    Select-Object Name, Version | Sort-Object Name

Write-Host "=== PowerShell Version ==="
$psVersion | Format-List

Write-Host "`n=== Installed PowerCLI Modules ==="
$vmwareModules | Format-Table -AutoSize

# 2. Current loaded modules (active in session)
Write-Host "`n=== Loaded Modules ==="
Get-Module | Where-Object { $_.Name -like 'VMware*' } |
    Select-Object Name, Version | Format-Table -AutoSize

# 3. Connection configuration
Write-Host "`n=== PowerCLI Configuration ==="
Get-PowerCLIConfiguration | Format-Table -AutoSize

# 4. vCenter version (if connected)
if ($global:DefaultVIServers.Count -gt 0) {
    Write-Host "`n=== Connected vCenter(s) ==="
    $global:DefaultVIServers | Select-Object Name, Version, Build, IsConnected |
        Format-Table -AutoSize
}
```

```powershell
# 5. Enable verbose/debug logging for a failing command
# This captures the raw API calls and responses
$VerbosePreference = 'Continue'
$DebugPreference = 'Continue'

# Run the failing command here
# Get-VM -Name "problem-vm"

$VerbosePreference = 'SilentlyContinue'
$DebugPreference = 'SilentlyContinue'

# 6. Capture full error record
try {
    # Replace with the failing command:
    Get-VM -Name "problem-vm"
} catch {
    Write-Host "=== Full Error Record ==="
    Write-Host "Exception: $($_.Exception.Message)"
    Write-Host "Category: $($_.CategoryInfo.Category)"
    Write-Host "Target: $($_.CategoryInfo.TargetName)"
    Write-Host "`nStack Trace:"
    Write-Host $_.ScriptStackTrace
    Write-Host "`nInner Exception:"
    Write-Host $_.Exception.InnerException
    $_ | ConvertTo-Json -Depth 5 | Out-File "powercli-error-$(Get-Date -Format 'yyyyMMddHHmm').json"
}
```

---

## Module Version Compatibility

```powershell
# Check recommended PowerCLI version for your vCenter
# PowerCLI 13.x → vCenter 8.x
# PowerCLI 12.x → vCenter 7.x and 8.x
# PowerCLI 11.x → vCenter 6.7 and 7.x

# Show version compatibility warnings when connecting
Connect-VIServer -Server "vcenter.example.com" -Verbose
# Watch for "The 'VimAutomation.Core' module version X is not supported with vCenter Y" warnings

# Upgrade to latest PowerCLI
Update-Module -Name VMware.PowerCLI -Force

# Install a specific version for compatibility
Install-Module -Name VMware.PowerCLI -RequiredVersion "13.3.0.24145081" -Force -AllowClobber

# Check for module conflicts — multiple versions installed
Get-Module -ListAvailable | Where-Object { $_.Name -like 'VMware*' } |
    Group-Object Name | Where-Object { $_.Count -gt 1 } |
    Select-Object Name, @{N='Versions';E={$_.Group.Version -join ', '}} |
    Format-Table -AutoSize

# Remove old versions (keep only latest)
Get-Module -ListAvailable | Where-Object { $_.Name -like 'VMware*' } |
    Group-Object Name | ForEach-Object {
        $latest = $_.Group | Sort-Object Version -Descending | Select-Object -First 1
        $old = $_.Group | Sort-Object Version -Descending | Select-Object -Skip 1
        $old | ForEach-Object {
            Write-Host "Removing $($_.Name) v$($_.Version)"
            Uninstall-Module -Name $_.Name -RequiredVersion $_.Version -Force
        }
    }
```

---

## Common API Error Codes

| Error | Likely Cause | First Step |
|---|---|---|
| `InvalidLogin` | Wrong credentials or SSO issue | Check service account password; test in vCenter UI |
| `NotAuthenticated` | Session expired or token invalid | Re-connect: `Connect-VIServer` again |
| `NoPermission` | Role missing required privilege | Check role in vCenter → Administration → Roles |
| `NotFound` | Object deleted or renamed since script run | Verify object name; check vCenter inventory |
| `InvalidArgument` | Parameter value out of range | Check vCenter API docs for the method constraints |
| `SystemError` | vCenter internal error | Check vCenter logs; may require vCenter restart |
| `Fault.VimFault` | Low-level VI API fault | Enable debug and capture full error; open support case |
| `ServerFaultCode` | vCenter returned SOAP fault | Check vCenter's vpxd.log for correlation |
| `HttpException` | TLS/connectivity error | Verify cert settings; test TCP 443 connectivity |

---

## Enable API Trace Logging

For API-level issues, enable PowerCLI's built-in trace log.

```powershell
# Enable API call tracing — writes SOAP XML to a log file
# WARNING: log files can grow large quickly — disable after capturing the issue
$global:DefaultVIServer | ForEach-Object {
    $_.ExtensionData.Client.TraceEnabled = $true
}

# Or set the trace file path before connecting
$env:POWERCLI_TRACE_FILE = "C:\temp\powercli-trace-$(Get-Date -Format 'yyyyMMdd').log"

# Reproduce the issue here
# Get-VM -Name "problem-vm"

# Disable tracing
$global:DefaultVIServer | ForEach-Object {
    $_.ExtensionData.Client.TraceEnabled = $false
}
Write-Host "Trace log: $env:POWERCLI_TRACE_FILE"
```

---

## VMware Support Case Process

**Before opening a case:**
1. Reproduce the issue with `$VerbosePreference = 'Continue'` and capture the output
2. Run the diagnostic collection script above and save the output
3. Note the exact PowerCLI and vCenter versions
4. Identify whether the issue appeared after a specific upgrade
5. Confirm the same operation works via vCenter UI (isolates PowerCLI vs vCenter API)

**Opening the case:**

1. Go to [VMware Customer Connect](https://customerconnect.vmware.com/) → Support → Open a Case
2. Product: **vSphere** (PowerCLI issues are handled under vSphere)
3. Severity: Set based on production impact (Sev 1 = production down; Sev 2 = degraded; Sev 3 = non-urgent)
4. Title format: `PowerCLI [ModuleName] [CmdletName] - [brief symptom] - vCenter [version]`
5. Attach: error JSON, diagnostic output, trace log (if captured)

**What to include in the case description:**
- Exact PowerCLI command that fails
- Full error message and stack trace
- PowerCLI module version (`Get-Module VMware.PowerCLI | Select Version`)
- vCenter version (`$global:DefaultVIServers.Version`)
- PowerShell version (`$PSVersionTable.PSVersion`)
- Whether the same operation works in the vCenter UI
- When the issue first appeared (after upgrade? always?)

---

## Community Resources

| Resource | URL | Best For |
|---|---|---|
| VMware {code} Community | `code.vmware.com` | Official forums, VMware staff engagement |
| vCommunity Slack (`#powercli`) | vmwarecode.slack.com | Quick questions, community answers |
| PowerCLI GitHub | `github.com/vmware/PowerCLI-Example-Scripts` | Sample scripts, issue tracking |
| PowerCLI documentation | `developer.vmware.com/docs/powercli` | Cmdlet reference, release notes |
| VMTN Community Boards | `communities.vmware.com` | Broader vSphere/VMware questions |
| Stack Overflow `[vmware-powercli]` | stackoverflow.com | Scripting/PowerShell questions |
