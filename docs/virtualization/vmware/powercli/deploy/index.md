---
tags:
  - deployment
  - powercli
  - vmware
search:
  boost: 1.5
---
# PowerCLI — Deploy

<div class="kb-summary">
Installing PowerCLI, first connection to vCenter, service account setup, certificate configuration, and proxy settings for environments without direct internet access.

*Applies to: PowerCLI 13.x*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
install_from_powershell_gallery: "Install from PowerShell Gallery" {shape: rectangle}
offline_install_airgapped_environmen: "Offline Install (Air-Gapped Environments)" {shape: rectangle}
first_connection: "First Connection" {shape: rectangle}
service_account_setup: "Service Account Setup" {shape: rectangle}
certificate_configuration: "Certificate Configuration" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> install_from_powershell_gallery
install_from_powershell_gallery -> offline_install_airgapped_environmen
offline_install_airgapped_environmen -> first_connection
first_connection -> service_account_setup
service_account_setup -> certificate_configuration
certificate_configuration -> validate
```

## Before you begin

- **Access:** local administrator rights to install the module; vCenter read-only minimum for connections; internet access or a pre-staged offline package for Gallery install
- **Timing:** safe to run any time; no infrastructure changes until you actively connect to vCenter
- **Dependencies:** PowerShell 5.1 (Windows) or PowerShell 7+ (cross-platform); .NET Framework 4.7.2+ for Windows PowerShell 5.1
- **Logging:** record the PowerCLI version installed (`Get-PowerCLIVersion`) and capture the connection test output

---

## Prerequisites

- PowerShell 5.1 (Windows built-in) or PowerShell 7+ (cross-platform)
- .NET Framework 4.7.2+ (Windows PowerShell 5.1)
- Network access to vCenter Server on TCP 443
- vCenter account with read permissions minimum (write for management operations)

## Install from PowerShell Gallery

```powershell
# Install PowerCLI for current user (no admin required)
Install-Module -Name VMware.PowerCLI -Scope CurrentUser

# Or install system-wide (requires admin)
Install-Module -Name VMware.PowerCLI -Scope AllUsers

# Verify installation
Get-Module -ListAvailable | Where-Object { $_.Name -like 'VMware*' } | Select-Object Name, Version
```

## Offline Install (Air-Gapped Environments)

```powershell
# On an internet-connected machine, save the module to a folder
Save-Module -Name VMware.PowerCLI -Path C:\PSModules -Repository PSGallery

# Copy C:\PSModules to the target machine (USB, file share, etc.)
# On the target machine:
$env:PSModulePath += ";C:\PSModules"
Import-Module VMware.PowerCLI

# Or install from local path permanently:
Register-PSRepository -Name "Local" -SourceLocation "C:\PSModules" -InstallationPolicy Trusted
Install-Module -Name VMware.PowerCLI -Repository "Local"
```

## First Connection

```powershell
# Ignore certificate warning (acceptable in lab; use trusted cert in production)
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

# Connect (will prompt for credentials)
Connect-VIServer -Server vcenter.example.com

# Connect with explicit credentials
$cred = Get-Credential
Connect-VIServer -Server vcenter.example.com -Credential $cred

# Verify connection
$global:DefaultVIServer | Select-Object Name, User, Version, IsConnected
```

## Service Account Setup

Create a dedicated service account for automation scripts. Never use an admin account.

```powershell
# Minimum permissions for read-only scripts (health checks, reporting)
# vCenter privilege: Read-only role on root vCenter object with Propagate to children

# For scripts that need to manage VMs:
# Custom role with: Virtual Machine.Interact (start/stop/reconfigure)
# Custom role with: Datastore.FileManagement (vSAN/VMDK operations)

# Assign the role via vCenter (GUI or PowerCLI):
$role = Get-VIRole -Name "AutomationReadOnly"
New-VIPermission -Entity (Get-Folder "Datacenters") -Principal "vsphere.local\svc-automation" -Role $role -Propagate

# Test the service account connection
$svcCred = New-Object PSCredential("vsphere.local\svc-automation", (Read-Host -AsSecureString "Password"))
Connect-VIServer -Server vcenter.example.com -Credential $svcCred
```

## Certificate Configuration

```powershell
# Options for InvalidCertificateAction:
# Ignore   = accept any cert (lab only)
# Warn     = connect but print warning (default in older versions)
# Prompt   = ask each session
# Fail     = reject untrusted certs (recommended in production)

# Production: use a cert signed by your PKI
Set-PowerCLIConfiguration -InvalidCertificateAction Fail -Confirm:$false

# If vCenter has a trusted cert (signed by enterprise CA):
# Add the CA cert to Windows Trusted Root store:
Import-Certificate -FilePath C:\Certs\enterprise-root-ca.crt -CertStoreLocation Cert:\LocalMachine\Root
# Now Connect-VIServer will validate the cert chain automatically
```

## Proxy Configuration

```powershell
# If a proxy is required to reach vCenter:
Set-PowerCLIConfiguration -ProxyPolicy UseSystemProxy -Confirm:$false

# Or explicit proxy:
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy("http://proxy.example.com:3128")
[System.Net.WebRequest]::DefaultWebProxy.Credentials = [System.Net.CredentialCache]::DefaultNetworkCredentials

# Bypass proxy for internal vCenter:
$noProxy = [System.Net.WebRequest]::DefaultWebProxy
$noProxy.BypassProxyOnLocal = $true
$noProxy.BypassList = @("*.example.com", "10.*.*.*")
```

## Post-Deploy Validation

```powershell
# 1. Connect successfully
Connect-VIServer -Server vcenter.example.com -Credential $cred

# 2. List all hosts
Get-VMHost | Select-Object Name, ConnectionState, PowerState, Version | Format-Table -AutoSize

# 3. List all VMs (top 10 by power state)
Get-VM | Sort-Object PowerState | Select-Object -First 10 Name, PowerState, NumCpu, MemoryGB | Format-Table -AutoSize

# 4. Check vSAN (if applicable)
$cluster = Get-Cluster | Select-Object -First 1
if ($cluster.VsanEnabled) {
    Get-VsanDisk -VMHost (Get-VMHost -Location $cluster) | Select-Object CanonicalName, State | Format-Table
}

# 5. Disconnect
Disconnect-VIServer -Confirm:$false
Write-Host "PowerCLI deployment validated." -ForegroundColor Green
```

---

## See also

- [PowerCLI — How It Works](../architecture/how-it-works/)
- [PowerCLI — Health Checks](../operations/health-checks/)
- [PowerCLI — Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
