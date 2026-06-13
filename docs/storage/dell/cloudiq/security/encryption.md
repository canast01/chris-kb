---
tags:
  - dell
  - security
---
# CloudIQ — Encryption


<div class="kb-summary">
CloudIQ data encryption settings, key management integration, and encryption compliance reporting.
</div>

```text
┌────────────────────────────────────── Dell CloudIQ — Encryption ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   CloudIQ encrypts all data in transit (TLS 1.2+) and at rest (AES-256) in Dell cloud stores  │   │
│   │   In transit: SCG to cloud and portal to cloud use TLS 1.2+; mutual TLS for SCG, HSTS portal  │   │
│   │      At rest: telemetry datastore, audit logs, and report exports encrypted with AES-256      │   │
│   │    Key management: Dell-managed KMS by default; BYOK (Bring Your Own Key) option available    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SCG collects plaintext telemetry on LAN → TLS tunnel to cloud → AES-256 stored at rest             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          In Transit         │  │           At Rest           │  │        Key Management       │   │
│   │           TLS 1.2+          │  │           AES-256           │  │       Dell-managed KMS      │   │
│   │         mTLS for SCG        │  │       Telemetry store       │  │         BYOK option         │   │
│   │         HSTS portal         │  │      Audit log encrypt      │  │       90-day rotation       │   │
│   │        AES-256 cipher       │  │        Report exports       │  │        Key audit log        │   │
│   │         Cert pinning        │  │        Backup encrypt       │  │          FIPS 140-2         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SCG local disk optionally encrypted via host-level encryption; not managed by CloudIQ              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Algorithm     │     Key Source    │     Rotation     │    Compliance    │   │
│   │     Transit      │     TLS 1.2+     │     PKI / cert    │   Annual cert    │   PCI DSS 4.0    │   │
│   │     Storage      │     AES-256      │      Dell KMS     │      90-day      │    FIPS 140-2    │   │
│   │       BYOK       │     AES-256      │    Customer HSM   │   Customer set   │  Customer req.   │   │
│   │    Audit logs    │     AES-256      │      Dell KMS     │      90-day      │    SOC 2 CC6     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell cloud stores (AWS/Azure) enforce encryption; customer encrypts SCG host disk        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    TLS 1.2+       = Transport Layer Security; encrypts all SCG to cloud and portal to cloud traffic   │
│    mTLS           = Mutual TLS; SCG presents client certificate to cloud for bidirectional auth       │
│    AES-256        = Advanced Encryption Standard, 256-bit key; used for all at-rest data              │
│    HSTS           = HTTP Strict Transport Security; forces browser to use HTTPS for portal            │
│    Cert pinning   = SCG validates cloud cert fingerprint; prevents MITM via rogue certificate         │
│    Dell KMS       = Dell-managed key management service in cloud; keys never leave cloud boundary     │
│    BYOK           = Bring Your Own Key; customer provides encryption key from their own HSM           │
│    HSM            = Hardware Security Module; tamper-resistant device for key storage and crypto      │
│    FIPS 140-2     = US federal standard for cryptographic modules; Level 2 for cloud KMS              │
│    90-day rotation = Encryption keys rotated every 90 days; old key used to decrypt existing data     │
│    Telemetry store = Cloud database holding array performance and capacity time-series data           │
│    Backup encrypt = CloudIQ backup snapshots of telemetry encrypted with same AES-256 scheme          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [CloudIQ](../index.md) reference.

---

| Layer | Protection |
|---|---|
| Telemetry in transit (SCG to Dell) | TLS 1.2 or higher; certificate-pinned connection from SCG to Dell SRS endpoint |
| Telemetry at rest (Dell cloud) | Encrypted at rest in Dell's cloud infrastructure |
| Portal access | HTTPS (TLS 1.2+); sessions protected by Dell's cloud infrastructure |
| Data content | Telemetry contains configuration metadata and performance statistics only — no user data, file contents, or host data is transmitted |

CloudIQ telemetry does not include: file names, directory paths, user credentials, application data, or any content stored on the managed arrays.

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

