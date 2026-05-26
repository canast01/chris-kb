# RecoverPoint

<div class="kb-summary">
Dell EMC RecoverPoint journal-based continuous data protection — RPA clusters intercept writes via splitters and maintain a rolling journal enabling point-in-time recovery across CDP, CRR, and CLR modes.
</div>

```
┌─────────────────────────────────────── RecoverPoint — Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Dell RecoverPoint for VMs (RP4VM): Continuous Data Protection for VMware environments     │   │
│   │  Intercepts every write via a splitter; journals writes to enable any-point-in-time recovery  │   │
│   │   Supports local protection, remote replication (single/multi-site), and cascade topologies   │   │
│   │              RPO: seconds (CDP journal); RTO: minutes (image access or failover)              │   │
│   │          Core objects: RPA cluster, splitter, consistency group, journal volume, copy         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Protected Site ──splitter intercepts writes──► RPA Cluster ──journal replication──► Recovery Site R│
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Protected Site Components           │  │           Recovery Site Components          │   │
│   │         RPA cluster (2–8 appliances)         │  │         RPA cluster (matching count)        │   │
│   │        ESXi splitter (vSphere plugin)        │  │            Remote journal volumes           │   │
│   │       Production VMs (consistency grp)       │  │         Remote copy (replica disks)         │   │
│   │         Local journal volumes (CDP)          │  │       vCenter (image access/failover)       │   │
│   │            vCenter + RP4VM plugin            │  │           Network replication link          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: RPAs are VMs or physical appliances; journal vols on shared datastore; replication over I│
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RPA              = RecoverPoint Appliance; manages replication, journaling, and failover logic     │
│    Splitter         = Write-interceptor at ESXi kernel or array layer; splits I/O to journal          │
│    Journal          = Sequential write log on target side; enables any-point-in-time image access     │
│    Consistency Group= Named set of VMs/volumes that fail over and recover together atomically         │
│    Copy             = A replication destination (local or remote); each CG has ≥1 copy                │
│    Bookmark         = Named point-in-time marker in the journal; used for crash-consistent recovery   │
│    CDP              = Continuous Data Protection; every write captured; journal depth = RPO window    │
│    Image Access     = Mount a journal image as read/write VM without committing to production         │
│    Failover         = Activate remote copy; production traffic moves to recovery site                 │
│    Failback         = Reverse replication; sync changes back; cut over to original production         │
│    Test Copy        = Non-disruptive test failover; recovery VMs isolated on bubble network           │
│    RPO              = Recovery Point Objective; max acceptable data loss (seconds with CDP)           │
│    RTO              = Recovery Time Objective; time to restore service after declaring failover       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>RPA topology, splitter types, replication modes, consistency groups, journal sizing, and HA.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, and scripts.</span>
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
