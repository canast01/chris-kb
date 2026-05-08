# Aria Suite Lifecycle — Access Control

## RBAC Model

LCM uses a role-based access control model backed by Workspace ONE Access (VIDM) for group resolution. Roles should be assigned to AD groups synced via VIDM — never assign roles to individual user accounts.

| Role | Capabilities |
|---|---|
| **LCM Admin** | Full access: deploy products, run upgrades, manage Locker (certs/passwords/licences), manage vCenter and VIDM integrations, manage users and roles |
| **LCM Content Developer** | Read access + content lifecycle operations (extract and deploy dashboards, blueprints); cannot initiate product deployments or upgrades |
| **Viewer** | Read-only dashboard access to environment health, Locker inventory, and request history; no write operations |

---

## Configuring Role Assignments

```
LCM → Settings → Access Control → Add Role Assignment
```

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
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.corp.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

curl -sk -X POST -H "x-xenon-auth-token: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://lcm-prod-01.corp.local/lcm/authz/api/v2/users" \
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
echo '*.* @@vrli-prod-01.corp.local:514' > /etc/rsyslog.d/lcm-remote.conf
systemctl restart rsyslog
```
