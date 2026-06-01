---
title: vSAN
---

# vSAN

<div class="kb-summary">
Technical and operational reference for VMware vSAN. Covers storage policies, disk groups, capacity management, resync operations, health monitoring, and troubleshooting for software-defined storage in vSphere clusters.
</div>

```
┌───────────────────────────────── vSAN Software-Defined Storage Stack ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     VMware vSAN — Hyper-Converged Software-Defined Storage                    │   │
│   │      Object-based storage: VMs stored as objects distributed across hosts in the cluster      │   │
│   │   Disk groups (OSA): 1 cache device + 1-7 capacity devices per host; or vSAN ESA (all-NVMe)   │   │
│   │     SPBM policies: FTT (failures to tolerate), stripe width, dedup/compression, encryption    │   │
│   │           Resync: data rebuilds after host/disk failure; controlled by I/O scheduler          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Disk groups form the storage layer · SPBM policies govern data protection                          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │  Disk group: cache+capacity │  │     SPBM: policy per VM     │  │    D@RE: AES-256 at rest    │   │
│   │  FTT: RAID-1/5/6 tolerance  │  │  Capacity: usage + forecast │  │  In-transit: encryption on  │   │
│   │   Witness host: stretched   │  │   Health: proactive checks  │  │   KMS: external key server  │   │
│   │   vSAN ESA: NVMe-only tier  │  │  Resync: monitor + throttle │  │       RBAC: vSAN roles      │   │
│   │  Dedup+compression: cluster │  │    Disk group: add/remove   │  │  Audit log: config changes  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines the disk groups · Operations manage policies and capacity                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │Non-compliant objs│vsan.health.health│ Health: all green?│GSS: collect logs │   esxcli vsan    │   │
│   │Disk group failure│ vsan.disks_stats │   Capacity <70%?  │  TAM escalation  │  rvc vsan.check  │   │
│   │Resync: high delay│vsan.resync_dashbo│    Resync: <1%?   │  Log bundle req  │ rvc vsan.summary │   │
│   │Performance: high │ vsan.perf.stats  │  FTT: compliant?  │ P1: data at risk │ cmmds-tool find  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts with NVMe/SSD disks · vSAN VMkernel NICs (25 GbE min) · ToR switches · Power & Cooling    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SPBM          = Storage Policy-Based Management; assigns FTT, stripe, dedup rules per VM disk        │
│  FTT           = Failures to Tolerate; RAID-1=1 host, RAID-5=1 host (4 needed), RAID-6=2 hosts        │
│  Disk group    = Per-host grouping of 1 cache device + 1-7 capacity NVMe/SSD devices                  │
│  vSAN ESA      = Express Storage Architecture; single-tier all-NVMe; replaces OSA disk groups         │
│  Resync        = Data rebuild after device or host failure; monitored via health dashboard            │
│  D@RE          = Data at Rest Encryption; AES-256 per disk group; requires external KMS               │
│  Witness host  = Tie-breaking third site in stretched cluster; holds metadata only, no data           │
│  Dedup         = Deduplication applied at block level across disk group; cluster-wide or host-local   │
│  CMMDS         = Cluster Monitoring, Membership, and Directory Services; vSAN metadata plane          │
│  Stripe width  = Number of capacity devices a single object is striped across for performance         │
│  RVC           = Ruby vSphere Console; CLI for vSAN health and capacity diagnostic commands           │
│  Non-compliant = Object does not meet its assigned SPBM policy; usually after host/disk failure       │
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
