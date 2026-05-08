# Unity — Hardening

## Hardening Checklist

Apply the following hardening steps on all Unity deployments:

- **Change the default admin password** on first login. Use a password meeting your organisation's complexity policy and store it in your secrets manager.
- **Enforce TLS 1.2 or higher**: disable TLS 1.0 and 1.1 in Unisphere under **Settings > Security > TLS**.
- **Disable unused management protocols**: disable FTP and Telnet on management interfaces if they are not required. Unisphere and `uemcli` over HTTPS/SSH are sufficient for all management tasks.
- **Restrict management access**: configure management access control to allow only known management subnets. In Unisphere, restrict allowed IP ranges under **Settings > Access > Management Interfaces**.
- **Enable SupportAssist**: required for proactive support and CloudIQ telemetry, and does not expose management access to Dell.
- **Disable unused SP ports**: if specific FC or iSCSI host ports are unused, consider disabling them to reduce the attack surface.

## Compliance Notes

| Standard | Unity Capability |
|---|---|
| FIPS 140-2 | Unity OE uses FIPS 140-2 validated cryptographic modules for management channel encryption |
| DISA STIG | Dell publishes Unity STIGs for DoD and regulated environments; available on DISA STIG viewer |
| PCI DSS | D@RE, TLS enforcement, audit logging, and RBAC support PCI DSS controls |
| HIPAA | Encryption at rest and in transit, access logging, and role-based access support HIPAA technical safeguards |

Verify FIPS mode status in Unisphere under **Settings > Security**. FIPS mode restricts the cipher suites available for management connections to FIPS-approved algorithms only.
