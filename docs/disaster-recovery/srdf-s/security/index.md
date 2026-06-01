# SRDF/S — Security



<div class="kb-summary">
SRDF/S — Security reference.
</div>

```
┌────────────────────────────────────────── SRDF/S — Security ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   SRDF/S — Security Posture                                   │   │
│   │  Authentication: Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access  │   │
│   │    Encryption: Data identical to R1 at R2; FA port encryption optional; Unisphere TLS/HTTPS   │   │
│   │              Network: management VLAN separated; 9443 (Unisphere) management port             │   │
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
│  Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment        │
│  R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency       │
│  R2            = target volume; must acknowledge each write; acts as synchronous mirror               │
│  RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency       │
│  RPO=0         = zero recovery point objective; no data loss possible under normal operation          │
│  RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min       │
│  symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver       │
│  Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split                          │
│  Consistent    = transient state where R1 write is in transit but not yet confirmed on R2             │
│  Failover      = makes R2 read-write; production continues from DR site after R1 failure              │
│  Restore       = re-synchronises after failover; direction is reversed until R1 catches up            │
│  RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters           │
│  FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)            │
│  RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Solutions Enabler RBAC, API accounts, and certificate management.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Role assignments, failover guards, and audit logging.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>FCIP encryption, AES-256 configuration, and FC fabric zoning.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>API security, TLS configuration, and operational hardening checklist.</span>
</a>

</div>
