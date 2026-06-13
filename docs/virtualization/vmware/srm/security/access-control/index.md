---
tags:
  - security
  - srm
  - vmware
---
# SRM — Access Control


<div class="kb-summary">
Access Control reference covering Least-Privilege Role Assignments, SRA Credential Management, Separation of Duties for Recovery, Network Access Control, Audit Trail.

*Applies to: SRM 8.x / 9.x*
</div>

  SRM RBAC: Recovery Plan Roles → vCenter Permissions
```text
┌───────────────────────────────────── VMware SRM — Access Control ─────────────────────────────────────┐
│                                                                                                       │
│  SRM access control uses vCenter SSO roles; SRM Administrator for full control,                       │
│  SRM Recovery Plan Admin for plan-only access, and read-only for auditors.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SRM Roles                   │  │               Role Assignments              │   │
│   │          SRM Administrator: all ops          │  │           Apply at SRM root level           │   │
│   │          Recovery Plan Admin: plans          │  │              AD groups → roles              │   │
│   │          View Inventory: read-only           │  │           Both sites: same groups           │   │
│   │          Integrate with vCenter SSO          │  │           No cross-site escalation          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SRM Administrator role should be restricted to DR team; plan testers get Plan Admin.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Failover Approval Control           │  │              Audit & Compliance             │   │
│   │          Planned failover: DR lead           │  │              Log: all plan runs             │   │
│   │          Disaster: break-glass proc          │  │            Events: vCenter + SRM            │   │
│   │        Approver: separate from runner        │  │              Review: quarterly              │   │
│   │        Dual-person: critical failover        │  │            Evidence: test results           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SRM Server uses vCenter SSO for auth; AD must be reachable from both SRM Servers;                    │
│  all failover actions are logged in vCenter event database.                                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM Administrator= full control; site pair, protection, plan management                              │
│  Recovery Plan Admin= can run and manage plans; cannot change protection                              │
│  View Inventory = read-only; for monitoring teams                                                     │
│  vCenter SSO   = SRM inherits vCenter identity and authentication                                     │
│  AD group      = map Active Directory group to SRM role                                               │
│  Break-glass   = emergency failover procedure; elevated access                                        │
│  Dual-person   = two named people required to approve real failover                                   │
│  DR lead       = designated approver for planned failover operations                                  │
│  Plan run log  = SRM records who ran each plan and when                                               │
│  Quarterly audit= review SRM role assignments; remove stale users                                     │
│  Evidence      = test results stored in SRM DB for compliance                                         │
│  No cross-site  = SRM roles are per-site; no admin across both sites                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

