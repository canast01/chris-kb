# Windows Server — Architecture

<div class="kb-summary">
Windows Server 2019/2022/2025 infrastructure — Active Directory DS, DNS, SMB file services, Hyper-V, WSUS, and PowerShell-based management. Available in Standard and Datacenter editions with Server Core (recommended) or Desktop Experience installation.
</div>

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">How It Works</div>
    <div class="kb-card-desc">Edition and installation types, key server roles, critical services, common ports, event log channels, and PowerShell reference.</div>
  </a>
  <a class="kb-card" href="integrations/">
    <div class="kb-card-icon">🔗</div>
    <div class="kb-card-title">Integrations</div>
    <div class="kb-card-desc">Active Directory, Group Policy, SAN/SMB storage connectivity, Hyper-V, and monitoring via WMI/WinRM.</div>
  </a>
  <a class="kb-card" href="design-standards/">
    <div class="kb-card-icon">📐</div>
    <div class="kb-card-title">Design Standards</div>
    <div class="kb-card-desc">Edition selection criteria, Server Core baseline, patch management policy, and firewall rule standards.</div>
  </a>
</div>

## Editions

| Version | Edition | Key Differentiator |
|---|---|---|
| Windows Server 2019/2022/2025 | Standard | Up to 2 Hyper-V VMs per licence |
| Windows Server 2019/2022/2025 | Datacenter | Unlimited Hyper-V VMs; Storage Spaces Direct, SDN |
| All | Server Core | No GUI; smaller attack surface; recommended for production |
| All | Desktop Experience | Full GUI; required for some legacy management tools |

## Topology

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
