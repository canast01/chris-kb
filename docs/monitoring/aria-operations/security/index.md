# Aria Operations Security

Aria Operations uses vCenter SSO as the identity provider, allowing centralised user management and avoiding local account sprawl. RBAC is enforced through built-in roles: Admin, Content Admin, PowerUser, and ReadOnly — role assignments should follow least-privilege principles. All management access is HTTPS-only; HTTP is disabled. API tokens should be rotated on a defined schedule (minimum every 90 days). Node OS hardening follows the VMware STIG baseline. Admin actions are captured in the audit log accessible under Admin > Audit Log.

| Role | Capabilities |
|---|---|
| Admin | Full platform administration |
| Content Admin | Manage policies, dashboards, reports |
| PowerUser | Create and edit dashboards, views |
| ReadOnly | View dashboards and alerts only |

- vCenter SSO integration for authentication
- HTTPS-only access (port 443); HTTP redirected
- API token rotation policy: every 90 days
- Node OS hardening: VMware STIG baseline
- Audit log: Admin > Audit Log (retain 12 months minimum)
