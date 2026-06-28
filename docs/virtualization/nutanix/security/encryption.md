---
tags:
  - nutanix
  - security
  - encryption
  - data-at-rest
  - sed
---
# Nutanix — Encryption

<div class="kb-summary">
Nutanix data-at-rest encryption (software and SED-based), key management (native key manager and external KMS), in-transit encryption, and encryption lifecycle operations (enable, re-key, disable).

*Applies to: AOS 6.x · AHV*
</div>
![Nutanix — Encryption](../../../assets/virtualization-nutanix-security-encryption.svg)





---

```d2
direction: down

external: External / Untrusted {shape: rectangle}
encryption_options: "Encryption Options" {shape: rectangle}
key_manager_options: "Key Manager Options" {shape: rectangle}
enable_software_dataatrest_encryptio: "Enable Software Data-at-Rest Encryption" {shape: rectangle}
enable_sedbased_hardware_encryption: "Enable SED-Based Hardware Encryption" {shape: rectangle}
external_kms_kmip_integration: "External KMS (KMIP) Integration" {shape: rectangle}
intransit_encryption_cvm_to_cvm: "In-Transit Encryption (CVM to CVM)" {shape: rectangle}
core: "Nutanix AHV Core" {shape: hexagon}

external -> encryption_options: traffic in
encryption_options -> key_manager_options
key_manager_options -> enable_software_dataatrest_encryptio
enable_software_dataatrest_encryptio -> enable_sedbased_hardware_encryption
enable_sedbased_hardware_encryption -> external_kms_kmip_integration
external_kms_kmip_integration -> intransit_encryption_cvm_to_cvm
intransit_encryption_cvm_to_cvm -> core: secured path
```

## Before you begin

- **Licence:** Data-at-rest encryption requires a Nutanix Pro or Ultimate licence
- **Hardware:** SED encryption requires Self-Encrypting Drives in each node
- **Key manager:** Choose before enabling — you cannot switch between native and external KMS without re-encryption
- **Impact:** Software encryption adds CPU overhead (~5–10% on non-AES-NI hardware, negligible on modern CPUs with AES-NI)

---

## Encryption Options

| Type | How it works | Requires |
|---|---|---|
| Software encryption | AES-256 in AOS Stargate | AOS Pro/Ultimate + any disk |
| SED (Hardware) | Self-Encrypting Drive with AOS KMS control | SED disks + Pro/Ultimate |
| In-transit (CVM-CVM) | TLS for replication traffic | Included, configurable |

---

## Key Manager Options

| KMS | Use case |
|---|---|
| Nutanix Native KMS | Simpler; keys stored distributed across CVMs |
| External KMS (KMIP) | Regulatory compliance (FIPS); integrates with Thales/SafeNet, Vormetric, IBM SKLM |

---

## Enable Software Data-at-Rest Encryption

!!! danger "Encryption causes background re-encryption of all existing data"
    Once enabled on a container, AOS re-encrypts all objects on that datastore. This is a long-running background operation (hours to days on large clusters) with significant I/O overhead. **It cannot be cancelled once started.** Ensure cluster capacity is below 70%, KMS is redundant, and a maintenance window is scheduled.

### Step 1 — Configure Native Key Manager

```text
Prism Element → Settings → Data Encryption → Key Management
  Key Management Mode: Native
  Passphrase: <strong passphrase — record securely>
  Confirm passphrase
  Save
```

The passphrase protects the master encryption key. **If lost, encrypted data cannot be recovered.** Store the passphrase in a password vault (CyberArk, HashiCorp Vault, or similar).

### Step 2 — Enable Encryption on a Container

```text
Prism Element → Storage → Storage Containers → select container
  Actions → Enable Encryption
  Confirm: Yes, I understand this will re-encrypt existing data
```

### Monitor Re-Encryption Progress

```bash
# Check Curator tasks — re-encryption shows as a Curator scan
curator_cli get_last_successful_scans | tail -20
curator_cli display_curator_tasks | grep -i encrypt

# NCC check for encryption status
ncc --health_checks data_encryption_check
```

---

## Enable SED-Based Hardware Encryption

Requires all nodes to have SED disks (verified during Foundation imaging).

```text
Prism Element → Settings → Data Encryption → Key Management
  Key Management Mode: Native (or KMIP external)
  Enable Hardware Encryption (SEDs): Yes
```

SED encryption is performed by the drive itself — no CPU overhead. Data on a failed/removed drive is unreadable without the encryption key, enabling secure drive disposal.

---

## External KMS (KMIP) Integration

For regulatory compliance (FIPS 140-2), use an external key manager.

```text
Prism Element → Settings → Data Encryption → Key Management
  Key Management Mode: External (KMIP)
  KMIP Server: <kmip-server-ip>:<port>   (default port 5696)
  TLS Certificate: upload client cert for mTLS
  CA Certificate: upload KMS CA cert
  Test Connectivity: click Test
```

Supported KMIP servers:
- Thales CipherTrust (SafeNet KeySecure)
- IBM Security Key Lifecycle Manager (SKLM)
- Gemalto/Thales Luna
- HashiCorp Vault Enterprise (KMIP secrets engine)

---

## In-Transit Encryption (CVM to CVM)

AOS encrypts replication traffic between remote sites by default for Nutanix DR policies. For Protection Domain replication, enable encryption explicitly:

```bash
ncli pd edit name=<pd-name> \
  enable-replication-ssl=true
```

For CVM-to-CVM within a cluster, inter-node traffic on the internal network is not encrypted by default (relies on network-level isolation). For cross-cluster or WAN replication, SSL is strongly recommended.

---

## Key Rotation (Re-Key)

Periodic key rotation is a compliance requirement (e.g., annually).

```text
Prism Element → Settings → Data Encryption → Key Management
  Rotate Key → confirm passphrase → New Passphrase → Confirm
```

```bash
# Monitor re-key (same Curator task monitoring as initial encryption)
curator_cli display_curator_tasks | grep -i encrypt
```

Re-key triggers a background re-encryption of all data with the new key. Same I/O impact as initial encryption — schedule during low-traffic windows.

---

## Verify Encryption Status

```bash
# Check if encryption is enabled per container
ncli ctr list | grep -i encrypt

# NCC encryption health check
ncc --health_checks data_encryption_check

# Check native KMS status
ncli cluster get-data-encryption-status
```

```text
Prism Element → Settings → Data Encryption
  Should show: "Encryption is enabled" for each protected container
  Key manager: status "Connected" (for external KMS)
```

---

## Disable Encryption

!!! warning "Disabling encryption triggers full re-decryption"
    Same I/O impact as enabling. Ensure capacity headroom and a maintenance window.

```text
Prism Element → Settings → Data Encryption → select container
  Actions → Disable Encryption → Confirm
```

---

## See also

- [Nutanix — Hardening](hardening/)
- [Nutanix — Health Checks](../operations/health-checks/)
