# Cisco DCNM — Access Control

> Part of the [Cisco DCNM](../../index.md) reference.

---

## Overview

DCNM RBAC uses roles to control what operations users can perform. Users can be scoped to specific fabrics (resource groups), restricting visibility and operations to only their assigned fabrics.

---

## Built-In Roles

| Role | Permissions | Typical Assignee |
|---|---|---|
| **Admin** | Full access: all DCNM configuration, user management, system administration | DCNM platform owner |
| **Network Admin** | Full SAN operations: zones, VSANs, device aliases, firmware, discovery. No user management. | SAN lead engineer |
| **Operator** | Read/write for zone changes and operational tasks. No system settings. | SAN operations team |
| **Network Operator** | Read-only access to all inventory, topology, events, and reports | NOC, helpdesk, capacity |
| **Access Admin** | Manage user accounts and roles only; no SAN operations | IT security / IAM team |

---

## Fabric-Level Scoping

Assign users to specific fabrics to restrict their scope:

1. Navigate to **Administration > Security > Fabric Access Control**.
2. Select the user.
3. Select fabrics: assign specific fabrics or **All Fabrics**.
4. Assign a role per fabric (a user can have different roles in different fabrics).
5. Click **Save**.

Example: Site B engineer gets `Network Admin` on `DC2-FABRIC-A` and `DC2-FABRIC-B`, but no access to DC1 fabrics.

---

## LDAP Group to Role Mapping

When LDAP is configured, roles are assigned via group membership rather than per-user assignment.

Navigate to **Administration > Security > Authentication > LDAP > Role Mapping**:

| AD Group | DCNM Role |
|---|---|
| `GRP-DCNM-Admins` | Admin |
| `GRP-DCNM-NetworkAdmins` | Network Admin |
| `GRP-DCNM-Operators` | Operator |
| `GRP-DCNM-ReadOnly` | Network Operator |
| `GRP-DCNM-AccessAdmins` | Access Admin |

When a user logs in via LDAP:
1. DCNM resolves their AD group memberships
2. Groups are matched against the role mapping table
3. The highest-privilege matching role is assigned

If a user belongs to multiple groups with different roles, the most permissive role applies. For strict least-privilege, avoid putting users in multiple DCNM role groups.

---

## Service Account Configuration

| Account | Role | Purpose |
|---|---|---|
| `svc-monitor` | Network Operator | Monitoring, health checks, read-only API queries |
| `svc-automation` | Operator | Automated zone changes, config deployment |
| `svc-reporting` | Network Operator | Report generation |

Service accounts:
- Named `svc-<purpose>` as local accounts
- Password in vault; never in scripts
- Rotate every 90 days, coordinated with automation owners
- No interactive login permissions (enforce via source IP restriction if DCNM supports)

---

## Least Privilege Reference

| Task | Minimum Role |
|---|---|
| View inventory, topology, events | Network Operator |
| View performance data | Network Operator |
| Acknowledge/clear alarms | Operator |
| Create/modify/activate zones | Network Admin |
| Create/modify VSANs | Network Admin |
| Manage device aliases | Network Admin |
| Firmware upgrade | Network Admin |
| Add/remove fabrics | Admin |
| Manage user accounts | Access Admin |
| Configure LDAP/TACACS+ | Admin |
| System settings, backup | Admin |

---

## Quarterly Access Review Procedure

1. Export user list from DCNM: **Administration > Security > Users > Export**.
2. Review each account:
   - User is still employed
   - Role matches job function
   - Account has had activity in the past 90 days
3. For LDAP accounts: verify AD group membership reflects current role requirement.
4. Disable or delete accounts for departed employees.
5. Downgrade accounts where privileges exceed current job function.
6. Document the review in the change management system.

```bash
# Export users via REST API for automated review
curl -sk -b dcnm-cookie.txt \
  "${DCNM_HOST}/rest/fm/users" | python3 -m json.tool > dcnm-users-$(date +%Y%m%d).json
```
