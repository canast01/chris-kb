# FlashArray — Encryption


<div class="kb-summary">
Encryption reference covering Encryption at Rest, Encryption in Transit, TLS Configuration Reference, Compliance Mapping, Operational Checklist.
</div>

FlashArray Encryption Architecture
```text
┌────────────────────────────────────────────────────────────┐
│  Data at Rest (always-on, no config required)                                                         │
│                                                                                                       │
│  Write I/O ──► NVRAM ──► NVMe SED                                                                     │
│                            ├── DEK (per-drive, internal)                                              │
│                            └── KEK (Purity, stored NVRAM)                                             │
│                                                                                                       │
│  AES-256-XTS hardware encryption in drive                                                             │
│  Removed drive: cryptographic erase (NIST SP 800-88)                                                  │
└────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────────────────────────────┐
│  Data in Transit (TLS, always-on)                                                                     │
│  ├── Management: HTTPS (443) + SSH (22)                                                               │
│  ├── Replication: TLS between arrays                                                                  │
│  └── Pure1 phone-home: HTTPS (443) outbound                                                           │
└────────────────────────────────────────────────────────────┘
```text

FlashArray provides encryption at rest (hardware-based, always-on) and encryption in transit (TLS for all management and replication traffic). Both are enabled by default and require no configuration to activate — the operational task is to manage certificates, verify status, and integrate with external key managers when required.

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

```bash
# Verify encryption is active on the array
purearray list --encryption

# Show hardware drive details including drive type (SED)
puredrive list --spec

# Show hardware component detail for encryption-related components
purehw list --type nvram
```

---

### External Key Management (KMIP)

For organisations that require external custody of encryption keys — for example, to meet FIPS 140-2 requirements, financial services regulations, or internal security policies that mandate separation of key management from storage infrastructure — FlashArray supports integration with an external Key Management Interoperability Protocol (KMIP) key manager.

**Supported KMIP servers:**
- Thales CipherTrust (formerly SafeNet KeySecure)
- IBM Security Key Lifecycle Manager (SKLM)
- HashiCorp Vault Enterprise (with KMIP secrets engine)
- Other KMIP 1.1+ compliant key management systems

**Behaviour with KMIP enabled:**

- The KEK is stored in the external KMIP server, not in the array's NVRAM
- On controller startup, Purity authenticates to the KMIP server and retrieves the KEK to unlock the drives
- If the KMIP server is unreachable at startup, the array will not unlock the drives — this is by design (key escrow means the array owner has custody)
- This architecture means the KMIP server becomes a dependency for array availability; design for KMIP HA accordingly (clustered KMIP appliances, or two KMIP servers configured in Purity)

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

**Pre-requisites for KMIP integration:**
- Purity//FA 6.1 or later
- Client certificate issued by the same CA as the KMIP server
- Network path from both array controllers to the KMIP server on port 5696 (TCP)
- KMIP server configured to accept the FlashArray client certificate

---

## Encryption in Transit

### Management Traffic (HTTPS / REST API)

All access to the Purity GUI, REST API, and CLI via the management interface uses **TLS 1.2 or 1.3** with server certificate validation. By default, Purity uses a self-signed certificate. Replace this with a certificate from an internal CA or a public CA before the array enters production.

```bash
# View the current TLS certificate details
purearray list --ssl-certificate

# Install a new certificate (PEM format, certificate + private key)
purearray setattr --tls-certificate <path_to_cert_pem>

# If the private key is in a separate file, combine them first:
# cat cert.pem key.pem > combined.pem
# purearray setattr --tls-certificate combined.pem
```

**Certificate requirements:**

| Requirement | Detail |
|---|---|
| Format | PEM (base64-encoded X.509) |
| Subject Alternative Name (SAN) | Must include the array management IP and/or FQDN |
| Key type | RSA 2048-bit minimum; RSA 4096 or ECDSA P-256 recommended |
| Expiry | Minimum 1 year; plan renewal before expiry — an expired cert does not break CLI access but breaks browser-based REST API calls |
| Issuer | Internal CA or public CA; both are accepted |

**Certificate renewal process:**

1. Generate a CSR from your CA infrastructure using the array's management IP/FQDN as the CN and SAN
2. Get the certificate signed by your CA
3. Stage the signed certificate + key in PEM format on a jump host accessible to the array
4. Import via CLI: `purearray setattr --tls-certificate <combined_pem>`
5. Verify in a browser and via `purearray list --ssl-certificate` — the new expiry date should be visible

---

### Replication Traffic

Inter-array replication traffic (async replication via protection groups, ActiveCluster synchronous replication) uses **TLS encryption by default**. No configuration is required to enable this — Purity negotiates a TLS session between the arrays when the replication connection is established.

