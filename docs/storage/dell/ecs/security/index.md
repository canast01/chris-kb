# ECS Security
## Hardening Checklist

- [ ] Change the default `sysadmin` password immediately after initial deployment
- [ ] Replace self-signed TLS certificates on the Management API (4443) and S3 endpoint (443) with certificates signed by the corporate CA
- [ ] Disable HTTP (port 9021) in production; require HTTPS for all S3 access
- [ ] Enable TLS 1.2 minimum on all endpoints; disable TLS 1.0 and 1.1
- [ ] Create named management service accounts; disable or restrict the `sysadmin` account from use in automation
- [ ] Apply namespace quotas; do not allow namespaces with no quota in production
- [ ] Enable bucket-level access logging for namespaces with compliance or audit requirements
- [ ] Configure syslog forwarding to the SIEM for all ECS management and access events
- [ ] Enable Object Lock (WORM) on buckets designated for compliance or immutable backup data
- [ ] Restrict ECS Portal (port 443) and Management API (port 4443) access to management network VLANs via firewall rules
- [ ] Review and disable unused API protocols (Swift, Atmos, CAS) on namespaces that only require S3
- [ ] Rotate object user secret keys every 12 months and update consuming applications

## RBAC

ECS implements role-based access at two levels: system management and object (data) access.

**System Management Roles:**

| Role | Scope | Permissions |
|---|---|---|
| System Admin | Global | Full system configuration, hardware management, VDC management |
| System Monitor | Global | Read-only access to system health, capacity, and alerts |
| Namespace Admin | Namespace | Create and manage buckets, IAM users, and lifecycle policies within the namespace |
| Namespace User | Namespace | Read-only namespace management; cannot create or delete buckets |

**Object (Data) Access via IAM Policies:**

ECS supports S3-style IAM bucket policies and object ACLs. Best practices:
- Grant the minimum required S3 actions (`s3:GetObject`, `s3:PutObject`) per application
- Do not use wildcard (`*`) actions on production buckets
- Prefer bucket policies over ACLs for maintainability
- Create one IAM object user per application or service; do not share credentials

## Encryption

| Layer | Method | Notes |
|---|---|---|
| Data in transit | TLS 1.2+ | Enforced on S3 (443), Management API (4443); configure minimum TLS version in ECS Portal → Settings → Security |
| Data at rest | Software AES-256 (ECS encryption at rest) | Enable per-namespace in ECS Portal → Namespace → Edit → Encryption; key management via internal or external KMIP KMS |
| Key management | Internal ECS KMS or external KMIP server | For compliance, use an external KMIP-compatible KMS (e.g., Dell PowerProtect Data Manager, HashiCorp Vault) |

Enable encryption at rest on namespaces that hold regulated data (PCI, HIPAA, GDPR). Note that enabling encryption on an existing namespace does not retroactively encrypt already-stored objects.

## Audit Logging

ECS generates audit logs for all administrative actions (namespace/bucket create/modify/delete, IAM changes) and optionally for object access.

- **Management audit log**: ECS Portal → Monitoring → Audit — export for compliance reviews
- **Access log**: Enable per-bucket via ECS Portal → Buckets → Edit → Access Logging; logs are written to a designated audit bucket
- **Syslog forwarding**: Configure in ECS Portal → Settings → Syslog; forward to a SIEM for real-time alerting on privileged actions
- Retain access logs per the organisation's data retention policy; ECS does not enforce audit log retention itself

## Compliance

| Framework | Relevant ECS Capability |
|---|---|
| WORM / SEC 17a-4 | S3 Object Lock in Compliance mode; immutable retention enforced at object level |
| GDPR | Object-level deletion capability; namespace-scoped data residency via VDC assignment |
| PCI DSS | Encryption at rest and in transit; audit logging; IAM least-privilege enforcement |
| HIPAA | Encryption at rest; access logging; RBAC namespace isolation |

For compliance deployments, always use Compliance mode Object Lock (not Governance mode) — Governance mode can be overridden by a privileged user.
