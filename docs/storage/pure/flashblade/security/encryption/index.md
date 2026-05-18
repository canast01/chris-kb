# FlashBlade — Encryption

```
FlashBlade Encryption Architecture
┌────────────────────────────────────────────────────────────┐
│  Data at Rest (always-on)                                  │
│  Write ──► blade NVMe drive ──► XTS-AES-256 (hardware)    │
│  Drive removed → crypto erase (DEK destroyed)              │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  Data in Transit                                           │
│  ├── NFS v4.1: Kerberos GSSAPI privacy (optional)         │
│  ├── SMB 3.0: end-to-end SMB encryption (AES-128-GCM)     │
│  ├── S3: HTTPS (TLS 1.2+)                                  │
│  ├── Management GUI/API: HTTPS (443)                       │
│  └── Replication (ActiveDR): TLS between FlashBlades      │
└────────────────────────────────────────────────────────────┘
```

> Part of the [FlashBlade Security](../) reference.

---

## Data at Rest

All data written to FlashBlade drives is encrypted using XTS-AES-256. Encryption is always on and cannot be disabled. Drives are self-encrypting; when a drive is removed or replaced, data is cryptographically erased by destroying the drive encryption key.

## Data in Flight — NFS

NFS v4.1 Kerberos authentication modes supported:

- `krb5` — authentication only
- `krb5i` — authentication + integrity
- `krb5p` — authentication + integrity + privacy (full encryption)

Configure Kerberos in the NFS export policy to enforce encrypted NFS sessions. Requires an Active Directory or MIT Kerberos KDC.

## Data in Flight — SMB

SMB encryption (AES-128-CCM or AES-256-GCM) is configurable per share. Enable SMB encryption to protect data in transit between Windows clients and FlashBlade:

```bash
purefb smb-share update --smb-encryption-mode required <sharename>
```

## Data in Flight — Management and S3

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
