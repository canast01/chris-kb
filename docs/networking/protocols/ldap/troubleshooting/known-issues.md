---
tags:
  - troubleshooting
  - ldap
  - networking
  - known-issues
---
# LDAP / LDAPS — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known LDAP and LDAPS issues covering bind failures, certificate errors, and search result issues.

*Applies to: Microsoft Active Directory LDAP, OpenLDAP 2.6.x*
</div>

## Before you begin

- Test LDAP with: `ldapsearch -H ldap://<dc>:389 -x -D "user@domain.com" -W -b "dc=domain,dc=com" "(sAMAccountName=testuser)"`
- LDAPS (636) requires the LDAP client to trust the DC's certificate.
- Most LDAP failures are port (389/636), certificate trust, or bind credential issues.

## Connectivity

| Error Code | Description | Cause | Fix |
|---|---|---|---|
| `LDAP error 49` | Invalid credentials | Wrong bind DN or password | Verify bind DN format: `cn=user,dc=domain,dc=com` or `user@domain.com` |
| `LDAP error 81: Can't contact LDAP server` | Network unreachable | TCP 389 or 636 blocked | Verify port open: `nc -zv <dc> 389` |
| `Connect error: TLS handshake failure` | LDAPS cert not trusted | DC certificate not in client trust store | Add DC CA cert to client trust store; test: `openssl s_client -connect <dc>:636` |

## Search Issues

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Search returns no results despite user existing | BaseDN wrong or filter incorrect | Verify BaseDN covers user's OU; test with `(objectClass=*)` filter first |
| `Size limit exceeded` — only 1000 results | AD default page size limit | Use paged results (`--paged-results` in ldapsearch); or request all results with VLV |
| LDAP attribute missing in response | Attribute not in default return set | Explicitly request attribute in search: `ldapsearch ... sAMAccountName mail memberOf` |

## LDAPS Certificate

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| LDAPS working then breaks after DC cert renewal | New DC cert from different CA; client trust not updated | Re-export CA cert and update client trust stores | N/A |
| `certificate has expired` error | DC LDAPS certificate expired | Renew certificate on DC via ADCS; issue from internal CA | N/A |

## See also

- [LDAP — Common Issues](common-issues.md)
- [Active Directory — Known Issues](../../../compute/windows-server/active-directory/troubleshooting/known-issues/)
