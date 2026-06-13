---
tags:
  - vmware
---
# Topics


<div class="kb-summary">
Deep-dive reference articles on specific VMware behaviors, edge cases, and troubleshooting scenarios — plus a structured learning path, cross-product scenarios, and 25 reactive and planned workflows.
</div>

```text
┌─────────────────────────────────────────── VMware — Topics ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      VMware technical deep-dive topics: cluster failure domains, cluster state validation     │   │
│   │     DRS/vMotion behavior, HA admission control, host isolation response, maintenance risk     │   │
│   │    Network packet loss, recovery behavior, resource contention, snapshot impact on storage    │   │
│   │     Storage latency troubleshooting: APD/PDL response, VMFS locking, datastore I/O queues     │   │
│   │        Time/DNS validation: NTP sync required for HA, vSAN, and certificate operations        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Cluster topics cover HA design · performance topics isolate bottlenecks                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Cluster Topics       │  │      Performance Topics     │  │      Resilience Topics      │   │
│   │       Failure domains       │  │       Resource conten       │  │        Recovery behav       │   │
│   │        Cluster state        │  │       Snapshot impact       │  │        HA restart ord       │   │
│   │         DRS/vMotion         │  │       Storage latency       │  │         APD/PDL resp        │   │
│   │         HA admission        │  │       Network pkt loss      │  │        Host isolation       │   │
│   │        Isolation resp       │  │        vMotion timing       │  │         Time/DNS val        │   │
│   │        Maint risk val       │  │         Balloon/swap        │  │         Upgrade seq         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Cluster topics cover HA/DRS · performance topics isolate contention                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    HA/Cluster    │   DRS/vMotion    │     Resources     │     Storage      │   Network/Time   │   │
│   │ Failure domains  │   DRS behavior   │   Resource cont   │ Storage latency  │ Network pkt loss │   │
│   │  Cluster state   │  vMotion timing  │  Snapshot impact  │   APD/PDL resp   │   Time/DNS val   │   │
│   │   HA admission   │    Maint risk    │   Memory balloon  │  Datastore I/O   │  DNS resolution  │   │
│   │  Isolation resp  │ Migration thres  │    CPU ready %    │    VMFS lock     │  NTP sync check  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 cluster · ESXi hosts · Shared storage (SAN/vSAN) · ToR switches · Physical NICs                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Failure domain      = Host group in a cluster; HA distributes VM restarts across domains to limit    │
│  Cluster state val.  = Verification of vCenter, HA agent, DRS, and vSAN state across all cluster hosts│
│  HA admission control = Policy reserving cluster capacity for VM restarts; slot-based or % resource   │
│  Host isolation resp = HA action when host loses heartbeat: power off, shutdown, or leave VMs running │
│  DRS migration thres = Aggressiveness setting (1-5) controlling how often DRS initiates vMotion       │
│  vMotion             = Live migration of a running VM between ESXi hosts with zero downtime           │
│  Resource contention = CPU ready, memory balloon/swap, or storage latency caused by overcommitment    │
│  Snapshot delta      = VMDK delta disk created at snapshot time; grows with writes; impacts           │
│  APD                 = All Paths Down; storage device unreachable; all paths to datastore failed      │
│  PDL                 = Permanent Device Loss; storage device reports itself gone; triggers HA restart │
│  NTP synchronization = Required for HA elections, vSAN, SSO certificates, and replication timestamps  │
│  Balloon driver      = VMware memory reclaim driver; inflates inside guest to force OS to free memory │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-5">

<a class="kb-card" href="learning-path/">
  <strong>Learning Path</strong>
  <span>Recommended reading order: vCenter → ESXi → vSAN → NSX → Aria Suite → VxRail.</span>
</a>

<a class="kb-card" href="scenarios/">
  <strong>Scenarios</strong>
  <span>25 cross-product scenarios: reactive troubleshooting and planned operational workflows.</span>
</a>

<a class="kb-card" href="cluster-failure-domains/">
  <strong>Cluster Failure Domains</strong>
  <span>Failure domain behavior, rules, and impact on vSAN and HA.</span>
</a>

<a class="kb-card" href="cluster-state-validation/">
  <strong>Cluster State Validation</strong>
  <span>Validating cluster health, HA status, DRS balance, and readiness.</span>
</a>

<a class="kb-card" href="drs-vmotion-behavior/">
  <strong>DRS and vMotion Behavior</strong>
  <span>DRS automation levels, vMotion triggers, and placement logic.</span>
</a>

<a class="kb-card" href="ha-admission-control/">
  <strong>HA Admission Control</strong>
  <span>HA admission control policies, slot sizing, and failover capacity.</span>
</a>

<a class="kb-card" href="host-isolation-response/">
  <strong>Host Isolation Response</strong>
  <span>ESXi host isolation behavior, response settings, and impact.</span>
</a>

<a class="kb-card" href="maintenance-risk-validation/">
  <strong>Maintenance Risk Validation</strong>
  <span>Pre-maintenance risk checks for hosts, storage, and network impact.</span>
</a>

<a class="kb-card" href="network-packet-loss/">
  <strong>Network Packet Loss</strong>
  <span>Packet loss troubleshooting on VMkernel, vSwitch, and physical NICs.</span>
</a>

<a class="kb-card" href="recovery-behavior/">
  <strong>Recovery Behavior</strong>
  <span>HA restart behavior, APD/PDL response, and VM recovery options.</span>
</a>

<a class="kb-card" href="resource-contention/">
  <strong>Resource Contention</strong>
  <span>CPU ready, memory pressure, storage latency, and network saturation.</span>
</a>

<a class="kb-card" href="snapshot-impact/">
  <strong>Snapshot Impact</strong>
  <span>Performance and storage impact of snapshots, and cleanup procedures.</span>
</a>

<a class="kb-card" href="storage-latency-troubleshooting/">
  <strong>Storage Latency Troubleshooting</strong>
  <span>Identifying and resolving datastore and vSAN latency issues.</span>
</a>

<a class="kb-card" href="time-dns-validation/">
  <strong>Time and DNS Validation</strong>
  <span>NTP sync, DNS resolution, and time drift troubleshooting.</span>
</a>

<a class="kb-card" href="upgrade-sequence-reference/">
  <strong>Upgrade Sequence Reference</strong>
  <span>Component upgrade order for vCenter, ESXi, vSAN, NSX, and VCF.</span>
</a>

</div>
