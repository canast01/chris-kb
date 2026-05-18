# Site Recovery Manager

<div class="kb-summary">
Site Recovery Manager knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```
  Protected Site                                Recovery Site
┌──────────────────────────┐                ┌──────────────────────────┐
│  vCenter (Protected)     │◄──── SRM ────►│  vCenter (Recovery)      │
│  ┌──────────────────┐    │   site pair    │  ┌──────────────────┐    │
│  │  Production VMs  │    │                │  │  Placeholder VMs │    │
│  │  ┌────────────┐  │    │                │  │  (shadow)        │    │
│  │  │  Replicated│──┼────┼────────────────┼─►│  ┌────────────┐  │   │
│  │  │  via VR or │  │    │                │  │  │ Recover on │  │   │
│  │  │  SAN array │  │    │                │  │  │ failover   │  │   │
│  │  └────────────┘  │    │                │  │  └────────────┘  │   │
│  └──────────────────┘    │                │  └──────────────────┘   │
│                          │                │                          │
│  Test ──► Failover ──► Failback           │  Recovery Plan runs:     │
│           (Planned Migration / DR)         │  Priority 1 → 2 → 3 → 4 │
└──────────────────────────┘                └──────────────────────────┘
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
