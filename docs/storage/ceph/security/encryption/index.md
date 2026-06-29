---
tags:
  - ceph
  - security
---
# Ceph — Encryption

<div class="kb-summary">
Ceph encryption: OSD-level dmcrypt for data at rest, RBD image encryption per-image, RGW server-side encryption with KMS, and in-transit encryption via messenger v2.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

A: "OSD at-rest\ndm-crypt / LUKS" {shape: rectangle}
B: "Key stored in\nMON KV store" {shape: rectangle}
C: "cephadm generates\nrandom LUKS key per OSD" {shape: rectangle}
D: "In-transit\nmsgr2 secure mode" {shape: rectangle}
E: "AES-GCM encryption\nall daemon connections" {shape: rectangle}
F: "Enable: ms_cluster_mode secure\nms_service_mode secure" {shape: rectangle}
H: "H" {shape: rectangle}
I: "SSE-S3\nCeph-managed keys" {shape: rectangle}
J: "SSE-KMS\nHashiCorp Vault" {shape: rectangle}
K: "SSE-C\nClient-provided key" {shape: rectangle}
G: "RGW SSE\nObject-level encryption" {shape: rectangle}

A -> B
B -> C
D -> E
E -> F
H -> I
H -> J
H -> K
```

```d2
direction: down

osd_encryption_at_rest_dmcrypt_cepha: "OSD Encryption at Rest (dmcrypt / cephadm)" {shape: rectangle}
dmcrypt_key_management: "dm-crypt Key Management" {shape: rectangle}
verify_osd_encryption_status: "Verify OSD Encryption Status" {shape: rectangle}
rbd_image_encryption: "RBD Image Encryption" {shape: rectangle}
rgw_serverside_encryption_sse: "RGW Server-Side Encryption (SSE)" {shape: rectangle}
encryption_options_summary: "Encryption Options Summary" {shape: rectangle}

osd_encryption_at_rest_dmcrypt_cepha -> dmcrypt_key_management: hardens
dmcrypt_key_management -> verify_osd_encryption_status: hardens
verify_osd_encryption_status -> rbd_image_encryption: hardens
rbd_image_encryption -> rgw_serverside_encryption_sse: hardens
rgw_serverside_encryption_sse -> encryption_options_summary: hardens
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## OSD Encryption at Rest (dmcrypt / cephadm)

OSD encryption uses dm-crypt (Linux kernel) to encrypt the block device. Must be configured at OSD creation time — cannot encrypt existing OSDs without destroying and re-creating them.

```bash
# Enable encryption for all available devices at provision time
ceph orch apply osd --all-available-devices --data-encrypt

# Or per OSD specification file (preferred for production):
cat > osd-spec.yaml <<EOF
service_type: osd
service_id: encrypted
placement:
  hosts: [node1, node2, node3]
spec:
  data_devices:
    all: true
  encrypted: true
EOF
ceph orch apply -i osd-spec.yaml

# For a specific device on a single host:
ceph orch daemon add osd ceph-node1:/dev/sdb --encrypted
```

## dm-crypt Key Management

cephadm generates a unique random LUKS key per OSD. Keys are stored in the MON KV store — no external KMS is required, but the MON quorum must remain intact or encrypted OSDs cannot be unlocked.

```bash
# Retrieve LUKS key for a specific OSD (requires admin caps)
ceph config-key get dm-crypt/osd/<id>/luks

# List all stored dm-crypt keys
ceph config-key dump | grep dm-crypt

# Back up all dm-crypt keys for escrow (store in vault or secure offline storage)
ceph config-key dump | grep dm-crypt > /secure-backup/ceph-luks-keys-$(date +%F).json

# Verify encryption is active on a running OSD
cryptsetup status /dev/mapper/ceph-<uuid>
# Output shows: cipher aes-xts-plain64, keysize 512 bits, mode rw
```

> **Critical**: if all MONs are lost, encrypted OSD data is unrecoverable. Always maintain MON quorum and back up MON keyrings separately from the cluster.

## See also

- [Ceph — Hardening](../hardening/)
- [Ceph — Health Checks](../../operations/health-checks/)

## Verify OSD Encryption Status

```bash
# Check OSD spec shows encrypted flag
ceph orch ls --service-type osd --format yaml | grep -A5 encrypted

# On OSD host: verify LUKS header present on device
cryptsetup isLuks /dev/sdb && echo "LUKS encrypted" || echo "Not encrypted"

# List all LUKS-encrypted mapper devices on a node
dmsetup ls --target crypt
```

## RBD Image Encryption

```bash
# Per-image encryption (Quincy+) — encrypt specific RBD images
# Useful when you need client-managed keys (not cluster-managed)

# Create a passphrase-based encrypted image
rbd create rbd/encrypted-vol --size 100G
rbd encryption format rbd/encrypted-vol luks2 --passphrase-file /root/secret.key

# Open encrypted image for use
rbd encryption open rbd/encrypted-vol --passphrase-file /root/secret.key

# Map the opened image as a block device
rbd map rbd/encrypted-vol
# Note: encryption metadata is stored in the image itself; the Ceph cluster is unaware of the key.
```

## RGW Server-Side Encryption (SSE)

### SSE-S3: Ceph-Managed Keys

```bash
# Enable SSE-S3 (Ceph manages the keys)
ceph config set client.rgw.myorg rgw_crypt_require_ssl true
ceph config set client.rgw.myorg rgw_crypt_s3_kms_backend secrettable

# Upload object with SSE-S3 (client sends encryption request header)
aws s3 cp myfile.dat s3://mybucket/myfile.dat \
  --endpoint-url https://rgw.ceph.local:443 \
  --sse AES256
```

