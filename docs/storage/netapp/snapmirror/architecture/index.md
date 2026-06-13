# SnapMirror — Architecture

<div class="kb-summary">
SnapMirror architecture reference — replication types (Async, Sync, SMBC, XDP), components, connectivity requirements, and DR failover procedures.
</div>

![SnapMirror Architecture](../../../../assets/snapmirror-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Replication types, components, connectivity, CLI commands, DR failover sequence, and SVM-level replication.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, policy baseline, and configuration checklist.</span></a>
</div>

| Type | RPO | Description |
|---|---|---|
| SnapMirror Async | Configurable, minutes to hours | Standard volume replication; transfers run on a schedule; destination read-only DP volume |
| SnapMirror Sync | Zero RPO | Every write acknowledged on both source and destination; requires <5ms RTT |
| SMBC (AutomatedFailOver) | Zero RPO, transparent failover | Consistency group-based; mediator-assisted automatic failover; no host reconfiguration |
| SnapVault / XDP | Daily/weekly backup copies | Extended data protection; independent retention on destination |

```mermaid
graph LR
  SRC["Source Volume\nSVM / Cluster A"] -->|"SnapMirror replication\n(incremental block diff)"| DST["Destination Volume\nSVM / Cluster B — read-only"]
  SRC --> SNAP[("Local Snapshots")]
  DST -->|"break to activate for DR"| DRACT["DR Active Volume\n(after SnapMirror break)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class SRC,DST ctrl
  class SNAP store
  class DRACT dr
```
