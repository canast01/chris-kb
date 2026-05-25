# SRDF/S — Architecture

<div class="kb-summary">
Dell PowerMax SRDF/S synchronous replication — every host write is committed to both R1 and R2 before acknowledgement, guaranteeing RPO = 0; requires ≤10ms inter-site RTT.
</div>

![SRDF/S Architecture](../../../assets/srdf-s-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Synchronous write commit model, pair states, RTT requirements, SYMCLI commands, and RTO targets.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>SRM automated failover, Solutions Enabler, and SRDF/Metro active-active variant.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>RTT thresholds, SRDF group naming, consistency group design, and failover runbook.</span></a>
</div>

| Pair State | Description | Host Write Impact |
|---|---|---|
| Synchronized | R1 and R2 identical; writes committed to both | Full protection, RPO = 0 |
| SyncInProg | Initial or resync copy in progress | R1 writable; R2 not consistent |
| Suspended | Replication paused | R1 writable; R2 stale |
| Failed Over | R1 unavailable; R2 writable | R2 takes production I/O |

```mermaid
graph LR
  HA(["Production Hosts\nSite A"]) --> PM_A["PowerMax R1\nSite A"]
  PM_A -->|"SRDF/S synchronous\n≤10ms RTT"| PM_B["PowerMax R2\nSite B"]
  PM_B -.->|"read-only\n(Synchronized state)"| HB(["Standby Hosts\nSite B"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PM_A ctrl
  class PM_B dr
  class HA host
  class HB dr
```
