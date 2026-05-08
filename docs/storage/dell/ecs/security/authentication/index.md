# Dell ECS — Authentication

## Local Accounts

ECS provides built-in local management accounts:

- **sysadmin**: Default system administrator account. Change the default password immediately after deployment and restrict use to break-glass scenarios only.
- **Management service accounts**: Create named service accounts (e.g., `svc-ecs-mgmt`) for automation and API access. Do not use `sysadmin` in automation scripts.

## LDAP / Active Directory

ECS can delegate IAM user authentication to an external LDAP or Active Directory service for namespace-level access. Configure under ECS Portal → Namespace → Edit → Authentication Domain.

- Object users with S3 access keys always authenticate locally — LDAP integration applies to management console users only
- LDAP is configured per namespace; multiple namespaces can reference different LDAP domains
- Supported protocols: LDAP (TCP 389) and LDAPS (TCP 636)

**Configuration steps:**
1. Navigate to ECS Portal → Namespace → Edit → Authentication Domain
2. Enter the LDAP server address, base DN, and bind credentials
3. Map LDAP groups to ECS namespace roles (Namespace Admin, Namespace User)
4. Test authentication before saving

## S3 Object User Authentication

S3 access to ECS is authenticated using access key / secret key pairs (IAM-style):

- Object users and their keys are managed per namespace in ECS Portal → Namespace → IAM Users
- Each application or service should have its own dedicated object user
- Secret keys are shown only once at creation; store securely in a secrets manager
- Rotate secret keys every 12 months per policy

## Audit Logging

ECS generates audit logs for all administrative actions (namespace/bucket create/modify/delete, IAM changes) and optionally for object access.

- **Management audit log**: ECS Portal → Monitoring → Audit — export for compliance reviews
- **Access log**: Enable per-bucket via ECS Portal → Buckets → Edit → Access Logging; logs are written to a designated audit bucket
- **Syslog forwarding**: Configure in ECS Portal → Settings → Syslog; forward to a SIEM for real-time alerting on privileged actions
- Retain access logs per the organisation's data retention policy; ECS does not enforce audit log retention itself
