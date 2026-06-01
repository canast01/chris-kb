# Dell ECS — Procedures


<div class="kb-summary">
Procedures reference covering Change Readiness, Maintenance Window, Post-Change Validation, Provisioning Flow: Namespace → Bucket → IAM User, Creating a Namespace and 7 more sections.
</div>
```
┌────────────────────────────────── Dell ECS — Operational Procedures ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              ECS operational procedures: standard tasks for day-2 administration              │   │
│   │           Covers: provisioning, expansion, maintenance, DR testing, and decommission          │   │
│   │           Pre/post checks required for all maintenance activities affecting storage           │   │
│   │            All procedures require approved change management tickets in production            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Open change → pre-check → execute → verify → post-check → close                                    │
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
│   │    Procedure     │    Pre-check     │       Steps       │      Verify      │    Post-check    │   │
│   │    Provision     │  Capacity free?  │   Create volume   │   Host access    │   Monitor I/O    │   │
│   │      Expand      │   Pool space?    │    Grow volume    │    FS resize     │   Verify size    │   │
│   │     Snapshot     │   Policy set?    │   Take snapshot   │   Snap listed    │   Consistency    │   │
│   │     Failover     │  Repl. in sync?  │    Break repl.    │    App online    │    Verify RTO    │   │
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


## Change Readiness

Verify these items before performing any change on an ECS cluster — node additions, software upgrades, replication group changes, or VDC configuration updates.

- [ ] All nodes report `GOOD` in ECS Portal or `GET /vdc/nodes` — do not begin an upgrade or node addition while any node is `DEGRADED` or offline
- [ ] No active disk rebuilds: ECS Portal → Hardware → Disks shows no `REBUILDING` disks — a concurrent rebuild during a node upgrade increases rebuild time and risk
- [ ] Geo-replication lag is at zero or within acceptable threshold for all VDC replication groups — confirm in ECS Portal → Geo Monitoring
- [ ] VDC quorum is healthy — all VDC nodes are online and the cluster has quorum before any configuration change
- [ ] Cluster capacity is below 70% — expansion operations and data rebalancing require headroom above the current used level
- [ ] No active alerts of `ERROR` or `CRITICAL` severity: `GET /vdc/alerts` — resolve pre-existing alerts before starting
- [ ] Inform consuming application teams of the maintenance window; confirm S3 application owners are aware if the endpoint may briefly be unavailable
- [ ] For upgrades: verify the target ECS version is a supported upgrade path from the current version in the Dell ECS release notes

| Item | Status | Notes |
|---|---|---|
| All nodes GOOD | | |
| No active disk rebuilds | | |
| Geo-replication lag at zero | | |
| VDC quorum healthy | | |
| Cluster capacity < 70% | | |

## Maintenance Window

Steps for planned maintenance on an ECS cluster — node maintenance, software upgrades, or VDC configuration changes.

1. Confirm the maintenance window and notify all teams consuming S3, Swift, or CAS endpoints from the cluster
2. Confirm all nodes are `GOOD` and geo-replication lag is at zero before starting
3. For node-level maintenance: use ECS Portal → Hardware → Node → Enter Maintenance Mode to safely drain the node before physical access; do not power off a node without placing it in maintenance mode first
4. For a rolling software upgrade: upload the upgrade package via ECS Portal → Settings → Software Update; ECS upgrades one node at a time — do not interrupt the rolling upgrade once started
5. Monitor per-node upgrade progress in the portal; wait for each node to return to `GOOD` state before the upgrade proceeds to the next node
6. If VDC quorum requires attention during the change, follow the Dell ECS quorum recovery procedure — do not attempt manual quorum changes without Dell support guidance
7. After the change, confirm all nodes return to `GOOD` via `GET /vdc/nodes` and geo-replication resumes with no lag
8. Run a functional S3 test from at least one consuming application before closing the maintenance window

## Post-Change Validation

Run these checks after any change to confirm the ECS cluster is healthy and object storage services have resumed.

- [ ] `GET /vdc/nodes` — all nodes report `GOOD`; no nodes remain in `DEGRADED` or maintenance state
- [ ] `GET /vdc/capacity` — capacity metrics are consistent with pre-change baseline; no unexpected increase
- [ ] ECS Portal → Geo Monitoring — geo-replication lag has returned to zero for all VDC replication groups
- [ ] `GET /vdc/alerts` — no new alerts introduced by the change
- [ ] S3 endpoint functional test: `HeadBucket` or `ListBuckets` succeeds from a representative consuming application
- [ ] `ecscli namespace list` — all namespaces accessible and intact
- [ ] ECS Portal → Hardware → Disks — no new `FAILED` or `SUSPECT` disks after the change
- [ ] Application teams confirm S3 workloads are running normally with no authentication or connectivity errors

## Provisioning Flow: Namespace → Bucket → IAM User

```mermaid
graph TD
  START([New application storage request]) --> NS["Create Namespace\necscli namespace create\n+ replication group + hard quota"]
  NS --> BKT["Create Bucket\nS3 name rules · versioning off by default"]
  BKT --> LOCK{Compliance\nor WORM?}
  LOCK -->|Yes| OBJ["Enable Object Lock at\nbucket creation (cannot add later)"]
  LOCK -->|No| USR
  OBJ --> USR["Create Object User\necscli user create\n--namespace --name svc-<app>-<env>"]
  USR --> KEY["Generate Access Key + Secret Key\n(shown once — store in vault immediately)"]
  KEY --> POL["Apply Bucket Policy\nleast-privilege s3 actions only"]
  POL --> LC{Versioning\nenabled?}
  LC -->|Yes| LCP["Add lifecycle policy\nNoncurrentVersionExpiration + MPU abort"]
  LC -->|No| TEST
  LCP --> TEST["Functional test:\naws s3 ls s3://bucket --endpoint-url ..."]
  TEST --> DONE([Bucket ready for application])
  classDef decision fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef term fill:#15803d,stroke:#166534,color:#fff
  class LOCK,LC decision
  class NS,BKT,OBJ,USR,KEY,POL,LCP,TEST action
  class START,DONE term
