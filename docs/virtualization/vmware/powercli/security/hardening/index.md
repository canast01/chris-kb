---
tags:
  - powercli
  - security
  - vmware
---
# PowerCLI — Hardening

<div class="kb-summary">
Hardening PowerCLI deployments: enforcing certificate validation, script execution policies, session timeout controls, audit log review, and secure pipeline configuration.

*Applies to: PowerCLI 13.x*
</div>

```text
┌──────────────────────────── PowerCLI — Hardening and Secure Configuration ────────────────────────────┐
│                                                                                                       │
│   Hardening PowerCLI protects vSphere management from credential theft and unauthorized access        │
│   Enforce TLS validation, execution policies, and least-privilege accounts before deploying scripts   │
│   Review audit logs regularly; vCenter logs all API calls made by automation service accounts         │
│                                                                                                       │
│   Certificate validation (most critical)                                                              │
│   Production: Set-PowerCLIConfiguration -InvalidCertificateAction Fail -Confirm:$false                │
│   Verify: Get-PowerCLIConfiguration | Select-Object InvalidCertificateAction                          │
│   Import vCenter CA into OS trust store so -Fail mode accepts valid internal certificates             │
│   Never use Ignore in production — MitM attacks against management plane become trivially easy        │
│                                                                                                       │
│   Script execution policy                                                                             │
│   Set-ExecutionPolicy RemoteSigned: scripts from the internet must be signed; local scripts run free  │
│   Set-ExecutionPolicy AllSigned: all scripts must be signed; strictest option                         │
│   CI/CD pipelines: use Set-ExecutionPolicy Bypass -Scope Process for ephemeral pipeline sessions      │
│                                                                                                       │
│   Credential hygiene                                                                                  │
│   Never store plaintext passwords in scripts or version control                                       │
│   Use Store-VICredentialStoreItem or Export-Clixml (machine-bound); rotate quarterly                  │
│   Service account passwords: managed in CyberArk or equivalent PAM; auto-rotated                      │
│                                                                                                       │
│   Audit log review                                                                                    │
│   vCenter events: filter for service account login events and bulk API operations                     │
│   ESXI audit: /var/log/shell.log captures SSH and ESXCLI commands on the host                         │
│   Review automation run logs monthly for anomalous patterns (unexpected object modifications)         │
│                                                                                                       │
│   Key terms:                                                                                          │
│   ExecutionPolicy  = PowerShell script signing policy; Bypass/Unrestricted/RemoteSigned/AllSigned     │
│   PAM              = Privileged Access Management; manages service account credentials (CyberArk)     │
│   CEIP             = Customer Experience Improvement Program; disable in air-gapped environments      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## PowerCLI Configuration Hardening

```powershell
# Show current configuration
Get-PowerCLIConfiguration -Scope AllUsers

# Enforce settings for all users on the host
Set-PowerCLIConfiguration -InvalidCertificateAction Fail -Scope AllUsers -Confirm:$false
Set-PowerCLIConfiguration -DefaultVIServerMode Single -Scope AllUsers -Confirm:$false
Set-PowerCLIConfiguration -CEIPDataTransferProxyPolicy UseSystemProxy -Scope AllUsers -Confirm:$false

# Disable CEIP phone-home
Set-PowerCLIConfiguration -ParticipateInCEIP $false -Scope AllUsers -Confirm:$false
```

## PowerShell Execution Policy

```powershell
# Require signed scripts (production standard)
Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope LocalMachine

# Or RemoteSigned (signs scripts from internet, allows local unsigned)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine

# Check current policy
Get-ExecutionPolicy -List
```

## Script Signing

```powershell
# Sign a script with a code-signing certificate from the local store
$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert | Select-Object -First 1
Set-AuthenticodeSignature -FilePath .\vsphere-health-check.ps1 -Certificate $cert

# Verify signature
Get-AuthenticodeSignature -FilePath .\vsphere-health-check.ps1 | Select-Object Status, SignerCertificate
```

## Session Timeout and Disconnect

```powershell
# Always disconnect at script end — prevents session accumulation
trap {
    Disconnect-VIServer -Confirm:$false -ErrorAction SilentlyContinue
    break
}

# Set connection timeout (default 600s)
# Controlled by vCenter SSO token policy — see security/authentication/
```

## Audit Log Review via PowerCLI

```powershell
# Review recent events for a service account
$account = "DOMAIN\svc-automation"
Get-VIEvent -MaxSamples 500 | Where-Object { $_.UserName -like "*$account*" } |
    Select-Object CreatedTime, UserName, FullFormattedMessage | Format-Table -AutoSize

# Find login events (track access)
Get-VIEvent -Types UserLoginSessionEvent -MaxSamples 200 |
    Select-Object CreatedTime, UserName, @{N="IP";E={$_.IpAddress}} | Format-Table -AutoSize

# Find permission changes
Get-VIEvent -MaxSamples 500 | Where-Object { $_.GetType().Name -like "*Permission*" } |
    Select-Object CreatedTime, UserName, FullFormattedMessage
```

## Secure Pipeline Configuration

For CI/CD pipelines running PowerCLI:

```powershell
# Never print credentials in logs
$VerbosePreference = "SilentlyContinue"
$DebugPreference   = "SilentlyContinue"

# Use secret stores (GitHub Actions example)
# In workflow: VCENTER_USER and VCENTER_PASS as repository secrets
$cred = New-Object System.Management.Automation.PSCredential(
    $env:VCENTER_USER,
    (ConvertTo-SecureString $env:VCENTER_PASS -AsPlainText -Force)
)

# Validate connection before proceeding
Connect-VIServer -Server $env:VCENTER_HOST -Credential $cred
if (-not $global:DefaultVIServer.IsConnected) {
    Write-Error "Failed to connect to vCenter"
    exit 1
}
```

## Hardening Checklist

| Item | Command / Action |
|---|---|
| Certificate validation enforced | `Set-PowerCLIConfiguration -InvalidCertificateAction Fail` |
| CEIP disabled | `Set-PowerCLIConfiguration -ParticipateInCEIP $false` |
| Execution policy set to AllSigned | `Set-ExecutionPolicy AllSigned` |
| Scripts signed with valid cert | `Set-AuthenticodeSignature` |
| Credentials never in script files | Use env vars or Export-Clixml |
| Disconnect after each session | `Disconnect-VIServer` in trap block |
| Dedicated service accounts per role | vCenter RBAC — see access-control/ |
| Audit log review scheduled | Monthly `Get-VIEvent` review |
