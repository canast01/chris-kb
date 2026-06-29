---
tags:
  - python
  - security
---
# Python Automation — Encryption

<div class="kb-summary">
Encryption reference covering Secrets and Encryption Architecture, Encrypting Local Files with cryptography, Encryption Reference.

*Applies to: Python 3.x*
</div>

```d2
direction: down

secrets_and_encryption_architecture: "Secrets and Encryption Architecture" {shape: rectangle}
encrypting_local_files_with_cryptogr: "Encrypting Local Files with cryptography" {shape: rectangle}
encryption_reference: "Encryption Reference" {shape: rectangle}

secrets_and_encryption_architecture -> encrypting_local_files_with_cryptogr: hardens
encrypting_local_files_with_cryptogr -> encryption_reference: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Secrets and Encryption Architecture

```d2
direction: right

script: "Python Script" {shape: rectangle}
envVars: "Environment Variables\n(os.environ" {shape: rectangle}
awsSM: "AWS Secrets Manager\n(boto3 client" {shape: rectangle}
hashiVault: "HashiCorp Vault\n(hvac client" {shape: rectangle}
secret: "Secret Value\n(password / token" {shape: rectangle}
fernet: "Fernet Encryption\n(cryptography library" {shape: rectangle}
encFile: "Encrypted File\n(.enc" {shape: rectangle}
tlsVerify: "TLS Verification\n(requests verify=True" {shape: rectangle}
apiCall: "API Call\n(HTTPS" {shape: rectangle}

script -> envVars
script -> awsSM
script -> hashiVault
envVars -> secret
awsSM -> secret
hashiVault -> secret
secret -> fernet
fernet -> encFile
script -> tlsVerify
tlsVerify -> apiCall
```

## Encrypting Local Files with cryptography

```bash
pip install cryptography
```

```python
from cryptography.fernet import Fernet
import os

# Generate and store a key (store in a secrets manager, not in source code)
key = Fernet.generate_key()   # returns bytes — keep this secret

# Encrypt a file
fernet = Fernet(key)
plaintext = b"sensitive configuration data"
ciphertext = fernet.encrypt(plaintext)

with open("config.enc", "wb") as f:
    f.write(ciphertext)

# Decrypt
with open("config.enc", "rb") as f:
    ciphertext = f.read()

plaintext = fernet.decrypt(ciphertext)
```

## Encryption Reference

| Scenario | Approach |
|---|---|
| API credentials at rest | Environment variables or secrets manager |
| Credentials in CI/CD | CI/CD platform secrets (GitHub Actions secrets, GitLab CI variables) |
| File encryption | `cryptography` library with Fernet or AES-GCM |
| TLS in transit | Always `verify=True`; use custom CA bundle for internal PKI |
| SSH keys | Generate with `ssh-keygen -t ed25519`; restrict permissions with `chmod 600` |

---

## See also

- [Python — Hardening](../hardening/)
- [Python — Authentication](../authentication/)
- [Python — Access Control](../access-control/)