Verify the inter-array replication connection is established:

```bash
# List connected remote arrays
purearray list --connection

# Show protection group replication targets and their connection status
purepgroup list --replication
```

---

### iSCSI Data Traffic

iSCSI data traffic between hosts and the FlashArray is **not encrypted by Purity** — it travels in plaintext over the Ethernet network. If your security policy requires encryption of data in transit for block storage:

- **Option 1 — IPsec:** Implement IPsec between the host NICs and the array iSCSI interfaces at the network layer. This requires IPsec support on the host OS (supported on Linux, Windows, and ESXi with appropriate configuration) and on the network infrastructure.
- **Option 2 — Network isolation:** Dedicate a physically separate network (separate switches, separate cabling) for iSCSI storage traffic with no routing paths to untrusted networks. This is the most common approach and satisfies most compliance frameworks' data-in-transit requirements for storage networks.
- **Option 3 — NVMe/TCP:** NVMe/TCP does not add encryption either; the same isolation approach applies.

---

### FC and NVMe/FC Data Traffic

FC and NVMe/FC data traffic encryption is a **fabric-layer concern**, not a Purity concern. Options:

- **FC-SP-2 (Fibre Channel Security Protocol):** Provides per-frame authentication and optional encryption between FC endpoints. Requires FC-SP-2-capable HBAs (e.g., Broadcom/Emulex LPe35000 series, Marvell/QLogic QLE2780) and FC switches that support FC-SP-2 (e.g., Brocade Gen 7, Cisco MDS 9000 with appropriate licences).
- **Link encryption on Brocade SAN:** Brocade Gen 6 and Gen 7 switches support encryption at the inter-switch link (ISL) level using AES-256; this encrypts all traffic transiting the fabric backbone even if end-to-end FC-SP-2 is not implemented.

Consult your FC switch vendor documentation for configuration procedures.

---

## TLS Configuration Reference

| Setting | Recommendation |
|---|---|
| TLS version | TLS 1.2 minimum; prefer TLS 1.3 (Purity//FA 6.4+ negotiates TLS 1.3 with supporting clients) |
| Certificate type | RSA 4096 or ECDSA P-256 |
| Certificate source | Internal PKI CA or public CA — not self-signed in production |
| Certificate renewal lead time | Begin renewal 30 days before expiry; automate renewal reminders |
| KMIP integration | Required when external key custody is mandated; add KMIP HA pair to avoid availability dependency |

---

## Compliance Mapping

| Regulatory Framework | Encryption Controls | FlashArray Support |
|---|---|---|
| **PCI DSS v4.0** | Req 3.5 (encryption at rest for CHD), Req 4.2.1 (TLS in transit) | AES-256 at rest (always-on); TLS 1.2+ for all management and replication traffic |
| **FIPS 140-2** | Level 2 validated cryptographic modules required | FlashArray //X supports FIPS 140-2 validated modules; verify specific model certification with Pure account team; KMIP integration required for external key custody |
| **ISO 27001:2022** | A.8.24 (use of cryptography) | Encryption at rest on all drives; TLS in transit; documented key management process |
| **HIPAA Technical Safeguards** | 164.312(a)(2)(iv) — Encryption/decryption; 164.312(e)(2)(ii) — Encryption in transit | AES-256 at rest; TLS for all admin and replication traffic; IPsec recommended for iSCSI if HIPAA strict interpretation applies |
| **SOC 2 Type II** | CC6.1 (logical access), CC6.7 (transmission encryption) | TLS in transit, AES-256 at rest, audit logging |
| **NIS2 / DORA** | Cryptographic measures for data protection and resilience | At-rest and in-transit encryption; availability via ActiveCluster for resilience requirement |
| **GDPR** | Art. 32 — appropriate technical measures including encryption | AES-256 at rest; TLS in transit; cryptographic erase on drive decommission satisfies Art. 17 data erasure |

---

## Operational Checklist

| Task | Frequency | Command / Action |
|---|---|---|
| Verify encryption is active | Initial setup + annually | `purearray list --encryption` |
| Verify TLS certificate expiry | Monthly | `purearray list --ssl-certificate` — check `expires` field |
| Renew TLS certificate | Before expiry (30-day lead) | Generate CSR, sign with CA, import with `purearray setattr --tls-certificate` |
| Test KMIP connectivity (if configured) | Monthly | `purekms test <kms_name>` |
| Confirm replication uses TLS | After adding new replication targets | `purearray list --connection` — verify connection is established |
| Cryptographic erase confirmation on drive replacement | Every drive replacement | Confirm with Pure Support that ISE was performed on the removed drive |
