# Aria Ops for Logs — Architecture Overview

## Overview

Aria Operations for Logs (formerly vRealize Log Insight) is a log analytics platform that collects, indexes, and correlates log data from VMware infrastructure and other sources.

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

## Cluster Topology

| Node Role | Description |
|---|---|
| **Master** | Primary node — handles ingestion, indexing, query coordination, and cluster management UI |
| **Worker** | Scale-out nodes — add workers to increase ingestion throughput and storage capacity |

A minimum of **3 nodes** (1 master + 2 workers) is recommended for production HA.
