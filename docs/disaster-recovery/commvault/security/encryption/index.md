# Commvault — Encryption


<div class="kb-summary">
Encryption reference covering Backup Encryption, Linux Hardened Repository (Immutable Backups).
</div>

```
┌──────────────────────── Commvault Encryption — At Rest, In Transit, Key Mgmt ─────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Data In Transit                │  │                 Data At Rest                │   │
│   │       TLS 1.2+ between all components        │  │           AES-256 CBC or XTS mode           │   │
│   │      Certificate mutual authentication       │  │        Encryption at MediaAgent layer       │   │
│   │        CS ↔ MA: TLS tunnel port 8403         │  │      Passphrase or key file per policy      │   │
│   │          Client ↔ CS: TLS port 8400          │  │          FIPS 140-2 mode available          │   │
│   │           GUI → CS: HTTPS port 443           │  │      Cloud target: server-side encrypt      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Encryption policy set in storage policy copy; applies to all jobs using that copy                  │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                         Key Management                                        │   │
│   │          Passphrase-based: user-defined passphrase → PBKDF2 key derivation → AES-256          │   │
│   │               Key file: randomly generated 256-bit key stored in CommServe CSDB               │   │
│   │            External KMS: integration with HashiCorp Vault, AWS KMS, Azure Key Vault           │   │
│   │              Key escrow: Commvault Key Management Server stores master key backup             │   │
│   │             Key rotation: re-encrypt job triggers re-encryption of DDB and chunks             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  MA CPU: AES-NI hardware acceleration (Intel/AMD) reduces encryption overhead                         │
│  KMS: external KMS requires HTTPS 443 from CommServe; verify latency < 10ms                           │
│  FIPS mode: requires FIPS-validated crypto libraries on CommServe and MA OS                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AES-256        = Advanced Encryption Standard 256-bit; NIST-approved symmetric cipher                │
│  PBKDF2         = Password-Based Key Derivation Function 2; derives AES key from passphrase           │
│  FIPS 140-2     = US NIST standard for cryptographic module validation (Level 1 min)                  │
│  KMS            = Key Management Server; external system managing encryption keys                     │
│  AES-NI         = Intel/AMD CPU instruction set extension for hardware AES acceleration               │
│  Passphrase     = User-supplied secret used to derive per-backup encryption key                       │
│  Key Escrow     = Secure backup of encryption keys to prevent permanent data loss                     │
│  Key File       = Random binary key stored in CSDB; used instead of passphrase                        │
│  Re-Encrypt Job = CommCell job that re-encrypts backup data with a new key                            │
│  SSE            = Server-Side Encryption; cloud provider encrypts objects at rest (S3/Blob)           │
│  TLS Mutual     = Both sides present certs; prevents man-in-the-middle on backup streams              │
│  CBC / XTS      = AES block cipher modes; XTS preferred for disk/chunk encryption                     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Configure via VBR Repository settings: enable "Immutable" with retention period matching recovery requirements.
