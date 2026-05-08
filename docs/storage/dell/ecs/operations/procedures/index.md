# Dell ECS — Procedures

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

## Bucket Management

Dell ECS (Elastic Cloud Storage) uses S3-compatible buckets as the fundamental storage object. Buckets contain objects and have associated policies, retention settings, and replication configuration.

### Bucket Operations

```bash
# List all buckets (using AWS CLI against ECS S3 endpoint)
aws s3 ls s3:// --endpoint-url https://<ecs_s3_endpoint>

# Create a bucket
aws s3 mb s3://<bucket_name> --endpoint-url https://<ecs_s3_endpoint>

# Delete a bucket (must be empty)
aws s3 rb s3://<bucket_name> --endpoint-url https://<ecs_s3_endpoint>
```

### Bucket Policies

ECS supports S3-compatible bucket policies for access control:

```bash
# View a bucket policy
aws s3api get-bucket-policy \
    --bucket <bucket_name> \
    --endpoint-url https://<ecs_s3_endpoint>

# Apply a bucket policy
aws s3api put-bucket-policy \
    --bucket <bucket_name> \
    --policy file://bucket_policy.json \
    --endpoint-url https://<ecs_s3_endpoint>
```

### Object Retention (Compliance)

ECS supports WORM (Write Once, Read Many) object lock for compliance use cases:

```bash
# Check object lock configuration on a bucket
aws s3api get-object-lock-configuration \
    --bucket <bucket_name> \
    --endpoint-url https://<ecs_s3_endpoint>
```

### Bucket ACLs

```bash
# View bucket ACL
aws s3api get-bucket-acl \
    --bucket <bucket_name> \
    --endpoint-url https://<ecs_s3_endpoint>
```

### Capacity Monitoring

| Metric | Check Location |
|---|---|
| Per-bucket usage | ECS Management Console → Monitoring → Bucket Usage |
| Cluster utilisation | ECS Management Console → Dashboard |
| Replication lag | ECS Management Console → Replication Groups |

### Common Operations

| Task | Command |
|---|---|
| List bucket contents | `aws s3 ls s3://<bucket> --endpoint-url ...` |
| Copy object to bucket | `aws s3 cp <file> s3://<bucket>/ --endpoint-url ...` |
| Delete object | `aws s3 rm s3://<bucket>/<key> --endpoint-url ...` |
| Sync local to bucket | `aws s3 sync <local_dir> s3://<bucket>/ --endpoint-url ...` |

## S3 Access

ECS exposes an S3-compatible API endpoint. Any S3-compatible client (AWS CLI, boto3, s3cmd, rclone) can access ECS using its S3 endpoint.

### Connection Details

| Parameter | Value |
|---|---|
| S3 Endpoint | `https://<ecs_s3_vip>` or `https://<ecs_node_ip>` |
| Auth | Access Key / Secret Key (managed in ECS UI or API) |
| TLS | Self-signed cert by default — clients need `--no-verify-ssl` or trusted CA |
| Port | 9020 (HTTP), 9021 (HTTPS) |

### AWS CLI Configuration

```bash
# Configure AWS CLI profile for ECS
aws configure --profile ecs
# AWS Access Key ID: <ecs_access_key>
# AWS Secret Access Key: <ecs_secret_key>
# Default region: us-east-1 (ECS ignores region — use any value)

# Test connectivity
aws s3 ls --profile ecs --endpoint-url https://<ecs_endpoint> --no-verify-ssl
```

### Common S3 Operations

```bash
# List buckets
aws s3 ls \
    --profile ecs \
    --endpoint-url https://<ecs_endpoint> \
    --no-verify-ssl

# List objects in a bucket
aws s3 ls s3://<bucket_name>/ \
    --profile ecs \
    --endpoint-url https://<ecs_endpoint> \
    --no-verify-ssl

# Upload a file
aws s3 cp /local/file s3://<bucket_name>/key \
    --profile ecs \
    --endpoint-url https://<ecs_endpoint> \
    --no-verify-ssl

# Download a file
aws s3 cp s3://<bucket_name>/key /local/destination \
    --profile ecs \
    --endpoint-url https://<ecs_endpoint> \
    --no-verify-ssl

# Sync a directory
aws s3 sync /local/dir s3://<bucket_name>/ \
    --profile ecs \
    --endpoint-url https://<ecs_endpoint> \
    --no-verify-ssl
```

### Access Keys Management

Access keys are created in the ECS Management Console:

- **Manage** → **Users** → select user → **Generate Secret Key**
- Keys can also be created via the ECS REST API

### Namespace and Bucket Paths

ECS organises data into namespaces. Buckets belong to a namespace. The S3 endpoint path style is:

```
https://<ecs_endpoint>/<bucket_name>/<object_key>
```

Some clients support virtual-hosted style:
```
https://<bucket_name>.<ecs_endpoint>/<object_key>
```

### Troubleshooting Access

| Error | Likely Cause | Fix |
|---|---|---|
| `Connection refused` | S3 endpoint down or wrong port | Check port 9021 (HTTPS) or 9020 (HTTP) |
| `SSL certificate error` | Self-signed cert | Use `--no-verify-ssl` or install ECS CA cert |
| `Access Denied` | Wrong access key or bucket policy | Verify key and bucket policy |
| `NoSuchBucket` | Bucket doesn't exist or wrong namespace | Check bucket name and namespace |
| `403 Forbidden` | Bucket policy denies access | Review bucket policy in ECS console |
