---
tags:
  - netapp
  - security
---
# Superna Eyeglass — Security



<div class="kb-summary">
Superna Eyeglass hardening — RBAC, TLS enforcement, audit logging, and management interface access controls.
</div>

```text
┌───────────────────────────────────── Superna Eyeglass — Security ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Superna Eyeglass — Security Posture                              │   │
│   │     Authentication: Eyeglass admin roles; PowerScale creds; AD integration for DFS-N mgmt     │   │
│   │        Encryption: HTTPS/TLS for all management; SyncIQ replication AES-256 in transit        │   │
│   │       Network: management VLAN separated; 8116 (Isilon/PowerScale mgmt) management port       │   │
│   │                 Audit: all admin actions logged; log retention minimum 1 year                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │          Encryption         │  │            Audit            │   │
│   │          RBAC roles         │  │       AES-256 at rest       │  │        Admin actions        │   │
│   │       Least privilege       │  │        TLS in transit       │  │         Login events        │   │
│   │         MFA optional        │  │         Key rotation        │  │        Syslog export        │   │
│   │       SVC acct rotate       │  │       WORM / immutable      │  │         SIEM forward        │   │
│   │         Just-In-Time        │  │         KMS managed         │  │       Quarterly review      │   │
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

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Built-in roles, least privilege, and service account requirements.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Network restrictions, RBAC, audit log, and SIEM integration.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>HTTPS enforcement and API token management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Audit log forwarding, appliance patching, and service account rotation.</span>
</a>

</div>

