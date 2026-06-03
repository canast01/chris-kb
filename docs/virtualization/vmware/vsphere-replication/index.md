# vSphere Replication

<div class="kb-summary">
vSphere Replication knowledge base — deploy, architecture, operations, CLI references, security, and troubleshooting for VM-level asynchronous replication between vCenter sites.
</div>

```text
┌────────────────────────────────────── vSphere Replication Stack ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 VMware vSphere Replication — VM-Level Asynchronous Replication                │   │
│   │       VR Server (VRMS): appliance per site managing replication config and site pairing       │   │
│   │     Delta sync: only changed disk blocks transmitted; compressed over replication network     │   │
│   │         RPO: configurable 5 min to 24 hours per VM; drives how often delta syncs occur        │   │
│   │     MPIT: Multiple Point-In-Time snapshots at target; retain recovery points for rollback     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VR Server pairs sites · HBRSVC on ESXi sends deltas · RPO and MPIT control recovery options        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │   VRMS: site pair + config  │  │     Configure: VM + RPO     │  │  RBAC: VR roles in vCenter  │   │
│   │   HBRSVC: ESXi repl agent   │  │   Monitor: lag + bandwidth  │  │     TLS: site pair cert     │   │
│   │   Delta sync: block-level   │  │   MPIT: snapshot at target  │  │    Encryption: in-transit   │   │
│   │     RPO: 5 min to 24 hrs    │  │  Failover: planned / forced │  │  Quiescing: app-consistent  │   │
│   │   Seed: initial full copy   │  │    Failback: reprotect VM   │  │    Audit: vCenter events    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines replication data path · Operations monitor and execute failover               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │Repl lag exceeds R│VRMS appliance log│RPO: met for all VM│   GSS + bundle   │ vicfg-module VR  │   │
│   │ Sync stuck at 0% │HBRSVC log on host│Site pair: connecte│  TAM escalation  │ hbr-manager stat │   │
│   │Full sync triggere│ vr-transfer.log  │Bandwidth: adequate│ Collect VR logs  │ esxcli vr config │   │
│   │MPIT: snapshot err│target-datastore l│ MPIT: captured OK?│  P1: repl loss   │vr-manager status │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VRMS appliance at each site · ESXi hosts running HBRSVC · replication network (dedicated or shared)  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VRMS          = vSphere Replication Management Server; per-site VA; manages config and site pair     │
│  HBRSVC        = Host-Based Replication Service; ESXi kernel module transmitting VM disk deltas       │
│  Delta sync    = Incremental block-level replication; only changed disk regions are transmitted       │
│  RPO           = Recovery Point Objective; minimum sync frequency; 5 min, 1 hr, or up to 24 hrs       │
│  MPIT          = Multiple Point-In-Time; snapshots of replicated VM at target site for rollback       │
│  Seed          = Initial full-copy replication; can be seeded from backup media to reduce WAN transfer│
│  Quiescing     = VSS/sync quiesce of VM guest before snapshot for application-consistent recovery     │
│  Failover      = Powered-on recovery of replicated VM at target site; planned (clean) or forced       │
│  Failback      = After failover: reprotect from recovery site back to original protected site         │
│  Replication lag= Time between a change at source and its arrival at target; must stay under RPO      │
│  Site pair     = VRMS-to-VRMS trust established via certificate exchange; required for replication    │
│  Compression   = vSphere Replication compresses delta blocks in transit; reduces WAN bandwidth        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌───────────────────────────── vSphere Replication — Installation Sequence ─────────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Deploy Checks                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Two vCenter instances: source and target (same or different SSO domains)                             │
│  Network: ports 80, 443, 31031, 44046 open between sites                                              │
│  Latency: ≤200 ms between sites for stable replication                                                │
│  Target datastore: sufficient free space for replica disks + delta files                              │
│  DNS: VR appliance FQDNs resolvable from both sites  ·  PTR records created                           │
│                                                                                                       │
│                                        │  deploy VR appliance at source site                          │
│                                        ▼                                                              │
│  Step 2 · VR Appliance — Source Site                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy vSphere Replication OVA via vCenter  ·  Confirm OVF checksum                                  │
│  Set FQDN, IP, gateway, DNS, NTP  ·  Set admin and root passwords                                     │
│  Register with local vCenter: VR Admin UI → Configuration → vCenter Server                            │
│  Accept vCenter thumbprint  ·  VR plugin appears in vSphere Client                                    │
│  Source site VR appliance shows Registered status                                                     │
│                                                                                                       │
│                                        │  deploy VR appliance at target site                          │
│                                        ▼                                                              │
│  Step 3 · VR Appliance — Target Site                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy second VR OVA on target site using same procedure                                             │
│  Register with target vCenter                                                                         │
│  Pair target VR with source VR: VR Admin UI → Configuration → Target Sites                            │
│  Enter source site VR FQDN + admin credentials  ·  Accept thumbprint                                  │
│  Pairing confirmed  ·  Both sites visible in vSphere Client VR plugin                                 │
│                                                                                                       │
│                                        │  configure replications                                      │
│                                        ▼                                                              │
│  Step 4 · Configure VM Replications                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Select VM in vSphere Client  ·  Actions → Configure Replication                                      │
│  Choose target site and target datastore  ·  Set RPO (minimum 5 minutes)                              │
│  Initial full sync: seed from backup or online full sync over network                                 │
│  Enable multiple point in time (MPIT) snapshots for point-in-time recovery                            │
│  Replication status: Initial Full Sync → Syncing  ·  Wait for first RPO met                           │
│                                                                                                       │
│                                        │  monitor replication health                                  │
│                                        ▼                                                              │
│  Step 5 · Monitor Replication                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  vSphere Client → Site Recovery → Replications: check all VMs RPO status                              │
│  RPO violations: amber/red indicators — investigate network or datastore latency                      │
│  Delta disk growth: monitor if network bandwidth limits replication throughput                        │
│  VR appliance alerts: configure email notification for replication failures                           │
│  Integrate with SRM if orchestrated failover required (see SRM sequence)                              │
│                                                                                                       │
│                                        │  test recovery and failback                                  │
│                                        ▼                                                              │
│  Step 6 · Recovery & Failback                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Planned migration: graceful shutdown at source  ·  VMs start cleanly at target                       │
│  Disaster recovery: power off at source (if possible)  ·  Recover at target                           │
│  Post-failover: reverse replication to reprotect  ·  Failback when ready                              │
│  Failback: planned migration back to original site  ·  Verify data consistency                        │
│  Document recovery test results  ·  Update runbook with observed RTO/RPO                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>VRA OVA deployment, vCenter registration, site pairing, VM replication config, and RPO validation.</span>
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
