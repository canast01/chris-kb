# Superna Eyeglass — Troubleshooting



<div class="kb-summary">
Diagnosing Superna Eyeglass replication failures, configuration sync errors, DR orchestration issues, and Eyeglass connectivity.
</div>

```text
┌───────────────────────────────── Superna Eyeglass — Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Superna Eyeglass — Troubleshooting Approach                          │   │
│   │                   1  Identify: which job, component, or resource is failing                   │   │
│   │                  2  Scope: single job vs all jobs; one source vs all sources                  │   │
│   │             3  Collect: logs and run status command; review recent change history             │   │
│   │                 4  Diagnose: match symptoms to known issues; check error codes                │   │
│   │                     5  Fix: apply resolution; verify fix; monitor next run                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Infrastructure       │  │         Application         │  │             Data            │   │
│   │        Network checks       │  │         Log analysis        │  │        Catalog check        │   │
│   │        Storage space        │  │       Job error codes       │  │         Consistency         │   │
│   │        Process health       │  │        Auth failures        │  │       Corruption scan       │   │
│   │    443 (Eyeglass web UI)    │  │        Timeout errors       │  │         Restore test        │   │
│   │        Firewall rules       │  │        Version compat       │  │          RPO drift          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link   │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection            │
│  RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats       │
│  SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies         │
│  DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS        │
│  Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster              │
│  Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product       │
│  Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits            │
│  Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site            │
│  Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team                  │
│  Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha       │
│  Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation      │
│  igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations                         │
│  SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation         │
│  Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>SyncIQ detection failures, readiness score drops, DNS cutover errors, and failover stalls.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and API connectivity checks.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Support bundle collection, SR requirements, severity levels, and vendor escalation path.</span>
</a>

</div>
