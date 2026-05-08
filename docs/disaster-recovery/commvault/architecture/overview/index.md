# Commvault — Architecture Overview

Commvault provides enterprise backup, recovery, replication, archive, and data protection management.

## Component Topology

```mermaid
graph TB
  CS["CommServe\n(command & control)"] --> WEBCON["Web Console\n& Command Center"]
  MA1["Media Agent 1\n(data mover)"] & MA2["Media Agent 2"] --> CS
  SRC(["Source — VMs / DBs / Files"]) --> MA1 & MA2
  MA1 & MA2 --> DISK[("Disk Library\nDDB dedup")]
  DISK -->|"aux copy"| TAPE[("Tape / Object\nlong-term retention")]
  ADMIN(["Backup Admin"]) --> WEBCON
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class CS,MA1,MA2 ctrl
  class DISK,TAPE store
  class SRC,ADMIN host
  class WEBCON mgmt
```

## Data Flow

```
Client (backup agent)
    │
    ▼ CVLT network (TCP 8403)
MediaAgent (reads data, applies dedup, writes to storage)
    │
    ├── Primary copy (disk/dedup, performance tier)
    └── Secondary copy (offsite/cloud/tape, retention tier)
    │
CommServe (orchestrates job, tracks metadata in SQL DB)
```

## Scale-Out with Hyperscale X

Hyperscale X integrates CommServe + MediaAgent + storage into scale-out nodes:
- Minimum 3-node cluster; add nodes for capacity/throughput
- Built-in object storage using erasure coding
- Managed via Command Center — no separate storage administration

## Port Requirements

| Source | Destination | Port | Purpose |
|---|---|---|---|
| Clients | CommServe | 8400 | Job requests |
| Clients | MediaAgent | 8403 | Data movement |
| CommServe | MediaAgent | 8400 | Job orchestration |
| Browser (admin) | Command Center | 443 | Web UI |
