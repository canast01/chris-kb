---
tags:
  - dell
  - operations
description: "ECS administration is split across three interfaces: the ECS Management Shell (ecscli), the ECS Management REST API (port 4443), and the S3-compatible..."
---
# Dell ECS — CLI Reference

<div class="kb-summary">
ECS administration is split across three interfaces: the **ECS Management Shell** (`ecscli`), the **ECS Management REST API** (port 4443), and the **S3-compatible object API** (port 9020 HTTP / 9021 HTTPS).

*Applies to: ECS 3.x*
</div>
![Dell ECS — CLI Reference](../../../../../assets/storage-dell-ecs-operations-cli-reference.svg)

 For system-level diagnostics, SSH access to individual nodes is also available.

> **Management API base URL**: `https://<ecs-node>:4443`
> **S3 endpoint**: `https://<ecs-node>:9021` (virtual-hosted or path-style)
> **SSH node access**: `ssh admin@<ecs-node>` (use `viprexec` for cluster-wide commands)

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Quick-Reference Command Table

| Command | Purpose |
|---|---|
| `ecscli login -u sysadmin -p <pass> -e <ecs-node>` | Authenticate ecscli session |
| `ecscli namespace list` | List all namespaces |
| `ecscli bucket list --namespace <ns>` | List buckets in a namespace |
| `curl -s -k -u sysadmin:<pass> https://<node>:4443/login -D -` | Get REST API auth token |
| `curl ... GET /vdc/capacity` | VDC total/used/available capacity |
| `curl ... GET /vdc/nodes` | All nodes and health status |
| `curl ... GET /vdc/alerts` | Active alerts |
| `aws s3 ls s3://<bucket> --endpoint-url https://<node>:9021` | List S3 objects |
| `aws s3api list-buckets --endpoint-url https://<node>:9021` | List all S3 buckets |
| `viprexec -v -cmd "df -h /data/"` | Disk usage on all nodes |

---

## ECS Management Shell (ecscli)

`ecscli` is a Python-based CLI that wraps the ECS Management REST API. Install it on a management workstation or use it from the ECS node directly.

```bash
# Install (requires Python 3 + pip)
pip install ecscli

# --- Authentication ---
# Login and store session token (~/.ecscli/session)
ecscli login \
  -u sysadmin \
  -p '<password>' \
  -e <ecs-node>

# Verify login (shows currently authenticated user)
ecscli user whoami

# Logout / invalidate token
ecscli logout

# --- Namespace management ---
# List all namespaces
ecscli namespace list

# Show namespace details (quota, replication group, retention)
ecscli namespace get --name <namespace>

# Create a namespace
ecscli namespace create \
  --name app_team_ns \
  --replication-group <rg-id> \
  --is-stale-allowed true

# --- Bucket management ---
# List buckets in a namespace
ecscli bucket list --namespace <namespace>

# Show bucket details (versioning, quota, replication group, owner)
ecscli bucket get --namespace <namespace> --name <bucket>

# Create a bucket
ecscli bucket create \
  --namespace <namespace> \
  --name app-data-bucket \
  --replication-group <rg-id> \
  --versioning-enabled false

# Enable versioning on an existing bucket
ecscli bucket update \
  --namespace <namespace> \
  --name app-data-bucket \
  --versioning-enabled true

# Set a bucket quota (in GB)
ecscli bucket update \
  --namespace <namespace> \
  --name app-data-bucket \
  --quota 5000

# Delete a bucket (must be empty)
ecscli bucket delete --namespace <namespace> --name app-data-bucket

# --- Object users / IAM ---
# List object users in a namespace
ecscli user list-object-users --namespace <namespace>

# Create an object user (S3 access)
ecscli user create --namespace <namespace> --name svc_app_backup

# Generate S3 access keys for a user
ecscli user secret-key create \
  --namespace <namespace> \
  --name svc_app_backup

# List user's secret keys (shows key IDs only, not values)
ecscli user secret-key list \
  --namespace <namespace> \
  --name svc_app_backup

# Delete a secret key
ecscli user secret-key delete \
  --namespace <namespace> \
  --name svc_app_backup \
  --secret-key <key_id>
```


