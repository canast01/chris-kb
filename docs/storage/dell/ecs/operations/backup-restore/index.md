---
tags:
  - dell
  - operations
---
# Dell ECS — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering Overview, Data Durability Model, Configuration Backup, Restoring Object Data, Veeam Backup Integration and 1 more sections.
</div>
```text
┌──────────────────────────────────── Dell ECS — Backup and Restore ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        ECS backup: snapshots, replication, and external backup application integration        │   │
│   │        Snapshot schedule: hourly for 24 h, daily for 7 days, weekly for 4 weeks minimum       │   │
│   │            Replication: async or sync to DR site for off-site data protection copy            │   │
│   │       Restore: volume-level or file-level restore from snapshot; test restore quarterly       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Snapshot → replicate to DR → verify → document → test restore                                      │
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
│   │       Type       │     Schedule     │     Retention     │     Offsite?     │    Test cycle    │   │
│   │     Snapshot     │   Hourly/daily   │    7/30/90 days   │        No        │     Monthly      │   │
│   │   Replication    │  Policy-driven   │     Per policy    │     Yes (DR)     │    Quarterly     │   │
│   │    Backup app    │ Daily full+incr  │      90+ days     │ Yes (tape/cloud  │    Quarterly     │   │
│   │     Archive      │     Monthly      │      7+ years     │   Yes (object)   │      Annual      │   │
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


## Overview

Dell ECS is an object storage platform. Data protection is primarily delivered through:

- **Geo-replication**: Objects are replicated across VDCs via replication groups. This is the primary mechanism for data durability and site-level recovery.
- **Erasure coding**: Within a VDC, objects are protected against disk and node failure through erasure coding (typically 12+4).
- **S3 Object Lock (WORM)**: Immutable retention for compliance and backup data; prevents deletion or overwrite within the retention period.

ECS does not have a traditional backup agent. Configuration backup covers the management layer; data is protected by replication and erasure coding.

## Data Durability Model

```mermaid
graph TD
  subgraph "VDC-Level Protection"
    VDC1[("VDC 1 — Site A\n(primary)")]
    VDC2[("VDC 2 — Site B\n(replica)")]
    VDC1 -->|"geo-replication\nasync or sync"| VDC2
  end
  subgraph "Within-VDC Protection"
    FRAG["Object split into\nEC fragments"]
    N1["Node 1"] & N2["Node 2"] & N3["Node 3"] & N4["Node 4+"]
    FRAG --> N1 & N2 & N3 & N4
  end
  WORM["Object Lock (WORM)\nper-object retention"]
  VER["Bucket Versioning\npoint-in-time recovery"]
  classDef vdc fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef node fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef protect fill:#15803d,stroke:#166534,color:#fff
  class VDC1,VDC2 vdc
  class N1,N2,N3,N4,FRAG node
  class WORM,VER protect
```

| Protection Layer | Scope | Failure Domain Covered |
|---|---|---|
| Erasure coding (12+4) | Within a single VDC | Protects against up to 4 simultaneous disk/node failures within a VDC |
| Geo-replication (async) | Cross-VDC | Protects against VDC-level site failure with RPO governed by replication lag |
| Geo-replication (sync) | Cross-VDC | Zero-RPO VDC-level protection; requires sufficient WAN bandwidth |
| Object Lock (WORM) | Per-object, per-bucket | Prevents accidental or malicious deletion/overwrite within the retention window |
| Bucket versioning | Per-bucket | Allows point-in-time recovery of individual objects to previous versions |

## Configuration Backup

Back up the following ECS configuration artefacts regularly. Configuration is not backed up by erasure coding or geo-replication — it must be captured separately.

| Artefact | Location | Backup Method | Frequency |
|---|---|---|---|
| Replication group topology | ECS Portal → Settings | `GET /vdc/data-service/vpools` — save JSON output | Weekly |
| Namespace configuration | `ecscli namespace get --name <ns>` | Script-based export via REST API | Weekly |
| Bucket configuration | `ecscli bucket get --namespace <ns> --name <bucket>` | Script-based export via REST API | Weekly |
| IAM users (object user names) | `ecscli user list-object-users --namespace <ns>` | Script-based export — keys cannot be retrieved after creation | Weekly |
| TLS certificates | ECS Portal → Settings → Certificates | Export certificate files; store private key in secrets management | Before rotation |
| Syslog and SNMP configuration | ECS Portal → Settings | Document in runbook | On change |
| Bucket policies | `aws s3api get-bucket-policy --bucket <bucket>` | Script-based export per bucket | Weekly |
| Lifecycle policies | `aws s3api get-bucket-lifecycle-configuration --bucket <bucket>` | Script-based export per bucket | Weekly |

### Scripted Configuration Export

```bash
#!/bin/bash
# Export key ECS configuration artefacts to a local directory
# Usage: ECS_HOST=ecs01.example.com ECS_USER=sysadmin ECS_PASS=secret ./ecs_config_export.sh

