# Key Management


<div class="kb-summary">
Cryptographic key lifecycle management — generation, storage, distribution, rotation, and revocation.
</div>

## Key Types and Storage

| Key Type | Storage | Rotation |
|---|---|---|
| Root CA private key | Air-gapped HSM | On CA renewal (~10 years) |
| Issuing CA private key | HSM (networked) | On CA renewal (~5 years) |
| TLS/server certificates | Venafi / cert store | Annually |
| Symmetric data encryption keys | KMS (AWS/Azure) | Annually or on incident |
| Backup encryption keys | Offline + KMS | Annually |
| Service account API keys | CyberArk / Secrets Manager | 90 days |

## AWS KMS Key Lifecycle

```bash
# Create a key
aws kms create-key --description "prod-data-key" --key-usage ENCRYPT_DECRYPT

# Enable automatic rotation (annual, symmetric only)
aws kms enable-key-rotation --key-id <key-id>

# Check rotation status
aws kms get-key-rotation-status --key-id <key-id>

# Schedule deletion (7–30 day waiting period)
aws kms schedule-key-deletion --key-id <key-id> --pending-window-in-days 30

# Cancel deletion
aws kms cancel-key-deletion --key-id <key-id>
```text
┌────────────────────────────────── Data Protection — Key Management ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Key management: generate, store, rotate, and retire encryption keys securely         │   │
│   │             Envelope encryption: DEK encrypts data; KEK (in KMS/HSM) wraps the DEK            │   │
│   │          Rotation: annual minimum; immediate on suspected compromise; automate in KMS         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Key Lifecycle                 │  │               HSM & Cloud KMS               │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           1. Generate (KMS or HSM)           │  │           AWS KMS: CMK / data keys          │   │
│   │           2. Activate + distribute           │  │        Azure Key Vault: keys/secrets        │   │
│   │            3. Rotate on schedule             │  │         HashiCorp Vault: transit eng        │   │
│   │           4. Revoke on compromise            │  │          BYOK: import customer key          │   │
│   │           5. Archive then destroy            │  │           HSM: FIPS 140-2 Level 3           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DEK          = Data Encryption Key; AES-256 key that encrypts actual data blocks                   │
│    KEK          = Key Encryption Key; wraps the DEK; stored in HSM or KMS; not exported               │
│    Envelope enc = Encrypt DEK with KEK; only KEK needs HSM protection; scales efficiently             │
│    CMK          = Customer Master Key (AWS); top-level KMS key used to derive data keys               │
│    BYOK         = Bring Your Own Key; customer generates key material and imports to cloud KMS        │
│    FIPS 140-2   = US standard for cryptographic module security; Level 3 = HSM tamper-evident         │
│    Key rotation = Generate new key version; re-encrypt new data; retain old to decrypt existing       │
│    Transit eng  = Vault secrets engine; encrypts/decrypts via API without exposing key material       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## ONTAP Key Manager

```bash
# Check key manager status
security key-manager show

# Query encryption keys
security key-manager key query

# Check volume encryption state
volume show -fields encryption-state
```

## Key Management Checklist

- [ ] All production keys stored in approved KMS/HSM — no plaintext keys in config files
- [ ] Rotation schedule confirmed for all key types
- [ ] Key backup tested and verifiable
- [ ] Access to key management restricted to named administrators
- [ ] Audit log for key operations forwarded to SIEM
- [ ] Key inventory reviewed quarterly