```text title="Expected output"
Collecting ecscli
  Downloading ecscli-2.4.1-py3-none-any.whl (156 kB)
Installing collected packages: ecscli
Successfully installed ecscli-2.4.1
Login successful. Session token stored in ~/.ecscli/session
Currently authenticated as: sysadmin
Logout successful. Session token invalidated.
Namespace List:
  app_team_ns          (replication_group: rg-prod-01, stale_allowed: true)
  backup_ns            (replication_group: rg-prod-01, stale_allowed: false)
  archive_ns           (replication_group: rg-dr-02, stale_allowed: true)
Namespace Details for 'app_team_ns':
  Name: app_team_ns
  Replication Group: rg-prod-01
  Retention: 0 days
  Quota: unlimited
Namespace 'app_team_ns' created successfully.
Bucket List (namespace: app_team_ns):
  app-data-bucket      (size: 2.3 TB, versioning: false)
  logs-bucket          (size: 156 GB, versioning: true)
Bucket Details for 'app-data-bucket':
  Name: app-data-bucket
  Owner: sysadmin
  Versioning: false
  Quota: 5000 GB
  Replication Group: rg-prod-01
Bucket 'app-data-bucket' created successfully.
Bucket 'app-data-bucket' updated: versioning enabled.
Bucket 'app-data-bucket' quota set to 5000 GB.
Bucket 'app-data-bucket' deleted successfully.
Object Users (namespace: app_team_ns):
  svc_app_backup       (created: 2024-01-15, uid: 3a8f2c91-d4e1-4b7f-9e2a-1c5d8f3b2a9e)
  svc_monitoring       (created: 2024-01-10, uid: 7b2e9f1a-c3d5-4a8e-8f1b-2d6c9a4e3f7b)
Object user 'svc_app_backup' created successfully.
Secret key created for user 'svc_app_backup':
  Access Key ID: 8F7C2A9E1B4D5F3C
  Secret Access Key: xK9mL2pQ7vW5nR8sT1uY4zX6cV3bN0jH (save this securely)
Secret Keys for user 'svc_app_backup':
  8F7C2A9E1B4D5F3C    (created: 2024-01-20, status: active)
  3D6E9F2A1C4B7E5H    (created: 2024-01-10, status: active)
Secret key '8F7C2A9E1B4D5F3C' deleted successfully.
```

!!! warning "Common errors"
    **`Error: Authentication failed. Invalid credentials or ECS node unreachable.`** — Verify the ECS node hostname/IP is correct, the user exists, and the password is accurate;
---

## S3 API (aws cli / s3cmd)

ECS is fully S3-compatible. Use the standard AWS CLI or s3cmd pointed at the ECS endpoint.

```bash
# --- AWS CLI configuration for ECS ---
# Configure a named profile for ECS
aws configure --profile ecs
# AWS Access Key ID:     <object_user_access_key>
# AWS Secret Access Key: <object_user_secret_key>
# Default region:        us-east-1  (arbitrary; ECS ignores region)
# Default output format: json

# All commands below use: --endpoint-url https://<ecs-node>:9021 --profile ecs
# Add --no-verify-ssl if using self-signed certificates

ECS_EP="https://<ecs-node>:9021"
PROFILE="--profile ecs --endpoint-url $ECS_EP --no-verify-ssl"

# --- Bucket operations ---
# List all buckets
aws s3api list-buckets $PROFILE

# Create a bucket
aws s3api create-bucket --bucket new-bucket $PROFILE

# Get bucket location
aws s3api get-bucket-location --bucket app-data-bucket $PROFILE

# --- Object operations ---
# List objects in a bucket (top level)
aws s3 ls s3://app-data-bucket $PROFILE

# List objects recursively with sizes
aws s3 ls s3://app-data-bucket --recursive --human-readable $PROFILE

# Upload a file
aws s3 cp /local/path/file.tar.gz s3://app-data-bucket/backups/ $PROFILE

# Upload an entire directory (recursive)
aws s3 sync /local/backup/ s3://app-data-bucket/backups/ $PROFILE

# Download an object
aws s3 cp s3://app-data-bucket/backups/file.tar.gz /local/restore/ $PROFILE

# Delete an object
aws s3 rm s3://app-data-bucket/backups/file.tar.gz $PROFILE

# Delete a bucket and all its contents
aws s3 rb s3://app-data-bucket --force $PROFILE

# --- Versioning ---
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket app-data-bucket \
  --versioning-configuration Status=Enabled $PROFILE

# List object versions (including delete markers)
aws s3api list-object-versions --bucket app-data-bucket $PROFILE

# Abort incomplete multipart uploads (cleans orphaned upload capacity)
aws s3api list-multipart-uploads --bucket app-data-bucket $PROFILE
aws s3api abort-multipart-upload \
  --bucket app-data-bucket \
  --key backups/largefile.tar.gz \
  --upload-id <UploadId> $PROFILE

# --- Lifecycle policy (expire old versions after 90 days) ---
aws s3api put-bucket-lifecycle-configuration \
  --bucket app-data-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "expire-old-versions",
      "Status": "Enabled",
      "Filter": {"Prefix": ""},
      "NoncurrentVersionExpiration": {"NoncurrentDays": 90}
    }]
  }' $PROFILE
```