ECS_HOST="${ECS_HOST:-}"
ECS_USER="${ECS_USER:-sysadmin}"
ECS_PASS="${ECS_PASS:-}"
OUTDIR="./ecs-config-$(date +%Y%m%d)"
ECS="https://$ECS_HOST:4443"

mkdir -p "$OUTDIR"

TOKEN=$(curl -sk -u "$ECS_USER:$ECS_PASS" -D - "$ECS/login" \
  | grep "X-SDS-AUTH-TOKEN" | awk '{print $2}' | tr -d '\r')

[[ -z "$TOKEN" ]] && echo "ERROR: Authentication failed." && exit 1

api() { curl -sk -H "X-SDS-AUTH-TOKEN: $TOKEN" -H "Accept: application/json" "$ECS$1"; }

# Export VDC info, nodes, alerts, capacity
api "/vdc/capacity"          > "$OUTDIR/vdc_capacity.json"
api "/vdc/nodes"             > "$OUTDIR/vdc_nodes.json"
api "/vdc/data-service/vpools" > "$OUTDIR/replication_groups.json"
api "/object/namespaces"     > "$OUTDIR/namespaces.json"

# Export per-namespace bucket list
NAMESPACES=$(api "/object/namespaces" | python3 -c \
  "import sys,json; [print(n['name']) for n in json.load(sys.stdin).get('namespace',[])]")

for NS in $NAMESPACES; do
  api "/object/bucket?namespace=$NS" > "$OUTDIR/buckets_${NS}.json"
done

curl -sk -H "X-SDS-AUTH-TOKEN: $TOKEN" "$ECS/logout" > /dev/null

echo "Configuration exported to $OUTDIR"
```

## Restoring Object Data

Object data restore depends on the failure scenario.

### Node Failure (Within a VDC)

ECS automatically rebuilds erasure coding stripes to surviving nodes when a node or disk fails.

```mermaid
graph TD
  FAIL(["Node or disk marked FAILED"]) --> AUTO["ECS auto-rebuild begins\nEC fragments reconstructed\nfrom surviving nodes"]
  AUTO --> MON["Monitor: ECS Portal →\nHardware → Disks\nStatus: REBUILDING → GOOD"]
  MON --> DONE{Rebuild\ncomplete?}
  DONE -->|No| WAIT["Wait — rebuild time:\n8–24 h for dense node\nDo NOT run upgrades or\nnode additions during rebuild"]
  WAIT --> MON
  DONE -->|Yes| CHK["Confirm node/disk shows GOOD\nCheck cluster capacity headroom"]
  CHK --> CLEAR(["Cluster redundancy restored"])
  classDef decision fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef warn fill:#b45309,stroke:#92400e,color:#fff
  classDef term fill:#15803d,stroke:#166534,color:#fff
  class DONE decision
  class AUTO,MON,CHK action
  class WAIT warn
  class FAIL,CLEAR term
```

- No manual restore required
- Monitor rebuild progress: ECS Portal → Hardware → Disks — `REBUILDING` state progresses to `GOOD` when complete
- Rebuild duration depends on the amount of data on the failed disk and available cluster bandwidth; typically 8–24 hours for a dense node
- Do not attempt any planned maintenance (upgrades, node additions) while a rebuild is in progress

```bash
# Monitor overall node and disk state during a rebuild
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/nodes" | python3 -m json.tool

# Watch capacity to ensure the cluster has sufficient headroom for the rebuild
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/capacity" | python3 -m json.tool
```

### VDC Failure (Geo-Replication Configured)

When a VDC becomes unavailable:

1. Update client S3 endpoints to point to the surviving VDC IP/FQDN
2. Confirm data is accessible:
   ```bash
   aws s3 ls s3://<bucket>/ \
     --endpoint-url https://<secondary-vdc>:9021 \
     --no-verify-ssl \
     --profile ecs
   ```
3. Check replication lag at the time of failure to understand RPO exposure — the geo-monitoring lag value at the moment of failure represents the maximum data loss window
4. Communicate RPO status to application owners; for asynchronous replication, objects written in the lag window may not be present on the surviving VDC
5. When the failed VDC recovers, re-add it to the replication group and allow data to resync before sending writes back to it
6. Monitor resync progress in ECS Portal → Geo Monitoring; wait for lag to return to zero before considering recovery complete

### Accidental Object Deletion

**With bucket versioning enabled:**

```bash
# List all versions and delete markers for an object
aws s3api list-object-versions \
  --bucket <bucket> \
  --prefix <object-key> \
  --endpoint-url https://<ecs-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Remove the delete marker to restore the object to the latest version
