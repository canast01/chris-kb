# Troubleshooting

Cross-platform troubleshooting guides for common infrastructure issues.


```text
┌─────────────────────────────────── Cross-Platform Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Common infrastructure issues across platforms: methodology + platform-specific paths     │   │
│   │         Universal triage: define symptom → collect data → isolate → test fix → confirm        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Alert fires → triage symptom → narrow scope → isolate component → fix → verify → close             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Compute / OS        │  │      Storage / Network      │  │       Services / Auth       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │           High CPU          │  │       Storage latency       │  │        Auth failures        │   │
│   │        VM performance       │  │       Replication fail      │  │        DNS resolution       │   │
│   │       Memory pressure       │  │     Network connectivity    │  │       Backup failures       │   │
│   │          Disk full          │  │        Path failures        │  │         Service down        │   │
│   │         Kernel panic        │  │         Packet loss         │  │         SSO failures        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Triage    = Rapid initial assessment to determine urgency, scope, and next diagnostic step         │
│    Isolate   = Narrow the problem to a specific component, host, or path                              │
│    RCA       = Root Cause Analysis; document underlying cause after resolution                        │
│    P1/P2/P3  = Priority levels; P1 = service down, P2 = degraded, P3 = no user impact                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-8">
<a class="kb-card" href="authentication-failures/"><strong>Authentication Failures</strong><span>AD, LDAP, Kerberos, and SSO authentication issues — diagnosis and resolution.</span></a>
<a class="kb-card" href="backup-failures/"><strong>Backup Failures</strong><span>Veeam, NetBackup, and Commvault job failures — snapshot errors, proxy issues, and repository problems.</span></a>
<a class="kb-card" href="dns-resolution/"><strong>DNS Resolution</strong><span>Forward and reverse lookup failures, forwarder issues, and DNS cache problems.</span></a>
<a class="kb-card" href="high-cpu/"><strong>High CPU</strong><span>Identifying CPU-heavy processes on Linux, Windows, and ESXi hosts.</span></a>
<a class="kb-card" href="replication-failures/"><strong>Replication Failures</strong><span>SRDF, SnapMirror, and vSphere Replication failures — link issues, lag, and pair state errors.</span></a>
<a class="kb-card" href="storage-latency/"><strong>Storage Latency</strong><span>High I/O latency triage — queue depth, path health, array performance, and contention.</span></a>
<a class="kb-card" href="vm-performance/"><strong>VM Performance</strong><span>Slow VM diagnosis — CPU ready, memory ballooning, disk latency, and network drops.</span></a>

<a class="kb-card" href="network-connectivity/">
  <strong>Network Connectivity</strong>
  <span>Network Connectivity notes, checks, commands, and references.</span>
</a>
</div>
