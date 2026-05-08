# FlashArray — Hardening

> Security baselines and compliance configuration.

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
