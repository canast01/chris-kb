# VMware Cloud Foundation — Operational Scripts

```text
┌──────────────────────────── VMware Cloud Foundation — Operational Scripts ────────────────────────────┐
│                                                                                                       │
│  PowerVCF scripts automate VCF operations: domain inventory, upgrade status,                          │
│  credential audit, certificate expiry check, and health report generation.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Inventory Scripts               │  │            Health & Cert Scripts            │   │
│   │          Get-VCFDomain | Export-Csv          │  │           Request-VCFToken (auth)           │   │
│   │           Get-VCFHost (all hosts)            │  │         Get-VCFCertificate (expiry)         │   │
│   │        Get-VCFCluster (all clusters)         │  │       VMware.CloudFoundation.Reporting      │   │
│   │          Get-VCFCredential (audit)           │  │            Invoke-VcfHealthReport           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  PowerVCF scripts connect to SDDC Manager REST API; read-only ops need no approval.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Scripts                │  │             Automation Examples             │   │
│   │         Get-VCFBundle (list bundles)         │  │            New-VCFDomain (create)           │   │
│   │            Start-VCFBundleUpload             │  │           Add-VCFHost (commission)          │   │
│   │          Start-VCFUpgrade (trigger)          │  │          Set-VCFCredential (rotate)         │   │
│   │          Get-VCFTask (status poll)           │  │          Watch upgrade via task ID          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Scripts run from management jump host; connect to SDDC Manager on port 443;                          │
│  VMware.CloudFoundation.Reporting module needs PowerCLI + PowerVCF.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PowerVCF       = PowerShell module for SDDC Manager automation                                       │
│  Request-VCFToken= authenticate and store bearer token for session                                    │
│  Get-VCFBundle  = list available upgrade bundles in depot/local                                       │
│  Start-VCFUpgrade= trigger upgrade for a domain or component                                          │
│  Get-VCFTask   = poll async task status by task ID                                                    │
│  Invoke-VcfHealthReport= generates HTML health report for all domains                                 │
│  Get-VCFCertificate= certificate expiry report for all components                                     │
│  New-VCFDomain = automate workload domain creation via API                                            │
│  Add-VCFHost   = commission new host to SDDC Manager                                                  │
│  Set-VCFCredential= trigger credential rotation for component                                         │
│  Reporting module= VMware.CloudFoundation.Reporting on PowerShell Gallery                             │
│  Task ID       = async operation ID; poll with Get-VCFTask until complete                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────── VMware Cloud Foundation — Operational Scripts ────────────────────────────┐
│                                                                                                       │
│  PowerVCF scripts automate VCF operations: domain inventory, upgrade status,                          │
│  credential audit, certificate expiry check, and health report generation.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Inventory Scripts               │  │            Health & Cert Scripts            │   │
│   │          Get-VCFDomain | Export-Csv          │  │           Request-VCFToken (auth)           │   │
│   │           Get-VCFHost (all hosts)            │  │         Get-VCFCertificate (expiry)         │   │
│   │        Get-VCFCluster (all clusters)         │  │       VMware.CloudFoundation.Reporting      │   │
│   │          Get-VCFCredential (audit)           │  │            Invoke-VcfHealthReport           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  PowerVCF scripts connect to SDDC Manager REST API; read-only ops need no approval.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Scripts                │  │             Automation Examples             │   │
│   │         Get-VCFBundle (list bundles)         │  │            New-VCFDomain (create)           │   │
│   │            Start-VCFBundleUpload             │  │           Add-VCFHost (commission)          │   │
│   │          Start-VCFUpgrade (trigger)          │  │          Set-VCFCredential (rotate)         │   │
│   │          Get-VCFTask (status poll)           │  │          Watch upgrade via task ID          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Scripts run from management jump host; connect to SDDC Manager on port 443;                          │
│  VMware.CloudFoundation.Reporting module needs PowerCLI + PowerVCF.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PowerVCF       = PowerShell module for SDDC Manager automation                                       │
│  Request-VCFToken= authenticate and store bearer token for session                                    │
│  Get-VCFBundle  = list available upgrade bundles in depot/local                                       │
│  Start-VCFUpgrade= trigger upgrade for a domain or component                                          │
│  Get-VCFTask   = poll async task status by task ID                                                    │
│  Invoke-VcfHealthReport= generates HTML health report for all domains                                 │
│  Get-VCFCertificate= certificate expiry report for all components                                     │
│  New-VCFDomain = automate workload domain creation via API                                            │
│  Add-VCFHost   = commission new host to SDDC Manager                                                  │
│  Set-VCFCredential= trigger credential rotation for component                                         │
│  Reporting module= VMware.CloudFoundation.Reporting on PowerShell Gallery                             │
│  Task ID       = async operation ID; poll with Get-VCFTask until complete                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────────────────┐
│  Script Output / Integration                                                                          │
│  → stdout / CSV / JSON                                                                                │
│  → monitoring platform (HTTP POST)                                                                    │
│  → ITSM ticketing system                                                                              │
│  → CMDB asset discovery                                                                               │
└─────────────────────────────────────────────────────┘
```

```powershell
┌──────────────────────────── VMware Cloud Foundation — Operational Scripts ────────────────────────────┐
│                                                                                                       │
│  PowerVCF scripts automate VCF operations: domain inventory, upgrade status,                          │
│  credential audit, certificate expiry check, and health report generation.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Inventory Scripts               │  │            Health & Cert Scripts            │   │
│   │          Get-VCFDomain | Export-Csv          │  │           Request-VCFToken (auth)           │   │
│   │           Get-VCFHost (all hosts)            │  │         Get-VCFCertificate (expiry)         │   │
│   │        Get-VCFCluster (all clusters)         │  │       VMware.CloudFoundation.Reporting      │   │
│   │          Get-VCFCredential (audit)           │  │            Invoke-VcfHealthReport           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  PowerVCF scripts connect to SDDC Manager REST API; read-only ops need no approval.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Scripts                │  │             Automation Examples             │   │
│   │         Get-VCFBundle (list bundles)         │  │            New-VCFDomain (create)           │   │
│   │            Start-VCFBundleUpload             │  │           Add-VCFHost (commission)          │   │
│   │          Start-VCFUpgrade (trigger)          │  │          Set-VCFCredential (rotate)         │   │
│   │          Get-VCFTask (status poll)           │  │          Watch upgrade via task ID          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Scripts run from management jump host; connect to SDDC Manager on port 443;                          │
│  VMware.CloudFoundation.Reporting module needs PowerCLI + PowerVCF.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PowerVCF       = PowerShell module for SDDC Manager automation                                       │
│  Request-VCFToken= authenticate and store bearer token for session                                    │
│  Get-VCFBundle  = list available upgrade bundles in depot/local                                       │
│  Start-VCFUpgrade= trigger upgrade for a domain or component                                          │
│  Get-VCFTask   = poll async task status by task ID                                                    │
│  Invoke-VcfHealthReport= generates HTML health report for all domains                                 │
│  Get-VCFCertificate= certificate expiry report for all components                                     │
│  New-VCFDomain = automate workload domain creation via API                                            │
│  Add-VCFHost   = commission new host to SDDC Manager                                                  │
│  Set-VCFCredential= trigger credential rotation for component                                         │
│  Reporting module= VMware.CloudFoundation.Reporting on PowerShell Gallery                             │
│  Task ID       = async operation ID; poll with Get-VCFTask until complete                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
