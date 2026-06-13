---
tags:
  - dell
  - operations
---
# Dell ECS — CLI Reference


<div class="kb-summary">
ECS administration is split across three interfaces: the **ECS Management Shell** (`ecscli`), the **ECS Management REST API** (port 4443), and the **S3-compatible object API** (port 9020 HTTP / 9021 HTTPS).
</div>
```text
┌────────────────────────────────────── Dell ECS — CLI Reference ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            ECS CLI: command-line interface for all management and operational tasks           │   │
│   │            Access: SSH or REST client to management IP; authenticate as admin role            │   │
│   │        Commands: status, list, create, modify, delete, show, and diagnostic operations        │   │
│   │          Scripting: use REST API or CLI in automation for provisioning and reporting          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH → authenticate → show status → configure → verify → log output                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Node            │  │        x86 appliance        │  │        Shared-nothing       │   │
│   │         Storage pool        │  │          Node group         │  │        Erasure coded        │   │
│   │             VDC             │  │          Virtual DC         │  │        Per-site unit        │   │
│   │          Rep. group         │  │          Multi-VDC          │  │        Geo redundancy       │   │
│   │            Bucket           │  │       Object container      │  │        S3/Swift/Blob        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Category     │     Command      │      Purpose      │      Output      │      Notes       │   │
│   │      Status      │   show status    │    Health check   │   State/alerts   │    Daily run     │   │
│   │       List       │     list all     │     Inventory     │   Name/ID/size   │    Read-only     │   │
│   │      Create      │  create volume   │     Provision     │    New object    │    Change req    │   │
│   │      Delete      │ delete resource  │    Decommission   │   Confirmation   │   Irreversible   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ECS appliance nodes · 10/25 GbE backend network · commodity SAS drives                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ECS                = Elastic Cloud Storage; Dell S3-compatible object store for unstructured data  │
│    VDC                = Virtual Data Center; group of ECS nodes at a single geographic site           │
│    Storage pool       = collection of nodes within a VDC; defines the erasure coding domain           │
│    Replication group  = links VDCs for geo-redundant object storage; 3-way replication                │
│    Bucket             = top-level S3 namespace; equivalent to S3 bucket or Azure container            │
│    Erasure coding     = data protection scheme; default 12+4 provides 4-drive fault tolerance         │
│    Namespace          = tenant-level isolation; multiple tenants share a single ECS cluster           │
│    CAS                = Content Addressed Storage; fixed-content object storage with WORM support     │
│    Replication factor = number of VDC copies; 3-way geo-replication for maximum durability            │
│    Atmos API          = legacy Dell Atmos-compatible API; supported for migration from Atmos systems  │
│    HDFS connector     = ECS Hadoop connector; ECS appears as HDFS namespace for analytics jobs        │
│    Quota              = per-namespace or per-bucket storage quota; enforced as hard or soft limit     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
