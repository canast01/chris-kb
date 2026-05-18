# Aria Operations — Access Control

```
┌─────────────────────────────────────────────────────────────┐
│             Aria Operations RBAC Model                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐      ┌─────────────────────────────┐  │
│  │  AD Groups       │      │  Roles                      │  │
│  │  ┌─────────────┐ │      │  ┌─────────────────────┐    │  │
│  │  │GG-VROPS-    │─┼─────►│  │ Administrator        │    │  │
│  │  │  Admins     │ │      │  │ (full access)        │    │  │
│  │  ├─────────────┤ │      │  ├─────────────────────┤    │  │
│  │  │GG-VROPS-    │─┼─────►│  │ Content Admin        │    │  │
│  │  │  Content    │ │      │  │ (dashboards/alerts)  │    │  │
│  │  ├─────────────┤ │      │  ├─────────────────────┤    │  │
│  │  │GG-VROPS-    │─┼─────►│  │ Operator             │    │  │
│  │  │  Operators  │ │      │  │ (ack alerts / run    │    │  │
│  │  ├─────────────┤ │      │  │  actions)            │    │  │
│  │  │GG-VROPS-    │─┼─────►│  ├─────────────────────┤    │  │
│  │  │  ReadOnly   │ │      │  │ Read Only            │    │  │
│  │  └─────────────┘ │      │  └─────────────────────┘    │  │
│  └──────────────────┘      └──────────────┬──────────────┘  │
│                                           │                 │
│                                           ▼                 │
│                         ┌───────────────────────────────┐   │
│                         │  Object Scope (optional)      │   │
│                         │  DC-LON / DC-NYC / All        │   │
│                         └───────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

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

```
Administration → Access Control → Object Permissions → Add Permission
```

1. Select an **Object Scope**: choose specific resources (e.g., a single vCenter, cluster, datacenter)
2. Assign the scope to a user or group
3. Users can only view and act on resources within their permitted scope

Example use case: Assign the `Operator` role with a scope limited to `DC-LON` — the team can only see and acknowledge alerts for London datacenter objects.

---

## Configuring LDAP Groups

```
Administration → Authentication Sources → (configure AD source first — see Authentication page)
Administration → Access Control → User Groups → Import Groups from Source
```

Search for the AD group by name or DN, select, and import. The group appears in the User Groups list. Assign a role:

```
Administration → Access Control → User Groups → select group → Assign Role → select role → Save
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

```
Administration → Access Control → User Accounts → Add → Local User
```

- Username: `svc-vrops-api`
- Role: assign minimum required role (Read Only for monitoring scripts; Content Admin for scripts that create alert definitions)
- Password: minimum 16 characters; store in vault

For API calls, authenticate as the service account:

```bash
TOKEN=$(curl -sk -X POST \
  "https://vrops-prod-01.corp.local/suite-api/api/auth/token/acquire" \
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
  "https://vrops-prod-01.corp.local/suite-api/api/auth/userquery" | \
  jq '.users[] | {username: .username, role: .role[].name, source: .authSourceName}'

# List all imported user groups
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.corp.local/suite-api/api/auth/usergroups" | \
  jq '.[] | {group: .name, role: .role[].name, source: .authSourceName}'
```

---

## Local Admin Account Hardening

- Change the default `admin` password immediately after deployment
- Minimum 16 characters, mixed case, numbers, symbols
- Restrict local admin use — prefer AD group-based RBAC for day-to-day access
- Store the admin credential in a secrets vault (CyberArk, HashiCorp Vault)
- Review local accounts monthly: **Administration → Access Control → User Accounts** — remove any accounts that are no longer needed
