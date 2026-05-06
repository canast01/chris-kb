# PowerMax Security

## Hardening Checklist

- [ ] Disable the default `smc` (array admin) local account after configuring LDAP/AD authentication
- [ ] Enforce TLS 1.2 or 1.3 for all Unisphere connections; disable TLS 1.0 and 1.1
- [ ] Replace the default Unisphere self-signed certificate with a CA-signed certificate
- [ ] Configure Unisphere session timeout (recommended: 15 minutes idle)
- [ ] Enable Solutions Enabler network daemon authentication (`/var/symapi/config/daemon_users`)
- [ ] Restrict SYMAPI daemon access to known management host IPs in `/var/symapi/config/netcnfg`
- [ ] Enable array-level audit logging and forward to a SIEM
- [ ] Ensure SRDF encryption (end-to-end) is configured for any SRDF links traversing untrusted networks
- [ ] Apply D@RE (Data at Rest Encryption) — enabled at factory; confirm encryption key manager is operational
- [ ] Review and remove any unused front-end port groups or masking views
- [ ] Confirm SupportAssist is configured with proxy restrictions to limit outbound data paths

## RBAC

Unisphere for PowerMax roles:

| Role | Permissions |
|---|---|
| `StorageAdmin` | Full read/write on storage provisioning (storage groups, masking views, pools, SnapVX, SRDF). No access to security or user management. |
| `SecurityAdmin` | Manage users, roles, certificates, and LDAP configuration. Cannot provision storage. |
| `Operator` | Read/write on routine operations (alert acknowledgement, scheduled tasks). Cannot create or delete storage objects. |
| `Monitor` | Read-only across all array objects; can view performance data. No configuration changes. |
| `StorageAdminLocal` | Same as StorageAdmin but scoped to a specific SID; used for delegating single-array management. |

Solutions Enabler CLI roles are controlled by the `daemon_users` file and OS-level permissions on the SE host. Restrict root-level SE access to operations accounts only.

## Encryption

| Layer | Mechanism | Notes |
|---|---|---|
| Data at Rest (D@RE) | AES-256; hardware-based encryption on NVMe drives | Enabled by factory default on PowerMax 2000/8000; key management via embedded EKMS or external KMIP server |
| Data in Flight (SRDF) | SRDF Encryption (AES-256 over FC or IP) | Must be explicitly enabled on RDF group; requires both arrays to be at a compatible code level |
| Management Traffic | TLS 1.2/1.3 for Unisphere REST API and HTTPS | Enforce strong ciphers; disable legacy TLS via Unisphere security settings |

For KMIP integration (external key manager such as Thales CipherTrust or Vormetric):
- Configure under Unisphere → Settings → Security → Encryption Key Management.
- Test key retrieval before placing array into production.

## Audit Logging

All configuration changes on PowerMax are logged as audit events:

```bash
# List recent audit events (last 100)
symevent -sid <SID> list -last 100

# Filter audit events for a specific user
symevent -sid <SID> list -filter "user eq <username>"

# Export audit log to file
symevent -sid <SID> list > /tmp/audit_events.txt
```

- Events include: timestamp, user, action, object type, object name, and result.
- Export audit logs to a SIEM (Splunk, QRadar, etc.) via syslog from the Unisphere host.
- Retain audit logs for a minimum of 12 months per most regulatory frameworks.

## Compliance Notes

| Framework | Relevant Control | PowerMax Capability |
|---|---|---|
| PCI-DSS | Requirement 3 (protect stored data) | D@RE with AES-256 satisfies encryption at rest requirement |
| PCI-DSS | Requirement 10 (audit logging) | Array audit events via `symevent`; forward to SIEM |
| ISO 27001 | A.8.2 (information classification) | Storage group naming and SLO policies align with data classification |
| NIST 800-53 | SC-28 (protection of information at rest) | D@RE covers this control |
| HIPAA | §164.312(a)(2)(iv) encryption | D@RE and SRDF encryption satisfy encryption obligations |

Engage the Dell Security team for a compliance readiness assessment for specific regulatory programs.
