---
tags:
  - ceph
  - security
description: "Ceph encryption: OSD-level dmcrypt for data at rest, RBD image encryption per-image, RGW server-side encryption with KMS, and in-transit encryption via..."
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


```text title="Expected output"
Scheduling OSD deployment with encryption enabled
Scheduled osd.encrypted update for host [node1,node2,node3]
Created OSD spec from osd-spec.yaml
Deploying OSDs with dmcrypt encryption
  node1: osd.0 (sda) - encrypted
  node2: osd.1 (sdb) - encrypted
  node3: osd.2 (sdc) - encrypted
Waiting for encrypted OSD daemons to start...
osd.0: up and in
osd.1: up and in
osd.2: up and in
All OSDs successfully deployed with encryption
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error EINVAL: invalid spec: service_type 'osd' requires 'placement' or 'unmanaged: true'` | Add a `placement` section to the spec or set `unmanaged: true` if managing OSDs manually. |
    | `Error: No available devices found on hosts [node1, node2, node3]` | Verify devices exist and are not already in use with `ceph orch device ls`, and ensure hosts are in the cluster with `ceph orch host ls`. |
    | `Error: --encrypted flag requires Ceph version Octopus or later` | Upgrade Ceph to Octopus (v15.2.0+) or later, as encryption support was added in that release. |
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


```text title="Expected output"
dm-crypt/osd/0/luks: AQDvK2Zl7x9mFRAAp8q3Z+Kw9L2m4vQ8xY5nJg==
dm-crypt/osd/1/luks: AQDvK2Zl7x9mFRAAp8q3Z+Kw9L2m4vQ8xY5nJh==
dm-crypt/osd/2/luks: AQDvK2Zl7x9mFRAAp8q3Z+Kw9L2m4vQ8xY5nJi==
dm-crypt/osd/3/luks: AQDvK2Zl7x9mFRAAp8q3Z+Kw9L2m4vQ8xY5nJj==
(no output — command completes silently)
/secure-backup/ceph-luks-keys-2024-01-15.json
/dev/mapper/ceph-a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6 is active.
  type:    LUKS2
  cipher:  aes-xts-plain64
  keysize: 512 bits
  mode:    rw
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: permission denied` | Ensure your Ceph client has admin capabilities by checking your keyring and using `ceph auth list` to verify permissions. |
    | `error: No such file or directory` | Verify the OSD ID exists and the device mapper path is correct by running `ls /dev/mapper/ceph-*` to list active encrypted volumes. |
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


```text title="Expected output"
service_type: osd
service_id: default
placement:
  hosts:
  - osd-node-01
  - osd-node-02
encrypted: true
data_devices:
  paths:
  - /dev/sdb
  - /dev/sdc
LUKS encrypted
crypt-osd-sdb-a7f2e91c	(253, 0)
crypt-osd-sdc-b3d4f82e	(253, 1)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Command 'cryptsetup' not found` | Install cryptsetup with `apt-get install cryptsetup` (Debian/Ubuntu) or `yum install cryptsetup` (RHEL/CentOS). |
    | `Device /dev/sdb does not contain a LUKS header` | Verify the correct device path with `lsblk` and ensure the OSD was deployed with encryption enabled in the spec. |
    | `No such device or address` | Confirm the device exists and is accessible on the OSD host with `lsblk` before running cryptsetup. |
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


