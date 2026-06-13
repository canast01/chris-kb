---
tags:
  - san
  - security
---
# Brocade SANnav — Authentication

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
```text
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

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

