# Security — Data Protection

<div class="kb-summary">
Data protection reference covering classification tiers, encryption standards, key management, governance frameworks, and data retention policy for enterprise environments.
</div>

```text
┌───────────────────────────────────── Security — Data Protection ──────────────────────────────────────┐
│                                                                                                       │
│   Five domains: classification, encryption, governance, retention policy, and key management          │
│   Classification drives handling requirements: Public → Internal → Confidential → Restricted          │
│   Encryption: TLS in-transit; AES-256 at-rest; column-level (Always Encrypted) for sensitive fields   │
│   Key management: HSM-backed KMS; 90-day rotation for data encryption keys; audit log per key op      │
│                                                                                                       │
│   Classification tiers                                                                                │
│   Public       No restrictions; approved for external sharing                                         │
│   Internal     Default for corporate data; not for public release                                     │
│   Confidential PII, financial records; need-to-know access; encrypted at rest and in transit          │
│   Restricted   Highest sensitivity; PAM-controlled access; HSM key protection; audit logging          │
│                                                                                                       │
│   Encryption standards                                                                                │
│   At-rest     AES-256; TDE for SQL databases; LUKS for Linux volumes; BitLocker for Windows           │
│   In-transit  TLS 1.2+ mandatory; TLS 1.3 preferred; certificate managed via Venafi / ADCS            │
│   Column-level Always Encrypted for PII fields; key never leaves client; SQL sees ciphertext          │
│                                                                                                       │
│   Key management                                                                                      │
│   KMS          HashiCorp Vault or Azure Key Vault; key hierarchy: master key → data encryption key    │
│   HSM          Hardware Security Module for master key protection; FIPS 140-2 Level 3                 │
│   Rotation     Data encryption keys: 90 days; master keys: annual; rotation logged in audit trail     │
│                                                                                                       │
│   Key terms:                                                                                          │
│   TDE          = Transparent Data Encryption; encrypts .mdf/.ldf files and backups at rest            │
│   Always Encrypted = column encryption where key never leaves the client application                  │
│   LUKS         = Linux Unified Key Setup; standard for Linux full-disk encryption                     │
│   HSM          = Hardware Security Module; tamper-resistant device for master key storage             │
│   DEK          = Data Encryption Key; per-dataset key encrypted by the master key                     │
│   KMS          = Key Management Service; centralised key lifecycle: create, rotate, revoke            │
│   legal hold   = data retention freeze overriding normal deletion schedule for litigation             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="data-classification/">
  <strong>Data Classification</strong>
  <span>Classification tiers, labelling standards, handling requirements, and policy enforcement.</span>
</a>

<a class="kb-card" href="data-encryption/">
  <strong>Data Encryption</strong>
  <span>Encryption standards, key management, at-rest and in-transit encryption configuration.</span>
</a>

<a class="kb-card" href="data-governance/">
  <strong>Data Governance</strong>
  <span>Data ownership, classification policy, lineage, and governance framework standards.</span>
</a>

<a class="kb-card" href="data-retention-policy/">
  <strong>Data Retention Policy</strong>
  <span>Retention schedules, data classification tiers, legal hold, and deletion standards.</span>
</a>

<a class="kb-card" href="key-management/">
  <strong>Key Management</strong>
  <span>KMS architecture, key rotation, HSM integration, and secret lifecycle procedures.</span>
</a>

</div>
