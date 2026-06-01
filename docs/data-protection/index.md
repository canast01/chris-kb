# Data Protection



<div class="kb-summary">
Data Protection reference: Backup Validation, Data Classification, Data Encryption, Data Governance, and 3 more.
</div>

```text
┌───────────────── Data Protection — Classification, Encryption, Retention & Recovery ──────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Data protection: classify data by sensitivity → encrypt at rest and in transit →       │   │
│   │        enforce retention schedules → manage encryption keys → test recovery procedures        │   │
│   │        Foundation: know what data exists, where it lives, who owns it, and for how long       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Classify → Encrypt → Retain → Test recovery → Govern access → Audit                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Classification       │  │          Encryption         │  │       Retention & Keys      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      Public / Internal      │  │       AES-256 at rest       │  │      Schedules by type      │   │
│   │         Confidential        │  │     TLS 1.2/1.3 transit     │  │      Legal hold process     │   │
│   │       Restricted / PII      │  │      KMS key management     │  │      Deletion verified      │   │
│   │     MIP sensitivity lbls    │  │      Key rotation sched     │  │       Restore testing       │   │
│   │      Handling controls      │  │     BYOK for compliance     │  │      Compliance reports     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PII        = Personally Identifiable Information; highest classification; GDPR/CCPA applies        │
│    PHI        = Protected Health Information; HIPAA regulated; strict access and audit logging        │
│    PCI        = Payment Card Industry; cardholder data subject to PCI DSS controls                    │
│    AES-256    = Advanced Encryption Standard 256-bit; standard for encryption at rest                 │
│    KMS        = Key Management Service; manages encryption key lifecycle and access policies          │
│    HSM        = Hardware Security Module; tamper-resistant device for key storage                     │
│    Legal hold = Suspend deletion of data pending litigation or regulatory investigation               │
│    DLP        = Data Loss Prevention; prevents unauthorised data exfiltration                         │
│    BYOK       = Bring Your Own Key; customer-managed keys in cloud KMS for compliance                 │
│    MIP        = Microsoft Information Protection; sensitivity labels on Office content                │
│    DEK        = Data Encryption Key; key that directly encrypts a data object                         │
│    KEK        = Key Encryption Key; wraps and protects data encryption keys                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="backup-validation/"><strong>Backup Validation</strong><span>Verifying backup jobs are complete, restores are testable, and retention policies are met.</span></a>
<a class="kb-card" href="data-classification/"><strong>Data Classification</strong><span>Data classification tiers, labelling requirements, and handling rules per classification level.</span></a>
<a class="kb-card" href="data-encryption/"><strong>Data Encryption</strong><span>Encryption at rest and in transit — standards, key management, and compliance requirements.</span></a>
<a class="kb-card" href="data-governance/"><strong>Data Governance</strong><span>Data ownership, access controls, audit requirements, and regulatory alignment.</span></a>
<a class="kb-card" href="data-retention-policy/"><strong>Data Retention Policy</strong><span>Retention schedules by data type, legal hold procedures, and deletion verification.</span></a>
<a class="kb-card" href="key-management/"><strong>Key Management</strong><span>KMS architecture, key rotation procedures, and HSM integration references.</span></a>
<a class="kb-card" href="recovery-testing/"><strong>Recovery Testing</strong><span>Restore test procedures, DR test schedules, and test result documentation.</span></a>
</div>
