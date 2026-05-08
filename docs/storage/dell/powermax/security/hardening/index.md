# PowerMax — Hardening

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

## Compliance Notes

| Framework | Relevant Control | PowerMax Capability |
|---|---|---|
| PCI-DSS | Requirement 3 (protect stored data) | D@RE with AES-256 satisfies encryption at rest requirement |
| PCI-DSS | Requirement 10 (audit logging) | Array audit events via `symevent`; forward to SIEM |
| ISO 27001 | A.8.2 (information classification) | Storage group naming and SLO policies align with data classification |
| NIST 800-53 | SC-28 (protection of information at rest) | D@RE covers this control |
| HIPAA | §164.312(a)(2)(iv) encryption | D@RE and SRDF encryption satisfy encryption obligations |

Engage the Dell Security team for a compliance readiness assessment for specific regulatory programs.
