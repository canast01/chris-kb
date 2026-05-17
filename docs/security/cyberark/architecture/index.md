# CyberArk — Architecture

<div class="kb-summary">
PAM platform with Digital Vault as the encrypted credential store, CPM for automated rotation, PSM for session proxying and recording, and PVWA as the web interface; primary and DR Vault pair with asynchronous replication.
</div>

![CyberArk Architecture](../../../assets/cyberark-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Component roles, network topology, credential checkout, HA, and DR activation.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## Component Overview

| Component | Role | Typical Count |
|---|---|---|
| Digital Vault | Encrypted credential store, core engine | 2 (primary + DR) |
| CPM (Central Policy Manager) | Automated password rotation | 1–2 per site |
| PSM (Privileged Session Manager) | Session proxy, recording, isolation | 2+ (load-balanced) |
| PVWA (Password Vault Web Access) | Web UI and REST API | 2+ (load-balanced) |
| PSMP | SSH proxy for Linux privileged access | 1–2 per site |
| DR Vault | Asynchronous replication replica of Vault | 1 per DR site |

## PAM Component Topology

```mermaid
graph TB
  PVWA["PVWA\n(web interface)"] & PSM["PSM\n(session proxy)"] & CPM["CPM\n(rotation engine)"] --> VAULT["CyberArk Vault\n(encrypted credential store)"]
  USER(["Privileged User"]) -->|"browser"| PVWA
  PSM -->|"RDP / SSH proxy\nsession recording"| TARGET(["Target Servers"])
  CPM -->|"password rotation"| TARGET
  VAULT -.->|"audit stream"| SIEM(["SIEM"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VAULT store
  class PVWA,PSM,CPM ctrl
  class USER,TARGET,SIEM host
```
