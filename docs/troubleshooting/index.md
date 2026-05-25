# Troubleshooting

```text
┌──────────────────────────────────────────────────────────────────────┐
│                   Troubleshooting Framework                          │
│                                                                      │
│  Symptom reported                                                    │
│        │                                                             │
│  ┌─────▼──────────────────────────────────────────────────────────┐  │
│  │  Categorise                                                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐   │    │
│  │  │ Storage  │ │ Network  │ │   Auth   │ │  Performance   │   │    │
│  │  │ latency  │ │connect.  │ │ failures │ │  CPU/Mem/Disk  │   │    │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───────┬────────┘   │    │
│  └───────┼────────────┼────────────┼────────────────┼────────────┘   │
│          │            │            │                │                │
│  ┌───────▼────────────▼────────────▼───────────────▼─────────────┐   │
│  │  Tool selection                                               │   │
│  │  esxtop / iostat · traceroute · Event Viewer · top / perfmon │    │
│  └───────────────────────────────────────┬────────────────────────┘  │
│                                          │                            │
│  ┌───────────────────────────────────────▼────────────────────────┐  │
│  │  Resolve or escalate                                           │  │
│  │  Fix ──► validate ──► document   ──or──   escalate to vendor  │   │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

Cross-platform troubleshooting guides for common infrastructure issues.

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
