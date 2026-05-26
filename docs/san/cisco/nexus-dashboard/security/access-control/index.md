# Nexus Dashboard — Access Control

> Part of the [Nexus Dashboard](../../index.md) reference.

---

## Overview

Nexus Dashboard RBAC is built around roles and site-level scoping. A user's effective access is the intersection of their platform role (what operations they can perform) and their site assignment (which fabrics they can see and manage). Applications (NDFC, NDI) inherit the platform roles but may add additional granularity at the application level.

---

## Platform Roles

| Role | Permissions | Typical Assignee |
|---|---|---|
| **Admin** | Full access: all ND configuration, user management, app settings, cluster administration | ND platform owner |
| **Operator** | Application operations (SAN management, zone changes, firmware) but no cluster/user admin | SAN operations team |
| **Viewer** | Read-only access to all dashboards, inventory, and reports | NOC, capacity, audit |
| **App User** | Application-specific access; defined per-app (NDFC / NDI define their own sub-roles) | App-specific users |

The **Admin** role is the only role with access to the Admin Console (cluster settings, user management, certificates, backup). Operators and Viewers access only application workspaces (NDFC, NDI).

---

## Site-Level Scoping

Users can be scoped to specific sites (fabrics), restricting their visibility and operations to only the assigned sites.

### Assign a User to a Site

1. Navigate to **Admin Console > Security > Users > [Username] > Sites**.
2. Click **Add Site**.
3. Select the site and the role for this site (can differ from the user's global role).
4. Click **Save**.

Example: a remote site engineer gets `Operator` role on `DC2-SAN` and `DC2-ACI` but `Viewer` role on DC1 fabrics.

### Site Scoping for LDAP Groups

LDAP group role mappings can also be scoped to sites:

1. Navigate to **Admin Console > Security > Roles > LDAP Role Mapping > [Group]**.
2. Set the site scope: **All Sites** or select specific sites.
3. Click **Save**.

This allows different AD groups to manage different sites without creating individual user assignments.

---

## NDFC Application Roles

NDFC adds its own role layer within the Operator permission level. When a user with Operator access logs into NDFC:

| NDFC Role | Permissions |
|---|---|
| Network Admin | Full SAN operations: zones, VSANs, device aliases, firmware, discovery. No user management. |
| Operator | Zone changes and operational tasks (read/write for fabric operations). |
| Network Operator | Read-only access to NDFC inventory, topology, and events. |
| Access Admin | Manage NDFC-level user accounts and roles only. |

NDFC roles are assigned in NDFC itself: **NDFC > Admin > Users > [User] > NDFC Role**.

---

## Service Account Configuration

| Account | Role | Purpose |
|---|---|---|
| `svc-monitor` | Viewer | Monitoring scripts, health checks, read-only API queries |
| `svc-automation` | Operator | Automated zone changes, zone exports, NDFC config |
| `svc-reporting` | Viewer | Report generation, audit exports |

Service account requirements:
- Named `svc-<purpose>` — local ND accounts
- Password stored in vault; never hard-coded or committed to scripts
- Rotate every 90 days, coordinated with automation owners
- Automation scripts must call logout endpoint when finished

### Create a Service Account

```bash
# Via REST API
TOKEN=$(curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"admin","userPasswd":"<pass>","domain":"local"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -X POST https://nd-dc1.corp.example.com/nexus/api/v1/users \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "svc-monitor",
    "password": "<strong-password>",
    "firstName": "Service",
    "lastName": "Monitor",
    "email": "san-team@corp.example.com",
    "roles": [{"name": "Viewer", "sites": [{"name": "DC1-SAN"}, {"name": "DC2-SAN"}]}]
  }' | python3 -m json.tool
```
┌─────────────────────────── Cisco Nexus Dashboard — Security Access Control ───────────────────────────┐
│                                                                                                       │
│  RBAC model with local and AAA-backed users; per-app roles scoped to tenant or site.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               User Management                │  │                  Role Model                 │   │
│   │          Local users: ND-native DB           │  │          Admin: full cluster access         │   │
│   │         Remote: LDAP/RADIUS/TACACS+          │  │        Operator: read + limited write       │   │
│   │          Groups: mapped to ND roles          │  │             Read-only: view only            │   │
│   │        Password policy: enforce cmplx        │  │         App roles: per NDFC/NDI/NDO         │   │
│   │        Session timeout: configurable         │  │         Site scope: per-site access         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Roles assigned at cluster level; app-specific roles further restrict within each app                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              API Access Control              │  │                    Audit                    │   │
│   │         REST API: Bearer token auth          │  │          Login events: success/fail         │   │
│   │          Token TTL: 60 min default           │  │           Config changes: who+what          │   │
│   │         Service accounts: dedicated          │  │          API calls: logged per user         │   │
│   │         IP allowlist: restrict mgmt          │  │            Export: syslog to SIEM           │   │
│   │            MFA: via SAML IdP only            │  │          Retention: 90-day default          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster · LDAP/RADIUS/TACACS+ server · SAML IdP · SIEM · management network                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RBAC           = Role-Based Access Control; maps users/groups to permitted actions                   │
│  LDAP group map = Mapping LDAP group DN to an ND role for automatic assignment                        │
│  App role       = Role scoped to a specific ND app (NDFC/NDI/NDO) not cluster-wide                    │
│  Site scope     = Restricting a user to only manage specific onboarded sites                          │
│  Service account= Dedicated ND user for automation; not used for human login                          │
│  IP allowlist   = Network ACL restricting management access to known source IPs                       │
│  MFA            = Multi-Factor Auth; enforced by SAML IdP (not natively by ND)                        │
│  Token TTL      = JWT lifetime; default 60 min; reduce for higher security posture                    │
│  Password complexity= Minimum length, upper/lower/digit/special char requirements                     │
│  Session timeout= Idle period after which UI session is automatically terminated                      │
│  SIEM export    = Forwarding ND audit logs via syslog TLS to Splunk or similar                        │
│  Audit retention= How long ND retains access logs before purging (default 90 days)                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Disabling and Removing Accounts

### Disable (Temporary)

1. Navigate to **Admin Console > Security > Local Users > [Username]**.
2. Click **Disable Account**.
3. The user cannot log in but the account and audit trail are retained.

### Delete (Permanent)

1. Navigate to **Admin Console > Security > Local Users > [Username]**.
2. Click **Delete**.

For LDAP users: removing the user from the mapped AD group is sufficient to revoke access. ND re-evaluates group membership on every login.
