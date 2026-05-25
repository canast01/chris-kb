# Commvault

<div class="kb-summary">
Commvault enterprise backup and recovery — CommServe command and control, MediaAgent data movement with deduplication, and multi-site storage library management.
</div>

```text
┌──────────────────────────────────────────────────────────────────────┐
│                     Commvault Architecture                           │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │               CommServe (Command & Control)                  │    │
│  │   Job engine · catalog database · policy scheduler          │     │
│  └──────────────────────────────┬───────────────────────────────┘    │
│                                 │ job dispatch                       │
│  ┌──────────────────────────────▼───────────────────────────────┐    │
│  │              MediaAgent(s)                                   │    │
│  │   Data movement · deduplication engine · SIDB catalog        │    │
│  └──────────────┬──────────────────────────┬─────────────────────┘   │
│                 │ agent data               │ write                   │
│  ┌──────────────▼──────────────┐  ┌────────▼─────────────────────┐   │
│  │  iDataAgents (clients)      │  │  Storage Libraries           │   │
│  │  File · VSA (VM) · Oracle   │  │  Disk library (DDB dedup)    │   │
│  │  SQL · Exchange             │  │  Cloud (S3/Blob)             │   │
│  └─────────────────────────────┘  │  Tape (library robot)        │   │
│                                   └──────────────────────────────┘   │
│                                                                      │
│  Multi-site: CommServe ◄──► remote MediaAgents at DR site            │
└──────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>CommServe topology, MediaAgent dedup, storage library types, multi-site design, and port requirements.</span>
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
