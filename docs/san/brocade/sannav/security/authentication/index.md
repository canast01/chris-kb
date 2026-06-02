# SANnav — Authentication


<div class="kb-summary">
> Part of the [SANnav](../../index.md) reference.
</div>

---

## Overview

SANnav supports three authentication methods: local accounts, LDAP/Active Directory, and (in newer versions) SAML-based SSO. Production environments should use LDAP or SSO for all user accounts, reserving local accounts as break-glass only.

---

## 1. Local Accounts

Local accounts are stored in the SANnav PostgreSQL database. Manage under **Administration > User Management > Local Users**.

### Creating a Local Account

1. Navigate to **Administration > User Management > Local Users > New User**.
2. Enter username, full name, and email address.
3. Set a strong initial password (meet SANnav's password policy: minimum 12 characters, upper/lower/number/special).
4. Assign a role (see [Access Control](../access-control/index.md)).
5. Click **Save**.

### Password Policy Configuration

Navigate to **Administration > Security Settings > Password Policy**:

| Setting | Recommended Value |
|---|---|
| Minimum length | 12 |
| Require uppercase | Yes |
| Require lowercase | Yes |
| Require numbers | Yes |
| Require special characters | Yes |
| Maximum age (days) | 90 |
| Password history | 12 (cannot reuse last 12) |
| Account lockout threshold | 5 failed attempts |
| Lockout duration (minutes) | 30 |

### Break-Glass Account

Maintain exactly one local admin account as break-glass for when LDAP is unavailable:
- Username: `admin` or `sannav-breakglass`
- Password: stored in vault (e.g., HashiCorp Vault, CyberArk), not known to individual engineers
- Rotate quarterly
- All use must be logged (audited in SANnav audit trail)

---

## 2. LDAP / Active Directory Integration

Configure under **Administration > Server Settings > LDAP**.

### Configuration Parameters

| Parameter | Value |
|---|---|
| Authentication type | LDAP |
| Server hostname | `ldap.corp.example.com` |
| Port | 636 (LDAPS, preferred) |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=sannav-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| User search base | `OU=SAN-Users,DC=corp,DC=example,DC=com` |
| User search attribute | `sAMAccountName` |
| Group search base | `OU=SAN-Groups,DC=corp,DC=example,DC=com` |
| Group member attribute | `member` |
| Follow referrals | Disabled (for single-domain environments) |

### LDAPS Certificate Trust

If the LDAP server uses a self-signed or internal CA certificate, import the CA certificate into SANnav:

```bash
# Copy CA cert to SANnav appliance
scp corp-ca.crt admin@sannav-dc1.corp.example.com:/tmp/

# SSH to appliance and import
ssh admin@sannav-dc1.corp.example.com

# Import CA certificate into Java truststore used by SANnav
sudo keytool -import -trustcacerts -alias corp-ldap-ca \
  -file /tmp/corp-ca.crt \
  -keystore /opt/sannav/jre/lib/security/cacerts \
  -storepass changeit -noprompt

# Restart SANnav to pick up new truststore
sudo sannav restart
```
```
┌─────────────────────────────────── Brocade SANnav — Authentication ───────────────────────────────────┐
│                                                                                                       │
│  SANnav auth: TACACS+/LDAP for GUI, REST API tokens, MFA via SSO, local fallback.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              GUI Authentication              │  │              API Authentication             │   │
│   │         TACACS+: primary auth method         │  │           POST /api/v1/login → JWT          │   │
│   │          LDAP: AD group-to-role map          │  │          Token expiry: configurable         │   │
│   │         SAML 2.0 SSO: IdP-initiated          │  │         HTTPS: TLS 1.2/1.3 required         │   │
│   │         Local: last-resort fallback          │  │         API key: long-lived service         │   │
│   │         Session timeout: 30 min idle         │  │          Rate limiting: brute-force         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  TACACS+/LDAP for human login; JWT tokens for automation; local only as break-glass.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Audit & Session Control            │  │           Switch Auth (via SANnav)          │   │
│   │         All logins logged: user+time         │  │          FOS auth: per-switch creds         │   │
│   │        Failed logins: alert threshold        │  │         SNMPv3: auth + privacy mode         │   │
│   │         Concurrent sessions: limited         │  │         SANnav proxies zone changes         │   │
│   │        Action audit: all GUI changes         │  │         Switch TACACS+ separate cfg         │   │
│   │         Export audit to SIEM/syslog          │  │         Credential vault: HashiCorp         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · TACACS+ server · LDAP/AD · IdP for SAML · Brocade FC switch management                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TACACS+         = Terminal Access Controller; centralized CLI + GUI auth for SANnav                  │
│  LDAP            = Lightweight Directory Access Protocol; AD group to SANnav role map                 │
│  SAML 2.0        = Security Assertion Markup Language; IdP-initiated SSO for SANnav                   │
│  JWT             = JSON Web Token; bearer token returned on REST API login                            │
│  API key         = long-lived service account token for non-interactive automation                    │
│  Session timeout = idle session expired after 30 minutes by default; configurable                     │
│  Rate limiting   = SANnav blocks repeated failed login attempts to prevent brute-force                │
│  Action audit    = every GUI/API change logged with user, timestamp, and action                       │
│  SIEM export     = SANnav audit log sent to Splunk/QRadar via syslog/webhook                          │
│  SNMPv3          = SNMP v3 auth+privacy used for switch polling from SANnav                           │
│  HashiCorp Vault = credential vault; stores SANnav switch passwords for automation                    │
│  Break-glass     = local admin account used only when TACACS+ is unreachable                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Track certificate expiry; renew at least 30 days before expiry. SANnav will issue a warning alert when the certificate is within the warning threshold if certificate monitoring is enabled.
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
