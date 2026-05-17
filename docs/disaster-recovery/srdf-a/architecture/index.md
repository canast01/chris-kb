# SRDF/A — Architecture

<div class="kb-summary">
Dell PowerMax SRDF/A asynchronous replication — delta set cycle model buffers writes and transmits to R2 on a ~30-second cycle; RPO equals the last completed cycle.
</div>

![SRDF/A Architecture](../../../../assets/srdf-a-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Delta set mechanics, SRDF group design, pair states, SYMCLI commands, and bandwidth sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>SRM, Solutions Enabler, and TimeFinder/SnapVX for backup offload.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>SRDF group naming, cycle time standards, lag thresholds, and DSE sizing.</span></a>
</div>

| State | Meaning | Normal? |
|---|---|---|
| Consistent | R2 is consistent and receiving cycles | Yes — normal SRDF/A state |
| SyncInProg | Synchronisation in progress after resume | Transient |
| Transmit Idle | No data being transmitted | Investigate if unexpected |
| Suspended | Replication manually suspended | Expected for maintenance |
| Failed Over | R1 read-only; R2 writable | Active failover underway |

```mermaid
graph LR
  HA(["Production Hosts"]) --> PM_A["PowerMax R1\nSite A"]
  PM_A -->|"writes buffered\nin delta set"| DSE["DSE Overflow Buffer\n(WAN saturation protection)"]
  DSE -->|"cycle flush ~30s"| PM_B["PowerMax R2\nSite B"]
  PM_B -.->|"lag / RPO monitor"| LAG["Cycle State\nMonitor"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PM_A ctrl
  class PM_B dr
  class DSE,LAG mgmt
  class HA host
```
