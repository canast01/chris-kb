# vSphere Replication

<div class="kb-summary">
vSphere Replication knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
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
