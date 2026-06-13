---
tags:
  - aria-operations
  - security
  - vmware
---
# Aria Operations — Access Control


<div class="kb-summary">
Access Control reference covering RBAC Roles, Object-Level Access Permissions, Creating a Service Account for API Access, Reviewing Current Role Assignments, Local Admin Account Hardening.

*Applies to: Aria Ops 8.x*
</div>

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## RBAC Roles

Aria Operations uses a hierarchical role model. Roles are assigned to local users or to groups imported from Active Directory / LDAP.

| Role | Permissions |
|---|---|
| **Administrator** | Full access: manage users, adapters, cluster settings, system configuration, and all content |
| **Content Admin** | Create and manage dashboards, views, reports, alert definitions, and policies; no system administration |
| **Operator** | Acknowledge and cancel alerts, run manual actions; view all content; no configuration changes |
| **Read Only** | View dashboards, alerts, and metrics; no actions or configuration |
| **PowerUser** | Deprecated — Content Admin is the replacement |

Roles are assigned in **Administration → Access Control → User Accounts** (local users) or **Administration → Access Control → User Groups** (imported AD groups).

---

## Object-Level Access Permissions

Beyond role-level access, Aria Operations supports **object permissions** to restrict which inventory objects a user can see.

Create an object permission policy:

```text
┌─────────────────────────────────── Aria Operations Access Control ────────────────────────────────────┐
│                                                                                                       │
│  Admin, Content Admin, General User, and Read-only roles with group mapping.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Built-in Roles                │  │               Role Permissions              │   │
│   │          Administrator: full access          │  │         Admin: all settings + users         │   │
│   │          Content Admin: dashboards           │  │         ContentAdmin: dash + alerts         │   │
│   │         General User: view+interact          │  │          GeneralUser: view/interact         │   │
│   │             Read-Only: view only             │  │         ReadOnly: no config changes         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Roles control UI access; group mapping assigns roles via AD; custom roles optional.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Group Mapping (LDAP/vIDM)           │  │                 Custom Roles                │   │
│   │            Admin > Access Control            │  │             Clone existing role             │   │
│   │           Import AD group to vROps           │  │          Assign specific privileges         │   │
│   │           Assign role to AD group            │  │          Limit to specific objects          │   │
│   │               Review quarterly               │  │           Named for team function           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; AD/LDAP directory; vIDM optional SSO; network to LDAP server                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Administrator Role   = Full vROps access: data sources, users, settings, all ops                     │
│  Content Admin        = Manage dashboards, alerts, and reports; no user mgmt                          │
│  General User         = View and interact with dashboards; cannot change settings                     │
│  Read-Only Role       = View-only; no interaction with alerts or config                               │
│  Custom Role          = User-defined role cloned from built-in with scoped perms                      │
│  AD Group Mapping     = AD security group assigned vROps role in Access Control                       │
│  vIDM Group Mapping   = vIDM group assigned role; used when SSO is configured                         │
│  Object Scope         = Restrict role to specific objects (e.g. one cluster)                          │
│  Privilege            = Granular permission: view, interact, modify, manage users                     │
│  Least Privilege      = Grant minimum role for each team; review regularly                            │
│  Quarterly Review     = Periodic access audit: remove leavers, check role drift                       │
│  Local Account        = vROps-internal account; use for break-glass only                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
| AD Group | Aria Operations Role | Object Scope |
|---|---|---|
| `GG-VROPS-Admins` | Administrator | All objects |
| `GG-VROPS-ContentAdmins` | Content Admin | All objects |
| `GG-VROPS-Operators-LON` | Operator | DC-LON only |
| `GG-VROPS-Operators-NYC` | Operator | DC-NYC only |
| `GG-VROPS-ReadOnly` | Read Only | All objects |

---

## Creating a Service Account for API Access

```text
Administration → Access Control → User Accounts → Add → Local User
```

- Username: `svc-vrops-api`
- Role: assign minimum required role (Read Only for monitoring scripts; Content Admin for scripts that create alert definitions)
- Password: minimum 16 characters; store in vault

For API calls, authenticate as the service account:

```bash
TOKEN=$(curl -sk -X POST \
  "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-vrops-api","password":"<password>","authSource":"Local"}' | \
  jq -r '.token')
```

---

## Reviewing Current Role Assignments

```bash
# List all user accounts and their roles via API
TOKEN=<your-token>
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/auth/userquery" | \
  jq '.users[] | {username: .username, role: .role[].name, source: .authSourceName}'

# List all imported user groups
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/auth/usergroups" | \
  jq '.[] | {group: .name, role: .role[].name, source: .authSourceName}'
```

---

## Local Admin Account Hardening

- Change the default `admin` password immediately after deployment
- Minimum 16 characters, mixed case, numbers, symbols
- Restrict local admin use — prefer AD group-based RBAC for day-to-day access
- Store the admin credential in a secrets vault (CyberArk, HashiCorp Vault)
- Review local accounts monthly: **Administration → Access Control → User Accounts** — remove any accounts that are no longer needed

## See also

- [Aria Operations — Authentication](authentication/)
- [Aria Operations Security Hardening](hardening/)
