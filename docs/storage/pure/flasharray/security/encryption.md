---
tags:
  - pure
  - security
---
# FlashArray — Encryption
![FlashArray — Encryption](../../../../assets/storage-pure-flasharray-security-encryption.svg)

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

```text title="Expected output"
Name                          Encryption
pure-array-01                 Enabled
pure-array-02                 Enabled

Name            Capacity  Type      RPM    SED
SSD-1           1.92TB    SSD       N/A    Yes
SSD-2           1.92TB    SSD       N/A    Yes
SSD-3           1.92TB    SSD       N/A    Yes
SSD-4           1.92TB    SSD       N/A    Yes
...

Name            Status    Slot      Capacity  Part Number
NVRAM-1         OK        1A        8GB       78-063456-01
NVRAM-2         OK        1B        8GB       78-063456-01
```

!!! warning "Common errors"
    **`Error: Invalid command 'purearray'`** — Verify the Pure Storage CLI tools are installed and in your PATH by running `which purearray`.
    **`Error: Connection refused to array management interface`** — Confirm the array hostname/IP is reachable and you have valid credentials configured in your Pure Storage CLI profile.
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

```text title="Expected output"
Created KMS server 'kmip-primary' with address 10.45.120.88:5696
Fingerprint: a7:2f:e4:9b:c1:56:3d:8a:b2:44:f9:7e:2c:61:d5:3b

Name              Address          Port  Status    Last Connected
kmip-primary      10.45.120.88     5696  connected 2024-01-15T09:32:14Z
kmip-backup       10.46.120.89     5696  connected 2024-01-15T09:31:52Z

Testing connection to kmip-primary...
✓ Connection successful
✓ Certificate validation passed
✓ Key operations available
Test completed in 1.2s
```

!!! warning "Common errors"
    **`Error: Certificate file not found: /etc/purity/kmip-client.crt`** — Verify the certificate path is correct and readable by the purity service user.
    **`Error: Failed to connect to KMIP server at 10.45.120.88:5696 (Connection refused)`** — Confirm the KMIP server is running and accessible on the specified IP and port from the array's management network.
    **`Error: Certificate validation failed: untrusted certificate authority`** — Ensure the CA certificate file is valid and matches the certificate chain used by the KMIP server.
```bash
# View the current TLS certificate details
purearray list --ssl-certificate

# Install a new certificate (PEM format, certificate + private key)
purearray setattr --tls-certificate <path_to_cert_pem>

# If the private key is in a separate file, combine them first:
# cat cert.pem key.pem > combined.pem
# purearray setattr --tls-certificate combined.pem
```

```text title="Expected output"
Certificate Details:
  Subject: CN=flasharray.example.com,O=Example Corp,C=US
  Issuer: CN=Example Corp CA,O=Example Corp,C=US
  Valid From: 2024-01-15T08:30:00Z
  Valid Until: 2025-01-15T08:30:00Z
  Fingerprint (SHA256): a7:b2:c4:d9:e1:f3:2a:5b:7c:8d:9e:0f:1a:2b:3c:4d:5e:6f:7a:8b
  Serial Number: 0x1A2B3C4D5E6F7A8B

Certificate installation successful.
New certificate will be active after array restart.
Restart required: yes
```

!!! warning "Common errors"
    **`Error: Certificate file not found at <path_to_cert_pem>`** — Verify the file path is correct and readable with `ls -la <path_to_cert_pem>`.
    **`Error: Invalid PEM format - certificate and/or private key malformed`** — Ensure the PEM file contains both the certificate block (-----BEGIN CERTIFICATE-----) and private key block (-----BEGIN PRIVATE KEY-----) with no extra whitespace.
    **`Error: Private key does not match certificate`** — Regenerate the combined.pem file ensuring the certificate and its corresponding private key are concatenated in the correct order.
```bash
# List connected remote arrays
purearray list --connection

# Show protection group replication targets and their connection status
purepgroup list --replication
```


```text title="Expected output"
Name                          Address           Connection
================================ ================= ==========
prod-array-01.dc1.local      192.168.1.50      connected
prod-array-02.dc1.local      192.168.1.51      connected
dr-array-west.dc2.local      10.20.30.40       connected
backup-array-vault.dc3.local 172.16.50.100     disconnected

Name                          Targets                    Status
================================ ========================== ===========
pg-database-prod              dr-array-west              synced
pg-database-prod              backup-array-vault         lagged
pg-vmware-cluster             prod-array-02              synced
pg-vmware-cluster             dr-array-west              synced
pg-file-services             backup-array-vault         disconnected
```

!!! warning "Common errors"
    **`Error: Connection refused — check array IP/hostname and network connectivity`** — Verify the array address is reachable with `ping` and confirm firewall rules allow port 443.
    **`Error: Authentication failed — invalid credentials`** — Re-authenticate using `purearray login` with correct management credentials.
    **`Error: No replication targets configured`** — Ensure protection groups have replication policies defined via the Pure management console or API.
---

## See also

- [FlashArray — Hardening](../hardening/)
- [FlashArray — Authentication](../authentication/)
- [FlashArray — Access Control](../access-control/)