```text title="Expected output"
rbd: create 2024-01-15 10:23:45.123456 7f8a9c2d1e4b INFO: creating image
100G
rbd: format 2024-01-15 10:23:46.987654 7f8a9c2d1e4b INFO: encryption format luks2 applied
rbd: open 2024-01-15 10:23:47.654321 7f8a9c2d1e4b INFO: image opened successfully
/dev/rbd0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `rbd: error: image rbd/encrypted-vol already exists` | Delete the existing image with `rbd rm rbd/encrypted-vol` or use a different image name. |
    | `rbd: error: unable to read passphrase file /root/secret.key: No such file or directory` | Create the passphrase file first with `echo 'your-passphrase' > /root/secret.key && chmod 600 /root/secret.key`. |
    | `rbd: error: image rbd/encrypted-vol is not encrypted or encryption format not recognized` | Ensure the image was formatted with `rbd encryption format` before attempting to open it. |
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


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
upload: ./myfile.dat to s3://mybucket/myfile.dat
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error putting object: InvalidArgument: The Ceph RGW server does not support the requested encryption method.` | Verify that `rgw_crypt_s3_kms_backend` is set to a supported backend (e.g., `vault`, `barbican`, or `secrettable`) and that the RGW daemon has been restarted after the config change. |
    | `error: Unable to locate credentials` | Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables with valid RGW user credentials. |
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


```text title="Expected output"
set client.rgw.myorg rgw_crypt_s3_kms_backend vault
set client.rgw.myorg rgw_crypt_vault_addr https://vault.example.com:8200
set client.rgw.myorg rgw_crypt_vault_auth token
set client.rgw.myorg rgw_crypt_vault_token_file /etc/ceph/vault-token
upload: ./myfile.dat to s3://mybucket/myfile.dat
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: error setting config option 'rgw_crypt_vault_addr': (22) Invalid argument` | Verify the Vault URL is reachable and uses the correct protocol (https://) with valid hostname and port. |
    | `fatal error: An error occurred (InvalidArgument) when calling the PutObject operation: The KMS key ID is invalid or not found` | Ensure the vault-key-id exists in Vault and the RGW service account has read permissions on that key path. |
    | `Error: error setting config option 'rgw_crypt_vault_token_file': (2) No such file or directory` | Create the Vault token file at /etc/ceph/vault-token with appropriate permissions (readable by ceph user) before applying the configuration. |
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


```text title="Expected output"
upload: ./myfile.dat to s3://mybucket/myfile.dat
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidArgument) when calling the PutObject operation: The object was stored using a form of Server Side Encryption. The correct parameters must be provided to retrieve the object.` | Supply the same `--sse-c` and `--sse-c-key` parameters on all subsequent GET/HEAD operations for this object. |
    | `An error occurred (InvalidRequest) when calling the PutObject operation: Bad Request` | Verify the key file exists at the specified path and contains exactly 32 bytes (use `wc -c /path/to/32-byte-key.bin` to confirm). |
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


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
secure
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error EINVAL: ms_cluster_mode is not a valid setting` | Use `ceph config help global` to verify the correct parameter name; the setting may be `ms_cluster_mode` only on specific Ceph versions (14.2.0+). |
    | `Error: unable to get config value: (2) No such file or directory` | Ensure the monitor daemon is running with `ceph -s` and that you have proper authentication credentials in `/etc/ceph/ceph.conf`. |
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


```text title="Expected output"
"initialized": true
rgw_crypt_vault_addr = https://vault.example.com:8200
rgw_crypt_s3_kms_backend = vault
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `--cacert /path/to/vault-ca.crt` to the curl command or use `-k` if testing in non-production. |
    | `Error ENOENT: error reading /etc/ceph/vault-token` | Ensure the Vault token file exists and is readable by the user running the command; regenerate with `ceph config-key put client.rgw/vault-token <token>` if missing. |
## Performance Impact Reference

| Encryption type | CPU overhead | Throughput impact | Notes |
|---|---|---|---|
| OSD dm-crypt (AES-NI) | ~1–3% | Negligible on modern CPUs | Always on once configured |
| RBD image encrypt (LUKS2) | ~3–5% | Small; per-image overhead | Client CPU bears the cost |
| RGW SSE-S3 | ~2–4% | Per-object encrypt/decrypt | CPU overhead on RGW nodes |
| RGW SSE-KMS | ~2–4% + KMS latency | KMS RTT adds per-object latency | Keep KMS co-located |
| msgr2 secure (AES-GCM) | ~5–10% | Most impactful on cluster network | Enable on cluster net first |