```text title="Expected output"
AWS Access Key ID [None]: 
AWS Secret Access Key [None]: 
Default region name [None]: us-east-1
Default output format [None]: json

{
    "Buckets": [
        {
            "Name": "app-data-bucket",
            "CreationDate": "2024-01-15T08:32:14.000Z"
        },
        {
            "Name": "backup-archive",
            "CreationDate": "2024-02-03T11:47:22.000Z"
        },
        {
            "Name": "new-bucket",
            "CreationDate": "2024-02-20T14:19:05.000Z"
        }
    ],
    "Owner": {
        "DisplayName": "object_user",
        "ID": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
    }
}

{
    "LocationConstraint": "us-east-1"
}

2024-02-20 09:15:32    4.2 GiB backups/
2024-02-19 14:22:18  512.0 MiB configs/
2024-02-18 16:45:01    1.1 GiB logs/

2024-02-20 09:15:32    4.2 GiB backups/file.tar.gz
2024-02-20 08:30:15    256.0 MiB backups/file-old.tar.gz
2024-02-19 14:22:18    512.0 MiB configs/app.conf
2024-02-18 16:45:01    1.1 GiB logs/system.log
...

upload: /local/path/file.tar.gz to s3://app-data-bucket/backups/file.tar.gz

Completed 12 of 15 files with 4.8 GiB transferred
upload: /local/backup/db-dump.sql to s3://app-data-bucket/backups/db-dump.sql
upload: /local/backup/config.yaml to s3://app-data-bucket/backups/config.yaml
Completed 15 of 15 files with 8.3 GiB transferred

download: s3://app-data-bucket/backups/file.tar.gz to /local/restore/file.tar.gz

delete: s3://app-data-bucket/backups/file.tar.gz

remove_bucket: app-data-bucket

(no output — command completes silently)

{
    "Versions": [
        {
            "ETag": "\"a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6\"",
            "Size": 4294967296,
            "StorageClass": "STANDARD",
            "Key": "backups/file.tar.gz",
            "VersionId": "v1708420532000",
            "IsLatest": true,
            "LastModified": "2024-02-20T09:15:32.000Z"
        },
        {
            "ETag": "\"b2c3d
```
---

## Object Store Admin API (curl)

The ECS Management REST API runs on port 4443. All requests after login require the `X-SDS-AUTH-TOKEN` header.

```bash
ECS="https://<ecs-node>:4443"
PASS="<sysadmin_password>"

# --- Authentication ---
# Get auth token (returned in response header X-SDS-AUTH-TOKEN)
TOKEN=$(curl -s -k -u "sysadmin:${PASS}" \
  "${ECS}/login" -D - | grep "X-SDS-AUTH-TOKEN" | awk '{print $2}' | tr -d '\r')

AUTH="-H \"X-SDS-AUTH-TOKEN: ${TOKEN}\""

# --- Capacity ---
# Get VDC capacity (totalProvisioned_GB, totalFree_GB, usedStorageCapacity_GB)
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/vdc/capacity" | python3 -m json.tool

# --- Node status ---
# List all nodes with health state
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/vdc/nodes" | python3 -m json.tool

# Get details for a specific node
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/vdc/nodes/<node-id>" | python3 -m json.tool

# --- Alerts ---
# List active alerts
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/vdc/alerts" | python3 -m json.tool

# --- Namespaces ---
# Create a namespace
curl -s -k -X POST \
  -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${ECS}/object/namespaces/namespace" \
  -d '{
    "id": "app_team_ns",
    "default_data_services_vpool": "<replication-group-id>",
    "is_stale_allowed": true,
    "is_compliance_enabled": false
  }' | python3 -m json.tool

# List all namespaces
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/object/namespaces" | python3 -m json.tool

# --- Buckets ---
# List buckets in a namespace
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/object/bucket?namespace=app_team_ns" | python3 -m json.tool

# Get bucket details
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/object/bucket/app-data-bucket/info?namespace=app_team_ns" | python3 -m json.tool

# --- Replication groups ---
# List replication groups (Virtual Data Center pools)
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/vdc/data-service/vpools" | python3 -m json.tool

# --- Logout ---
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/logout"
```


