# Unity — Architecture Overview

## Overview

Dell Unity XT is a mid-range unified storage platform delivering block (Fibre Channel, iSCSI) and file (NFS, SMB) storage from a single system. It uses a dual storage processor architecture with automatic failover between SP A and SP B. Unity XT is available as purpose-built hardware (Unity XT 380, 480, 680, 880) and as a software-defined appliance (UnityVSA). Administration is via the Unisphere for Unity web GUI or the `uemcli` command-line interface.

## Dual Storage Processor Architecture

```mermaid
graph TB
  SPA["Storage Processor A\n(active for pool set A)"] <-->|"HA heartbeat"| SPB["Storage Processor B\n(standby / active)"]
  SPA & SPB --> POOL[("Drive Pool\nSSD / NL-SAS / SAS")]
  SPA --> NAS["NFS · SMB · FTP\nData Mover"]
  SPA --> SAN["iSCSI · FC\nBlock LUNs"]
  SPB --> NAS & SAN
  NAS --> NH(["NAS Clients"])
  SAN --> SH(["SAN Hosts"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class SPA,SPB ctrl
  class POOL store
  class NH,SH host
```

## HA Topology

Unity XT uses an active-passive dual-SP model where LUN and filesystem ownership is distributed across both SPs, but each resource is owned by only one SP at a time.

- Both SPs are powered on and connected to the same storage enclosures and host FC/iSCSI fabric.
- Each SP independently serves I/O for the LUNs and NAS servers assigned to it.
- If an SP fails, the peer SP automatically takes ownership of all resources within approximately 30 seconds — no data loss occurs because write cache is mirrored between SPs.
- During SP failover, host multipath drivers (PowerPath, MPIO, DM-MPIO) redirect I/O to the surviving SP's ports.
- Optional replication: asynchronous or synchronous replication to a secondary Unity or PowerStore array for DR.