### SSE-KMS: HashiCorp Vault-Backed Keys

```bash
# Configure Vault integration in ceph.conf / config DB
ceph config set client.rgw.myorg rgw_crypt_s3_kms_backend vault
ceph config set client.rgw.myorg rgw_crypt_vault_addr https://vault.example.com:8200
ceph config set client.rgw.myorg rgw_crypt_vault_auth token
ceph config set client.rgw.myorg rgw_crypt_vault_token_file /etc/ceph/vault-token

# Client sends KMS header with key reference
aws s3 cp myfile.dat s3://mybucket/myfile.dat \
  --endpoint-url https://rgw.ceph.local:443 \
  --sse aws:kms \
  --sse-kms-key-id vault-key-id
```

### SSE-C: Client-Provided Keys

```bash
# Client supplies the encryption key with every request
# Ceph applies the key for encryption/decryption but never stores it
aws s3 cp myfile.dat s3://mybucket/myfile.dat \
  --endpoint-url https://rgw.ceph.local:443 \
  --sse-c AES256 \
  --sse-c-key fileb:///path/to/32-byte-key.bin

# Client MUST supply the same key for every subsequent GET; Ceph cannot recover data without it
```

## Encryption Options Summary

| Option | Scope | Key management | Perf impact | Use case |
|---|---|---|---|---|
| OSD dmcrypt | All cluster data at rest | MON KV store (LUKS key per OSD) | ~1–3% (AES-NI) | Disk theft / decommission protection |
| RBD image encrypt | Single RBD image | Client-held passphrase | ~3–5% | Tenant isolation, client-side key control |
| RGW SSE-S3 | Object data in RGW | Ceph-managed per-object DEK | ~2–4% | S3-compatible object encryption, simple config |
| RGW SSE-KMS | Object data in RGW | External KMS (Vault) wraps DEK | ~2–4% + KMS latency | Compliance, centralized key governance |
| RGW SSE-C | Object data in RGW | Client provides key per request | ~2–4% | Client retains full key custody |
| msgr2 secure | All in-transit data | Session keys negotiated per connection | ~5–10% | MITM protection on cluster/public networks |

## Messenger v2 (In-Transit Encryption)

```bash
# Enable encryption for all connections
ceph config set global ms_cluster_mode secure    # OSD-to-OSD (cluster network)
ceph config set global ms_service_mode secure    # client-to-OSD
ceph config set global ms_client_mode secure     # client connections
ceph config set global ms_mon_cluster_mode secure  # MON-to-MON

# Disable legacy msgr1 to prevent downgrade attacks
ceph config set global ms_bind_msgr1 false

# Verify connections use secure mode
ceph config get mon ms_cluster_mode
# Expected: secure
```

## Encryption Deployment Checklist

| Step | Check | Command |
|---|---|---|
| OSD encryption enabled at creation | `--data-encrypt` flag in OSD spec | `ceph orch ls --service-type osd -f yaml \| grep encrypted` |
| LUKS key backup exists | dm-crypt keys exported to escrow | `ceph config-key dump \| grep dm-crypt` |
| LUKS headers present on devices | `isLuks` check on OSD disks | `cryptsetup isLuks /dev/sdb` |
| msgr2 secure mode active | All modes set to secure | `ceph config get mon ms_cluster_mode` |
| msgr1 disabled | No legacy port binding | `ceph config get global ms_bind_msgr1` |
| RGW HTTPS enforced | `rgw_crypt_require_ssl true` | `ceph config get client.rgw rgw_crypt_require_ssl` |
| RGW SSE configured | Backend set for object encryption | `ceph config get client.rgw rgw_crypt_s3_kms_backend` |

## Key Management Recommendations

For clusters processing regulated data (PCI-DSS, HIPAA, FedRAMP):

- **OSD keys**: back up MON KV store dm-crypt keys offline in addition to the cluster; loss of all MONs = unrecoverable OSD data.
- **RGW SSE-KMS**: use HashiCorp Vault with HSM-backed keys; enable Vault audit logging for all key access events.
- **Key rotation schedule**: rotate `client.admin` and service account keys quarterly; rotate RGW KMS KEK annually or after any suspected compromise.
- **Backup encryption**: if backing up with Ceph snapshots, ensure backup destination also uses encryption at rest.

```bash
# Verify Vault connectivity for RGW SSE-KMS
curl -s -H "X-Vault-Token: $(cat /etc/ceph/vault-token)" \
  https://vault.example.com:8200/v1/sys/health | python3 -m json.tool | grep initialized

# Check RGW encryption config
ceph config get client.rgw rgw_crypt_vault_addr
ceph config get client.rgw rgw_crypt_s3_kms_backend
```

## Performance Impact Reference

| Encryption type | CPU overhead | Throughput impact | Notes |
|---|---|---|---|
| OSD dm-crypt (AES-NI) | ~1–3% | Negligible on modern CPUs | Always on once configured |
| RBD image encrypt (LUKS2) | ~3–5% | Small; per-image overhead | Client CPU bears the cost |
| RGW SSE-S3 | ~2–4% | Per-object encrypt/decrypt | CPU overhead on RGW nodes |
| RGW SSE-KMS | ~2–4% + KMS latency | KMS RTT adds per-object latency | Keep KMS co-located |
| msgr2 secure (AES-GCM) | ~5–10% | Most impactful on cluster network | Enable on cluster net first |
