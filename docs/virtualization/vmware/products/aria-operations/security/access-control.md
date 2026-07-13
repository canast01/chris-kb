---
tags:
  - aria-operations
  - security
  - vmware
description: "Access Control reference covering RBAC Roles, Object-Level Access Permissions, Creating a Service Account for API Access, Reviewing Current Role..."
---
# Aria Operations — Access Control

<div class="kb-summary">
Access Control reference covering RBAC Roles, Object-Level Access Permissions, Creating a Service Account for API Access, Reviewing Current Role Assignments, Local Admin Account Hardening.

*Applies to: Aria Ops 8.x*
</div>
![Aria Operations — Access Control](../../../../../assets/virtualization-vmware-aria-operations-security-access-contro.svg)

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


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdmMtdnJvcHMtYXBpIiwiaWF0IjoxNzA5MzE2ODAwLCJleHAiOjE3MDkzMjA0MDB9.kR9mL2pQxZ8vN4jWqL5sT6uY3aB1cD2eF4gH5iJ6kL7
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip SSL verification (already present in example, but ensure it's not removed in production variants). |
    | `jq: parse error: Cannot index null with string "token"` | Verify credentials are correct and the API endpoint is accessible; check response with `curl -sk ... | jq '.'` to see the actual error message from vROps. |
    | `command not found: jq` | Install jq package using `apt-get install jq` (Debian/Ubuntu) or `yum install jq` (RHEL/CentOS). |
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


```text title="Expected output"
{
  "username": "admin",
  "role": "Administrator",
  "source": "Local"
}
{
  "username": "svc-monitoring",
  "role": "ReadOnly",
  "source": "LDAP"
}
{
  "username": "ops-team-lead",
  "role": "Administrator",
  "source": "LDAP"
}
{
  "username": "audit-user",
  "role": "ReadOnly",
  "source": "Local"
}
{
  "group": "cn=vrops-admins,ou=groups,dc=example,dc=local",
  "role": "Administrator",
  "source": "LDAP"
}
{
  "group": "cn=vrops-readonly,ou=groups,dc=example,dc=local",
  "role": "ReadOnly",
  "source": "LDAP"
}
{
  "group": "cn=vrops-operators,ou=groups,dc=example,dc=local",
  "role": "Operator",
  "source": "LDAP"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the vROps CA certificate into your system trust store. |
    | `jq: parse error: Cannot index string with string "username"` | Verify the API response is valid JSON by running the curl command without jq piping first; check that the token is not expired. |
    | `curl: (401) Unauthorized` | Ensure the TOKEN variable is set correctly and the token has not expired; regenerate a new API token from the vROps UI under Administration > API Access. |
---

## Local Admin Account Hardening

- Change the default `admin` password immediately after deployment
- Minimum 16 characters, mixed case, numbers, symbols
- Restrict local admin use — prefer AD group-based RBAC for day-to-day access
- Store the admin credential in a secrets vault (CyberArk, HashiCorp Vault)
- Review local accounts monthly: **Administration → Access Control → User Accounts** — remove any accounts that are no longer needed

## See also

- [Aria Operations — Authentication](../authentication/)
- [Aria Operations Security Hardening](../hardening/)
