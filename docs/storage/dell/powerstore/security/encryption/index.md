# PowerStore — Encryption


<div class="kb-summary">
Encryption reference covering Data-at-Rest Encryption (D@RE), Encryption in Transit, Encryption Compliance Summary.
</div>
```text
┌──────────────────────────────────── Dell PowerStore — Encryption ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PowerStore encryption: data at rest and in transit encryption for all stored data       │   │
│   │          At rest: AES-256 encryption using controller-managed or external key manager         │   │
│   │          In transit: TLS 1.2+ for management; protocol encryption for data in flight          │   │
│   │         Key management: external KMIP-compatible KMS or built-in key lifecycle manager        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Enable encryption → configure KMS → verify → audit → rotate keys                                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Standard     │     Key source    │       KMS        │      Notes       │   │
│   │     At rest      │     AES-256      │     Controller    │  Internal/KMIP   │    Always on     │   │
│   │    In transit    │     TLS 1.2+     │      PKI cert     │   Internal CA    │   Mgmt + data    │   │
│   │   Key rotation   │      Annual      │     KMS policy    │   External KMS   │    Automated     │   │
│   │    Key escrow    │     Required     │     KMS vault     │   External KMS   │    DR access     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Data-at-Rest Encryption (D@RE)

PowerStore encrypts all data at rest using AES-256 encryption at the drive level. D@RE is enabled by default on all PowerStore models and cannot be disabled. Encryption is transparent to hosts — no host-side configuration is required.

### Key Management Architecture

PowerStore D@RE uses a two-tier key hierarchy:

```text
Drive Encryption Keys (DEKs)
  └── Unique per NVMe SSD; generated and stored on the drive controller
Key Encryption Keys (KEKs)
  └── Encrypt the DEKs; held by PowerStore node
      Options:
      ├── Internal Key Management (IKM)  — KEKs stored within PowerStoreOS (default)
      └── External Key Management (EKM)  — KEKs stored in an external KMIP key server
```

### Verify D@RE Status

```bash
# Check encryption status via REST API
curl -k -X GET "https://<mgmt-ip>/api/rest/appliance?select=name,is_encryption_enabled,encryption_mode" \
  -H "DELL-EMC-TOKEN: <token>"

# Expected response for a correctly configured system:
# {
#   "is_encryption_enabled": true,
#   "encryption_mode": "Software"   <- Internal Key Management
# }
# or for external KMIP:
# {
#   "encryption_mode": "KMIP"
# }
```

### Internal Key Management (Default)

By default, PowerStore uses Internal Key Management — the Key Encryption Keys are stored within PowerStoreOS. This provides drive-level encryption (data is unreadable if a drive is physically removed from the appliance) but does not provide appliance-level key separation.

This is acceptable for most environments and is required by FIPS 140-2 at the drive layer (PowerStore uses FIPS 140-2 validated NVMe SSDs).

### External Key Management (KMIP)

For environments requiring centralised key management with separation of duties between storage administration and key administration, configure PowerStore to use an external KMIP key server.

Supported KMIP key servers:

| Product | Vendor | Notes |
|---|---|---|
| Thales CipherTrust Manager (KeySecure) | Thales | Recommended; KMIP 1.1+ |
| Entrust KeyControl (HyTrust) | Entrust | KMIP 1.1+ |
| Vormetric Data Security Manager | Thales | KMIP 1.1+ |
| HashiCorp Vault | HashiCorp | Requires KMIP secrets engine (Enterprise) |
| IBM Security Guardium | IBM | KMIP 1.1+ |

```bash
# Configure KMIP key server
curl -k -X POST "https://<mgmt-ip>/api/rest/kmip_server" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "thales-ciphertrust-prod",
    "address": "192.168.10.100",
    "port": 5696,
    "username": "powerstore-kmip-user",
    "password": "<kmip-service-account-password>",
    "timeout": 30,
    "server_type": "CipherTrust"
  }'

# Verify KMIP connectivity
curl -k -X POST "https://<mgmt-ip>/api/rest/kmip_server/<kmip-id>/verify_connection" \
  -H "DELL-EMC-TOKEN: <token>"

# Switch appliance key management mode to KMIP
# WARNING: This operation is irreversible without a full data migration
# Ensure KMIP server is HA and backed up before switching
curl -k -X POST "https://<mgmt-ip>/api/rest/appliance/<appliance-id>/set_encryption_key_manager" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"kmip_server_id": "<kmip-id>"}'
```

### KMIP Key Rotation

Rotate encryption keys annually (or per your security policy):

```bash
# Rotate the KMIP-managed KEK for the appliance
curl -k -X POST "https://<mgmt-ip>/api/rest/appliance/<appliance-id>/rotate_encryption_key" \
  -H "DELL-EMC-TOKEN: <token>"

# Monitor the rotation job status
curl -k -X GET "https://<mgmt-ip>/api/rest/job?type=encryption_key_rotation" \
  -H "DELL-EMC-TOKEN: <token>"
```

Key rotation does not cause host I/O interruption. The process runs in the background and re-encrypts the DEKs with a new KEK. Duration depends on the number of drives.

### Cryptographic Erase (Drive Sanitisation)

When decommissioning a PowerStore appliance or replacing drives, perform a cryptographic erase to render data unrecoverable:

```bash
# Perform secure erase on a drive (example: failed drive being replaced)
# This invalidates the DEK for the drive — all data becomes permanently unreadable
# PowerStore Manager → Hardware → Drives → select drive → Actions → Erase

