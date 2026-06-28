---
tags:
  - architecture
  - windows
---
# Windows Server — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Editions and Installation Types, Role Topology.

*Applies to: Windows Server 2019 / 2022*
</div>

## Overview

Windows Server delivers infrastructure services through **Roles** (major functions) and **Features** (supporting components) installed on top of the base OS. The current supported versions are 2019, 2022, and 2025, available in Standard and Datacenter editions. All server administration uses PowerShell, WinRM remoting, or RSAT tools. Server Core (no GUI) is the recommended installation type for security and performance.

## Editions and Installation Types

| Version | Edition | Notes |
|---|---|---|
| Windows Server 2019/2022/2025 | Standard | Up to 2 Hyper-V VMs per licence |
| Windows Server 2019/2022/2025 | Datacenter | Unlimited Hyper-V VMs; Storage Spaces Direct, SDN |
| All | Server Core | No GUI; PowerShell remoting / RSAT; smaller attack surface |
| All | Desktop Experience | Full GUI; larger footprint; required for some legacy tools |

## Role Topology

```mermaid
graph TB
  WS["Windows Server 2019 / 2022"]
  WS --> AD["Active Directory DS\n(DC role)"]
  WS --> DNS_R["DNS Server"]
  WS --> FS["File Server\nSMB · DFS"]
  WS --> IIS["IIS / App Roles"]
  WS --> WSUS["Windows Update\nWSUS / Azure Update Manager"]
  WS --> SEC["Windows Defender\nFirewall · Audit Policy"]
  ADMIN(["Windows Admin"]) -->|"RDP / PowerShell"| WS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class WS ctrl
  class AD,DNS_R,FS,IIS,WSUS,SEC mgmt
  class ADMIN host
```

---

## See also

- [Windows Server — Design Standards](../design-standards/)
- [Windows Server — Integrations](../integrations/)
- [Windows Server — Deploy](../../deploy/)
