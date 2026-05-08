# Commvault — Access Control

## RBAC Roles

CommVault roles are assigned through User Groups scoped to specific Client Groups, Storage Policies, or Subclients:

| Role | Capabilities |
|---|---|
| Master | Full CommCell administration |
| Tenant Admin | Manage users and jobs within assigned tenant |
| Operator | Start/stop jobs; no configuration changes |
| End User | Self-service restore of own data only |
| View Only | Read-only — view jobs and configuration |

Assign roles in Command Center: Manage → Security → User Groups.

**Never share admin accounts** — create individual named accounts for each operator; map AD groups to CommVault roles.

## Audit Trail

```powershell
# View CommVault audit log
qoperation execscript -sn GetAuditLog -si starttime=<timestamp>
```

Forward audit logs to SIEM via syslog:
- Command Center: Manage → Alerts → configure syslog destination
- Alert on: admin account creation, policy modifications, job deletion, encryption key access
