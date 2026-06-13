# Data Domain — Architecture

<div class="kb-summary">
Dell PowerProtect DD (Data Domain) is a purpose-built backup appliance with inline global deduplication via the SISL engine. DDBoost integration with backup software reduces network traffic by ~50% via source-side deduplication. Typical dedup ratios: 20:1 or greater.
</div>

![Data Domain Architecture](../../../../assets/data-domain-architecture-overview.svg)

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

