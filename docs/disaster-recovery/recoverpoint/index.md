# RecoverPoint

<div class="kb-summary">
Dell EMC RecoverPoint journal-based continuous data protection — RPA clusters intercept writes via splitters and maintain a rolling journal enabling point-in-time recovery across CDP, CRR, and CLR modes.
</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                   RecoverPoint Architecture                          │
│                                                                      │
│  Primary Site                         DR Site                        │
│  ┌────────────────────────┐           ┌────────────────────────┐     │
│  │  Host / ESXi           │           │  Host / ESXi           │     │
│  │  (writes I/O)          │           │  (standby / copy)      │     │
│  └──────────┬─────────────┘           └─────────────┬──────────┘     │
│             │ via splitter (kernel/                 │                │
│             │  array-based)                         │                │
│  ┌──────────▼─────────────┐           ┌─────────────▼──────────┐     │
│  │  RPA Cluster (source)  │──────────►│  RPA Cluster (target)  │     │
│  │  Journal: rolling CDP  │  WAN repl │  Journal: remote copy  │     │
│  └──────────┬─────────────┘           └─────────────┬──────────┘     │
│             │                                       │                │
│  ┌──────────▼─────────────┐           ┌─────────────▼──────────┐     │
│  │  Source Array           │           │  Target Array          │    │
│  │  (production LUNs)      │           │  (replica LUNs)        │    │
│  └─────────────────────────┘           └────────────────────────┘    │
│                                                                      │
│  RPO = journal depth   ·   RTO = activate copy (minutes)             │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>RPA topology, splitter types, replication modes, consistency groups, journal sizing, and HA.</span>
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
