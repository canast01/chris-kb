# Aria Ops for Logs — Access Control

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Ops for Logs RBAC Model                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  AD Groups (via LDAPS)     →  Role Assignment               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  GG-VRLI-Admins          →  Super Admin              │   │
│  │  GG-VRLI-Operators       →  Admin                    │   │
│  │  GG-VRLI-ReadOnly        →  User                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  Role Capabilities:                                         │
│  Super Admin — cluster config · users · all settings        │
│  Admin       — content · alerts · dashboards                │
│  User        — Interactive Analytics query/view only        │
│                                                             │
│  Local Accounts (break-glass only):                         │
│  admin → Super Admin (change password immediately)          │
│  svc-vrli-api → Admin (automation scripts)                  │
│  svc-monitoring → User (read-only queries)                  │
└─────────────────────────────────────────────────────────────┘
```

## RBAC Roles

Aria Operations for Logs uses a simple two-tier RBAC model: users are either administrators or users. More granular access control is applied through Active Directory group assignment and, in Advanced/Enterprise editions, through **user roles** with object-level scoping.

| Role | Capabilities |
|---|---|
| **Super Admin** | Full access: cluster management, user accounts, alert definitions, content packs, archiving, all log data |
| **Admin** | Manage content (dashboards, queries, alerts) and users — no cluster infrastructure settings |
| **User** | Access the Interactive Analytics UI and dashboards — view only; cannot modify alert definitions or system configuration |

---

## Configuring Active Directory Integration

```
Administration → Authentication → Active Directory → Configure
```

Provide:
- **Domain**: `corp.local`
- **Domain controller**: `dc01.example.local` (use multiple for HA)
- **Port**: 636 (LDAPS) — required for production
- **Bind DN**: `CN=svc-vrli-ldap,OU=Service Accounts,DC=corp,DC=local`
- **Bind password**: stored in CyberArk or vault; retrieved during configuration

Import the domain CA certificate before configuring LDAPS:
```
Administration → SSL → Import Certificate → paste the root CA PEM
```

---

## AD Group-Based Role Assignment

After AD is configured, map AD groups to Aria Ops for Logs roles:

```
Administration → Authentication → Active Directory → Group Access
```

| AD Group | Aria Ops for Logs Role |
|---|---|
| `GG-VRLI-Admins` | Super Admin |
| `GG-VRLI-Operators` | Admin |
| `GG-VRLI-ReadOnly` | User |

Users who are members of multiple groups receive the highest-privilege role from the combined membership.

---

## Local User Accounts

Local accounts are used for break-glass access and service accounts. Manage via:

```
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
