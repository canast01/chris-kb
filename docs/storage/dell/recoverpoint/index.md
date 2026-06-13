---
tags:
  - dell
---
# RecoverPoint

<div class="kb-summary">
Dell EMC RecoverPoint journal-based continuous data protection — RPA clusters intercept writes via splitters and maintain a rolling journal enabling point-in-time recovery across CDP, CRR, and CLR modes.

*Applies to: RecoverPoint 5.x*
</div>

```text
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
│    Protected Site ──splitter intercepts──► RPA Cluster ──journal replication──► Recovery RPA          │
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
│    Physical: RPAs are VMs or appliances; journal vols on shared datastore; replication IP             │
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


```text
┌───────────────────────────────── RecoverPoint — Deployment Sequence ──────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Supported storage arrays at protected and recovery sites  ·  check RecoverPoint HCL                  │
│  ESXi host splitter compatibility (for vRPA virtual appliances)  ·  confirm VMware version            │
│  IP network between sites: dedicated replication VLAN  ·  latency < 100 ms for CDP mode               │
│  Service accounts: storage admin + vCenter admin  ·  NTP synced across both sites                     │
│  Licence files obtained  ·  DNS records for all RPA management IPs created                            │
│                                                                                                       │
│                                        │  deploy RPA cluster                                          │
│                                        ▼                                                              │
│  Step 2 · RPA Cluster Deployment                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy vRPA OVA at protected site: 8 vCPU / 24 GB RAM / management + WAN NICs                        │
│  Deploy 2+ vRPAs per site for HA  ·  configure cluster during initial setup wizard                    │
│  Set management IP, gateway, NTP, DNS during OVA deploy  ·  power on all RPAs                         │
│  Form RPA cluster via RecoverPoint Management Application (RPMA) at https://<rpa-ip>                  │
│  Activate licence  ·  verify cluster status: all RPAs Online in System Settings                       │
│                                                                                                       │
│                                        │  install and configure splitters                             │
│                                        ▼                                                              │
│  Step 3 · Splitters                                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  vSphere API splitter (kit/vRPA): enable I/O splitter in vCenter during RPA wizard                    │
│  RecoverPoint Splitter for VMAX/PowerMax: installed on storage side  ·  no host impact                │
│  Fabric splitter (FC-based): deployed as E_port on SAN fabric  ·  intercepts FC writes                │
│  Assign splitter to RPA cluster  ·  verify splitter health in RPMA cluster view                       │
│  Test splitter: enable splitting on a non-critical volume  ·  verify write intercept                  │
│                                                                                                       │
│                                        │  create replication links                                    │
│                                        ▼                                                              │
│  Step 4 · Replication Links                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add recovery site RPA cluster: Topology → Add Remote Cluster  ·  enter remote RPA IP                 │
│  Configure WAN link: compression on  ·  encryption if traffic crosses untrusted network               │
│  Set bandwidth throttle per link to avoid saturating WAN during peak hours                            │
│  Verify bidirectional link health: RPMA → Topology  ·  both site clusters visible                     │
│  Test link: send test transfer  ·  confirm throughput matches available bandwidth                     │
│                                                                                                       │
│                                        │  create consistency groups                                   │
│                                        ▼                                                              │
│  Step 5 · Consistency Groups                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create CG: define source volumes (production)  ·  define target (copy) volumes at DR site            │
│  Select replication mode: CDP (continuous), CRR (async to remote), CLR (local + remote)               │
│  Set journal size: 10–200 GB depending on write rate and desired rollback window                      │
│  Initialise CG: full sweep of source to target  ·  monitor transfer in RPMA dashboard                 │
│  Verify RPO: RPMA shows lag in seconds for CDP or minutes for CRR  ·  target met                      │
│                                                                                                       │
│                                        │  test and validate                                           │
│                                        ▼                                                              │
│  Step 6 · Testing & Validation                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Enable Image Access: select BookMark  ·  mount DR volumes read-only  ·  test app                     │
│  Test failover: Failover wizard  ·  select BookMark  ·  confirm data integrity on DR                  │
│  After test: re-enable protection  ·  RPMA shows resync in progress  ·  wait for green                │
│  Document RTO/RPO achieved vs SLA  ·  sign off with application owner                                 │
│  Set RPMA alerts: RPO breach  ·  journal overflow  ·  link down  ·  splitter fault                    │
│  Schedule quarterly DR test rehearsals  ·  confirm runbook updated after each test                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>RPA topology, splitter types, replication modes, consistency groups, journal sizing, and HA.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
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
