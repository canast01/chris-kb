---
tags:
  - pure
  - security
---
# FlashArray — Encryption

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Data at Rest (always-on, no config required)                                                         │
│                                                                                                       │
│  Write I/O ──► NVRAM ──► NVMe SED                                                                     │
│                            ├── DEK (per-drive, internal)                                              │
│                            └── KEK (Purity, stored NVRAM)                                             │
│                                                                                                       │
│  AES-256-XTS hardware encryption in drive                                                             │
│  Removed drive: cryptographic erase (NIST SP 800-88)                                                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Data in Transit (TLS, always-on)                                                                     │
│  ├── Management: HTTPS (443) + SSH (22)                                                               │
│  ├── Replication: TLS between arrays                                                                  │
│  └── Pure1 phone-home: HTTPS (443) outbound                                                           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text

FlashArray provides encryption at rest (hardware-based, always-on) and encryption in transit (TLS for all management and replication traffic). Both are enabled by default and require no configuration to activate — the operational task is to manage certificates, verify status, and integrate with external key managers when required.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Encryption at Rest

### Mechanism

FlashArray //X and //C series use **NVMe Self-Encrypting Drives (SEDs)** with hardware-accelerated AES-256-XTS encryption. Every drive is encrypted from the factory — there is no unencrypted mode and no configuration option to disable encryption. The hardware encryption engine operates inside the drive itself, so encryption has zero performance impact on the array.

**How it works:**

- Each drive holds an internal Data Encryption Key (DEK) that encrypts the data stored on it
- Purity manages a Key Encryption Key (KEK) that protects the DEK; the KEK is stored in the NVRAM on both controllers
- When Purity initialises or recovers from a restart, it unlocks the drives by supplying the KEK
- A removed or stolen drive cannot be read without the KEK — the data is cryptographically inaccessible

**Cryptographic sanitisation on drive decommission:**

When a drive reaches end-of-life or fails and is replaced, Pure Storage performs a cryptographic erase (Instant Secure Erase, ISE) — the drive's internal DEK is overwritten, rendering all data permanently unrecoverable without needing to zero-fill the drive. This is compliant with NIST SP 800-88 media sanitisation requirements.

```

```bash
# Verify encryption is active on the array
purearray list --encryption

# Show hardware drive details including drive type (SED)
puredrive list --spec

# Show hardware component detail for encryption-related components
purehw list --type nvram
```
```bash
# Configure KMIP server (Purity//FA 6.x)
purekms create --address <kmip_server_ip> \
    --port 5696 \
    --certificate <client_cert_path> \
    --ca-certificate <ca_cert_path> \
    kmip-primary

# List configured KMS servers
purekms list

# Test KMS connectivity
purekms test kmip-primary
```
```bash
# View the current TLS certificate details
purearray list --ssl-certificate

# Install a new certificate (PEM format, certificate + private key)
purearray setattr --tls-certificate <path_to_cert_pem>

# If the private key is in a separate file, combine them first:
# cat cert.pem key.pem > combined.pem
# purearray setattr --tls-certificate combined.pem
```
```bash
# List connected remote arrays
purearray list --connection

# Show protection group replication targets and their connection status
purepgroup list --replication
```
