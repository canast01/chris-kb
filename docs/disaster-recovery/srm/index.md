---
title: SRM
---

# SRM

<div class="kb-summary">
VMware Site Recovery Manager DR orchestration — vCenter plugin automating storage presentation, VM registration, power-on sequencing, and IP customisation across a site pair.
</div>

```
┌─────────────────────────────────────────── SRM — Overview ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                              SRM                                              │   │
│   │    VMware DR orchestration — protection groups, recovery plans, automated failover/failback   │   │
│   │     SRM Server (Protected) — vCenter plugin at production site; manages protection groups     │   │
│   │            SRM Server (Recovery)  — vCenter plugin at DR site; runs recovery plans            │   │
│   │     SRA (Storage Replication Adapter) — translates SRM calls to array replication commands    │   │
│   │     Management: 443 (SRM HTTPS) · Auth: vCenter SSO / AD integration; SRM admin role; site    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture: components work together to deliver SRM capabilities                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                  Operations                 │   │
│   │ SRM Server (Protected) — vCenter plugin at   │  │               srm-cli vm list               │   │
│   │ SRM Server (Recovery)  — vCenter plugin at   │  │             srm-cli recovery run            │   │
│   │ SRA (Storage Replication Adapter) — transla  │  │              srm-cli plan test              │   │
│   │ Protection Group      — set of VMs protecte  │  │               srm-cli pg list               │   │
│   │ Recovery Plan         — ordered steps: pre-  │  │               srm-cli history               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery site) · SRA installed on SRM server · Array replication l│
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────────────────────────────────────┐
│                       SRM Architecture                               │
│                                                                      │
│  Primary Site                           DR Site                      │
│  ┌──────────────────────┐               ┌──────────────────────┐     │
│  │  vCenter + SRM       │◄─────────────►│  vCenter + SRM       │     │
│  │  (protected site)    │  site pair    │  (recovery site)     │     │
│  └──────────┬───────────┘               └──────────┬───────────┘     │
│             │                                      │                 │
│  ┌──────────▼───────────┐               ┌──────────▼───────────┐     │
│  │  Protection Groups   │               │  Recovery Plans      │     │
│  │  VMs grouped by tier │──replication─►│  Boot sequence       │     │
│  │  vSphere Replication │               │  IP customisation    │     │
│  │  Array SRA           │               │  Test failover       │     │
│  └──────────────────────┘               └──────────┬───────────┘     │
│                                                    │                 │
│               Failover process:                    │                 │
│               Trigger ──► Activate ──► Power on ──► Validate         │
│               Failback: Re-protect ──► Reverse replication           │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Site pair topology, recovery plan boot sequence, recovery modes, SRAs, and vSphere Replication.</span>
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