```text title="Expected output"
HTTP/1.1 200 OK
X-SDS-AUTH-TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzeXNhZG1pbiIsImV4cCI6MTcwOTMxNjgwMH0.abc123def456
{
  "totalProvisioned_GB": 50000,
  "totalFree_GB": 12450,
  "usedStorageCapacity_GB": 37550
}
{
  "nodes": [
    {
      "id": "ecs-node-01.corp.local",
      "health": "Good",
      "version": "3.6.1.0.1234",
      "ip_address": "192.168.1.101"
    },
    {
      "id": "ecs-node-02.corp.local",
      "health": "Good",
      "version": "3.6.1.0.1234",
      "ip_address": "192.168.1.102"
    }
  ]
}
{
  "id": "ecs-node-01.corp.local",
  "health": "Good",
  "cpu_usage_percent": 34.2,
  "memory_usage_percent": 58.7,
  "disk_usage_percent": 75.1
}
{
  "alerts": [
    {
      "id": "alert-5f8c2a1b",
      "severity": "Warning",
      "message": "Disk usage above 75% on ecs-node-03",
      "timestamp": "2024-03-01T14:32:15Z"
    }
  ]
}
{
  "id": "app_team_ns",
  "default_data_services_vpool": "vpool-prod-01",
  "is_stale_allowed": true,
  "is_compliance_enabled": false,
  "created": "2024-03-01T14:35:22Z"
}
{
  "namespaces": [
    {
      "id": "app_team_ns",
      "created": "2024-03-01T14:35:22Z"
    },
    {
      "id": "legacy_ns",
      "created": "2023-11-15T09:12:44Z"
    }
  ]
}
{
  "buckets": [
    {
      "name": "app-data-bucket",
      "created": "2024-02-28T10:15:33Z",
      "size_bytes": 2147483648
    }
  ]
}
{
  "name": "app-data-bucket",
  "namespace": "app_team_ns",
  "size_bytes": 2147483648,
  "object_count": 1024,
  "versioning_enabled": false
}
{
  "vpools": [
    {
      "id": "vpool-prod-01",
      "name": "Production-Replication",
      "replication_factor": 3,
      "status": "Active"
    },
    {
      "id
```
---

## System CLI (SSH — Node-Level Access)

For hardware diagnostics and low-level checks, SSH to an individual node as `admin` or `root`.

```bash
# SSH to an ECS node
ssh admin@<ecs-node>

# Check disk usage on the data partition
df -h /data/

# Check all mount points
df -h

# Check data disk status (ECS uses XFS on large raw disks)
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,STATE

# --- viprexec: run a command on ALL nodes in the cluster ---
# Show disk usage on every node simultaneously
viprexec -v -cmd "df -h /data/"

# Show uptime on all nodes
viprexec -v -cmd "uptime"

# Check ECS service status on all nodes
viprexec -v -cmd "service storageos status"

# Restart ECS services on all nodes (use with caution)
viprexec -v -cmd "service storageos restart"

# --- Per-node service checks ---
# Check all running ECS Java processes
ps aux | grep -i ecs

# View current ECS node log
tail -f /opt/emc/caspian/fabric/agent/logs/agent.log

# View storageos service log
journalctl -u storageos -f

# Check NTP sync status (ECS nodes are time-sensitive)
chronyc tracking
timedatectl status
```


```text title="Expected output"
admin@ecs-node-01:~$ df -h /data/
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       7.3T  4.2T  3.1T  58% /data

admin@ecs-node-01:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       512M  128M  384M  25% /boot
/dev/sda2        50G   18G   32G  36% /
/dev/sda3       7.3T  4.2T  3.1T  58% /data
tmpfs           7.8G     0  7.8G   0% /dev/shm

admin@ecs-node-01:~$ lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,STATE
NAME    SIZE FSTYPE MOUNTPOINT STATE
sda     7.3T                   running
├─sda1  512M ext4   /boot      running
├─sda2   50G ext4   /          running
└─sda3  7.3T xfs    /data      running
sdb     7.3T xfs    /data2     running

admin@ecs-node-01:~$ viprexec -v -cmd "df -h /data/"
ecs-node-01: /dev/sda3 7.3T 4.2T 3.1T 58% /data
ecs-node-02: /dev/sda3 7.3T 3.9T 3.4T 54% /data
ecs-node-03: /dev/sda3 7.3T 4.5T 2.8T 62% /data

admin@ecs-node-01:~$ viprexec -v -cmd "uptime"
ecs-node-01:  14:32:18 up 187 days, 3:42, 2 users, load average: 2.14, 1.87, 1.92
ecs-node-02:  14:32:19 up 185 days, 8:15, 1 user,  load average: 1.43, 1.51, 1.68
ecs-node-03:  14:32:18 up 189 days, 1:03, 2 users, load average: 3.21, 2.94, 2.87

admin@ecs-node-01:~$ viprexec -v -cmd "service storageos status"
ecs-node-01: ● storageos.service - EMC ECS StorageOS
   Loaded: loaded (/etc/systemd/system/storageos.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2024-01-10 08:15:22 UTC; 6 days ago
ecs-node-02: ● storageos.service - EMC ECS StorageOS
   Active: active (running) since Wed 2024-01-10 08:16:05 UTC; 6 days ago
ecs-node-03: ● storageos.service - EMC ECS StorageOS
   Active: active (running) since Wed 2024-
```
---

