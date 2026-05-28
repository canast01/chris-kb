# SRM — Access Control

```text
  SRM RBAC: Recovery Plan Roles → vCenter Permissions
┌──────────────────────────────────────────────────────────────┐
│  AD Groups                SRM Roles (via vCenter Global Perms)│
│  ┌────────────────┐       ┌───────────────────────────────┐   │
│  │ CORP\SRM-Admins│──────►│ Site Recovery Administrator   │   │
│  │                │       │ (configure + execute)         │   │
│  ├────────────────┤       ├───────────────────────────────┤   │
│  │ CORP\SRM-DR-   │──────►│ Site Recovery Recovery Admin  │   │
│  │ RunTeam        │       │ (execute only — no config)    │   │
│  ├────────────────┤       ├───────────────────────────────┤   │
│  │ CORP\Infra-    │──────►│ Site Recovery User            │   │
│  │ ReadOnly       │       │ (view only)                   │   │
│  └────────────────┘       └───────────────────────────────┘   │
│                                                               │
│  SRA credentials: stored encrypted in SRM                    │
│  Rotate: array API token ──► update in SRM ──► delete old    │
└──────────────────────────────────────────────────────────────┘
```
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

---

## Least-Privilege Role Assignments

| AD Group | Role | Rationale |
|---|---|---|
| `CORP\SRM-Admins` | Site Recovery Administrator | Full config and run |
| `CORP\SRM-DR-RunTeam` | Site Recovery Recovery Admin | DR team — run plans only |
| `CORP\Infra-ReadOnly` | Site Recovery User | View-only for auditing |

Separate the configuration role (SRM-Admins) from the run role (SRM-DR-RunTeam) — different people should configure DR plans and execute them during an actual disaster.

---

## SRA Credential Management

SRA (Storage Replication Adapter) stores array credentials encrypted in SRM:

```text
Site Recovery → Storage → Array Pairs → [pair] → Configure Adapter
  Array credentials: FlashArray management IP + API token
  Credentials are stored encrypted — only SRM can decrypt them
```

Rotate SRA credentials:
```text
1. Create new API token on storage array
2. Site Recovery → Storage → Array Pairs → [pair] → Edit → update credentials
3. Delete old API token from array
```

---

## Separation of Duties for Recovery

| Action | Who |
|---|---|
| Configure protection groups | SRM Admin |
| Configure recovery plans | SRM Admin |
| Run test recovery | SRM Admin or DR Run Team |
| Run planned migration | SRM Admin (requires sign-off process) |
| Run disaster recovery | DR Run Team (emergency — restricted to this team) |
| Re-protect / failback | SRM Admin |

Implement the separation by assigning the DR Run Team to the "Site Recovery Recovery Admin" role — they can execute plans but cannot modify protection group or plan configuration.

---

## Network Access Control

SRM Server should be accessible only from:
- Management workstations (HTTPS 443)
- vCenter Server (TCP 443 and TCP 9086)
- Remote SRM Server across sites (TCP 9086)

Block direct access from desktop VLANs. Use a dedicated management VLAN for SRM Server.

---

## Audit Trail

SRM logs all actions to vCenter events:
```text
vCenter → Monitor → Events → filter by "drm" (Site Recovery events prefix)
```

Key events to monitor:
- Recovery Plan started (type, who initiated)
- Recovery Plan completed/failed
- Protection Group configuration changed
- SRA adapter configuration changed
