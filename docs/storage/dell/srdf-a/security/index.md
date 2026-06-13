---
tags:
  - dell
  - security
---
# SRDF/A — Security



<div class="kb-summary">
SRDF/A security controls — management access restrictions, SRDF encryption, and Unisphere for PowerMax hardening.
</div>

```text
┌────────────────────────────────────────── SRDF/A — Security ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   SRDF/A — Security Posture                                   │   │
│   │     Authentication: PowerMax admin creds; Solutions Enabler (SYMAPI); role-based Unisphere    │   │
│   │      Encryption: SRDF encryption at the FA/RF port level; Unisphere HTTPS; SE service TLS     │   │
│   │           Network: management VLAN separated; 9443 (Unisphere HTTPS) management port          │   │
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
│  Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports      │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology               │
│  R1            = source SRDF volume on production array; host writes flow here                        │
│  R2            = target SRDF volume on DR array; receives replicated data asynchronously              │
│  Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically          │
│  Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO                  │
│  symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore       │
│  SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth             │
│  Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle            │
│  Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts                   │
│  Restore       = after failover resolution, re-establishes replication with R1 as source              │
│  Establish     = initial sync or re-sync operation that copies R1 to R2 in full                       │
│  Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication                 │
│  FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link                      │
│  Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Solutions Enabler service accounts, credential rotation, and access policies.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC roles, scope restrictions, and preventing accidental resync.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>SRDF/E in-flight encryption with AES-256 and verification commands.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Network port requirements, firewall rules, audit logging, and SIEM integration.</span>
</a>

</div>

