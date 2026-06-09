# PowerCLI — Lifecycle

<div class="kb-summary">
PowerCLI module lifecycle: upgrading to new versions, managing individual sub-modules, handling multi-vCenter version compatibility, and offline bundle management.
</div>

```text
┌─────────────────────────────── PowerCLI — Module Lifecycle Management ────────────────────────────────┐
│                                                                                                       │
│   PowerCLI is versioned independently from vCenter; check compatibility before upgrading              │
│   Each sub-module has its own version; the meta-package pins all sub-module versions                  │
│   Upgrade process: remove old version → install new → test connection → test key cmdlets              │
│                                                                                                       │
│   Version management                                                                                  │
│   Check current: Get-Module -Name VMware.PowerCLI -ListAvailable | Select-Object Name, Version        │
│   Check all sub-modules: Get-Module -Name VMware.* -ListAvailable | Sort-Object Name                  │
│   Find latest: Find-Module -Name VMware.PowerCLI (requires PSGallery access)                          │
│                                                                                                       │
│   Upgrade procedure                                                                                   │
│   Step 1: note current version; check the VMware compatibility matrix for the target vCenter version  │
│   Step 2: uninstall old version: Uninstall-Module -Name VMware.PowerCLI -AllVersions                  │
│   Step 3: install new version: Install-Module -Name VMware.PowerCLI -Scope CurrentUser                │
│   Step 4: verify: connect to vCenter and run Get-Cluster to confirm basic operation                   │
│                                                                                                       │
│   Multi-vCenter version compatibility                                                                 │
│   PowerCLI supports connecting to vCenter versions up to N-2 (two major versions behind)              │
│   Use -Force with Connect-VIServer to connect to unsupported older vCenter versions                   │
│   Cmdlet behaviour may differ: test critical scripts against each vCenter version                     │
│                                                                                                       │
│   Offline (air-gapped) management                                                                     │
│   Save on internet host: Save-Module -Name VMware.PowerCLI -Path C:\offline-modules                   │
│   Copy to air-gapped system; register as local repo: Register-PSRepository                            │
│   Install from local: Install-Module -Name VMware.PowerCLI -Repository LocalRepo                      │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Meta-package = VMware.PowerCLI; installs all sub-modules; pinned to specific versions               │
│   PSGallery   = PowerShell Gallery; public module repository; requires internet access                │
│   NuGet        = package manager provider; required for PSGallery; Install-PackageProvider NuGet      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Check Installed Version

```powershell
# Show all installed PowerCLI modules
Get-Module -Name VMware.* -ListAvailable | Select-Object Name, Version | Sort-Object Name

# Show the main PowerCLI meta-package version
Get-Module -Name VMware.PowerCLI -ListAvailable | Select-Object Name, Version
```

## Upgrade PowerCLI

```powershell
# Upgrade from PSGallery (online)
Update-Module -Name VMware.PowerCLI -Force

# Verify new version
Get-Module -Name VMware.PowerCLI -ListAvailable | Select-Object Name, Version
```

## Selectively Install Sub-modules

```powershell
# Install only the modules you need (reduces footprint)
Install-Module VMware.VimAutomation.Core    -Scope CurrentUser
Install-Module VMware.VimAutomation.Vds     -Scope CurrentUser
Install-Module VMware.VimAutomation.Storage -Scope CurrentUser
Install-Module VMware.VimAutomation.Nsxt    -Scope CurrentUser

# Skip unused modules (e.g., Horizon, HCX) for faster import
```

## Offline Upgrade

```powershell
# On internet-connected machine: download bundle
Save-Module -Name VMware.PowerCLI -Path C:\PSModules -Repository PSGallery

# Copy C:\PSModules to airgapped host, then install
$modulePath = "C:\PSModules"
$env:PSModulePath = "$modulePath;$($env:PSModulePath)"

# Or copy directly into module path
$targetPath = "$([Environment]::GetFolderPath('MyDocuments'))\PowerShell\Modules"
Copy-Item -Path "$modulePath\VMware*" -Destination $targetPath -Recurse -Force
```

## Multi-vCenter Compatibility

PowerCLI connects to vCenter using the vSphere API version supported by the vCenter. When you manage multiple vCenter versions:

```powershell
# Connect to multiple vCenters (different versions)
Connect-VIServer -Server vcenter-old.example.com   # vCenter 7.0
Connect-VIServer -Server vcenter-new.example.com   # vCenter 8.0

# PowerCLI tracks all active connections
$global:DefaultVIServers | Select-Object Name, Version, Build

# Target a specific vCenter in cmdlets
Get-VM -Server vcenter-old.example.com | Select-Object Name
```

**Compatibility notes:**
- PowerCLI 13+ supports vCenter 6.5 through 8.x
- Newer cmdlet parameters may not exist against older APIs — wrap in `try/catch`
- `Get-VsanClusterHealthSummary` requires vSAN API availability (vCenter ≥ 6.5)

## Uninstall Old Modules

```powershell
# Remove specific old version
Uninstall-Module -Name VMware.PowerCLI -RequiredVersion 13.0.0 -Force

# Remove all VMware modules (clean slate)
Get-Module -Name VMware.* -ListAvailable | ForEach-Object {
    Uninstall-Module -Name $_.Name -AllVersions -Force -ErrorAction SilentlyContinue
}
```

## Module Load Time Optimization

```powershell
# Reduce startup time: import only needed sub-modules
# Instead of: Import-Module VMware.PowerCLI  (loads all 40+ sub-modules)
Import-Module VMware.VimAutomation.Core
Import-Module VMware.VimAutomation.Storage

# Measure import time
Measure-Command { Import-Module VMware.PowerCLI } | Select-Object TotalSeconds
```
