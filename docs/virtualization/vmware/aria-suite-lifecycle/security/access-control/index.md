---
tags:
  - aria-lcm
  - security
  - vmware
---
# Aria Suite Lifecycle — Access Control


<div class="kb-summary">
Access Control reference covering Service Account for API Automation, Separation of Duties, Auditing Access.

*Applies to: Aria LCM 8.x*
</div>

  LCM RBAC — AD Groups → LCM Roles
```text
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
```
Assign the minimum role required for the automation task — use `LCM_CONTENT_DEVELOPER` for scripts that only query health; use `LCM_ADMIN` only for scripts that trigger upgrades or certificate replacements.

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

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
