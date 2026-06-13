---
tags:
  - security
  - srm
  - vmware
---
# SRM — Hardening


<div class="kb-summary">
Hardening reference covering Least-Privilege SRA Service Accounts, Rotate SRA Credentials, Test Recovery Plans Regularly, Restrict Who Can Execute Recovery, Secure Recovery Site Network Design and 3 more sections.

*Applies to: SRM 8.x / 9.x*
</div>

  SRM Hardening Controls
```text
┌─────────────────────────────────────── VMware SRM — Hardening ────────────────────────────────────────┐
│                                                                                                       │
│  SRM hardening: restrict failover to authorised users, enforce TLS 1.2+, isolate                      │
│  SRM management traffic, audit all plan runs, and use MFA for DR access.                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Access Hardening               │  │              Network Hardening              │   │
│   │         SRM Admin: 2–3 accounts max          │  │             Mgmt VLAN: isolated             │   │
│   │             MFA: via vCenter SSO             │  │            No SRM from guest nets           │   │
│   │          Dual-person: real failover          │  │             WAN: encrypted link             │   │
│   │         Least privilege: plan tester         │  │           Firewall: SRM ↔ SRM only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Dual-person control for real failover prevents accidental production impact.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Config Hardening               │  │              Audit & Compliance             │   │
│   │           TLS 1.2 min: disable old           │  │          Log: all plan runs + user          │   │
│   │       Enterprise cert: replace self-s        │  │             SIEM: vCenter events            │   │
│   │           Patch: SRM on 30-day SLA           │  │           DR test evidence: stored          │   │
│   │          SQL: TDE + regular backup           │  │            Quarterly: role audit            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SRM Server VMs on management network; WAN replication over encrypted link;                           │
│  SQL Server VM hardened separately with Windows security baseline.                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Dual-person   = two approvals required to trigger real failover                                      │
│  Least privilege= Plan Admin role for testers; Admin for DR team only                                 │
│  TLS 1.2       = disable TLS 1.0/1.1 via IIS TLS settings on SRM                                      │
│  Enterprise cert= replace self-signed for compliance; re-pair required                                │
│  SQL TDE       = Transparent Data Encryption for SRM config DB                                        │
│  MFA           = enforced at SSO layer; requires RADIUS or smart card                                 │
│  SIEM          = collect vCenter events including SRM failover events                                 │
│  Evidence      = DR test results; screenshot or export of plan run                                    │
│  Quarterly audit= review SRM admin + plan admin role assignments                                      │
│  WAN encrypted = IPSEC or MPLS encryption for replication traffic                                     │
│  Patch SLA     = apply SRM patches within 30 days of release                                          │
│  DR test evidence= required for DR compliance (ISO 22301, SOC 2)                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
