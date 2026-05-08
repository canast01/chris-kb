# Aria Operations — Access Control

## RBAC Roles

| Role | Permissions |
|------|------------|
| Administrator | Full access — manage users, adapters, system settings |
| Content Admin | Manage dashboards, views, reports, alerts, policies |
| Operator | Acknowledge/cancel alerts, run actions; no admin access |
| Read Only | View dashboards, alerts, and metrics; no changes |

Roles are assigned in **Administration > Access Control > User Accounts** or via imported AD/LDAP groups.

## Local Admin Account Hardening

- Change the default `admin` password immediately after deployment
- Minimum 16 characters, mixed case, numbers, symbols
- Restrict local admin use — prefer AD group-based RBAC for day-to-day access
- Store the admin credential in a secrets vault
