# Superna Eyeglass — Architecture

<div class="kb-summary">
Superna Eyeglass DR orchestration for NetApp PowerScale — automates SyncIQ failover, SMB/NFS share reconfiguration, quota migration, and DNS cutover in 5–15 minutes.
</div>

![Superna Eyeglass Architecture](../../../../assets/superna-eyeglass-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Failover execution flow, DR readiness scoring, CLI commands, sizing, and RPO tiers.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>PowerScale SyncIQ, Active Directory DNS, and SNMP/email alerting.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Policy naming, RPO tier assignments, readiness thresholds, and test schedule.</span></a>
</div>

| Component | Role | Location |
|---|---|---|
| Eyeglass Primary Appliance | Monitors SyncIQ; syncs share/quota config; DR orchestration control | Primary site |
| Eyeglass DR Appliance | Standby node; activates when primary site unavailable | DR site |
| PowerScale SyncIQ | Underlying data replication engine | Both sites |
| DNS Integration | Automated SmartConnect zone cutover during failover | Primary / DR DNS |

```mermaid
graph LR
  PS_A["PowerScale Cluster A\n(production)"] -->|"SyncIQ policy"| PS_B["PowerScale Cluster B\n(DR)"]
  EG["Superna Eyeglass\nDR Assistant"] -->|"monitors SyncIQ"| PS_A
  EG -->|"orchestrates failover\naccess zone migration"| PS_B
  ADMIN(["Admin"]) -->|"Eyeglass UI"| EG
  DNS(["DNS / AD\naccess zone cutover"]) <--> EG
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PS_A ctrl
  class PS_B dr
  class EG mgmt
  class ADMIN,DNS host
```