# For full appliance decommissioning: Security Erase the entire appliance
# PowerStore Manager → Settings → Security → Secure Erase Appliance
# This operation:
# 1. Deletes all data (volumes, NAS, snapshots)
# 2. Cryptographically erases all drives
# 3. Resets the appliance to factory state
```

After cryptographic erase, drives can be returned to Dell or disposed of without further physical destruction — the data is permanently unrecoverable.

## Encryption in Transit

### Management Plane (HTTPS)

PowerStore Manager and the REST API are served over HTTPS. PowerStore ships with a self-signed certificate — replace it with a CA-signed certificate before production use.

```bash
# Step 1: Generate a CSR
openssl req -new -newkey rsa:4096 -nodes \
  -keyout powerstore.key \
  -out powerstore.csr \
  -subj "/C=GB/ST=London/O=Example Corp/CN=lon01-pstore-001.corp.example.com" \
  -addext "subjectAltName=DNS:lon01-pstore-001.corp.example.com,IP:192.168.10.50"

# Step 2: Submit to internal CA; receive the signed certificate chain

# Step 3: Import certificate via REST API
curl -k -X POST "https://<mgmt-ip>/api/rest/x509_certificate" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "Manager",
    "certificate": "<base64-encoded-cert-chain>",
    "private_key": "<base64-encoded-private-key>",
    "passphrase": ""
  }'

# Step 4: Verify the new certificate is active
echo | openssl s_client -connect <mgmt-ip>:443 2>/dev/null \
  | openssl x509 -noout -issuer -subject -dates
```

| Certificate Parameter | Requirement |
|---|---|
| Key size | RSA 4096 or ECDSA P-256/P-384 |
| Signature algorithm | SHA-256 or stronger |
| SAN | Must include the management FQDN and IP |
| Validity | Maximum 2 years; monitor expiry 30 days before renewal |

### TLS Version and Cipher Configuration

```bash
# Verify TLS 1.0 and 1.1 are disabled (both should fail)
openssl s_client -connect <mgmt-ip>:443 -tls1   2>&1 | grep -i "failure\|error\|handshake"
openssl s_client -connect <mgmt-ip>:443 -tls1_1 2>&1 | grep -i "failure\|error\|handshake"

# Verify TLS 1.2 is functional
openssl s_client -connect <mgmt-ip>:443 -tls1_2 2>&1 | grep Protocol

# Enumerate active cipher suites
nmap --script ssl-enum-ciphers -p 443 <mgmt-ip>
# Acceptable: ECDHE-RSA-AES256-GCM-SHA384, ECDHE-RSA-AES128-GCM-SHA256
# Reject: RC4, 3DES, EXPORT, NULL, MD5
```

Configure TLS settings: PowerStore Manager → **Settings → Security → TLS Configuration**.

### Replication Encryption

Async replication traffic between PowerStore systems is encrypted in transit. The replication link uses TLS on port 443 — the same management port used for REST API communication.

For Metro Volume (synchronous replication), traffic uses the dedicated inter-site link. If this link traverses untrusted network segments (e.g., a third-party MPLS circuit), implement IPsec encryption at the network layer for the inter-site link.

### iSCSI in-Transit Encryption

iSCSI does not natively encrypt data in transit. Options for iSCSI traffic encryption:

| Method | Implementation |
|---|---|
| IPsec | Encrypt at the network layer; requires IPsec-capable switches/routers |
| Dedicated VLAN | Isolate iSCSI traffic on a separate, physically segregated network |
| NVMe-oF (RoCE) | Does not natively encrypt; same isolation approach as iSCSI |

For environments requiring iSCSI encryption, consider switching to Fibre Channel (which is physically isolated by nature of a separate fabric) or NVMe-oF with proper VLAN isolation.

### NFS in-Transit Encryption

Enable Kerberos with privacy (`krb5p`) on NFS exports to encrypt file data in transit. This requires:

1. NAS server joined to Active Directory
2. Kerberos keytab deployed on NAS server
3. NFS export `min_security` set to `krb5p`
4. NFS clients configured for Kerberos authentication

For purely internal file transfers on trusted networks, `sys` security is acceptable; `krb5p` is required if NFS traffic traverses untrusted segments.

## Encryption Compliance Summary

| Framework | Requirement | PowerStore Implementation |
|---|---|---|
| PCI-DSS v4.0 Req 3.5 | Protect primary account numbers with strong cryptography | D@RE with AES-256 on all drives |
| NIST 800-53 SC-28 | Protection of information at rest | D@RE enabled by default; external KMIP for key separation |
| NIST 800-53 SC-8 | Transmission confidentiality | TLS 1.2+ on management plane; replication encrypted |
| NIST 800-53 SC-12 | Cryptographic key establishment | KMIP for centralised key management; annual key rotation |
| ISO 27001 A.8.24 | Use of cryptography | AES-256 at rest; TLS in transit; KMIP for key management |
| HIPAA §164.312(e) | Encryption of ePHI in transit | TLS on management; IPsec or dedicated fabric for data traffic |
| GDPR Art. 32 | Appropriate security measures | D@RE + secure erase for right-to-erasure compliance |
