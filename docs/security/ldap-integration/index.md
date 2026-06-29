---
title: Standard LDAP Integration
tags:
  - security
---

# Standard LDAP Integration

<div class="kb-summary">
Canonical LDAP/Active Directory integration reference for all KB-covered products. Use this page for field definitions, security standards, and connectivity testing. Product authentication pages link here for the shared baseline and document only their product-specific steps.
</div>

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Connectivity testing, service account standards, sync troubleshooting</div>
  </a>
</div>

---

## Standard Field Reference

These fields appear in virtually every product's LDAP configuration. Values must be agreed with the AD team before deploying any integration.

| Field | Standard Value | Notes |
|---|---|---|
| LDAP URL (primary) | `ldaps://dc01.corp.local:636` | Use LDAPS — never plain LDAP in production |
| LDAP URL (secondary) | `ldaps://dc02.corp.local:636` | Always configure a secondary for resilience |
| Use SSL / TLS | Yes | Mandatory |
| Base DN | `DC=corp,DC=local` | Top-level DN for all searches |
| User DN (bind account) | `CN=svc-ldap-ro,OU=ServiceAccounts,DC=corp,DC=local` | Read-only service account — see service account standards below |
| User Search Base | `OU=Users,DC=corp,DC=local` | Scope searches to users OU only |
| Group Search Base | `OU=Groups,DC=corp,DC=local` | Scope group searches |
| Username attribute | `sAMAccountName` | Use `userPrincipalName` if cross-domain |
| Display name attribute | `displayName` | |
| Email attribute | `mail` | |
| Group member attribute | `member` | For static groups; use `memberOf` on user objects for reverse lookup |
| Synchronisation interval | 60 minutes | Incremental sync where supported; use `uSNChanged` for large directories |
| Nested groups | Enable if required | Evaluate performance impact on large directories |

---

## Service Account Standards

Every LDAP integration must use a dedicated service account, never a personal account.

| Requirement | Standard |
|---|---|
| Name | `svc-<product>-ldap` (e.g. `svc-jira-ldap`, `svc-snow-ldap`) |
| AD group | `SVC-LDAP-ReadOnly` — grants read access to Users and Groups OUs |
| Password type | Managed by CyberArk (preferred) or PAM vault — never stored in config files |
| Password rotation | Every 90 days or on personnel change |
| Account type | Non-expiring password, account never expires, cannot log on interactively |
| Permissions | Read-only on Users and Groups OUs only — no write access, no admin rights |
| Expiry audit | Review quarterly — disable if unused for 30 days |

---

## Connectivity Testing

Run before configuring any product to confirm the bind account and search base work correctly.

```bash
# Test LDAPS connectivity and bind
ldapsearch -H ldaps://dc01.corp.local:636 \
  -D "CN=svc-ldap-ro,OU=ServiceAccounts,DC=corp,DC=local" \
  -W \
  -b "DC=corp,DC=local" \
  -s sub \
  "(sAMAccountName=testuser)" \
  displayName mail memberOf

# Test TLS certificate validity
openssl s_client -connect dc01.corp.local:636 -showcerts </dev/null 2>&1 | \
  openssl x509 -noout -dates -subject -issuer

# Verify secondary DC is reachable
ldapsearch -H ldaps://dc02.corp.local:636 \
  -D "CN=svc-ldap-ro,OU=ServiceAccounts,DC=corp,DC=local" \
  -W \
  -b "DC=corp,DC=local" \
  -s base "(objectClass=*)"
```


