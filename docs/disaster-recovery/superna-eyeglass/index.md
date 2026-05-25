# Superna Eyeglass

<div class="kb-summary">
Superna Eyeglass DR orchestration for NetApp PowerScale — automates SyncIQ failover, SMB/NFS share reconfiguration, quota migration, and DNS cutover in 5–15 minutes.
</div>

```text
┌──────────────────────────────────────────────────────────────────────┐
│                   Superna Eyeglass Architecture                      │
│                                                                      │
│  Primary Site                          DR Site                       │
│  ┌──────────────────────┐              ┌──────────────────────────┐  │
│  │  PowerScale (source) │              │  PowerScale (target)     │  │
│  │  NFS/SMB shares      │──SyncIQ ────►│  replica data            │  │
│  │  Access zones        │  replication │  (synced, read-only)     │  │
│  └──────────┬───────────┘              └────────────┬─────────────┘  │
│             │                                       │                │
│  ┌──────────▼───────────────────────────────────────▼─────────────┐  │
│  │                  Superna Eyeglass VM                           │  │
│  │  Monitors SyncIQ · Detects failover trigger                   │   │
│  │  Automates: allow writes ──► reconfigure shares               │   │
│  │             migrate quotas ──► DNS cutover (5-15 min RTO)     │   │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Failback: re-sync to primary ──► revert DNS ──► validate            │
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
