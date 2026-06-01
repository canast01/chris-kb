# Superna Eyeglass — Access Control


<div class="kb-summary">
Superna Eyeglass — Access Control reference.
</div>

```powershell
┌────────────────────────────────── Superna Eyeglass — Access Control ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           Superna Eyeglass — RBAC and Access Control                          │   │
│   │ Auth: Eyeglass admin roles; PowerScale admin credentials; AD integration for DFS-N management │   │
│   │             Principle of least privilege: each role gets only required permissions            │   │
│   │              Service accounts: dedicated, non-interactive; rotation every 90 days             │   │
│   │               Emergency break-glass: documented, monitored, time-limited access               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Role       │   Access Level   │    Typical User   │   Review Freq    │    Granted By    │   │
│   │      Admin       │ Full config/ops  │   Sr Backup Eng   │    Quarterly     │  Security team   │   │
│   │     Operator     │ Start/stop jobs  │     Backup Eng    │    Quarterly     │    Team lead     │   │
│   │     Monitor      │  Read-only view  │      NOC / L1     │    Quarterly     │    Team lead     │   │
│   │   Service Acct   │  API / headless  │     Automation    │   Per rotation   │  Security team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
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
Network access to the Eyeglass management interface must be restricted to the management VLAN or jump host only. Direct access from user workstations or untrusted networks is not permitted.

| Control | Detail |
|---|---|
| Network access | Restrict Eyeglass UI and API to management network |
| Console access | HTTPS only; restrict to management VLAN or jump host |
| OneFS API credentials | Dedicated service account; minimum required OneFS privileges |
| RBAC | Admin and read-only roles; enforce least privilege |

All failover events are recorded in the Eyeglass audit log. The audit log must be forwarded to a SIEM to ensure a complete record of all failover and configuration events is retained outside the appliance.
