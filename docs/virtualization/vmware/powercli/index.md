---
tags:
  - powercli
  - vmware
---
# VMware PowerCLI

<div class="kb-summary">
PowerCLI is VMware's official PowerShell module suite for automating and managing vSphere, NSX, vSAN, vCD, and other VMware products. It provides 900+ cmdlets covering the full vSphere API, enabling scripted VM operations, host configuration, storage management, and reporting at scale.
</div>

```text
┌────────────────────────────────────── VMware PowerCLI Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                VMware PowerCLI — PowerShell module suite for vSphere automation               │   │
│   │             Built on top of the vSphere SOAP/REST APIs — same calls as vCenter UI             │   │
│   │               Platform: PowerShell 7+ (cross-platform) or Windows PowerShell 5.1              │   │
│   │            Install: Install-Module VMware.PowerCLI from PSGallery; 40+ sub-modules            │   │
│   │           Session: Connect-VIServer -> $global:DefaultVIServer -> all cmdlets use it          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │                 Core Modules                 │                                                    │
│   │   VimAutomation.Core  VM + host + cluster    │                                                    │
│   │     VimAutomation.Vds   vDS + portgroups     │                                                    │
│   │   VimAutomation.Storage  VMDK + datastores   │                                                    │
│   │   VimAutomation.Nsxt  NSX-T policy objects   │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │                Add-on Modules               │   │
│                                                     │    VimAutomation.Srm   SRM recovery plans   │   │
│                                                     │      VimAutomation.Hcx   HCX migration      │   │
│                                                     │      VimAutomation.Horizon  Horizon VDI     │   │
│                                                     │     VimAutomation.vROps  Aria Operations    │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │               Connection Model               │                                                    │
│   │       Connect-VIServer -Server <FQDN>        │                                                    │
│   │           -> SSO token from vCenter          │                                                    │
│   │         -> $global:DefaultVIServer set       │                                                    │
│   │       -> All cmdlets use this implicitly     │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │                 API Binding                 │   │
│                                                     │       High-level: Get-VM -> VI objects      │   │
│                                                     │    Low-level: Get-View -> raw vSphere API   │   │
│                                                     │      View objects: faster, no wrappers      │   │
│                                                     │        ExtensionData: .NET SDK access       │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure: Windows/Linux jump host with PowerShell 7+ installed                        │
│  Network: HTTPS/443 to vCenter FQDN  ·  DNS resolution required                                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VI Object    = high-level wrapper (Get-VM, Get-VMHost) with helper properties                        │
│  View Object  = raw vSphere API object; faster but no helper properties                               │
│  SOAP API     = vSphere legacy API (port 443 /sdk); used by most cmdlets                              │
│  REST API     = vSphere modern API; used by newer NSX/vSAN cmdlets                                    │
│  SSO Token    = session credential; valid 8 h by default; auto-renewed                                │
│  PSGallery    = PowerShell module repository; source for Install-Module                               │
│  DefaultVIServer = implicit connection target for all cmdlets in session                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<!-- diagram:powercli -->

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How PowerCLI connects to vCenter/ESXi, module structure, credential handling, and integration points.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installing PowerCLI, connecting to vCenter, service account setup, and multi-vCenter environments.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Cmdlet reference, scripts library, health checks, procedures, lifecycle, and automation patterns.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Service account least privilege, credential storage, certificate validation, and connection hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Connection errors, cmdlet failures, certificate issues, and API permission errors.</span>
</a>

</div>
