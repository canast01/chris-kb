# CyberArk — Authentication

PVWA is accessible over HTTPS only (TLS 1.2 minimum, TLS 1.3 preferred). All privileged user logons require MFA via RADIUS. LDAP/AD group membership drives safe entitlements without requiring manual PVWA user management.

| Control | Implementation |
|---|---|
| PVWA TLS | TLS 1.2+ only; valid internal CA certificate |
| MFA enforcement | RADIUS-based MFA at PVWA logon for all privileged users |
| LDAP / AD auth | PVWA authenticates against AD; group-based safe membership |
| Break-glass account | Emergency Vault Admin account in sealed safe; access via dual-control + incident ticket |

## PVWA Authentication Flow

```mermaid
sequenceDiagram
    participant user as Privileged User
    participant pvwa as PVWA
    participant ad as Active Directory
    participant mfa as Duo MFA Proxy
    participant vault as Vault

    user->>pvwa: Login (HTTPS / TLS 1.2+)
    pvwa->>ad: LDAP bind — validate credentials
    ad-->>pvwa: Auth success + group membership
    pvwa->>mfa: RADIUS challenge to user
    mfa-->>user: Push / OTP prompt
    user-->>mfa: Approve MFA
    mfa-->>pvwa: RADIUS accept
    pvwa->>vault: SDK connect — open session
    vault-->>pvwa: Session token
    pvwa-->>user: Dashboard — safe entitlements loaded
```

---

## LDAP Configuration

PVWA Administration > LDAP Integration:

```text
LDAP Host:   ldaps://dc01.corp.example.com:636
Base DN:     DC=corp,DC=example,DC=com
Bind DN:     CN=svc-cyberark-ldap,OU=Service Accounts,OU=Managed,DC=corp,DC=example,DC=com
Bind Pwd:    <managed by CyberArk itself in the Vault>
```

## MFA (RADIUS) Configuration

PVWA Administration > Authentication Methods > RADIUS:
- RADIUS server: `duo-proxy.corp.example.com` port 1812
- Shared secret: stored in CyberArk safe `CyberArk-Platform-Accounts`
- Timeout: 60 seconds
- Retries: 2
---

## Related Reference

- [Standard LDAP Integration](../../../ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
