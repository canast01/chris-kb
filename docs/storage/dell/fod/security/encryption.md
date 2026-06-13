---
tags:
  - dell
  - security
---
# FOD — Encryption


<div class="kb-summary">
Encryption reference covering Encryption Controls, Key Points.

*Applies to: Dell FOD*
</div>

```text
┌──────────────────────────────────────── Dell FoD — Encryption ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FoD encryption: protect .lic key files in transit and at rest; portal uses TLS 1.2+      │   │
│   │        Key files: FoD .lic files are cryptographically signed by Dell; cannot be forged       │   │
│   │       At rest: .lic files stored in encrypted vault (AES-256); never stored in plaintext      │   │
│   │      In transit: portal download over TLS 1.2+; array import over HTTPS management plane      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Portal TLS download → vault AES-256 storage → HTTPS import to array → signature verified           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Key File Security      │  │           Transit           │  │           At Rest           │   │
│   │       Dell PKI signed       │  │           TLS 1.2+          │  │        Vault AES-256        │   │
│   │          SN binding         │  │         HTTPS portal        │  │       Encrypted share       │   │
│   │        Tamper evident       │  │       HTTPS array mgmt      │  │       Never plaintext       │   │
│   │       Sig verification      │  │         No email/FTP        │  │        Key access log       │   │
│   │          No re-use          │  │         Cert pinning        │  │       Backup encrypted      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Array firmware verifies Dell PKI signature on .lic file; rejects unsigned or modified files        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Algorithm     │     Applied To    │      Owner       │      Notes       │   │
│   │  Key signature   │   Dell PKI/RSA   │  Every .lic file  │       Dell       │Verified on import│   │
│   │     Transit      │     TLS 1.2+     │ Download + import │ Dell + customer  │    HTTPS only    │   │
│   │     At rest      │     AES-256      │   Vault storage   │     Customer     │Vault-managed key │   │
│   │      Backup      │     AES-256      │  Encrypted share  │     Customer     │ Mirror of vault  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: .lic files never transit unencrypted network segments; TLS or encrypted channel only     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Dell PKI       = Dell Public Key Infrastructure; signs every FoD .lic file with private key        │
│    Sig verification = Array firmware checks Dell public key signature on .lic at import time          │
│    Tamper evident = Any modification to .lic file content invalidates the Dell PKI signature          │
│    SN binding     = .lic cryptographic content includes the target array serial number                │
│    No re-use      = A FoD key for SN-A cannot be applied to SN-B; signature check fails               │
│    TLS 1.2+       = Dell portal and array management plane require TLS 1.2 minimum                    │
│    No email/FTP   = .lic files must not transit unencrypted channels; vault and HTTPS only            │
│    Cert pinning   = Array management HTTPS; trust only Dell-issued cert; rejects MITM cert            │
│    Vault AES-256  = HashiCorp Vault encrypts all stored secrets (inc. .lic files) with AES-256        │
│    Key access log = Vault audit log records every read of a .lic file; who, when, IP                  │
│    Backup encrypted = Secondary .lic backup on encrypted file server; same AES-256 protection         │
│    Vault-managed key = Vault handles AES-256 key rotation for stored secrets automatically            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Flex on Demand](../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Encryption Controls

| Control | Detail |
|---|---|
| **Telemetry transmission** | Capacity metrics are forwarded from the array to CloudIQ via the Secure Connect Gateway (SCG) over TLS 1.2 or higher. The payload contains only capacity counters — no user data, file contents, or host identifiers are transmitted. |
| **APEX Console access** | The APEX Console web UI and its underlying REST API are served exclusively over HTTPS (TLS 1.2+). Certificate management is handled by Dell's cloud infrastructure; no customer-managed certificate is required. |
| **SCG communication security** | The SCG appliance initiates all outbound connections to Dell's cloud endpoints. It uses certificate pinning to validate Dell's cloud TLS certificates, preventing man-in-the-middle interception. Inbound connections from Dell to the SCG are not required and should be blocked at the perimeter firewall. |
| **Data-at-rest** | FOD is a metering and billing overlay; it does not own storage volumes. Data-at-rest encryption is governed entirely by the underlying array (PowerStore, PowerMax, Unity XT, etc.). Refer to the respective platform's security documentation for encryption configuration — for example, PowerStore supports D@RE using self-encrypting drives managed through Unisphere. |
| **API encryption** | All APEX API calls (OAuth token exchange and subsequent requests) are made over HTTPS. API credentials are bearer tokens scoped to a service account; credentials in transit are protected by the same TLS layer as the console. |
| **Internal array-to-SCG path** | Communication between the array and the co-located or remote SCG appliance travels over the management network segment. Place the SCG on a VLAN that is accessible to the array management interface only; do not route SCG traffic through untrusted segments. |

## Key Points

- No user data or file content ever leaves the array through the FOD telemetry path.
- TLS 1.2 is the minimum enforced by Dell's endpoints; TLS 1.0 and 1.1 are not accepted.
- Data-at-rest encryption for stored data is a platform-level control, not a FOD control.
- If SCG uses a proxy for outbound internet access, ensure the proxy does not perform TLS inspection on Dell cloud endpoints — certificate pinning will cause the connection to fail.
