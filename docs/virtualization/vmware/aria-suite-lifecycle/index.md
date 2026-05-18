# Aria Suite Lifecycle

<div class="kb-summary">
Technical and operational reference for VMware Aria Suite Lifecycle Manager. Covers deployment, patching, certificate management, upgrade orchestration, and environment health for all Aria Suite products.
</div>

```
  Aria Suite Lifecycle — Core Architecture
┌─────────────────────────────────────────────────────────────────┐
│  LCM Appliance (lcm-prod-01.corp.local)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Lifecycle Operations    Locker (vault)                  │   │
│  │  ┌──────────────────┐    ┌───────────────────────────┐   │   │
│  │  │ Environments     │    │ Certificates (CA-signed)  │   │   │
│  │  │  ├ Prod Env      │    │ Passwords (service accts) │   │   │
│  │  │  │  ├ vrops       │    │ Licences                  │   │   │
│  │  │  │  ├ vra         │    └───────────────────────────┘   │   │
│  │  │  │  └ vrli        │                                    │   │
│  │  │  └ Dev Env        │    NFS Binary Repo (/data)         │   │
│  │  └──────────────────┘    .pak bundles per product ver.   │   │
│  └──────────────────────────────────────────────────────────┘   │
│          │ deploy/upgrade/patch/scale                           │
│          ▼                                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Managed Products (vCenter-hosted OVA appliances)        │   │
│  │  Workspace ONE Access → Aria Operations → Aria Automation│   │
│  │  Aria Log Insight → Aria Operations for Networks         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
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
