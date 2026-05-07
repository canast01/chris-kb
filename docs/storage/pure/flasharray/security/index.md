# FlashArray Security
## Hardening Checklist

Apply the following in order on every new FlashArray before it enters production:

1. **Change default credentials** — disable or change the default `pureuser` local account; create named admin accounts with role-based access
2. **Configure AD/LDAP authentication** — join to Active Directory or configure LDAP; map AD groups to Purity roles; remove shared local accounts after validation
3. **Enforce MFA** — use SAML SSO with an IdP that enforces MFA (Okta, Azure AD); SAML integration available on Purity//FA 6.x+
4. **Restrict management access by IP** — configure management network ACLs at the network layer to restrict SSH and HTTPS access to admin jump hosts only
5. **Enable TLS on management interface** — install a certificate from an internal CA or public CA; do not use self-signed certificates in production (`purearray setattr --tls-certificate`)
6. **Disable unused protocols** — disable iSCSI if only FC is in use; disable SNMPv1/v2 if SNMPv3 is configured
7. **Configure SNMPv3** — use SNMPv3 with authPriv security level (SHA authentication, AES encryption); disable SNMPv1 and SNMPv2c
8. **Enable SafeMode** — contact Pure Support to enable SafeMode (immutable snapshots); SafeMode prevents snapshot deletion even by array admins without a dual-approval process
9. **Enable encryption at rest** — NVMe drives on //X series use hardware-based self-encrypting drives (SEDs); verify encryption is active with `purearray list --encryption`
10. **Configure TLS for replication** — verify replication traffic is encrypted in transit; Purity uses TLS for all inter-array replication by default
11. **Enable audit logging** — configure syslog forwarding to a SIEM so all admin actions are logged externally and cannot be tampered with on the array
12. **Set session timeout** — configure CLI and GUI session timeout to 15 minutes or less
13. **Review and disable unused API tokens** — audit service account API tokens quarterly; disable any that are unused
14. **Configure SMTP alert encryption** — use STARTTLS or SSL/TLS when configuring the SMTP relay for alert emails

## RBAC

Purity//FA uses a fixed set of built-in roles. Custom roles are not supported — map AD groups to these roles based on the principle of least privilege.

| Role | Permissions | Use Case |
|---|---|---|
| `array_admin` | Full read/write access to all array configuration, user management, and data operations | Storage team leads; break-glass admin accounts |
| `storage_admin` | Read/write access to volumes, hosts, host groups, protection groups, and snapshots; cannot modify array-level configuration or user accounts | Storage administrators performing day-to-day provisioning |
| `ops_admin` | Read/write access to operational tasks (start/stop replication, acknowledge alerts, run diagnostics); cannot modify provisioning or array config | Operations team; on-call engineers |
| `readonly` | Read-only access to all array data and configuration; no ability to make changes | Monitoring integrations; audit accounts; read-only access for application teams |

**Assigning roles:**

```bash
# Assign a local account to a role
pureadmin setattr --role storage_admin <username>

# Map an AD group to a role
pureadmin setattr --role ops_admin --group "CN=pure-ops,OU=Groups,DC=example,DC=com"

# List all admin accounts and their roles
pureadmin list
```

## Encryption

**Encryption at rest:**

- FlashArray //X and //C series use NVMe Self-Encrypting Drives (SEDs) with hardware AES-256 encryption
- Encryption is always-on and requires no configuration; drive data is unreadable without the Purity-managed encryption keys
- Verify encryption status: `purearray list --encryption`
- Key management: Purity manages drive encryption keys internally; external KMIP key manager integration is supported on Purity//FA 6.x for organisations requiring external key custody (e.g., for FIPS or compliance requirements)

**Encryption in flight:**

- All management traffic (HTTPS, REST API) uses TLS 1.2 or 1.3; configure a trusted certificate (`purearray setattr --tls-certificate`)
- Replication traffic between FlashArray arrays uses TLS encryption by default
- iSCSI data traffic is not encrypted by Purity — use IPsec at the network layer if encryption of iSCSI data-in-transit is required
- FC and NVMe/FC data traffic encryption is handled at the fabric layer (FC-SP-2 / link encryption on compatible HBAs and switches)

## Audit Logging

Purity//FA logs all administrative actions including logins, configuration changes, volume operations, and snapshot management.

**What is logged:**
- All CLI and GUI login/logout events (success and failure)
- All configuration changes with the admin account name and timestamp
- All data operations (volume create/delete/connect, snapshot create/delete, replication changes)
- API token creation and deletion
- Failed authentication attempts

**Syslog forwarding:**

```bash
# Add a syslog server
puresyslog create --uri udp://<syslog_ip>:514 <syslog_name>
# Or for TLS syslog
puresyslog create --uri tls://<syslog_ip>:6514 <syslog_name>

# List configured syslog destinations
puresyslog list
```

**View audit log directly on the array:**

```bash
pureadmin list --audit
```

## Compliance Notes

| Framework | Relevant Controls |
|---|---|
| **FIPS 140-2** | FlashArray //X supports FIPS 140-2 Level 2 validated cryptographic modules; confirm with Pure account team for specific model certification status |
| **PCI DSS** | Encryption at rest (Req. 3.5), TLS in transit (Req. 4.2), access control RBAC (Req. 7), audit logging (Req. 10), vulnerability management via Purity patches (Req. 6) |
| **ISO 27001** | Supported by access control policies (RBAC), encryption at rest and in transit, audit logging, and SafeMode for data integrity |
| **SOC 2 Type II** | Pure1 and the Evergreen//One service operate under SOC 2 Type II; on-premises array controls must be implemented per this document |
| **HIPAA** | Encryption at rest and in transit, audit logging, and access control satisfy the primary technical safeguard requirements for PHI stored on FlashArray |
| **NIS2 / DORA** | Audit trail, encryption, and availability controls (ActiveCluster) support NIS2 and DORA operational resilience requirements |
