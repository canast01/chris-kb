# Cisco DCNM — Authentication


<div class="kb-summary">
> Part of the [Cisco DCNM](../../index.md) reference.
</div>

---

## Overview

DCNM supports local accounts, LDAP/Active Directory, TACACS+, and RADIUS for user authentication. Production environments should use LDAP or TACACS+ for all named users, with local admin as break-glass only.

---

## 1. Local Accounts

Managed under **Administration > Security > Local User Management**.

### Create a Local Account

1. Navigate to **Administration > Security > Local User Management > Add User**.
2. Enter username, password, and email.
3. Assign a role (see [Access Control](../access-control/index.md)).
4. Click **Save**.

### Password Policy

Configure under **Administration > Security > Password Policy**:

| Setting | Recommended Value |
|---|---|
| Minimum length | 12 characters |
| Uppercase required | Yes |
| Lowercase required | Yes |
| Numbers required | Yes |
| Special characters required | Yes |
| Maximum age | 90 days |
| Password history | 10 |
| Account lockout after | 5 failed attempts |
| Lockout duration | 30 minutes |

---

## 2. LDAP / Active Directory

Configure under **Administration > Security > Authentication > LDAP**.

### Configuration

| Field | Value |
|---|---|
| Server | `ldap.corp.example.com` |
| Port | 636 (LDAPS) |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=dcnm-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| Bind password | Service account password |
| User attribute | `sAMAccountName` |
| Group base DN | `OU=DCNM-Groups,DC=corp,DC=example,DC=com` |
| Role attribute | `memberOf` |

### Import CA Certificate (for LDAPS)

```bash
ssh root@dcnm-dc1.corp.example.com

# Copy CA cert to DCNM
scp corp-ca.crt root@dcnm-dc1.corp.example.com:/tmp/

# Import into Java truststore
keytool -import -trustcacerts -alias corp-ldap-ca \
  -file /tmp/corp-ca.crt \
  -keystore /usr/java/default/jre/lib/security/cacerts \
  -storepass changeit -noprompt

# Restart DCNM to apply
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart
```
┌───────────────────────────────────── Cisco DCNM — Authentication ─────────────────────────────────────┐
│                                                                                                       │
│  DCNM auth: ISE TACACS+ for GUI, REST JWT, SAML SSO, local accounts as break-glass.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              GUI Authentication              │  │              API Authentication             │   │
│   │         ISE TACACS+: primary method          │  │            POST /rest/logon → JWT           │   │
│   │          LDAP: AD group-to-role map          │  │           Token expiry: 8h default          │   │
│   │         SAML 2.0 SSO: IdP-federated          │  │           HTTPS: TLS 1.2/1.3 only           │   │
│   │           Local: break-glass only            │  │            Service acct: API key            │   │
│   │          Lockout: 5 failed attempts          │  │           Rate limit: brute-force           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ISE TACACS+ for human GUI login; JWT for automation; SAML SSO integrates MFA.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Session & Audit Control            │  │           Switch Auth (DCNM-side)           │   │
│   │         All logins: user + timestamp         │  │         SSH creds stored per switch         │   │
│   │         Failed logins: alert to SIEM         │  │            NX-OS TACACS+ separate           │   │
│   │         Concurrent sessions: limited         │  │         Credential vault: HashiCorp         │   │
│   │          Action audit: all changes           │  │            SNMPv3: auth + privacy           │   │
│   │          Export audit: syslog / CSV          │  │          Rotation: quarterly creds          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · Cisco ISE · LDAP/AD · IdP for SAML · Cisco MDS switch management                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ISE TACACS+     = Cisco ISE provides TACACS+ protocol; maps to DCNM role                             │
│  LDAP            = AD group-to-DCNM role mapping via LDAP bind                                        │
│  SAML 2.0        = SSO federation; MFA enforced at identity provider level                            │
│  JWT             = JSON Web Token; bearer token returned on /rest/logon                               │
│  Service account = dedicated API user; separate credentials for automation                            │
│  Lockout         = DCNM locks account after 5 failed logins; unlock via admin                         │
│  Rate limiting   = blocks repeated failed attempts to prevent brute-force                             │
│  Session timeout = idle GUI/API session terminated after configurable period                          │
│  Action audit    = all DCNM GUI clicks and API calls logged with user/timestamp                       │
│  NX-OS TACACS+   = MDS switch CLI authentication via ISE; separate from DCNM                          │
│  HashiCorp Vault = credential vault; stores DCNM switch passwords for automation                      │
│  SNMPv3 auth     = SNMP v3 authentication (SHA); privacy (AES) for polling                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
