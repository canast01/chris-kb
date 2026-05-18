# Veeam

<div class="kb-summary">
Veeam Backup & Replication — Backup Server scheduling, Proxy data movement via VADP or agent, and Scale-Out Backup Repository with immutable object storage offload.
</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Veeam Architecture                               │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Backup Job (schedule + policy)                  │   │
│  │     Veeam Backup Server ──► vCenter API ──► snapshot VM      │   │
│  └──────────────────────────────┬───────────────────────────────┘   │
│                                 │ data movement                     │
│  ┌──────────────────────────────▼───────────────────────────────┐   │
│  │              Veeam Proxy (VADP / agent)                      │   │
│  │  Hot-add transport · NBD · Direct SAN · Linux agent          │   │
│  └──────────────────────────────┬───────────────────────────────┘   │
│                                 │                                   │
│  ┌──────────────────────────────▼───────────────────────────────┐   │
│  │         Backup Repository (Scale-Out / SOBR)                 │   │
│  │  Primary extent (fast disk)  ──►  Capacity tier (S3/object) │   │
│  │  Immutable (hardened Linux)  ──►  Archive tier (tape/cloud) │   │
│  └──────────────────────────────┬───────────────────────────────┘   │
│                                 │ replication (DR)                  │
│  ┌──────────────────────────────▼───────────────────────────────┐   │
│  │              Secondary Site / Cloud Connect                  │   │
│  │          Restore: FLR · VM restore · Instant recovery        │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
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
