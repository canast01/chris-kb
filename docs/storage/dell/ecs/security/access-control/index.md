# Dell ECS — Access Control

## RBAC

ECS implements role-based access at two levels: system management and object (data) access.

### System Management Roles

| Role | Scope | Permissions |
|---|---|---|
| System Admin | Global | Full system configuration, hardware management, VDC management |
| System Monitor | Global | Read-only access to system health, capacity, and alerts |
| Namespace Admin | Namespace | Create and manage buckets, IAM users, and lifecycle policies within the namespace |
| Namespace User | Namespace | Read-only namespace management; cannot create or delete buckets |

### Object (Data) Access via IAM Policies

ECS supports S3-style IAM bucket policies and object ACLs. Best practices:

- Grant the minimum required S3 actions (`s3:GetObject`, `s3:PutObject`) per application
- Do not use wildcard (`*`) actions on production buckets
- Prefer bucket policies over ACLs for maintainability
- Create one IAM object user per application or service; do not share credentials

## Compliance

| Framework | Relevant ECS Capability |
|---|---|
| WORM / SEC 17a-4 | S3 Object Lock in Compliance mode; immutable retention enforced at object level |
| GDPR | Object-level deletion capability; namespace-scoped data residency via VDC assignment |
| PCI DSS | Encryption at rest and in transit; audit logging; IAM least-privilege enforcement |
| HIPAA | Encryption at rest; access logging; RBAC namespace isolation |

For compliance deployments, always use Compliance mode Object Lock (not Governance mode) — Governance mode can be overridden by a privileged user.
