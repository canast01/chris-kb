# FlashBlade — Components

> Part of the [FlashBlade Architecture](../) reference.

---

## Core Components

| Component | Description |
|---|---|
| Blades | Individual storage nodes within the chassis; each blade contains NVMe flash and dedicated compute; capacity scales by adding blades |
| Fabric Modules (FM) | Internal high-speed interconnect cards in the chassis; redundant FMs provide fault tolerance; all blades communicate through the FMs |
| Chassis | Physical enclosure holding up to 15 blades (//S) or 10 blades (//E series) plus Fabric Modules, power supplies, and management hardware |
| Purity//FB OS | Operating system running across all blades; manages data services including deduplication, compression, snapshots, replication, and protocol serving |
| Pure1 cloud management | SaaS monitoring, capacity forecasting, upgrade scheduling, and AI analytics — same platform as FlashArray |
| ActiveDR | Asynchronous replication for filesystems and object store to a remote FlashBlade for disaster recovery |
| ActiveCluster (FB) | Synchronous replication for filesystems between two FlashBlade arrays for zero-RPO failover (Purity//FB 4.x+) |
| SafeMode snapshots | Immutable, admin-delete-locked snapshots for ransomware protection |

---

## File Services

FlashBlade provides NFS and SMB file services through managed file systems.

### List File Systems

```bash
purefb fs list
purefb fs list --all    # includes destroyed
```

### Create a File System

```bash
# NFS file system
purefb fs create --name <fs_name> --size 10T --nfs-v3-enabled true --nfs-v4-1-enabled true

# SMB file system
purefb fs create --name <fs_name> --size 10T --smb-enabled true
```

### Manage NFS Exports

```bash
# Show NFS export rules for a file system
purefb fs list <fs_name> --nfs

# Set NFS export rules
purefb fs update <fs_name> \
    --nfs-rules "*(rw,no_root_squash)" \
    --nfs-v3-enabled true \
    --nfs-v4-1-enabled true
```

### Manage SMB Shares

```bash
# Enable SMB on a file system
purefb fs update <fs_name> --smb-enabled true

# SMB shares are accessible at \\<VIP_FQDN>\<fs_name>
```

### Resize a File System

```bash
purefb fs update <fs_name> --size 20T
```

### Mount Points (Client Side)

```bash
# NFS mount from a Linux client
mount -t nfs <FlashBlade_VIP>:/<fs_name> /mnt/<mountpoint>

# NFSv4.1 mount
mount -t nfs4 -o minorversion=1 <FlashBlade_VIP>:/<fs_name> /mnt/<mountpoint>
```

### Destroy and Eradicate a File System

```bash
# Destroy (recoverable for 24 hours)
purefb fs destroy <fs_name>

# Eradicate permanently
purefb fs eradicate <fs_name>
```

---

## Object Services (S3)

FlashBlade provides S3-compatible object storage through object store accounts, buckets, and access keys.

### List Buckets

```bash
purefb bucket list
```

### Create a Bucket

```bash
purefb bucket create --name <bucket_name> --account <account_name>
```

### Manage Object Store Accounts

```bash
# List accounts
purefb object-store-account list

# Create an account
purefb object-store-account create --name <account_name>

# Delete an account (all buckets must be empty)
purefb object-store-account destroy --name <account_name>
```

### Manage Object Store Users

```bash
# List users
purefb object-store-user list

# Create a user
purefb object-store-user create --name <user_name> --account <account_name>

# Delete a user
purefb object-store-user destroy --name <user_name> --account <account_name>
```

### Access Keys

```bash
# List access keys
purefb object-store-access-key list

# Create an access key for a user
purefb object-store-access-key create --user <user_name>/<account_name>
```

The output provides the `access_key_id` and `secret_access_key` — save the secret immediately (it is not retrievable later).

### S3 Client Access

```bash
# Configure AWS CLI to point at FlashBlade S3 endpoint
aws configure
# Set: access key, secret key, region (any string), output format

aws s3 ls --endpoint-url https://<flashblade_s3_vip>/
aws s3 cp local_file.txt s3://<bucket_name>/ --endpoint-url https://<flashblade_s3_vip>/
```

### Destroy and Eradicate a Bucket

```bash
# Destroy (bucket must be empty)
purefb bucket destroy --name <bucket_name>

# Eradicate
purefb bucket eradicate --name <bucket_name>
```
