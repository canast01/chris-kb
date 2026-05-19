# Pure FlashArray

<div class="kb-summary">
All-flash block storage running Purity//FA — ActiveDR, ActiveCluster, NVMe/FC, NVMe/RoCE, snapshots, protection groups, and Pure1 cloud management for tier-1 and mission-critical block workloads.
</div>

```
┌──────────────────────────────────────── Pure FlashArray Stack ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     Pure FlashArray — All-Flash Block Storage (Purity//FA)                    │   │
│   │   Dual-controller HA pair: CT0 + CT1 active/active with NVRAM mirroring for < 1 ms write ACK  │   │
│   │     Protocols: Fibre Channel (16/32G) · iSCSI (10/25 GbE) · NVMe/FC · NVMe/RoCE · NVMe/TCP    │   │
│   │Pure1: cloud management portal — telemetry, AI support alerts, capacity forecasting, proactive │   │
│   │  Replication: ActiveDR (async, RPO minutes) · ActiveCluster (sync, zero RPO, stretch cluster) │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    FlashArray management layer feeds architecture, operations, security, and troubleshooting          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │    CT0/CT1 HA pair design   │  │   purearray CLI + REST API  │  │  SafeMode: immutable snaps  │   │
│   │  NVRAM: write buffer+mirror │  │ Volume: create, expand, map │  │   RBAC: roles + API tokens  │   │
│   │   Flash shelves: NVMe SSD   │  │   Snapshots + clones + PGs  │  │    Data-at-rest: AES-256    │   │
│   │   Inline dedup+compression  │  │ Health: drives, ports, cache│  │  Audit log + syslog export  │   │
│   │ ActiveCluster: stretch vols │  │ ActiveDR: async replication │  │ Directory services: AD/LDAP │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines HA and data path · Operations manage volumes · Security hardens access and dat│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │  Volume offline  │  purearray list  │  Drive health OK  │  Case: array ID  │  purearray get   │   │
│   │Repl lag/BW check │ purelog download │  Port: link state │  Log bundle req  │ purevolume list  │   │
│   │ HA failover path │puresupport bundle│  Capacity: >80%?  │  Remote assist   │ purehgroup list  │   │
│   │Snap space growth │ netconfig verify │ Repl state: Active│  P1/P2 severity  │  pureport list   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dual controllers (CT0/CT1) · NVMe flash shelves · FC/iSCSI/NVMe HBAs · SAN switches · Power & Cooling│
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Purity//FA    = FlashArray operating system; manages data services, dedup, compression, and protocols│
│  NVRAM         = Non-volatile RAM; write buffer mirrored CT0↔CT1 before ACK — guarantees < 1 ms writes│
│  ActiveCluster = Synchronous stretch cluster; zero RPO across two sites or arrays on same fabric      │
│  ActiveDR      = Asynchronous replication; RPO in minutes; automated failover and failback workflow   │
│  SafeMode      = Pure immutable snapshot protection; delete requires PIN from Pure Storage support    │
│  Protection Group= PG; set of volumes replicated together on a schedule to a target array or cloud    │
│  Inline dedup  = Deduplication applied before data hits flash; no post-process latency penalty        │
│  CT0 / CT1     = Controller 0 and Controller 1; both actively serve I/O simultaneously                │
│  NVMe/RoCE     = NVMe over RDMA over Converged Ethernet; ultra-low latency block access over IP fabric│
│  NVMe/FC       = NVMe over Fibre Channel; block protocol for NVMe SSDs transported over FC fabric     │
│  Pure1         = Cloud management portal; remote telemetry, AI-driven alerts, capacity forecasting    │
│  RBAC          = Role-Based Access Control; Storage Admin, Array Admin, Read-Only built-in roles      │
│  purearray     = CLI entry point on FlashArray; purearray get/list/set for array-level config         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
