# Aria Suite Lifecycle — Access Control

```text
  LCM RBAC — AD Groups → LCM Roles
┌─────────────────────────────────────────────────────────────────┐
│  AD (via VIDM sync)          LCM Roles                          │
│  ┌─────────────────────┐     ┌─────────────────────────────┐    │
│  │ GG-LCM-Admins       │────►│ LCM Admin                   │    │
│  │                     │     │  deploy/upgrade/Locker/users │    │
│  ├─────────────────────┤     ├─────────────────────────────┤    │
│  │ GG-LCM-Operators    │────►│ LCM Content Developer       │    │
│  │                     │     │  extract/deploy content packs│    │
│  │                     │     │  read env health             │    │
│  ├─────────────────────┤     ├─────────────────────────────┤    │
│  │ GG-LCM-ReadOnly     │────►│ Viewer                      │    │
│  │                     │     │  read-only; no write ops    │    │
│  └─────────────────────┘     └─────────────────────────────┘    │
│                                                                 │
│  API service account: svc-lcm-api@local → min required role     │
│  Never assign roles to individual user accounts                 │
└─────────────────────────────────────────────────────────────────┘
```
┌──────────────────────────────────── Aria Suite LCM Access Control ────────────────────────────────────┐
│                                                                                                       │
│  Admin and User roles with vIDM group mapping for Aria Suite Lifecycle Manager.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Built-in Roles                │  │               Role Permissions              │   │
│   │            System Admin: full LCM            │  │           SystemAdmin: all actions          │   │
│   │          Content Admin: deploy only          │  │         ContentAdmin: deploy/upgrade        │   │
│   │              Viewer: read-only               │  │          Viewer: no config changes          │   │
│   │         Least privilege: use Viewer          │  │             Admin: ops team only            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Three roles cover LCM access; vIDM maps AD groups to roles for SSO login.                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              vIDM Group Mapping              │  │              API Access Control             │   │
│   │           LCM: Settings > Identity           │  │           REST API: session token           │   │
│   │            Map vIDM group to role            │  │           Token tied to user role           │   │
│   │              SSO login via vIDM              │  │          No separate API-only role          │   │
│   │           Review group mapping 90d           │  │         Rotate API tokens regularly         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM; vIDM appliance for SSO; AD/LDAP for group source; network to vIDM                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  System Admin        = Full LCM access: deploy, upgrade, cert, user management                        │
│  Content Admin       = Can deploy and upgrade products; no user management                            │
│  Viewer Role         = Read-only: see environments and health; no actions                             │
│  vIDM Group Mapping  = AD group in vIDM assigned LCM role for SSO access                              │
│  SSO Login           = SAML2 redirect to vIDM on LCM browser access                                   │
│  Local Admin         = LCM-internal admin account; break-glass only                                   │
│  API Token           = Session token from POST /auth/login; inherits user role                        │
│  Least Privilege     = Assign Viewer to read-only teams; Admin to ops only                            │
│  Group Review        = Quarterly check of vIDM group to LCM role mappings                             │
│  Token Rotation      = Invalidate and reissue API tokens periodically                                 │
│  vIDM Integration    = LCM registered as app in vIDM for SAML SSO                                     │
│  Audit Log           = LCM records all user actions and config changes                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

1. Select the role from the dropdown
2. Click **Add Group** — search for the AD group synced via VIDM (e.g., `GG-LCM-Admins`)
3. Save — the group is immediately assigned the role

Remove a role assignment by selecting the row and clicking **Remove**.

| AD Group | Assigned Role | Members |
|---|---|---|
| `GG-LCM-Admins` | LCM Admin | Platform team leads, on-call engineers |
| `GG-LCM-Operators` | LCM Content Developer | Platform team engineers |
| `GG-LCM-ReadOnly` | Viewer | Management, auditors, other teams |

---

## Service Account for API Automation

Create a dedicated local account for automation scripts — do not use `admin@local` for scripted access.

```bash
# Create a local API service account via LCM API (as admin)
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.example.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

curl -sk -X POST -H "x-xenon-auth-token: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://lcm-prod-01.example.local/lcm/authz/api/v2/users" \
  -d '{
    "username": "svc-lcm-api@local",
    "password": "<strong-password>",
    "role": "LCM_CONTENT_DEVELOPER"
  }'
```

Assign the minimum role required for the automation task — use `LCM_CONTENT_DEVELOPER` for scripts that only query health; use `LCM_ADMIN` only for scripts that trigger upgrades or certificate replacements.

---

## Separation of Duties

Apply the principle of least privilege across team functions:

| Function | Required Role | Team |
|---|---|---|
| Deploy/upgrade Aria products | LCM Admin | Platform team lead |
| Manage Locker certificates | LCM Admin | Platform team / PKI team |
| Rotate Locker passwords | LCM Admin | Platform team |
| View environment health | Viewer | Any team |
| Extract/deploy content packs | LCM Content Developer | Operations team |
| API health monitoring | LCM Content Developer | Monitoring team (service account) |

---

## Auditing Access

LCM logs all write operations (deploy, upgrade, certificate import) to the application log. Parse for audit records:

```bash
# List all login events
grep -i "login\|authenticated\|logout" /var/log/vmware/vrlcm/lcm-app.log | \
  grep -v "health\|ping" | tail -100

# List all Locker write operations (certificate/password imports and updates)
grep -i "locker\|certificate\|password" /var/log/vmware/vrlcm/lcm-app.log | \
  grep -i "import\|update\|delete\|create" | tail -100

# List all upgrade/deploy requests with user attribution
grep -i "upgrade\|deploy\|install" /var/log/vmware/vrlcm/lcm-app.log | \
  grep -i "user\|request" | tail -100
```

For formal audit trails, forward the LCM syslog to Aria Operations for Logs or a SIEM:

```bash
# Configure syslog forwarding from LCM appliance
# Edit /etc/rsyslog.d/lcm-remote.conf (create if not present)
echo '*.* @@vrli-prod-01.example.local:514' > /etc/rsyslog.d/lcm-remote.conf
systemctl restart rsyslog
```
