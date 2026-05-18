# vSphere Replication

<div class="kb-summary">
vSphere Replication knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```
  Source Site                                      Target Site
┌────────────────────────────┐                ┌───────────────────────────┐
│  Source VM                 │                │  VR Appliance (target)    │
│  ┌──────────────────────┐  │                │  ┌─────────────────────┐  │
│  │  hbrsvc (ESXi agent) │──┼── TCP 31031 ──►│  │  Replica VMDKs      │  │
│  │  tracks changed      │  │  (delta sync)  │  │  (.vrepl files)     │  │
│  │  blocks (CBT)        │  │                │  │  N recovery points  │  │
│  └──────────────────────┘  │                │  └─────────────────────┘  │
│                            │                │                           │
│  VR Appliance (VRMS)       │                │  Recover VM               │
│  ┌──────────────────────┐  │  TCP 44046     │  ┌─────────────────────┐  │
│  │  Manages replication │◄─┼──────────────►│  │  (standalone or via │  │
│  │  schedules + RPO     │  │  (mgmt plane)  │  │   SRM orchestration)│  │
│  └──────────────────────┘  │                │  └─────────────────────┘  │
└────────────────────────────┘                └───────────────────────────┘
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
