---
tags:
  - san
  - security
---
# SANnav — Access Control


<div class="kb-summary">
Access Control reference covering Overview, Built-In Roles, Resource Group Scoping, Service Accounts, Least Privilege Guidance and 2 more sections.
</div>

```text
┌─────────────────────────────────────── SANnav — Access Control ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          SANnav RBAC: three roles mapped from AD groups; optionally scoped per fabric         │   │
│   │        Network Administrator: full access including zone management and switch firmware       │   │
│   │        Network Operator: port admin, monitoring, and reporting; no zone set activation        │   │
│   │        Read-only: dashboard and inventory view only; no configuration changes permitted       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Role assignment via AD group → fabric scope applied → API token for automation accounts            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Network Admin        │  │       Network Operator      │  │          Read-Only          │   │
│   │       Zone management       │  │       Port enable/dis       │  │        View dashboard       │   │
│   │       FW upgrade jobs       │  │       Alert management      │  │        View inventory       │   │
│   │       User management       │  │        Report export        │  │         View reports        │   │
│   │        SANnav config        │  │        Health checks        │  │         View alerts         │   │
│   │        Fabric add/del       │  │       Performance mon       │  │          No changes         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Service accounts use API tokens (no password); scoped to minimum required role                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Role       │     AD group     │    Fabric scope   │    API token     │   Review freq    │   │
│   │    Net Admin     │    SAN-Admins    │    All fabrics    │    Yes (auto)    │    Quarterly     │   │
│   │   Net Operator   │     SAN-Ops      │     Per fabric    │   Yes (RO API)   │    Quarterly     │   │
│   │    Read-only     │   SAN-Viewers    │    All fabrics    │    View only     │      Annual      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SANnav on management network; access from jump host only                                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RBAC          = Role-Based Access Control; SANnav maps AD groups to built-in roles                 │
│    Fabric scope  = Restrict a role to specific fabrics; admin sees only assigned fabrics              │
│    API token     = SANnav-generated token for REST API access; no password exchange                   │
│    Zone activate = cfgenable equivalent; Network Admin role required to push changes                  │
│    AD group      = Active Directory security group mapped to SANnav role in LDAP settings             │
│    Service acct  = Non-human account for ITSM/monitoring integration; least-privilege                 │
│    Port admin    = Enable or disable individual FC ports; Operator role minimum                       │
│    FW upgrade    = Firmware upgrade job scheduling on switches; Admin role required                   │
│    User mgmt     = Create/delete/modify SANnav user accounts; Admin only                              │
│    Performance   = Per-port and per-ISL bandwidth graphs; Operator and above                          │
│    Quarterly rev = Access list reviewed against joiners/movers/leavers each quarter                   │
│    Break-glass   = Local admin account; password in vault; used if LDAP unavailable                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [SANnav](../../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Overview

SANnav RBAC is built around roles, resource groups, and optional scope restrictions. A user's effective access is the intersection of their role (what operations they can perform) and their resource group assignment (which fabrics and switches they can see).

---

## Built-In Roles

| Role | Description | Typical Assignee |
|---|---|---|
| **SAN Admin** | Full read/write access to all operations: zoning, firmware, user management, system settings | SAN infrastructure lead |
| **SAN Operator** | Read/write for fabric operations (zoning, port config, firmware) but no user management or system settings | SAN operations team |
| **SAN Viewer** | Read-only access to inventory, events, and dashboards | Capacity team, helpdesk, audit |
| **Security Admin** | Manage users, roles, LDAP, and security settings; no fabric operations | IT security team |
| **Report Admin** | Create, schedule, and download reports; no configuration access | Reporting / management |

Custom roles are not supported in the base SANnav release; the built-in roles above cover most operational needs.

---

## Resource Group Scoping

SANnav organises switches and fabrics into resource groups. Users can be scoped to specific resource groups, restricting their visibility and operations to only the fabrics in their group.

### Assign a User to a Resource Group

1. Navigate to **Administration > User Management > [Username]**.
2. Under **Resource Group Access**, click **Add**.
3. Select the resource group (fabric) and the role to apply within it.
4. Click **Save**.

Example: a remote site operator can be given SAN Operator role on `SITE-B-FABRIC-A` only, with no visibility into other fabrics.

### Create a Resource Group

1. Navigate to **Administration > Resource Groups > New Group**.
2. Name the group: `DC2-FABRIC-A`.
3. Add switches to the group from the switch inventory.
4. Click **Save**.

---

## Service Accounts

Service accounts are local accounts used by automation scripts, monitoring tools, and integrations. Follow these standards:

| Requirement | Detail |
|---|---|
| Naming | `svc-<purpose>` (e.g., `svc-monitor`, `svc-automation`) |
| Role | Minimum required: `SAN Viewer` for read-only; `SAN Operator` for config pushes |
| Password | Stored in vault only; never in scripts or configuration files |
| Password rotation | Every 90 days; coordinated with automation owners |
| Session tokens | Scripts must call `/rest/logout` at completion to release sessions |

### Creating a Service Account

1. Navigate to **Administration > User Management > Local Users > New User**.
2. Username: `svc-monitor`.
3. Role: `SAN Viewer`.
4. Email: SAN team distribution list.
5. Assign to required resource groups.
6. Click **Save**.

---

## Least Privilege Guidance

| Task | Minimum Role | Notes |
|---|---|---|
| View dashboards and inventory | SAN Viewer | Most helpdesk and capacity tasks |
| Acknowledge / clear alerts | SAN Operator | |
| Create/modify/activate zones | SAN Operator | Two-person review recommended |
| Firmware upgrade | SAN Operator | Requires change approval |
| Add/remove switches | SAN Admin | Discovery operations |
| Manage user accounts | Security Admin | |
| Configure LDAP / SSO | Security Admin | |
| Configure backup settings | SAN Admin | |
| View audit log | SAN Admin or Security Admin | |

---

## Audit Log Review

All RBAC-relevant actions are logged:
- User created / deleted / modified
- Role assigned / removed
- Resource group changed
- Permission used (zone change, firmware push)

Access audit log: **Administration > Audit Log**. Filter by event category **Authorization** or **User Management**. Export to CSV for quarterly access reviews.

### Access Review Procedure (Quarterly)

1. Export the user list: **Administration > User Management > Export**.
2. Export the audit log for the past 90 days: **Administration > Audit Log > Export**.
3. For each user:
   - Confirm the user is still employed and in the correct role
   - Confirm the user has logged in within the past 90 days (inactive accounts should be disabled)
   - Confirm service accounts are still in use by active integrations
4. Disable any accounts that no longer require access.
5. Document the review results in the change management system.

---

## Disabling and Removing Accounts

### Disable (Temporary, e.g. Leave of Absence)

1. Navigate to **Administration > User Management > [Username]**.
2. Toggle **Account Status** to **Disabled**.
3. Click **Save**. The user cannot log in but the account and its configuration remain.

### Delete (Permanent, e.g. Offboarding)

1. Navigate to **Administration > User Management > [Username]**.
2. Click **Delete**.
3. Confirm deletion. Any scheduled reports owned by this user will need to be reassigned.

For LDAP-authenticated users: removing the user from the AD group is sufficient to prevent access. SANnav does not cache group membership; the next login attempt will fail. No SANnav-side deletion is required unless the account was also created locally.
