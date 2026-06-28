---
tags:
  - commvault
  - security
---
# Commvault — Authentication


<div class="kb-summary">
Authentication reference covering Two-Factor Authentication, CyberArk Integration, Related Reference.

*Applies to: Commvault 2024.x*
</div>
![Commvault — Authentication](../../../../assets/backup-commvault-security-authentication-index.svg)



```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "Commvault" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

note over SVC
  Two-Factor Authentication
  CyberArk Integration
  Related Reference
end note

@enduml
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Two-Factor Authentication

Enable 2FA for Command Center:
- Manage → Security → Identity Providers → configure SAML or TOTP
- Require MFA for all admin-level accounts
- Exempt automated service accounts (use dedicated service account with IP restriction instead)

## CyberArk Integration

CommVault supports CyberArk Central Credential Provider (CCP) for runtime password retrieval:

1. Command Center: Manage → Security → Credential Manager
2. Add credential → select CyberArk CCP as vault type
3. Configure: CCP URL, app ID, safe name, object name

Service account passwords never stored in CommVault config — retrieved from CyberArk at job runtime.
---

## Related Reference

- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements

---

## See also

- [Commvault — Access Control](../access-control/)
- [Commvault — Hardening](../hardening/)
- [Commvault — Encryption](../encryption/)
