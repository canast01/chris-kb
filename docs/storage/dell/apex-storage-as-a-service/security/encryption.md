---
tags:
  - dell
  - security
---
# APEX Storage as a Service — Encryption


<div class="kb-summary">
Encryption reference covering Encryption Controls, Key Points.
</div>

```text
┌──────────────────────────────────── Dell Apex STaaS — Encryption ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Apex encryption: AES-256 at rest on all arrays; TLS 1.2+ for portal and API          │   │
│   │         At rest: self-encrypting drives (SED); AES-256-XTS; always on, no user config         │   │
│   │          In transit: iSCSI CHAP session auth; NFS sec=krb5; HTTPS/TLS for management          │   │
│   │             Key management: Dell-managed by default; customer KMIP server optional            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Write → SED encrypts inline → AES-256 stored → read → SED decrypts → host receives                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           At Rest           │  │          In Transit         │  │           Key Mgmt          │   │
│   │         AES-256-XTS         │  │           TLS 1.2+          │  │         Dell managed        │   │
│   │          SED drives         │  │          iSCSI CHAP         │  │        KMIP optional        │   │
│   │          Always on          │  │         NFS Kerberos        │  │         Key rotation        │   │
│   │        No perf impact       │  │         HTTPS portal        │  │          FIPS 140-2         │   │
│   │        Drive destruct       │  │        Cipher TLS 1.3       │  │          Audit keys         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SED: cryptographic erase on drive decommission; no data recovery risk when drive replaced          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Algorithm     │     Enabled by    │      Verify      │      Notes       │   │
│   │     At rest      │   AES-256-XTS    │      Default      │   Console view   │   SED hardware   │   │
│   │     iSCSI tx     │    CHAP auth     │      Per host     │   CHAP secret    │   Not payload    │   │
│   │      NFS tx      │     Kerberos     │    Mount option   │     sec=krb5     │    KDC needed    │   │
│   │     Mgmt tx      │     TLS 1.2+     │     Always on     │     TLS cert     │    Portal/API    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SED drives in array · iSCSI network switch (not inspecting payload) · KDC server         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SED            = Self-Encrypting Drive; AES-256 hardware encryption on-chip; no CPU overhead       │
│    AES-256-XTS    = XEX-based tweaked codebook mode; NIST-approved for storage encryption             │
│    Always on      = Apex SED encryption cannot be disabled; all data encrypted at write               │
│    Crypto erase   = Reset SED encryption key; instantly renders all data unreadable                   │
│    KMIP           = Key Management Interoperability Protocol; customer-managed key server             │
│    FIPS 140-2     = US encryption standard; Apex optionally runs FIPS-validated mode                  │
│    CHAP           = iSCSI host authentication only; does NOT encrypt I/O payload                      │
│    Kerberos       = NFS data integrity/confidentiality; sec=krb5i adds integrity signing              │
│    TLS 1.2+       = Minimum TLS version for Apex Console and REST API endpoints                       │
│    Key rotation   = Periodic re-encryption of SED keys; Dell-managed on schedule                      │
│    FIPS 140-2 L2  = Validated cryptographic modules in Apex arrays; regulatory compliance             │
│    Drive destruct = Physical destruction of retired SEDs; crypto erase is equivalent                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [APEX Storage as a Service](../index.md) reference.

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
| **APEX Console TLS** | The APEX Console web UI and REST API are served exclusively over HTTPS (TLS 1.2+). Certificate management is handled by Dell's cloud infrastructure. Customers do not manage these certificates. |
| **SCG telemetry transmission** | The Secure Connect Gateway (SCG) forwards telemetry from on-premises hardware to CloudIQ over TLS 1.2 or higher. The SCG initiates all outbound connections; no inbound connectivity from Dell's cloud to the SCG is required. |
| **API authentication encryption** | All APEX API requests use OAuth 2.0 client credentials. The token exchange and all subsequent API calls are protected by the same TLS layer as the console — credentials are never transmitted in plaintext. |
| **Data-in-transit (replication / host I/O)** | Host I/O between servers and APEX-managed storage uses standard block or file protocols (FC, iSCSI, NFS, SMB). Encryption of these I/O paths is a network and host configuration concern — enable IPsec or in-flight encryption at the fabric or host level if required by policy. |
| **PowerStore data-at-rest** | PowerStore supports Drive Encryption (D@RE) using self-encrypting drives managed through Unisphere. APEX does not alter this configuration — it is set during array deployment and follows the PowerStore security hardening guide. |
| **PowerScale data-at-rest** | PowerScale supports DARE using the Self-Encrypting Drive (SED) feature. Key management can be delegated to an external KMIP server. APEX does not manage this — configure it per the PowerScale Security Configuration Guide. |
| **PowerFlex data-at-rest** | PowerFlex supports volume-level encryption through the PowerFlex Data Security feature. Volumes can be individually encrypted with AES-256. APEX subscription does not change the encryption configuration — apply it via the PowerFlex Manager or REST API as part of storage provisioning. |
| **Management network path** | Communication between on-premises hardware and the SCG appliance travels over the management VLAN. Isolate this path from untrusted networks. If a proxy is used for SCG outbound access, ensure TLS inspection is not applied to Dell cloud endpoints — certificate pinning will reject inspected connections. |

## Key Points

- APEX is a subscription and management overlay; it does not own or encrypt stored data.
- Data-at-rest encryption is a platform-level control on the underlying hardware (PowerStore, PowerScale, PowerFlex).
- Telemetry transmitted via SCG contains capacity metrics only — no user data or file content leaves the array through this path.
- TLS 1.0 and 1.1 are not accepted by Dell's cloud endpoints.
