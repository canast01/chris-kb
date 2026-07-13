---
tags:
  - powershell
  - security
description: "PowerShell encryption: ConvertTo-SecureString, New-SelfSignedCertificate, encrypting credential exports, and SecretManagement module for vault integration."
---
# PowerShell — Encryption

<div class="kb-summary">
PowerShell encryption: `ConvertTo-SecureString`, `New-SelfSignedCertificate`, encrypting credential exports, and SecretManagement module for vault integration.

*Applies to: PowerShell 7.x*
</div>

---

```d2
direction: down

powershell_encryption_and_secure_com: "PowerShell Encryption and Secure Communication" {shape: rectangle}
encryption_reference: "Encryption Reference" {shape: rectangle}

powershell_encryption_and_secure_com -> encryption_reference: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## PowerShell Encryption and Secure Communication

```d2
direction: right

plainText: "Plaintext Password\n/ API Key" {shape: rectangle}
secureString: "SecureString\n(in-memory, encrypted" {shape: rectangle}
dpapi: "ConvertFrom-SecureString\n(DPAPI encrypted string" {shape: rectangle}
diskFile: "Encrypted file\n(api-key.txt" {shape: rectangle}
clixml: "Export-Clixml\n(PSCredential .xml" {shape: rectangle}
winrmHTTPS: "WinRM HTTPS\n(port 5986" {shape: rectangle}
remoteSession: "Remote PSSession\n(encrypted channel" {shape: rectangle}

plainText -> secureString
secureString -> dpapi
dpapi -> diskFile
diskFile -> secureString
secureString -> clixml
clixml -> secureString
secureString -> winrmHTTPS
winrmHTTPS -> remoteSession
```

## Encryption Reference

| Technique | Scope | Use case |
|---|---|---|
| `SecureString` | In-memory | Pass passwords to cmdlets |
| DPAPI / `ConvertFrom-SecureString` | Current user + machine | Store encrypted values on disk |
| `Export-Clixml` | Current user + machine | Serialize full `PSCredential` objects |
| WinRM over HTTPS (port 5986) | In-transit | Secure remote sessions |
| Azure Key Vault + SecretManagement | Cross-machine | Enterprise secret storage |

---

## See also

- [PowerShell — Hardening](../hardening/)
- [PowerShell — Authentication](../authentication/)
- [PowerShell — Access Control](../access-control/)
