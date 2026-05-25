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

---

## Least Privilege Reference

| Task | Minimum Role | Notes |
|---|---|---|
| View dashboards, inventory, topology | Viewer | |
| View NDI anomalies | Viewer | NDI site must be in scope |
| Acknowledge/clear NDFC alarms | Operator | |
| Create/modify/activate NDFC zones | Operator | NDFC Network Admin required |
| Manage VSANs and device aliases | Operator | NDFC Network Admin required |
| MDS firmware upgrade via NDFC | Operator | NDFC Network Admin required |
| Register new sites | Admin | |
| Install/upgrade ND applications | Admin | |
| Manage ND user accounts | Admin | |
| Configure LDAP/TACACS+/SAML | Admin | |
| ND cluster backup and restore | Admin | |
| TLS certificate management | Admin | |

---

## Quarterly Access Review Procedure

1. Export the user list: **Admin Console > Security > Local Users > Export**.
2. For LDAP accounts: export the current LDAP group membership for all ND-mapped groups.
3. For each account:
   - Confirm the user is still employed and in the correct role
   - Confirm the user has logged in within the past 90 days (inactive accounts should be disabled or deleted)
   - Confirm service accounts are still in use by active automation
4. Disable accounts no longer required:
   - Navigate to **Admin Console > Security > Local Users > [Username] > Disable**
   - For LDAP accounts: remove the user from the AD group; ND denies access on next login attempt
5. Document the review in the change management system.

### API-Based User Audit

```bash
# List all local users with their roles
curl -sk https://nd-dc1.corp.example.com/nexus/api/v1/users \
  -H "Authorization: Bearer ${ND_TOKEN}" \
  | python3 -c "
import sys, json, csv
users = json.load(sys.stdin)
w = csv.writer(sys.stdout)
w.writerow(['username','email','roles','lastLoginTime'])
for u in users:
    roles = ', '.join(r.get('name','') for r in u.get('roles',[]))
    w.writerow([u.get('username',''), u.get('email',''), roles, u.get('lastLoginTime','')])
"
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
