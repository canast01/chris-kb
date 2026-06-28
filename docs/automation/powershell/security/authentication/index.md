---
tags:
  - powershell
  - security
---
# PowerShell — Authentication

<div class="kb-summary">
PowerShell authentication: credential objects, `Get-Credential`, service account management, certificate-based auth, and `-UseDefaultCredentials` with Kerberos.

*Applies to: PowerShell 7.x*
</div>

---

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "PowerShell" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

note over SVC
  PowerShell Credential Storage and Flow
  Authentication Reference
end note

@enduml
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## PowerShell Credential Storage and Flow

```mermaid
graph TD
    interactiveUser["Interactive Session\n(user present)"]
    scheduledJob["Scheduled Task\n(unattended)"]
    prodScript["Production Script\n(enterprise)"]

    getCredential["Get-Credential\n(prompt user)"]
    exportClixml["Export-Clixml\n(DPAPI encrypted .xml)"]
    importClixml["Import-Clixml\n(decrypt on same machine)"]
    secretMgmt["SecretManagement\n(Set-Secret / Get-Secret)"]
    azKeyVault["Azure Key Vault\n(cross-machine)"]

    psCred["PSCredential object\n($cred)"]
    cmdlet["Cmdlet\n(Connect-VIServer,\nInvoke-Command...)"]

    interactiveUser --> getCredential
    scheduledJob --> importClixml
    exportClixml --> importClixml
    prodScript --> secretMgmt
    prodScript --> azKeyVault

    getCredential --> psCred
    importClixml --> psCred
    secretMgmt --> psCred
    azKeyVault --> psCred
    psCred --> cmdlet
```

## Authentication Reference

| Method | Encryption | Portability | Best for |
|---|---|---|---|
| `Get-Credential` | In-memory only | None | Interactive scripts |
| `Export-Clixml` | DPAPI (user-bound) | Same user/machine | Scheduled tasks |
| SecretManagement | Vault-dependent | Configurable | Production scripts |
| Azure Key Vault | AES-256 | Cross-machine | Enterprise / cloud |

---

## See also

- [PowerShell — Access Control](../access-control/)
- [PowerShell — Hardening](../hardening/)
- [PowerShell — Encryption](../encryption/)
