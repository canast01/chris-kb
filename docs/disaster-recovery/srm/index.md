---
title: SRM
---

# SRM

<div class="kb-summary">
VMware Site Recovery Manager DR orchestration — vCenter plugin automating storage presentation, VM registration, power-on sequencing, and IP customisation across a site pair.
</div>

```
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
