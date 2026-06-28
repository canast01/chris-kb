---
tags:
  - architecture
  - aria-logs
  - vmware
---
# Aria Operations for Logs — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Log Pipeline Architecture, ESXi Syslog Configuration.

*Applies to: Aria Operations for Logs 8.x*
</div>
![Aria Operations for Logs — How It Works](../../../../assets/virtualization-vmware-aria-operations-for-logs-architecture-.svg)


```d2
direction: right

center: "Aria Operations for Logs" {shape: hexagon}
log_pipeline_architecture: "Log Pipeline Architecture" {shape: rectangle}

center -> log_pipeline_architecture
```

## Overview

Aria Operations for Logs (formerly vRealize Log Insight) collects, indexes, and correlates log data from VMware infrastructure and other sources. It provides real-time search, pattern-based alerting, content pack dashboards, and bidirectional launch-in-context integration with Aria Operations. Logs are retained in a hot Cassandra index and optionally archived to NFS for long-term storage.

## Log Pipeline Architecture

```mermaid
graph TB
  SRC1(["ESXi / vCenter syslog"]) & SRC2(["NSX / VMs syslog"]) & SRC3(["Linux / Windows agent"]) --> VRLI["Aria Operations for Logs\n(Log Intelligence cluster)"]
  VRLI --> IDX[("Log Index\nhot + warm retention")]
  VRLI --> ALERTS["Alert Rules & Notifications"]
  ADMIN(["Operator"]) -->|"browser"| VRLI
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VRLI ctrl
  class IDX store
  class SRC1,SRC2,SRC3,ADMIN host
```




## See also

- [Aria Ops for Logs — Standards](design-standards/)
- [Aria Operations for Logs — Deploy](../deploy/)
- [Aria Ops for Logs — Integrations](integrations/)
