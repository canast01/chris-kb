# Data Domain — Architecture

<div class="kb-summary">
Dell PowerProtect DD (Data Domain) is a purpose-built backup appliance with inline global deduplication via the SISL engine. DDBoost integration with backup software reduces network traffic by ~50% via source-side deduplication. Typical dedup ratios: 20:1 or greater.
</div>

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">How It Works</div>
    <div class="kb-card-desc">SISL dedup engine, DDFS/MTree namespace, DDBoost source-side filtering, DD Replicator, cloud tier, and key CLI commands.</div>
  </a>
  <a class="kb-card" href="integrations/">
    <div class="kb-card-icon">🔗</div>
    <div class="kb-card-title">Integrations</div>
    <div class="kb-card-desc">NetBackup, Commvault, Veeam DDBoost integration, VTL for legacy backup software, and cloud tier object storage.</div>
  </a>
  <a class="kb-card" href="design-standards/">
    <div class="kb-card-icon">📐</div>
    <div class="kb-card-title">Design Standards</div>
    <div class="kb-card-desc">MTree layout, replication topology, DDBoost vs NFS protocol selection, and cloud tier lifecycle policy design.</div>
  </a>
</div>

## Protocol Access

| Protocol | Port | Use Case |
|---|---|---|
| DDBoost over IP | TCP 2052 / 2053 | Primary — backup software integration |
| NFS v3 | TCP/UDP 2049 | Unix/Linux backup clients |
| CIFS/SMB | TCP 445 | Windows backup clients |
| VTL | FC | Tape-emulation for legacy backup software |
| DD Replicator | TCP 2051 | DD-to-DD replication |
| Management | TCP 22 / 443 | SSH CLI and HTTPS UI |

## Topology

```mermaid
graph TB
  BU(["Backup Servers\nNetBackup / Commvault / Veeam"]) -->|"DDBoost / NFS / CIFS / VTL"| DD["Dell Data Domain\n(dedup + compression)"]
  DD -->|"DD Replicator\nTCP 2051"| DDDR["Remote Data Domain\n(DR copy)"]
  DD --> CLOUD["Cloud Tier\nS3 / Azure Blob — long-term"]
  DD --> VTL["Virtual Tape Library\n(optional — FC)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class DD ctrl
  class BU host
  class CLOUD cloud
  class DDDR dr
```