```

## Creating a Namespace

Namespaces are the top-level multi-tenancy boundary in ECS. Create a separate namespace per team or application workload.

**Via ECS Portal:**
1. Navigate to ECS Portal → Manage → Namespaces → New Namespace
2. Enter a name (lowercase, hyphen-separated; e.g., `analytics-prod`)
3. Select the Replication Group that spans the required VDCs
4. Set a hard quota (recommended; prevents unbounded capacity growth)
5. Configure encryption at rest if the namespace holds regulated data
6. Enable metadata search if object-level search is required (adds indexer overhead)
7. Save; the namespace becomes immediately available for bucket creation

**Via Management REST API:**

```bash
# Create a namespace
curl -s -k -X POST \
  -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://<ecs-node>:4443/object/namespaces/namespace" \
  -d '{
    "id": "analytics-prod",
    "default_data_services_vpool": "<replication-group-id>",
    "is_stale_allowed": true,
    "is_compliance_enabled": false,
    "namespace_quota": {
      "blockSize": 10240,
      "notificationSize": 9216
    }
  }' | python3 -m json.tool

# Verify the namespace was created
ecscli namespace get --name analytics-prod
```

**Namespace configuration parameters:**

| Parameter | Description | Recommendation |
|---|---|---|
| `default_data_services_vpool` | The replication group ID assigned to this namespace | Always specify; do not use the system default |
| `is_stale_allowed` | Allow reads from a VDC that may have stale data during TSF | `true` for HA; `false` for strong consistency |
| `is_compliance_enabled` | Enable CAS compliance mode (immutable write-once) | Enable only for compliance/WORM namespaces |
| `namespace_quota.blockSize` | Hard quota in GB — writes fail when exceeded | Set to expected monthly data volume + 20% buffer |
| `namespace_quota.notificationSize` | Soft quota in GB — alerts are raised when exceeded | Set ~10% below the hard quota |

## Creating a Bucket

Buckets are the S3-visible object containers within a namespace.

**Via ECS Portal:**
1. Navigate to ECS Portal → Manage → Buckets → New Bucket
2. Enter a bucket name (must be S3-compatible: lowercase, 3–63 characters, no dots)
3. Select the parent namespace
4. Choose the replication group (inherits from namespace by default)
5. Configure versioning (default: disabled — enable only if application recovery requirements demand it)
6. Set a bucket quota if finer-grained control than namespace quota is needed
7. Enable Object Lock (WORM) only at bucket creation — cannot be enabled after creation

**Via S3 API or ecscli:**

```bash
# Create a bucket (ecscli)
ecscli bucket create \
  --namespace analytics-prod \
  --name analytics-prod-raw \
  --replication-group <rg-id> \
  --versioning-enabled false

