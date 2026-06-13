---
title: vSAN
tags:
  - vmware
  - vsan
  - vsphere-8
---

# vSAN

<div class="kb-summary">
Technical and operational reference for VMware vSAN. Covers storage policies, disk groups, capacity management, resync operations, health monitoring, and troubleshooting for software-defined storage in vSphere clusters.
</div>

```text
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

```text
┌──────────────────────────────────── vSAN — Installation Sequence ─────────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Checks                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  All hosts in cluster have vSAN VMkernel adapter  ·  MTU 9000 confirmed                               │
│  vSAN HCL: SSD/NVMe cache tier and HDD/NVMe capacity tier all listed                                  │
│  Minimum disk requirements: 1 cache + 1 capacity per disk group per host                              │
│  Network: dedicated 10 GbE+ uplinks for vSAN traffic  ·  No shared vMotion                            │
│  Cluster has ≥3 hosts for FTT=1  ·  ≥5 hosts for RAID-5 erasure coding                                │
│                                                                                                       │
│                                        │  enable vSAN on cluster                                      │
│                                        ▼                                                              │
│  Step 2 · Enable vSAN                                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  vCenter → Cluster → Configure → vSAN → Turn On                                                       │
│  Select single-site or stretched cluster  ·  Enable deduplication/compression                         │
│  Fault domains: configure if multi-rack to honour rack-level failure tolerance                        │
│  Encryption: enable at rest if data-at-rest policy requires it                                        │
│  vSAN bootstrap: first disk group created on each host during wizard                                  │
│                                                                                                       │
│                                        │  claim disks and configure disk groups                       │
│                                        ▼                                                              │
│  Step 3 · Disk Group Configuration                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Claim cache tier (NVMe/SSD)  ·  Claim capacity tier (NVMe/SSD/HDD)                                   │
│  Disk format: disk group type — hybrid or all-flash  ·  On-disk format v14+                           │
│  Add capacity hosts: each host must contribute at least one disk group                                │
│  Verify disk groups healthy: no degraded, absent, or inaccessible components                          │
│  Capacity: confirm usable capacity matches expected after FTT overhead                                │
│                                                                                                       │
│                                        │  configure storage policies                                  │
│                                        ▼                                                              │
│  Step 4 · Storage Policy Configuration                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create SPBM policies: FTT=1 RAID-1 (default), FTT=1 RAID-5, FTT=2 RAID-6                             │
│  Assign default policy to cluster  ·  VM home namespace policy set                                    │
│  Tag-based placement rules if multiple datastores or fault domains exist                              │
│  Test policy compliance: deploy test VM, confirm object placement correct                             │
│  Verify existing VM storage objects are compliant (no yellow/red warnings)                            │
│                                                                                                       │
│                                        │  migrate workloads                                           │
│                                        ▼                                                              │
│  Step 5 · Workload Migration                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  svMotion existing VMs from local/NFS datastores to vSAN datastore                                    │
│  Monitor resyncing objects: vSAN → Monitor → Resyncing Objects                                        │
│  Confirm all objects reach Healthy state after migration                                              │
│  Remove old datastores and disconnect legacy storage paths if decommissioning                         │
│  Performance: enable vSAN Performance Service for per-VM IOPS dashboards                              │
│                                                                                                       │
│                                        │  health, monitoring and day-2                                │
│                                        ▼                                                              │
│  Step 6 · Health & Monitoring                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  vSAN Health Service: run full check  ·  Resolve any warnings before production                       │
│  Network partition test: verify all hosts see same vSAN partition                                     │
│  Proactive rebalance: run if capacity usage is uneven across hosts                                    │
│  Skyline Health: onboard cluster for ongoing vSAN health recommendations                              │
│  Backup: configure VM-level backup via Veeam/Commvault before go-live                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, component states, resync mechanics, integrations, and design standards.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>End-to-end deployment from bare metal through vSAN enablement, policies, and validation.</span>
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
