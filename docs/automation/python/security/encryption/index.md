# Python Automation — Encryption


<div class="kb-summary">
Encryption reference covering Secrets and Encryption Architecture, Encrypting Local Files with cryptography, Encryption Reference.
</div>

## Secrets and Encryption Architecture

```mermaid
graph TD
    script["Python Script"]
    envVars["Environment Variables\n(os.environ)"]
    awsSM["AWS Secrets Manager\n(boto3 client)"]
    hashiVault["HashiCorp Vault\n(hvac client)"]
    secret["Secret Value\n(password / token)"]
    fernet["Fernet Encryption\n(cryptography library)"]
    encFile["Encrypted File\n(.enc)"]
    tlsVerify["TLS Verification\n(requests verify=True)"]
    apiCall["API Call\n(HTTPS)"]

    script --> envVars
    script --> awsSM
    script --> hashiVault
    envVars --> secret
    awsSM --> secret
    hashiVault --> secret
    secret --> fernet
    fernet --> encFile
    script --> tlsVerify
    tlsVerify --> apiCall
```text
┌───────────────────────────────────────── Python — Encryption ─────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Python encryption: cryptography library for AES/RSA; TLS via ssl/requests; key management   │   │
│   │     Use: cryptography library (PyCA); avoid: pycrypto (unmaintained), roll-your-own crypto    │   │
│   │     Transport: requests library uses SSL by default; verify=True (default) validates certs    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Encryption Patterns              │  │                Key Management               │   │
│   │        Fernet: symmetric AES-128-CBC         │  │        AWS KMS: boto3 encrypt/decrypt       │   │
│   │        RSA: asymmetric (sign/verify)         │  │             Azure Key Vault: SDK            │   │
│   │           PBKDF2: password hashing           │  │        HashiCorp Vault: hvac library        │   │
│   │        hashlib: sha256/sha512 digests        │  │        Never store key in code or git       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Fernet       = symmetric auth encryption; from cryptography.fernet import Fernet       │   │
│   │        hvac         = HashiCorp Vault Python client; read secrets, write, authenticate        │   │
│   │           verify=False = requests flag to skip TLS verification; NEVER in production          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
