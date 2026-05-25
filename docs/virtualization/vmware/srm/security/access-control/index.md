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

---

## SRM Uses vCenter RBAC

SRM does not have its own user store. All authentication and authorization goes through vCenter SSO. SRM-specific privileges are added to vCenter's permission model.

---

## SRM-Specific Roles

| Role | Description |
|---|---|
| Site Recovery Administrator | Full SRM control — configure protection groups, recovery plans, run recovery |
| Site Recovery User | View SRM configuration — no changes |
| Site Recovery Recovery Admin | Run Recovery Plans — cannot configure protection groups |

These roles appear in vCenter after SRM is installed. Assign them via vCenter Permissions:

```text
vCenter → Administration → Global Permissions → Add Permission
  User/Group: CORP\SRM-Admins
  Role: Site Recovery Administrator
  Propagate: Yes
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