aws s3api delete-object \
  --bucket <bucket> \
  --key <object-key> \
  --version-id <delete-marker-version-id> \
  --endpoint-url https://<ecs-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Alternatively, restore a specific previous version by copying it as the current object
aws s3api copy-object \
  --bucket <bucket> \
  --copy-source "<bucket>/<object-key>?versionId=<version-id>" \
  --key <object-key> \
  --endpoint-url https://<ecs-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs
```

**Without versioning enabled:**
- The object is unrecoverable unless it exists on a remote VDC with replication lag less than the time of deletion
- Immediately check the remote VDC:
  ```bash
  aws s3api head-object \
    --bucket <bucket> \
    --key <object-key> \
    --endpoint-url https://<remote-vdc>:9021 \
    --no-verify-ssl \
    --profile ecs
  ```
- If found on the remote VDC, copy it back:
  ```bash
  aws s3 cp \
    s3://<bucket>/<object-key> \
    s3://<bucket>/<object-key> \
    --source-region us-east-1 \
    --copy-props none \
    --endpoint-url https://<remote-vdc>:9021 \
    --no-verify-ssl \
    --profile ecs
  ```

### Object Lock (WORM) Protected Objects

Objects within their Object Lock retention period cannot be deleted or overwritten. This is expected behaviour for compliance deployments.

- To verify the retention status of an object:
  ```bash
  aws s3api get-object-retention \
    --bucket <bucket> \
    --key <object-key> \
    --endpoint-url https://<ecs-endpoint>:9021 \
    --no-verify-ssl \
    --profile ecs
  ```
- Compliance mode locks cannot be shortened or removed even by `sysadmin`; they expire automatically when the `RetainUntilDate` passes
- Governance mode locks can be overridden by a user with the `s3:BypassGovernanceRetention` permission — do not use Governance mode for regulated compliance workloads

## Veeam Backup Integration

ECS serves as an S3-compatible target for Veeam Backup & Replication (Capacity Tier or Scale-out Backup Repository). ECS retains Veeam backup data; Veeam manages its own restore procedures.

**ECS configuration for Veeam:**

1. Create a dedicated namespace: `veeam-prod`
2. Create a dedicated bucket: `veeam-prod-offload` with Object Lock enabled (if immutable backups are required)
3. Create a dedicated object user: `svc-veeam-prod` with read/write access to the bucket
4. Set a hard quota on the namespace equal to the planned Veeam storage allocation + 20% buffer
5. In Veeam: Backup Infrastructure → Add Backup Repository → Object Storage → S3 Compatible
   - Endpoint: `https://<ecs-load-balancer>:9021`
   - Credentials: access key and secret key for `svc-veeam-prod`
   - Bucket: `veeam-prod-offload`
   - Enable immutability if Object Lock was enabled on the bucket

**Validating Veeam backup data on ECS:**

```bash
# Confirm backup data is present on ECS
aws s3 ls s3://veeam-prod-offload/ \
  --recursive --human-readable \
  --endpoint-url https://<ecs-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs

# Check bucket size and object count
aws s3api list-objects-v2 \
  --bucket veeam-prod-offload \
  --query 'length(Contents)' \
  --endpoint-url https://<ecs-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs
```

## Validation After Restore or Failover

After any restore or VDC failover, validate the following before declaring recovery complete:

- [ ] S3 endpoint functional test: `HeadBucket` or `ListBuckets` succeeds from the primary consuming application
- [ ] `ecscli namespace list` — all expected namespaces present on the surviving VDC
- [ ] Spot-check a sample of critical objects with `HeadObject` to confirm accessibility and correct size
- [ ] For versioned buckets: verify expected versions are present with `list-object-versions`
- [ ] Confirm geo-replication is running and lag is at zero between all VDCs (after VDC recovery)
- [ ] Application teams confirm S3 workloads are running normally with no authentication or connectivity errors
- [ ] No new `FAILED` or `DEGRADED` nodes in `GET /vdc/nodes`
- [ ] Capacity utilisation is within expected range; no unexpected jump from rebalancing
