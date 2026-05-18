# VMware Cloud Foundation

<div class="kb-summary">
Technical and operational reference for VMware Cloud Foundation (VCF). Covers SDDC Manager, workload domains, lifecycle management, vSphere, vSAN, and NSX integration across the full-stack private cloud platform.
</div>

```
VMware Cloud Foundation (VCF) — Full Stack Overview
┌─────────────────────────────────────────────────────┐
│  SDDC Manager                                        │
│  lifecycle orchestration · inventory · passwords     │
│  certificates · network pools · LCM upgrades         │
└──────────┬───────────────┬──────────────────────────┘
           │               │
           ▼               ▼
┌──────────────────┐  ┌────────────────────────────────┐
│ Management       │  │ Workload Domains (up to 15)    │
│ Domain           │  │                                │
│ ┌─────────────┐  │  │  ┌──────────┐  ┌──────────┐    │
│ │  vCenter    │  │  │  │  VI WLD  │  │ VVF WLD  │    │
│ │  NSX Mgr   │  │  │  │ vCenter  │  │ vCenter  │     │
│ │  vSAN      │  │  │  │ NSX      │  │ NSX      │     │
│ └─────────────┘  │  │  │ vSAN    │  │ vSAN+TKG │     │
│ 4+ ESXi hosts   │  │  └──────────┘  └──────────┘     │
└──────────────────┘  └────────────────────────────────┘
           │                        │
           ▼                        ▼
    ┌─────────────┐         ┌──────────────┐
    │ Mgmt ESXi   │         │ Workload ESXi│
    │ hosts       │         │ hosts        │
    └─────────────┘         └──────────────┘
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
