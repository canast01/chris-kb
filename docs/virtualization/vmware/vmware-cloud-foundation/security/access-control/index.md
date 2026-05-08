# VCF — Access Control

## SDDC Manager Roles

| Role | Access |
|---|---|
| ADMIN | Full access — lifecycle, security, credential rotation |
| OPERATOR | Day-to-day operations — health, tasks, monitoring; no credential access |
| VIEWER | Read-only dashboards and health views |

**Assign roles to AD groups:**

1. SDDC Manager → Administration → Single Sign-On → add Active Directory identity source
2. Administration → Users and Groups → assign roles to AD groups
3. Remove direct user-level assignments — group-based assignment is auditable and survives staff changes
