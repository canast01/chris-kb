---
tags:
  - dell
  - security
description: "Encryption reference covering Overview, Data at Rest Encryption (D@RE), Data in Flight Encryption — SRDF Encryption, Management Traffic — TLS Encryption..."
---
# PowerMax — Encryption

<div class="kb-summary">
Encryption reference covering Overview, Data at Rest Encryption (D@RE), Data in Flight Encryption — SRDF Encryption, Management Traffic — TLS Encryption, Encryption Key Rotation and 2 more sections.

*Applies to: PowerMax 2500 / 8500*
</div>
![PowerMax — Encryption](../../../../../assets/storage-dell-powermax-security-encryption.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Overview

PowerMax provides encryption at three layers: data at rest on NVMe drives, data in flight over SRDF replication links, and management traffic over TLS. All three layers are independently configurable. Data at Rest Encryption (D@RE) is enabled by factory default on PowerMax 2000 and 8000 systems; replication encryption and management TLS require explicit configuration to enforce strong settings.

![Overview](../../../../../assets/storage-dell-powermax-security-encryption-mermaid-svg.svg)

## Data at Rest Encryption (D@RE)

PowerMax implements D@RE using AES-256 hardware encryption on every NVMe drive. Encryption is transparent to hosts and applications — no performance impact, no configuration required on the host side.

### How D@RE Works

- Every NVMe drive in the array has an embedded encryption engine.
- Data is encrypted before being written to the drive media and decrypted on read.
- Encryption keys are managed per drive (DEK — Data Encryption Key) and wrapped by a Key Encryption Key (KEK) held in the array's key management system.
- When a drive is removed from the array, the DEK is inaccessible without the KEK; the data on the drive is cryptographically unrecoverable.
- Drive retirement and secure disposal do not require physical destruction — a cryptographic erase (key destruction) renders drive data unrecoverable instantly.

### Confirming D@RE Status

```bash
# Check encryption status via Unisphere REST API
curl -sk -u admin:password \
  https://<unisphere-host>:8443/univmax/restapi/100/system/symmetrix/<SID> \
  | python3 -m json.tool | grep -i "encry"

# Check D@RE status via SYMCLI
symcfg -sid <SID> show | grep -i "encrypt\|D@RE\|dare"

# Verify encryption on a specific storage resource pool
symcfg -sid <SID> list -srp | grep -i "encrypt"

# Via Unisphere GUI:
# System → Hardware → Drives → select a drive → Properties → Encryption: Enabled
```


```text title="Expected output"
{
  "symmetrixId": "000123456789",
  "encryptionCapable": true,
  "encryptionEnabled": true,
  "encryptionStatus": "Enabled",
  "dareEnabled": true,
  "keyManagementServer": "kms.example.com:5696"
}

Symmetrix ID: 000123456789
Symmetrix Mode: PowerMax
D@RE (Data at Rest Encryption): Enabled
Encryption Status: Active
Encryption Capable: Yes

Storage Resource Pool (SRP): SRP_001
  Encryption: Enabled
  D@RE Status: Active
  Encrypted Drives: 960/960

Storage Resource Pool (SRP): SRP_002
  Encryption: Enabled
  D@RE Status: Active
  Encrypted Drives: 480/480
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification, or import the Unisphere certificate into your system's CA bundle.
    **`symcfg: Command not found`** — Install the EMC Solutions Enabler (SE) package or ensure the SYMCLI bin directory is in your PATH environment variable.
    **`Authentication failed: Invalid credentials`** — Verify the admin username and password are correct and the account has not been locked after failed login attempts.
### Key Management Modes

| Mode | Description | Use Case |
|---|---|---|
| Embedded EKMS | Built-in key management service on the array | Default; suitable for environments without an external KMIP server |
| External KMIP | Key management integrated with an external server (e.g., Thales CipherTrust, Vormetric, Entrust KeyControl) | Required for regulatory compliance programs that mandate external key custody |

### KMIP Integration

External KMIP (Key Management Interoperability Protocol) server integration allows you to manage encryption keys independently of the array, enabling:
- Centralized key rotation across multiple arrays
- Separation of duties between storage admin and security admin for key custody
- Key escrow and audit logging in the external key manager

#### KMIP Configuration Steps

1. Provision a KMIP server (Thales CipherTrust, Entrust KeyControl, or equivalent) and create a KMIP client certificate for the PowerMax array.
2. In Unisphere: **Settings → Security → Encryption Key Management → Add KMIP Server**.
3. Enter the KMIP server address and port (typically `5696`).
4. Upload the KMIP client certificate and CA certificate chain.
5. Test connectivity — Unisphere will attempt a KMIP `Discover` operation.
6. Configure key creation policy on the KMIP server: algorithm AES, length 256, usage mask = Encrypt + Decrypt.
7. Initiate a key rotation on the array to migrate from embedded EKMS to the external KMIP server.

#### KMIP Server Requirements

| Requirement | Specification |
|---|---|
| Protocol version | KMIP 1.1 or later |
| Transport | TLS 1.2 or 1.3 (mandatory) |
| Default port | 5696 |
| Certificate | Mutual TLS (mTLS); array presents client cert, KMIP server presents server cert |
| High availability | KMIP server must be highly available; array cannot decrypt data if KMIP is unreachable |
| Key type | AES-256 symmetric |

> **Critical:** If an external KMIP server becomes unreachable, the array cannot retrieve KEKs to decrypt drive data for new I/O. Ensure the KMIP server has redundant nodes and that the management network path to the KMIP server is fault-tolerant. Test KMIP HA failover before placing the integration into production.

### Drive Retirement and Cryptographic Erase

When retiring a failed or end-of-life drive:

```bash
# Initiate cryptographic erase (key destruction) on a specific physical drive
# This is typically done via Unisphere when removing a drive from an enclosure
# Unisphere → System → Hardware → Drive Bay → select drive → Cryptographic Erase

# Via SYMCLI (requires StorageAdmin or Administrator role):
sympd -sid <SID> erase <pd_name> -noprompt

# Verify the drive shows as erased (all data unrecoverable)
sympd show <pd_name> -sid <SID> | grep -i "erase\|state"
```


```text title="Expected output"
Cryptographic Erase initiated on physical drive DA.10B.0
Erase Status: In Progress
Estimated Time to Completion: 2 minutes 45 seconds

Physical Drive DA.10B.0
State: Erasing
Erase Status: In Progress (87%)
Last Updated: 2024-01-15 14:32:18
Erase Completion Time: 2024-01-15 14:35:03

Physical Drive DA.10B.0
State: Erased
Erase Status: Complete
Data Recovery Probability: 0.00%
Last Updated: 2024-01-15 14:35:18
```

!!! warning "Common errors"
    **`Error: Drive DA.10B.0 is in use by RAID group RG_001`** — Remove the drive from the RAID group or hot-spare pool using `symrdf` or Unisphere before initiating cryptographic erase.
    **`Error: Insufficient privileges. User does not have StorageAdmin role`** — Request StorageAdmin or Administrator role assignment from your Unisphere security administrator.
    **`Error: Physical drive DA.10B.0 not found in array <SID>`** — Verify the SID and drive name are correct using `sympd list -sid <SID>`.
After cryptographic erase, drives can be returned to Dell or disposed of via standard e-waste without additional physical destruction. Document the erase event for compliance records.

## Data in Flight Encryption — SRDF Encryption

SRDF replication traffic traverses WAN links (dark fibre, DWDM, or IP) between sites. Without SRDF encryption, this traffic is protected only by the physical security of the link. SRDF encryption uses AES-256 to encrypt replication traffic at the RDF director level before it leaves the array.

> **Important:** SRDF encryption must be enabled on both the R1 and R2 arrays simultaneously. Mixed encrypted/unencrypted RDF groups are not supported.

### SRDF Encryption Configuration

```bash
# Check current encryption state for an RDF group
symrdf -sid <SID> -rdfg <rdfg_id> list -v | grep -i "encrypt"

# Enable SRDF encryption on an RDF group (both arrays must be at compatible code level)
# This is a disruptive operation — suspend SRDF first
symrdf -sid <SID> -rdfg <rdfg_id> suspend -noprompt

# Configure encryption via Unisphere:
# SRDF → RDF Groups → select RDFG → Edit → Enable Encryption

# Or via SYMCLI:
symrdf -sid <SID> -rdfg <rdfg_id> set -encrypt enable -noprompt

# Resume replication after enabling encryption
symrdf -sid <SID> -rdfg <rdfg_id> resume -noprompt

# Verify encryption is active
symrdf -sid <SID> -rdfg <rdfg_id> list -v | grep -i "encrypt"
```


```text title="Expected output"
RDF Group ID: 001, Symmetrix ID: 000123456789012
    Encryption: Disabled
    Encryption Cipher: AES
    Encryption Key Server: Not Configured

RDF Group 001 suspended successfully.

(no output — command completes silently)

RDF Group 001 resumed successfully.

RDF Group ID: 001, Symmetrix ID: 000123456789012
    Encryption: Enabled
    Encryption Cipher: AES
    Encryption Key Server: 10.50.20.15:5696
    Encryption Status: Active
```

!!! warning "Common errors"
    **`SYMCLI ERROR: RDF group 001 is not in a valid state for this operation`** — Suspend the RDF group with `symrdf -sid <SID> -rdfg <rdfg_id> suspend -noprompt` before attempting to enable encryption.
    **`SYMCLI ERROR: Remote array code level incompatible for encryption`** — Upgrade both the local and remote array to the same compatible firmware level before enabling SRDF encryption.
    **`SYMCLI ERROR: Encryption key server unreachable or not configured`** — Configure a valid KMIP key server in Unisphere under System → Security → Key Servers before enabling encryption.
### SRDF Encryption Scope

| SRDF Mode | Encryption Support | Notes |
|---|---|---|
| SRDF/S (Synchronous) | Supported | Encrypts all synchronous write data in flight |
| SRDF/A (Asynchronous) | Supported | Encrypts all asynchronous delta set transmissions |
| SRDF/Metro | Supported | Encrypts active-active metro writes |
| SRDF/IP | Supported | Especially important — IP links are more exposed than FC dark fibre |
| SRDF/FC (dark fibre) | Optional | Physical dark fibre may be considered adequately secured; evaluate per policy |

### When to Enable SRDF Encryption

| Scenario | Recommendation |
|---|---|
| SRDF over leased DWDM or dark fibre between owned data centres | Optional; assess physical security of the fibre path |
| SRDF/IP over MPLS or internet-connected WAN | Required — IP transport cannot be assumed secure |
| SRDF to a co-location facility | Required — shared physical infrastructure |
| SRDF to a cloud provider (SRDF/IP) | Required |
| Regulatory compliance (PCI-DSS, HIPAA, GDPR) | Required regardless of link type |

## Management Traffic — TLS Encryption

All Unisphere for PowerMax management traffic (GUI and REST API) is transported over HTTPS using TLS. Solutions Enabler network daemon traffic (SYMAPI) also supports TLS.

### Unisphere TLS Configuration

| Setting | Recommended Value | Location |
|---|---|---|
| Minimum TLS version | TLS 1.2 | Unisphere → Settings → Security → TLS |
| Maximum TLS version | TLS 1.3 | (automatic if server and client both support it) |
| Disabled protocols | TLS 1.0, TLS 1.1, SSL 3.0 | These must be explicitly disabled |
| Cipher suites | ECDHE-RSA-AES256-GCM-SHA384, ECDHE-RSA-AES128-GCM-SHA256 | Disable RC4, 3DES, and NULL cipher suites |
| Certificate | CA-signed (internal CA or public CA) | Replace default self-signed certificate |

```bash
# Verify TLS version in use from a management host
openssl s_client -connect <unisphere-host>:8443 -tls1_2 2>&1 | grep "Protocol"
openssl s_client -connect <unisphere-host>:8443 -tls1_3 2>&1 | grep "Protocol"

# Confirm TLS 1.0 is disabled (should fail)
openssl s_client -connect <unisphere-host>:8443 -tls1 2>&1 | grep "handshake failure\|no protocols"

# List accepted cipher suites
nmap --script ssl-enum-ciphers -p 8443 <unisphere-host>

# Check certificate details
echo | openssl s_client -connect <unisphere-host>:8443 2>/dev/null \
  | openssl x509 -noout -text | grep -E "Subject:|Issuer:|Not After:|Subject Alternative"
```


```text title="Expected output"
Protocol  : TLSv1.2
Protocol  : TLSv1.3
connect: Connection refused
Nmap scan report for unisphere-prod.lab.local (192.168.45.220)
Host is up (0.042s latency).
PORT     STATE SERVICE
8443/tcp open  https-alt
| ssl-enum-ciphers: 
|   TLSv1.2: 
|     ciphers: 
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (secp256r1) - A
|       TLS_RSA_WITH_AES_256_GCM_SHA384 - A
|   TLSv1.3: 
|     ciphers: 
|       TLS_AES_256_GCM_SHA384 (secp256r1) - A
Subject: CN=unisphere-prod.lab.local,O=Dell Technologies,C=US
Issuer: CN=Dell EMC Root CA,O=Dell Technologies,C=US
Not After : Dec 15 18:32:44 2026 GMT
Subject Alternative Name: DNS:unisphere-prod.lab.local, DNS:*.lab.local, IP:192.168.45.220
```

!!! warning "Common errors"
    **`connect: Connection refused`** — Verify the Unisphere host is reachable and port 8443 is open with `telnet <unisphere-host> 8443` or check firewall rules.
    **`unable to load client cert`** — Ensure you have network connectivity to the Unisphere host and it is not blocking the management host's IP address.
    **`no protocols available`** — Confirm nmap is installed with `nmap --version` and that the ssl-enum-ciphers script is present in `/usr/share/nmap/scripts/`.
### SYMAPI Daemon TLS (Solutions Enabler)

The SYMAPI network daemon supports TLS for client-to-daemon communication. Enable in the `netcnfg` file:

```bash
# /var/symapi/config/netcnfg — SECURE flag enables TLS
SYMAPI_SERVER - 192.168.1.10 - 000123456789 - 2707 SECURE

# Verify daemon is listening on TLS-enabled port
netstat -tlnp | grep 2707

# Test TLS connection to the SYMAPI daemon
openssl s_client -connect 192.168.1.10:2707 2>&1 | grep -E "Protocol|Cipher"
```


```text title="Expected output"
tcp        0      0 192.168.1.10:2707      0.0.0.0:*               LISTEN      4521/symapid
Protocol  : TLSv1.2
Cipher    : ECDHE-RSA-AES256-GCM-SHA384
```

!!! warning "Common errors"
    **`netstat: command not found`** — Use `ss -tlnp | grep 2707` on modern Linux distributions where netstat is deprecated.
    **`connect: Connection refused`** — Verify the SYMAPI daemon is running with `systemctl status symapid` and check that port 2707 is not blocked by firewall rules.
    **`CERTIFICATE_VERIFY_FAILED`** — Add `-CAfile /var/symapi/config/ca.pem` to the openssl command or use `-insecure` flag for testing self-signed certificates.
## Encryption Key Rotation

Regular key rotation limits the exposure window of any compromised key.

### Embedded EKMS Key Rotation

```bash
# Initiate a key rotation on the embedded EKMS
# This is typically done via Unisphere:
# Settings → Security → Encryption Key Management → Rotate Keys

# Monitor key rotation progress
symcfg -sid <SID> show | grep -i "key\|rotation"

# Key rotation is non-disruptive — production I/O continues during rotation
# Each drive's DEK is re-wrapped with the new KEK without decrypting/re-encrypting drive media
```


```text title="Expected output"
Symmetrix ID: 000297123456789
                                    Symmetrix Capabilities
                                    =====================
Symmetrix Model        : PowerMax 8000
Microcode Version      : 5978.669.669
Symmetrix Serial Number: 000297123456789
Symmetrix SCSI ID      : 0
Symmetrix WWN          : 50:00:14:40:5d:e2:b1:23

Encryption Status      : Enabled
Key Encryption Key (KEK) Status: Active
Key Rotation Status    : In Progress (87% complete)
Last Key Rotation      : 2024-01-15 14:32:18
Next Scheduled Rotation: 2024-04-15 00:00:00
Drives Processed       : 847/974
Estimated Time Remaining: 18 minutes
```

!!! warning "Common errors"
    **`symcfg: Command not found`** — Ensure Symmetrix CLI tools are installed and the `$PATH` includes the Unisphere installation directory (typically `/opt/emc/SYMCLI/bin`).
    **`No such Symmetrix: <SID>`** — Verify the SID value is correct and the array is discoverable by running `symcfg discover` first.
    **`Key rotation already in progress`** — Wait for the current rotation to complete before initiating a new one, or contact EMC support if the rotation is stalled beyond the estimated time window.
### External KMIP Key Rotation

When using an external KMIP server, key rotation is initiated from the KMIP server's management interface:

1. In the KMIP server (e.g., Thales CipherTrust), create a new key for the PowerMax array.
2. Associate the new key with the array's KMIP client registration.
3. Initiate key rotation from Unisphere (Settings → Security → Encryption Key Management → Rotate).
4. Unisphere contacts the KMIP server, retrieves the new KEK, and re-wraps all drive DEKs.
5. Retain the old key in the KMIP server for at least 30 days after rotation (in case of rollback requirement).
6. Archive the old key after 30 days; do not delete it until you are confident the new key is validated across all drives.

## Compliance Reference

| Framework | Applicable Control | PowerMax Capability |
|---|---|---|
| PCI-DSS v4.0 | Req 3.5: Render PAN unreadable anywhere it is stored | D@RE (AES-256) satisfies this for cardholder data stored on PowerMax volumes |
| PCI-DSS v4.0 | Req 4.2.1: Strong cryptography for data in transit | SRDF encryption (AES-256) + TLS 1.2/1.3 for management traffic |
| HIPAA § 164.312(a)(2)(iv) | Encryption and decryption — addressable safeguard for ePHI | D@RE + SRDF encryption satisfy this as a technical safeguard |
| HIPAA § 164.312(e)(2)(ii) | Encryption of ePHI in transit | SRDF encryption for replication; TLS for management |
| NIST 800-53 Rev 5 | SC-28: Protection of information at rest | D@RE with AES-256 maps directly to this control |
| NIST 800-53 Rev 5 | SC-8: Transmission confidentiality and integrity | SRDF encryption + TLS management traffic |
| GDPR Article 32 | Appropriate technical measures including encryption | D@RE and SRDF encryption as pseudonymization/encryption controls |
| ISO 27001:2022 | A.8.24: Use of cryptography | D@RE, SRDF encryption, TLS management, and KMIP key management |
| FIPS 140-2 | Cryptographic module validation | PowerMax D@RE uses FIPS 140-2 validated cryptographic modules (confirm specific firmware level with Dell) |

## Encryption Verification Checklist

| Item | Verification Command / Location | Expected Result |
|---|---|---|
| D@RE enabled on all drives | `symcfg -sid <SID> show \| grep -i encrypt` | `Encryption: Enabled` |
| KMIP connectivity (if external) | Unisphere → Settings → Security → Encryption | Status: Connected |
| SRDF encryption enabled (WAN links) | `symrdf -sid <SID> -rdfg <id> list -v \| grep -i encrypt` | `Encryption: Enabled` |
| TLS 1.0 disabled on Unisphere | `openssl s_client -connect host:8443 -tls1` | Handshake failure |
| TLS 1.2 functional | `openssl s_client -connect host:8443 -tls1_2` | Handshake success |
| CA-signed certificate installed | `openssl s_client -connect host:8443 \| openssl x509 -noout -issuer` | Shows internal or public CA, not self-signed |
| Management cipher strength | `nmap --script ssl-enum-ciphers -p 8443 host` | Only strong GCM ciphers listed |
| SYMAPI daemon TLS enabled | `grep SECURE /var/symapi/config/netcnfg` | SECURE flag present |

---

## See also

- [Powermax — Hardening](../hardening/)
- [Powermax — Authentication](../authentication/)
- [Powermax — Access Control](../access-control/)
