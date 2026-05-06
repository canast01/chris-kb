# Connection & Session

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

## Install and Configure PowerCLI

```powershell
# Install from PowerShell Gallery (run once)
Install-Module VMware.PowerCLI -Scope CurrentUser -Force

# Suppress invalid certificate warnings (lab/self-signed)
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

# Opt out of CEIP telemetry
Set-PowerCLIConfiguration -ParticipateInCeip $false -Confirm:$false

# Check installed version
Get-Module VMware.PowerCLI -ListAvailable | Select-Object Name, Version

# Update to latest
Update-Module VMware.PowerCLI
```

## Connecting

```powershell
# Interactive (prompts for credentials)
Connect-VIServer -Server <vcenter_fqdn>

# Credential in command (scripts — use a secret vault for production)
Connect-VIServer -Server vcenter.corp.local -User administrator@vsphere.local -Password <password>

# Using a credential object (safer for scripts)
$cred = Get-Credential
Connect-VIServer -Server vcenter.corp.local -Credential $cred

# Connect to multiple vCenters
Connect-VIServer -Server vcenter1.corp.local, vcenter2.corp.local
```

## Session Info

```powershell
# Current connection(s)
$global:DefaultVIServer
$global:DefaultVIServers   # when connected to multiple

# Session details (user, API version, connection time)
$global:DefaultVIServer | Select-Object Name, User, Version, IsConnected, SessionId
```

## Disconnecting

```powershell
# Disconnect from all vCenters
Disconnect-VIServer * -Confirm:$false

# Disconnect from a specific vCenter
Disconnect-VIServer -Server vcenter.corp.local -Confirm:$false
```

## Running as a Script / Non-Interactive

```powershell
# Store encrypted credential on disk (per-user, per-machine)
$cred = Get-Credential
$cred | Export-Clixml -Path "$env:USERPROFILE\.vcenter_cred.xml"

# Load credential in script
$cred = Import-Clixml -Path "$env:USERPROFILE\.vcenter_cred.xml"
Connect-VIServer -Server vcenter.corp.local -Credential $cred
```

## Proxy and Certificate Settings

```powershell
# Skip proxy for vCenter (when vCenter is on-prem but proxy is active)
Set-PowerCLIConfiguration -ProxyPolicy NoProxy -Confirm:$false

# Trust all certificates (only for lab environments)
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

# Require valid certificates (production default)
Set-PowerCLIConfiguration -InvalidCertificateAction Fail -Confirm:$false
```
