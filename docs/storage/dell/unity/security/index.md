# Dell Unity Security
## Hardening

Apply the following hardening steps on all Unity deployments:

- **Change the default admin password** on first login. Use a password meeting your organisation's complexity policy and store it in your secrets manager.
- **Enforce TLS 1.2 or higher**: disable TLS 1.0 and 1.1 in Unisphere under **Settings > Security > TLS**.
- **Disable unused management protocols**: disable FTP and Telnet on management interfaces if they are not required. Unisphere and `uemcli` over HTTPS/SSH are sufficient for all management tasks.
- **Restrict management access**: configure management access control to allow only known management subnets. In Unisphere, restrict allowed IP ranges under **Settings > Access > Management Interfaces**.
- **Enable SupportAssist**: required for proactive support and CloudIQ telemetry, and does not expose management access to Dell.
- **Disable unused SP ports**: if specific FC or iSCSI host ports are unused, consider disabling them to reduce the attack surface.

## RBAC

Unisphere for Unity provides role-based access control for all administrative operations.

| Role | Permissions |
|---|---|
| Administrator | Full system access: storage provisioning, system configuration, user management, upgrades |
| Storage Administrator | Storage provisioning operations: create and manage pools, LUNs, filesystems, snapshots, replication |
| Operator | Read access plus limited operational actions: acknowledge alerts, collect service bundles |
| Viewer | Read-only: view health, capacity, configuration; cannot make any changes |

Configure users and role assignments in Unisphere under **Settings > Access > Users**. Use LDAP/AD group-to-role mapping to manage Unisphere access via your directory service rather than managing local accounts individually.

## Encryption

| Layer | Method | Notes |
|---|---|---|
| Data at Rest (D@RE) | AES-256 self-encrypting drives | Enabled at pool creation on capable hardware; cannot be enabled on an existing unencrypted pool without data migration |
| External Key Management | KMIP protocol to an external KMS (Thales, Vormetric, SafeNet) | Configure KMIP in Unisphere under Settings > Encryption; recommended for compliance environments |
| Data in Transit (management) | TLS 1.2+ for Unisphere GUI, REST API, and uemcli | Disable TLS 1.0/1.1; verify with `uemcli /sys/security show` |
| Data in Transit (iSCSI) | CHAP authentication for iSCSI initiator authentication | Configure CHAP per host in Unisphere > Hosts; mutual CHAP is recommended |
| Data in Transit (NFS) | Kerberos (krb5, krb5i, krb5p) for NFS v4 with AD-joined NAS servers | Configure Kerberos security mode on NFS exports requiring in-transit protection |

## Audit Logging

Unity OE records all administrative actions — login/logout, configuration changes, and alert acknowledgements — in an audit log.

**Viewing the audit log:**

In Unisphere, navigate to **System > Events** to review recent administrative events. The event log can be filtered by severity and time range.

**Syslog forwarding for SIEM integration:**

```bash
# Create a syslog destination for audit log forwarding
uemcli -d <sp_ip> -u admin -p <password> /sys/syslog create \
  -addr <syslog_server_ip> -protocol udp -port 514 -facility local0

# Confirm the syslog configuration
uemcli -d <sp_ip> -u admin -p <password> /sys/syslog show
```

Retain audit log data for a minimum of 90 days. For regulated environments (PCI DSS, SOX, HIPAA), ensure the syslog destination retains logs for the required compliance period.

## Compliance

| Standard | Unity Capability |
|---|---|
| FIPS 140-2 | Unity OE uses FIPS 140-2 validated cryptographic modules for management channel encryption |
| DISA STIG | Dell publishes Unity STIGs for DoD and regulated environments; available on DISA STIG viewer |
| PCI DSS | D@RE, TLS enforcement, audit logging, and RBAC support PCI DSS controls |
| HIPAA | Encryption at rest and in transit, access logging, and role-based access support HIPAA technical safeguards |

Verify FIPS mode status in Unisphere under **Settings > Security**. FIPS mode restricts the cipher suites available for management connections to FIPS-approved algorithms only.