## Common Troubleshooting Commands

```bash
# --- dtquery: check data table / chunk health ---
# Run from any ECS node as root (internal diagnostic tool)
ssh root@<ecs-node>

# Query chunk status for a specific object
/opt/storageos/tools/dtquery query --type CHUNK --id <chunk-id>

# --- Cassandra (ECS metadata store) health ---
# Check Cassandra ring status from a node
/opt/storageos/tools/nodetool status

# Check Cassandra compaction stats
/opt/storageos/tools/nodetool compactionstats

# Flush Cassandra memtables to disk
/opt/storageos/tools/nodetool flush

# Check Cassandra heap usage
/opt/storageos/tools/nodetool info | grep -i heap

# --- ZooKeeper (ECS coordination service) health ---
# Check ZooKeeper cluster status from a node
echo "stat" | nc localhost 2181

# List ZooKeeper ensemble members
echo "conf" | nc localhost 2181

# Check ZooKeeper leader/follower role
echo "srvr" | nc localhost 2181 | grep Mode

# --- Geo-replication lag (REST API) ---
curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/vdc/geo-replication/status" | python3 -m json.tool

# --- Check S3 endpoint responsiveness ---
curl -sv --max-time 10 \
  "https://<ecs-node>:9021/" \
  --resolve "<ecs-node>:9021:<ecs-node-ip>" 2>&1 | grep -E "< HTTP|Connected|SSL"

# --- ECS log collection (for Dell Support) ---
# Trigger diagnostic bundle from Management API
curl -s -k -X POST \
  -H "X-SDS-AUTH-TOKEN: ${TOKEN}" \
  "${ECS}/vdc/support-bundle" | python3 -m json.tool
```


```text title="Expected output"
root@ecs-node-01:~# /opt/storageos/tools/dtquery query --type CHUNK --id 0x00a4c8f2e1b9d7c3
Chunk ID: 0x00a4c8f2e1b9d7c3
Status: HEALTHY
Replication Factor: 3
Replicas: [ecs-node-01, ecs-node-02, ecs-node-03]
Last Modified: 2024-01-15T14:32:18Z

root@ecs-node-01:~# /opt/storageos/tools/nodetool status
Datacenter: us-east-1
===============================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address          Load       Tokens  Owns (effective)  Host ID
UN  192.168.1.101    256.42 KB  256     33.3%             a7f2c1e8-9d4b-4a2f-b1c3-8e9f2d4a6b7c
UN  192.168.1.102    251.88 KB  256     33.3%             b8g3d2f9-0e5c-5b3g-c2d4-9f0g3e5b7c8d
UN  192.168.1.103    248.15 KB  256     33.4%             c9h4e3g0-1f6d-6c4h-d3e5-0g1h4f6c8d9e

root@ecs-node-01:~# /opt/storageos/tools/nodetool compactionstats
pending tasks: 0
Active compaction remaining time :   0h00m00s

root@ecs-node-01:~# /opt/storageos/tools/nodetool flush
Flushing keyspace system...
Flushing keyspace system_auth...
Flushing keyspace system_distributed...

root@ecs-node-01:~# /opt/storageos/tools/nodetool info | grep -i heap
Heap Memory (MB)        : 4096.00 / 8192.00

root@ecs-node-01:~# echo "stat" | nc localhost 2181
Zookeeper version: 3.4.13-2d71af4dbe22557fda74f9a9a4309dee, built on 06/29/2018 12:17 GMT
Latency min/avg/max: 0/1/45
Received: 18472
Sent: 18491
Mode: follower
Node count: 847

root@ecs-node-01:~# echo "conf" | nc localhost 2181
server.1=ecs-zk-01:2888:3888
server.2=ecs-zk-02:2888:3888
server.3=ecs-zk-03:2888:3888

root@ecs-node-01:~# echo "srvr" | nc localhost 2181 | grep Mode
Mode: follower

root@ecs-node-01:~# curl -s -k -H "X-SDS-AUTH-TOKEN: ${TOKEN}" "${ECS
```
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Ecs — Procedures](../procedures/)
- [Ecs — Scripts](../scripts/)
- [Ecs — Health Checks](../health-checks/)
