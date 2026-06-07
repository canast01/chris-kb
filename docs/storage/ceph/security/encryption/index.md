# Ceph — Encryption

<div class="kb-summary">
Ceph encryption: OSD-level dmcrypt for data at rest, RBD image encryption per-image, RGW server-side encryption with KMS, and in-transit encryption via messenger v2.
</div>

## OSD Encryption at Rest (dmcrypt)

```bash
# OSD encryption uses dm-crypt (Linux kernel) to encrypt the block device.
# Must be configured at OSD creation time — cannot encrypt existing OSDs.

# Enable encryption for new OSDs via cephadm
ceph orch apply osd --all-available-devices --method raw --encrypt

# Or for specific device:
ceph orch daemon add osd ceph-node1:/dev/sdb --encrypted

# Verify encryption status
ceph osd tree
ceph device ls | grep encrypted
# Encrypted OSDs show "encrypted" in their OSD spec

# Note: encryption keys are stored in the MON keystore.
# If all MONs are lost, encrypted OSDs cannot be recovered.
# Always maintain a MON quorum and backup MON keyrings.
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

# Note: encryption metadata is stored in the image itself.
# The Ceph cluster is unaware of the encryption key.
```

## RGW Server-Side Encryption (S3-SSE)

```bash
# RGW supports SSE-S3 (cluster-managed keys) and SSE-KMS (external KMS).
# Configure SSE-KMS with HashiCorp Vault or AWS KMS.

# Enable SSE-S3 (Ceph manages the keys)
# /etc/ceph/ceph.conf or via config:
ceph config set client.rgw.myorg rgw_crypt_require_ssl true
ceph config set client.rgw.myorg rgw_crypt_s3_kms_backend secrettable

# Upload object with SSE-S3
aws s3 cp myfile.dat s3://mybucket/myfile.dat \
  --endpoint-url http://rgw.ceph.local:7480 \
  --sse AES256

# Upload with SSE-KMS (requires Vault integration)
aws s3 cp myfile.dat s3://mybucket/myfile.dat \
  --endpoint-url http://rgw.ceph.local:7480 \
  --sse aws:kms --sse-kms-key-id vault-key-id
```

## Messenger v2 (In-Transit Encryption)

```bash
# msgr2 protocol (Nautilus+) supports optional encryption for daemon-to-daemon
# and client-to-daemon communication.

# Enable encryption for all connections
ceph config set global ms_cluster_mode secure    # OSD-to-OSD (cluster network)
ceph config set global ms_service_mode secure    # client-to-OSD
ceph config set global ms_mon_cluster_mode secure  # MON-to-MON

# Verify connections use secure mode
ceph -s
# Look for: "mon: ... using msgr2"

# Note: "secure" mode adds AES-GCM overhead (~5-10% throughput reduction).
# "crc" mode (default) provides integrity only, no confidentiality.
ceph config set global ms_cluster_mode crc     # back to integrity-only if needed
```