```text title="Expected output"
Enter LDAP Password: 
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=local> with scope subtree
# filter: (sAMAccountName=testuser)
# requesting: displayName mail memberOf
#

dn: CN=testuser,OU=Users,OU=corp,DC=corp,DC=local
displayName: Test User
mail: testuser@corp.local
memberOf: CN=Engineering,OU=Groups,DC=corp,DC=local
memberOf: CN=VPN-Access,OU=Groups,DC=corp,DC=local

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1

notBefore=Jan 15 08:32:14 2024 GMT
notAfter=Jan 14 08:32:14 2026 GMT
subject=CN=dc01.corp.local,OU=Domain Controllers,DC=corp,DC=local
issuer=CN=corp-CA,OU=Certification Authorities,DC=corp,DC=local

Enter LDAP Password: 
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=local> with scope base
# filter: (objectClass=*)
# requesting: ALL
#

dn: DC=corp,DC=local
objectClass: top
objectClass: domain
dc: corp

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account is not locked; check DC event logs for failed bind attempts.
    **`ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)`** — Confirm dc01.corp.local resolves correctly, port 636 is open in firewall rules, and the DC is online using `ping` or `nslookup`.
    **`error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed`** — Add the DC's root CA certificate to the system trust store or use `ldapsearch -Z -o LDTLS_CACERT=/path/to/ca.crt` to specify the CA bundle explicitly.
---

## Synchronisation and Failover

- **Always configure both primary and secondary DCs.** Single-DC configuration causes outages during patching windows.
- **Incremental sync**: where supported, use `uSNChanged` attribute (Active Directory) to sync only changed objects. Reduces load for directories > 10,000 users.
- **Full sync schedule**: run outside business hours (e.g. 02:00). Incremental can run every 15–60 minutes.
- **Failover behaviour**: confirm with the product team whether failover is automatic or requires manual intervention on DC failure.

---

## TLS Certificate Management

| Item | Action |
|---|---|
| Certificate expiry | Alert at 60 days; renew at 30 days |
| Root CA | Import the internal CA root certificate into the product's trust store |
| Hostname validation | Ensure the LDAP URL matches the certificate SAN or CN exactly |
| Self-signed certs | Never use in production — always use CA-signed certificates |
| Certificate change | Coordinate with AD team; update all integrations before cutover |

---

## Common Issues

| Symptom | Likely Cause | Resolution |
|---|---|---|
| `LDAP: Invalid credentials` | Bind account password expired or changed | Rotate password in PAM vault, update product config |
| `SSL handshake failure` | CA certificate not trusted, or TLS version mismatch | Import CA root cert into product trust store; confirm TLS 1.2+ |
| `No such object` | Wrong Base DN or OU moved in AD | Confirm Base DN with AD team; update search base |
| Connection timeout | Port 636 blocked by firewall | Confirm firewall rules; test with `nc -zv dc01.corp.local 636` |
| Users not syncing | Incremental sync missed changes | Trigger full sync; check `uSNChanged` attribute support |
| Groups not resolving | Group search base too narrow, or nested groups not enabled | Expand group search base; enable nested group support |
| `Referral` errors | Search base set to root; DC returns referral to child domain | Set search base to specific domain DN, not bare root |

---

## Product-Specific LDAP Pages

Each product documents its exact configuration path and any non-standard field names:

- [Jira — Authentication](../../tools/jira/security/authentication/index.md)
- [Confluence — Authentication](../../tools/confluence/security/authentication/index.md)
- [ServiceNow — Authentication](../../tools/servicenow/security/authentication/index.md)
- [vCenter — Authentication](../../virtualization/vmware/vcenter/security/authentication//)
- [NSX — Authentication](../../virtualization/vmware/nsx/security/authentication//)
- [ONTAP — Authentication](../../storage/netapp/ontap/security/authentication//)
- [Veeam — Authentication](../../backup/veeam/security/authentication/index.md)

---

## Related Pages

- [Standard SAML Configuration](../saml-configuration/index.md)
- [Active Directory](../../compute/windows-server/active-directory/index.md)
- [MFA](../mfa/index.md)
- [PKI](../pki/index.md)
- [TLS and HTTPS](../../protocols/tls/index.md)
- [LDAP Protocol Reference](../../protocols/ldap/index.md)
