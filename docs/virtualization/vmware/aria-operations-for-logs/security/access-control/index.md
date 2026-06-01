# Aria Ops for Logs — Access Control


<div class="kb-summary">
Access Control reference covering RBAC Roles, Configuring Active Directory Integration, AD Group-Based Role Assignment, Local User Accounts, API Authentication for Automation and 1 more sections.
</div>

## RBAC Roles

Aria Operations for Logs uses a simple two-tier RBAC model: users are either administrators or users. More granular access control is applied through Active Directory group assignment and, in Advanced/Enterprise editions, through **user roles** with object-level scoping.

| Role | Capabilities |
|---|---|
| **Super Admin** | Full access: cluster management, user accounts, alert definitions, content packs, archiving, all log data |
| **Admin** | Manage content (dashboards, queries, alerts) and users — no cluster infrastructure settings |
| **User** | Access the Interactive Analytics UI and dashboards — view only; cannot modify alert definitions or system configuration |

---

## Configuring Active Directory Integration

```text
Administration → Authentication → Active Directory → Configure
```
```powershell
┌────────────────────────────── Aria Operations for Logs — Access Control ──────────────────────────────┐
│                                                                                                       │
│  vRLI access is controlled by built-in roles and AD group mappings via LDAP integration.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Built-in Roles                │  │              LDAP Group Mapping             │   │
│   │       Super Admin: full configuration        │  │       AD group → vRLI role assignment       │   │
│   │        User: view and query logs only        │  │      LDAP config: Administration → Auth     │   │
│   │       Dashboard User: dashboards only        │  │      Group DN: full distinguished name      │   │
│   │       API: programmatic ingest access        │  │      Test LDAP: verify bind and search      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Network access control limits which systems can push logs and access the UI.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Network Access Control            │  │              API Access Control             │   │
│   │      Firewall: restrict UI to mgmt nets      │  │      API key: separate from user login      │   │
│   │     Syslog: allow from source CIDR only      │  │      Session token: 30 min default TTL      │   │
│   │      Admin VAMI (:9543): jumphost only       │  │         Rotate API key periodically         │   │
│   │      No direct DB access from prod nets      │  │         Audit: log all admin actions        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI appliance · AD/LDAP server · firewall rules · management VLAN · NTP                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Super Admin       = Full access to all vRLI configuration, sources, and users                        │
│  User role         = Can search and view logs and dashboards; cannot change config                    │
│  Dashboard User    = Restricted role; view dashboards only, no Explore or admin access                │
│  LDAP integration  = AD connection in vRLI; maps AD groups to Super Admin or User role                │
│  Group DN          = Distinguished Name of AD group used in LDAP group mapping                        │
│  LDAP bind user    = Read-only service account vRLI uses to query AD for group membership             │
│  API key           = vRLI static token for ingest API; does not expire unless rotated                 │
│  Session token     = Short-lived bearer token returned by /api/v1/sessions login                      │
│  VAMI access       = Port 9543; restrict to jump hosts or management network only                     │
│  Syslog source ACL = Firewall rule limiting which source IPs can reach vRLI ports                     │
│  Audit log         = vRLI logs all login, config change, and admin actions for review                 │
│  MFA               = Not native to vRLI; enforce MFA via vIDM if SSO integrated                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

| AD Group | Aria Ops for Logs Role |
|---|---|
| `GG-VRLI-Admins` | Super Admin |
| `GG-VRLI-Operators` | Admin |
| `GG-VRLI-ReadOnly` | User |

Users who are members of multiple groups receive the highest-privilege role from the combined membership.

---

## Local User Accounts

Local accounts are used for break-glass access and service accounts. Manage via:

```text
Administration → Authentication → Local Users → Add User
```

| Account | Role | Purpose |
|---|---|---|
| `admin` | Super Admin | Break-glass; change password immediately post-deployment |
| `svc-vrli-api` | Admin | API automation (alert management, queries) |
| `svc-monitoring` | User | Read-only monitoring queries from external systems |

Password requirements for local accounts:
- Minimum 12 characters
- Mixed case, numbers, and at least one symbol
- Store in enterprise vault — not shared documents

---

## API Authentication for Automation

```bash
# Authenticate — Aria Ops for Logs uses HTTP Basic auth; no separate token endpoint
# All API calls use: -u 'admin:<password>' or -u 'svc-vrli-api:<password>'

# Test API authentication
curl -sk -u 'svc-vrli-api:<password>' \
  "https://vrli-prod-01.example.local/api/v2/version" | jq '.'
# Expected: {"version": "8.x.y.zzz", ...}
```

For service accounts: assign the minimum required role — use the `User` role for scripts that only query logs; use the `Admin` role for scripts that create or modify alert definitions.

---

## Session and Access Logging

All authentication events are logged to the runtime log:

```bash
# View login and authentication events
grep -i "login\|authenticated\|logout\|failed" /var/log/loginsight/runtime.log | tail -100

# View admin operations (alert create/delete, user changes)
grep -i "admin\|user\|alert\|content" /var/log/loginsight/runtime.log | \
  grep -i "create\|update\|delete" | tail -100
```

Forward these logs to a SIEM or dedicated audit log store by configuring the appliance's syslog output:

```bash
# Forward syslog from the Aria Ops for Logs appliance to an external SIEM
echo '*.* @@siem.example.local:514' > /etc/rsyslog.d/vrli-audit.conf
systemctl restart rsyslog
```
