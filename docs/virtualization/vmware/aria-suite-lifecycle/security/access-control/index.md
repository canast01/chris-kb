# Aria Suite Lifecycle — Access Control

## RBAC

LCM roles are assigned via Workspace ONE Access (VIDM) groups — never assign to individual accounts:

| Role | Capabilities |
|---|---|
| LCM Admin | Full access: deploy products, run upgrades, manage Locker |
| LCM Content Developer | Read-only + content library (package management); no upgrades |
| Viewer | Read-only dashboard access |

Configure RBAC:
1. LCM → Settings → Access Control → Add Role Assignment
2. Select role → assign to AD group (synced via VIDM)