# Create a bucket (S3 API via AWS CLI)
aws s3api create-bucket \
  --bucket analytics-prod-raw \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Enable Object Lock at creation (cannot be enabled post-creation)
aws s3api create-bucket \
  --bucket compliance-immutable \
  --object-lock-enabled-for-bucket \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Set a bucket quota (ecscli)
ecscli bucket update \
  --namespace analytics-prod \
  --name analytics-prod-raw \
  --quota 5000

# Verify bucket configuration
ecscli bucket get --namespace analytics-prod --name analytics-prod-raw
```

**Bucket configuration parameters:**

| Parameter | Description | Default | Recommendation |
|---|---|---|---|
| Versioning | Retain multiple versions of each object key | Disabled | Enable only with a corresponding lifecycle policy to expire non-current versions |
| Object Lock | WORM — objects cannot be deleted or overwritten within retention period | Disabled | Enable at creation for compliance or immutable backup buckets |
| Quota | Hard capacity limit on this bucket in GB | None (namespace quota applies) | Set per bucket for large or fast-growing workloads |
| Replication Group | Which VDCs store this bucket's data | Inherits namespace default | Override only if this bucket has different geo-replication requirements |
| Access Logging | Write access log records to a designated audit bucket | Disabled | Enable for buckets holding regulated or auditable data |

## Creating IAM Object Users and Access Keys

Object users are per-namespace IAM identities. Each application or service should have a dedicated object user.

```mermaid
graph LR
  subgraph "Key Rotation (zero downtime)"
    NEWKEY["1. Create new key\necscli user secret-key create"]
    DEPLOY["2. Deploy new key\nto app / secrets manager"]
    VERIFY["3. Verify app is using\nnew key (access logs)"]
    DELOLD["4. Delete old key\necscli user secret-key delete"]
    NEWKEY --> DEPLOY --> VERIFY --> DELOLD
  end
  note1(["ECS allows up to 2 active keys per user\nenabling zero-downtime rotation"])
  classDef step fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef note fill:#b45309,stroke:#92400e,color:#fff
  class NEWKEY,DEPLOY,VERIFY,DELOLD step
  class note1 note
```

```bash
# Create an object user in a namespace
ecscli user create \
  --namespace analytics-prod \
  --name svc-spark-prod

# Generate a new S3 access key / secret key pair for the user
# NOTE: The secret key is returned once and cannot be retrieved again — store it immediately
ecscli user secret-key create \
  --namespace analytics-prod \
  --name svc-spark-prod

# List object users in a namespace
ecscli user list-object-users --namespace analytics-prod

# List access keys for a user (key IDs only — not the secret values)
ecscli user secret-key list \
  --namespace analytics-prod \
  --name svc-spark-prod

# Key rotation: create new key, deploy it, then delete old key
# 1. Create new key
ecscli user secret-key create --namespace analytics-prod --name svc-spark-prod
# 2. Deploy new key to the application (configuration or secrets manager)
# 3. Confirm application is using new key
# 4. Delete old key
ecscli user secret-key delete \
  --namespace analytics-prod \
  --name svc-spark-prod \
  --secret-key <old-key-id>
```

## Configuring Bucket Lifecycle Policies

Lifecycle policies automate object expiration and version cleanup. Always attach a lifecycle policy to versioned buckets.

```bash
# Apply a lifecycle policy: expire non-current versions after 90 days,
# abort incomplete multipart uploads after 7 days
aws s3api put-bucket-lifecycle-configuration \
  --bucket analytics-prod-raw \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs \
  --lifecycle-configuration '{
    "Rules": [
      {
        "ID": "expire-noncurrent-versions",
        "Status": "Enabled",
        "Filter": {"Prefix": ""},
        "NoncurrentVersionExpiration": {"NoncurrentDays": 90}
      },
      {
        "ID": "abort-incomplete-mpu",
        "Status": "Enabled",
        "Filter": {"Prefix": ""},
        "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}
      }
    ]
  }'

