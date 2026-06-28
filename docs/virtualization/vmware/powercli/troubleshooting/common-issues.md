---
tags:
  - powercli
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# PowerCLI — Common Issues

<div class="kb-summary">
Solutions for the most frequent PowerCLI problems: certificate errors, connection failures, module conflicts, API incompatibility, session expiry, and cmdlet parameter mismatches.

*Applies to: PowerCLI 13.x*
</div>
![PowerCLI — Common Issues](../../../../assets/virtualization-vmware-powercli-troubleshooting-common-issues.svg)




```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
certificate_error_on_connect: "Certificate Error on Connect" {shape: rectangle}
module_not_found: "Module Not Found" {shape: rectangle}
connection_refused_timeout: "Connection Refused / Timeout" {shape: rectangle}
session_expired_invalid_session: "Session Expired / Invalid Session" {shape: rectangle}
cmdlet_parameter_not_found: "Cmdlet Parameter Not Found" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> certificate_error_on_connect: investigate
symptom -> module_not_found: investigate
symptom -> connection_refused_timeout: investigate
symptom -> session_expired_invalid_session: investigate
symptom -> cmdlet_parameter_not_found: investigate
diagnostic_flow -> resolution
certificate_error_on_connect -> resolution
module_not_found -> resolution
connection_refused_timeout -> resolution
session_expired_invalid_session -> resolution
cmdlet_parameter_not_found -> resolution
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1[Connect-VIServer fails with SSL error]
    S --> B2[Module not found]
    S --> B3[Connection refused or timeout]
    S --> B4[Session expired or invalid]
    S --> B5[Cmdlet parameter not found]
    S --> B6[Multiple module version conflict]

    B1 --> D1{Lab or\nproduction?}
    D1 -->|Lab| R1[Set InvalidCertificateAction Ignore\n→ Certificate Error on Connect]
    D1 -->|Production| R2[Import vCenter CA to OS Trust Store\n→ Certificate Error on Connect]

    B2 --> R3[Install-Module VMware.PowerCLI · Check PSModulePath\n→ Module Not Found]

    B3 --> D2{Network\nreachable?}
    D2 -->|No| R4[Test-NetConnection Port 443 · Check DNS\n→ Connection Refused / Timeout]
    D2 -->|Yes| R5[Check Existing Sessions · Disconnect and Retry\n→ Connection Refused / Timeout]

    B4 --> R6[Check IsConnected · Reconnect · Extend SSO Token Lifetime\n→ Session Expired / Invalid Session]

    B5 --> R7[Check PowerCLI vs vCenter API Compatibility\n→ Cmdlet Parameter Not Found]

    B6 --> R8[Uninstall Old Module Versions · Keep Latest Only\n→ Multiple Module Versions Conflict]

    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8 section
    class D1,D2 decision
    class S start
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Certificate Error on Connect

**Symptom:** `Connect-VIServer` fails with `The underlying connection was closed` or `SSL/TLS` errors.

```powershell
# Quick fix for lab / self-signed certs
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false
Connect-VIServer -Server vcenter.example.com

# Production: add vCenter CA to OS trust store, then use Fail policy
# Windows: Import CA cert into Trusted Root Certification Authorities
Import-Certificate -FilePath ".\vcenter-ca.cer" -CertStoreLocation Cert:\LocalMachine\Root
Set-PowerCLIConfiguration -InvalidCertificateAction Fail -Confirm:$false
```

## Module Not Found

**Symptom:** `The term 'Connect-VIServer' is not recognized` or `Import-Module: Module 'VMware.PowerCLI' was not found`.

```powershell
# Check if module is installed
Get-Module -Name VMware.* -ListAvailable

# Install from PSGallery
Install-Module -Name VMware.PowerCLI -Scope CurrentUser -AllowClobber

# If PSGallery is not trusted
Install-Module -Name VMware.PowerCLI -Scope CurrentUser -AllowClobber -Force

# Check PSModulePath
$env:PSModulePath -split [IO.Path]::PathSeparator
```

## Connection Refused / Timeout

**Symptom:** `Connect-VIServer` hangs or returns `Unable to connect to vCenter`.

```powershell
# Test network connectivity first
Test-NetConnection -ComputerName vcenter.example.com -Port 443

# Check DNS resolution
Resolve-DnsName vcenter.example.com

# Try with explicit port
Connect-VIServer -Server vcenter.example.com -Port 443

# Check if another session is blocking (single-server mode)
$global:DefaultVIServers
Disconnect-VIServer -Confirm:$false
```

## Session Expired / Invalid Session

**Symptom:** Cmdlets fail with `NotAuthenticated` or `An error occurred while sending the request`.

```powershell
# Check if still connected
$global:DefaultVIServer.IsConnected

# Reconnect
if (-not $global:DefaultVIServer.IsConnected) {
    Connect-VIServer -Server $vCenter -Credential $cred
}
```

Default SSO token lifetime is 8 hours. For long-running scripts, add periodic reconnect logic or increase token lifetime in vCenter SSO policy.

## Cmdlet Parameter Not Found

**Symptom:** `A parameter cannot be found that matches parameter name 'X'`.

```powershell
# Check PowerCLI version vs vCenter version compatibility
Get-Module -Name VMware.PowerCLI -ListAvailable | Select-Object Version
(Get-View ServiceInstance).Content.About | Select-Object Version, Build

# Get help for the cmdlet to see available parameters
Get-Help Set-VM -Full | Select-Object -Expand Parameters
```

New parameters (e.g., `-CryptoSpec` for VM encryption) are only available against vCenter versions that support the underlying API. Wrap in `try/catch` for multi-version environments.

## Multiple Module Versions Conflict

**Symptom:** `Assembly with same name is already loaded` or inconsistent cmdlet behavior.

```powershell
# List all installed versions
Get-Module -Name VMware.* -ListAvailable | Select-Object Name, Version | Sort-Object Name, Version

# Remove old versions
Get-Module -Name VMware.* -ListAvailable |
    Group-Object Name |
    ForEach-Object {
        $sorted = $_.Group | Sort-Object Version -Descending
        $sorted | Select-Object -Skip 1 | ForEach-Object {
            Uninstall-Module -Name $_.Name -RequiredVersion $_.Version -Force -ErrorAction SilentlyContinue
        }
    }
```

## Get-VM Returns Empty on Known VMs

**Symptom:** `Get-VM` returns nothing even though VMs exist.

```powershell
# Confirm connected to correct vCenter
$global:DefaultVIServers | Select-Object Name, IsConnected

# Specify -Server explicitly
Get-VM -Server vcenter.example.com

# Check permissions (service account may lack read on datacenter)
Get-VIPermission | Where-Object { $_.Principal -like "*$env:USERNAME*" }
```

## vSAN Cmdlets Unavailable

**Symptom:** `Get-VsanClusterHealthSummary : The term '...' is not recognized`.

```powershell
# Ensure vSAN module is installed
Get-Module -Name VMware.VimAutomation.Storage -ListAvailable

# Install if missing
Install-Module VMware.VimAutomation.Storage -Scope CurrentUser -Force

# Import explicitly
Import-Module VMware.VimAutomation.Storage
```

---

## See also

- [PowerCLI — Diagnostics](diagnostics/)
- [PowerCLI — Escalation](escalation/)
- [PowerCLI — Health Checks](../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
