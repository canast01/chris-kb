# Pure FlashBlade Security

## Hardening Checklist

- Disable unused data protocols — if the array only serves S3, disable NFS and SMB in the Purity//FB protocol configuration to reduce attack surface
- Enforce HTTPS for all management access; confirm HTTP redirect is disabled in the array management settings
- Rotate API tokens for all service accounts on a defined schedule (90 days recommended); revoke tokens for departed staff immediately
- Disable or rename default local accounts; all operational access should use named accounts or SSO/SAML integration
- Restrict management network access to a dedicated out-of-band management VLAN; do not expose the management interface on data networks
- Enable SafeMode for snapshots where supported — requires Pure Support to modify or destroy protected snapshots, protecting against ransomware
- Review and restrict S3 bucket policies to minimum required permissions; avoid wildcard (`*`) principal grants on production buckets
- Confirm NFS exports are restricted to specific client IP ranges or subnets; avoid exporting with `*` (all hosts) in production

## RBAC

Purity//FB uses role-based access control with the following built-in roles:

| Role | Permissions | Use Case |
|---|---|---|
| `array_admin` | Full administrative access including system configuration, user management, and protocol settings | Array administrators responsible for full platform management |
| `storage_admin` | Manage filesystems, buckets, snapshots, and replication; cannot modify system or user configuration | Storage operations team creating and managing data resources |
| `ops_admin` | Read access plus ability to acknowledge and resolve alerts; cannot modify configuration | Operations centre staff performing monitoring and alert response |
| `readonly` | Read-only access to all configuration and status information | Auditors, capacity planners, and monitoring integrations |

To list current user accounts and roles:

```bash
purefb user list
```

SAML 2.0 SSO integration is supported for mapping IdP groups to Purity roles. Configure under **Settings > Access > SSO** in the Purity//FB GUI.

## Encryption

**Data at Rest**

All data written to FlashBlade drives is encrypted using XTS-AES-256. Encryption is always on and cannot be disabled. Drives are self-encrypting; when a drive is removed or replaced, data is cryptographically erased by destroying the drive encryption key.

**Data in Flight — NFS**

NFS v4.1 Kerberos authentication modes supported:

- `krb5` — authentication only
- `krb5i` — authentication + integrity
- `krb5p` — authentication + integrity + privacy (full encryption)

Configure Kerberos in the NFS export policy to enforce encrypted NFS sessions. Requires an Active Directory or MIT Kerberos KDC.

**Data in Flight — SMB**

SMB encryption (AES-128-CCM or AES-256-GCM) is configurable per share. Enable SMB encryption to protect data in transit between Windows clients and FlashBlade:

```bash
purefb smb-share update --smb-encryption-mode required <sharename>
```

**Data in Flight — Management and S3**

All management API and GUI traffic uses TLS 1.2 or higher. S3 data plane also uses TLS; configure clients to require HTTPS endpoints and reject HTTP.

## Audit Logging

Purity//FB records an audit log entry for every administrative action performed via GUI, CLI, or REST API, including the username, source IP, timestamp, and the specific action taken.

Forward audit logs to a SIEM or syslog server:

```bash
purearray syslog add --uri udp://siem:514
```

For TLS-encrypted syslog:

```bash
purearray syslog add --uri tls://siem:6514
```

Verify syslog configuration:

```bash
purearray syslog list
```

Audit log entries are also available in the Purity//FB GUI under **Settings > Audit Log**. Ensure logs are forwarded off-array so they cannot be tampered with by an attacker with array access.

## Compliance Notes

**FIPS 140-2**

FlashBlade encryption modules are FIPS 140-2 validated. This satisfies encryption requirements for frameworks requiring FIPS-validated cryptography.

**Relevant Frameworks**

| Framework | Relevant Controls |
|---|---|
| SOC 2 Type II | CC6 (logical and physical access), CC7 (system operations including monitoring and audit logging) |
| ISO 27001 | A.10 (cryptography), A.12 (operations security including logging), A.9 (access control) |
| PCI DSS | Requirement 3 (protect stored data), Requirement 8 (identify and authenticate access), Requirement 10 (track and monitor access) |
| HIPAA | §164.312(a)(2)(iv) encryption/decryption, §164.312(b) audit controls |

Maintain evidence of FIPS-validated encryption, RBAC configuration, syslog forwarding, and snapshot protection for audit purposes. Pure1 can generate health and configuration reports to support compliance documentation.