# Verify the lifecycle policy was applied
aws s3api get-bucket-lifecycle-configuration \
  --bucket analytics-prod-raw \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs
```

## Applying Bucket Policies (S3 IAM)

Bucket policies restrict which object users can perform which S3 actions on a bucket.

```bash
# Apply a read-write policy scoped to a specific object user
cat > /tmp/bucket-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAppRW",
      "Effect": "Allow",
      "Principal": {
        "AWS": "urn:ecs:iam::analytics-prod:user/svc-spark-prod"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::analytics-prod-raw",
        "arn:aws:s3:::analytics-prod-raw/*"
      ]
    }
  ]
}
EOF

aws s3api put-bucket-policy \
  --bucket analytics-prod-raw \
  --policy file:///tmp/bucket-policy.json \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# View current bucket policy
aws s3api get-bucket-policy \
  --bucket analytics-prod-raw \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs
```

## Cleaning Up Incomplete Multipart Uploads

Incomplete multipart uploads (MPUs) consume capacity without contributing accessible objects. Clean them up regularly on buckets with high-throughput upload workloads.

```bash
# List incomplete multipart uploads
aws s3api list-multipart-uploads \
  --bucket analytics-prod-raw \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Abort a specific incomplete MPU
aws s3api abort-multipart-upload \
  --bucket analytics-prod-raw \
  --key path/to/large-object.tar.gz \
  --upload-id <UploadId> \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs
```

A lifecycle policy rule with `AbortIncompleteMultipartUpload` (7 days) is the preferred long-term solution over manual cleanup.

## Bucket Management

Dell ECS uses S3-compatible buckets as the fundamental storage object. Buckets contain objects and have associated policies, retention settings, and replication configuration.

### Common Bucket Operations

```bash
# List all buckets accessible to the configured object user
aws s3 ls \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Delete a bucket (must be empty)
aws s3 rb s3://<bucket-name> \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Force-delete a bucket and all its objects (use with caution)
aws s3 rb s3://<bucket-name> --force \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# View bucket ACL
aws s3api get-bucket-acl \
  --bucket <bucket-name> \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Check Object Lock configuration
aws s3api get-object-lock-configuration \
  --bucket <bucket-name> \
  --endpoint-url https://<ecs-s3-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs
```

### Capacity Monitoring

| Metric | Check Location |
|---|---|
| Per-bucket usage | ECS Management Console → Monitoring → Bucket Usage |
| Cluster utilisation | ECS Management Console → Dashboard |
| Replication lag | ECS Management Console → Replication Groups |

### Common Object Operations

| Task | Command |
|---|---|
| List bucket contents | `aws s3 ls s3://<bucket> --endpoint-url ...` |
| Copy object to bucket | `aws s3 cp <file> s3://<bucket>/ --endpoint-url ...` |
| Delete object | `aws s3 rm s3://<bucket>/<key> --endpoint-url ...` |
| Sync local to bucket | `aws s3 sync <local-dir> s3://<bucket>/ --endpoint-url ...` |

## Troubleshooting Access

| Error | Likely Cause | Fix |
|---|---|---|
| `Connection refused` | S3 endpoint down or wrong port | Check port 9021 (HTTPS) or 9020 (HTTP) |
| `SSL certificate error` | Self-signed cert not trusted | Use `--no-verify-ssl` or install ECS CA cert on clients |
| `Access Denied` | Wrong access key or bucket policy | Verify key and check bucket policy in ECS console |
| `NoSuchBucket` | Bucket does not exist or wrong namespace | Check bucket name and namespace assignment |
| `403 Forbidden` | Bucket policy denies access | Review bucket policy: `aws s3api get-bucket-policy ...` |
| `QuotaExceeded` | Bucket or namespace quota reached | Increase quota in ECS Portal or expire old objects |
