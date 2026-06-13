---
tags:
  - architecture
  - dell
---
# Dell ECS — Integrations


<div class="kb-summary">
Integrations reference covering S3 Client Integration, Veeam Object Repository, Commvault Integration, NetBackup Integration, HDFS Integration and 4 more sections.

*Applies to: ECS 3.x*
</div>
```text
┌─────────────────────────────────────── Dell ECS — Integrations ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       ECS integrations: VMware vSphere, Kubernetes CSI, backup software, and monitoring       │   │
│   │           Protocols: S3 · Azure Blob API · Swift · Atmos · NFS (via gateway) · HDFS           │   │
│   │ API: ECS Management Portal / REST API REST API enables automation and third-party tool integr │   │
│   │             Plug-ins available for vCenter, OpenShift, Splunk, and SIEM platforms             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ECS → REST API / plug-ins → VMware / K8s / backup / monitoring                                     │
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
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   Storage pool   │ Drive aggregatio │      Internal     │       N/A        │   Erasure 12+4   │   │
│   │       VDC        │  Site grouping   │      Internal     │       N/A        │   HA per site    │   │
│   │      Bucket      │ Object namespace │   S3/Swift/Blob   │   S3 keys/IAM    │    Per tenant    │   │
│   │ Replication grp  │ Geo replication  │    ECS protocol   │   Certificate    │    3-way geo     │   │
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


## S3 Client Integration

ECS exposes a native S3-compatible API on HTTPS port 443 (or 9021 for the non-standard S3 port; 9020 for plain HTTP in lab environments). Any S3-compatible client can connect using path-style or virtual-hosted-style addressing.

```mermaid
graph LR
  subgraph "Client Layer"
    AWSCLI["aws CLI\n(SigV4)"]
    S3CMD["s3cmd"]
    JAVA["S3 SDK\n(Java / Python / Go)"]
    VBR["Veeam B&R\n(S3 compatible)"]
  end
  subgraph "ECS Endpoint"
    LB["Load Balancer VIP\nHTTPS 443 / 9021"]
    NODE1["ECS Node 1"]
    NODE2["ECS Node 2"]
    NODEN["ECS Node N"]
    LB --> NODE1 & NODE2 & NODEN
  end
  AWSCLI & S3CMD & JAVA & VBR -->|"HTTPS + SigV4"| LB
  classDef client fill:#15803d,stroke:#166534,color:#fff
  classDef ecs fill:#2563eb,stroke:#1d4ed8,color:#fff
  class AWSCLI,S3CMD,JAVA,VBR client
  class LB,NODE1,NODE2,NODEN ecs
```

**Connection parameters:**

| Parameter | Value |
|---|---|
| Endpoint | `https://<ecs-load-balancer-or-node>` (port 443 or 9021) |
| Access key | Object user access key from ECS Portal → Namespace → IAM Users |
| Secret key | Associated secret from key creation (shown once at creation only) |
| Region | ECS does not enforce AWS regions; set to any value (e.g., `us-east-1`) in client config |
| Signature version | AWS Signature Version 4 (SigV4) — required; SigV2 is not supported in ECS 3.8+ |
| Addressing style | Path-style (`<endpoint>/<bucket>`) or virtual-hosted (`<bucket>.<endpoint>`) |

**AWS CLI configuration:**

```bash
# Configure a named profile for ECS
aws configure --profile ecs
# AWS Access Key ID:     <object_user_access_key>
# AWS Secret Access Key: <object_user_secret_key>
# Default region:        us-east-1
# Default output format: json

ECS_EP="https://<ecs-node-or-lb>:9021"
PROFILE="--profile ecs --endpoint-url $ECS_EP --no-verify-ssl"

# List all buckets accessible to this user
aws s3api list-buckets $PROFILE

# Upload a file
aws s3 cp localfile.tar.gz s3://<bucket>/path/ $PROFILE

# Sync a directory recursively
aws s3 sync /local/backup/ s3://<bucket>/backups/ $PROFILE
```

ECS supports S3 multipart upload, S3 Object Lock (WORM), presigned URLs, bucket versioning, and lifecycle policies. Virtual-hosted-style (`<bucket>.<ecs-endpoint>`) requires DNS configuration pointing `*.ecs.example.com` to the ECS load balancer VIP; path-style (`<ecs-endpoint>/<bucket>`) works without DNS changes and is easier to configure in most clients.

**s3cmd configuration:**

```ini
# ~/.s3cfg for Dell ECS
[default]
access_key = <ecs_access_key>
secret_key = <ecs_secret_key>
host_base = <ecs-endpoint>:9021
host_bucket = <ecs-endpoint>:9021/%(bucket)s
use_https = True
check_ssl_certificate = False
signature_v2 = False
```

```bash
# Test s3cmd connectivity
s3cmd ls

# Upload a file
s3cmd put localfile.tar.gz s3://<bucket>/path/

# Sync a directory
s3cmd sync /local/path/ s3://<bucket>/
```

## Veeam Object Repository

ECS is a certified S3-compatible target for Veeam Backup & Replication object repositories (Scale-out Backup Repository offload and Capacity Tier).

```mermaid
graph LR
  subgraph "Veeam Infrastructure"
    VBR["Veeam B&R Server"]
    SOBR["Scale-out Backup Repo\n(Performance Tier)"]
    VBR --> SOBR
  end
  subgraph "ECS"
    S3EP["ECS S3 Endpoint\nHTTPS 9021"]
    NS["Namespace: veeam-prod"]
    BKT["Bucket: veeam-prod-offload\n(Object Lock optional)"]
    USR["Object User: svc-veeam-prod"]
    S3EP --> NS --> BKT
    USR --> BKT
  end
  SOBR -->|"offload — Capacity Tier\nHTTPS + SigV4"| S3EP
  classDef veeam fill:#15803d,stroke:#166534,color:#fff
  classDef ecs fill:#2563eb,stroke:#1d4ed8,color:#fff
  class VBR,SOBR veeam
  class S3EP,NS,BKT,USR ecs
```

**Integration steps:**

1. Create a dedicated ECS namespace for Veeam: `veeam-prod`
2. Create a dedicated bucket: `veeam-prod-offload`
   - Enable Object Lock at bucket creation if Veeam Immutability is required
   - Set a hard quota matching the planned Veeam storage allocation + 20% buffer
3. Create a dedicated object user: `svc-veeam-prod`
   - Generate access key and secret key; store in Veeam credential store
4. In Veeam VBR: **Backup Infrastructure** → **Add Backup Repository** → **Object Storage** → **S3 Compatible**
   - Service point: `https://<ecs-load-balancer>:9021`
   - Region: any value (e.g., `us-east-1`)
   - Credentials: `svc-veeam-prod` access key and secret key
   - Bucket: `veeam-prod-offload`
   - Enable Immutability (if Object Lock enabled on bucket): set retention period matching backup policy RPO
5. Add the ECS object repository as a Capacity Tier or Performance Tier extent in the Scale-out Backup Repository

**Key ECS settings for Veeam:**

| Setting | Recommendation |
|---|---|
| Bucket versioning | Not required for Veeam; Veeam manages its own metadata structures |
| Object Lock | Enable only if Veeam Immutability is required; must be enabled at bucket creation |
| Object Lock mode | Compliance mode for air-gap immutability against ransomware; Governance mode for operational flexibility |
| Namespace quota | Set hard quota; Veeam can consume all available cluster capacity without a quota |
| Bucket quota | Set per-bucket quota in addition to namespace quota for finer-grained control |
| S3 endpoint | Use the load balancer VIP or a DNS round-robin for resilience; do not point Veeam at a single node |

**Validating Veeam backup data on ECS:**

```bash
# Confirm Veeam backup data is present
aws s3 ls s3://veeam-prod-offload/ \
  --recursive --human-readable \
  --endpoint-url https://<ecs-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs
```

## Commvault Integration

Commvault supports ECS as an S3-compatible cloud library target for secondary copy and archival. Configuration is performed in the Commvault Command Center.

**Integration steps:**

1. Create a dedicated ECS namespace and bucket for Commvault: `commvault-prod` / `commvault-prod-archive`
2. Create a dedicated object user: `svc-commvault-prod`
3. In Commvault Command Center: **Storage** → **Cloud** → **Add Cloud Storage** → **S3 Compatible**
   - Service host: `<ecs-endpoint>` (without `https://` prefix in some Commvault versions)
   - Port: `9021`
   - Access key and secret key: `svc-commvault-prod` credentials
   - Bucket: `commvault-prod-archive`
4. Configure the cloud library as a storage pool target for secondary or archive copies
5. Test a synthetic full backup to confirm end-to-end connectivity and write throughput

## NetBackup Integration

Veritas NetBackup can use ECS as an object storage target via the NetBackup CloudCatalyst or as a direct S3-compatible storage unit.

**CloudCatalyst (deduplication target):**
- Deploy NetBackup CloudCatalyst on a dedicated server with network access to ECS
- Configure the CloudCatalyst to use ECS as its backing S3 store with the ECS endpoint and object user credentials
- CloudCatalyst deduplicates backup streams before writing to ECS, reducing ECS capacity consumption

**Direct S3 storage unit:**
- NetBackup 8.3+: create a Cloud Storage Server with `S3` type and ECS endpoint
- Configure the storage unit to use the ECS bucket and object user credentials
- Enable CloudCatalyst on the media server for deduplication (recommended for large environments)

## HDFS Integration

ECS supports HDFS-compatible access through the ECS HDFS connector, enabling Hadoop ecosystem tools (Spark, Hive, MapReduce) to read and write directly to ECS buckets.

**Integration steps:**

1. Download the ECS HDFS connector JAR from the Dell Support portal
2. Install the JAR on all Hadoop cluster nodes (place in the Hadoop classpath)
3. Configure `core-site.xml` to point to the `ecshdfs://` scheme:
   ```xml
   <property>
     <name>fs.ecshdfs.impl</name>
     <value>com.emc.hadoop.fs.vipr.ViPRFileSystem</value>
   </property>
   <property>
     <name>fs.AbstractFileSystem.ecshdfs.impl</name>
     <value>com.emc.hadoop.fs.vipr.ViPRAbstractFilesystem</value>
   </property>
   <property>
     <name>viprfs.client.access_key</name>
     <value><ecs_object_user_access_key></value>
   </property>
   <property>
     <name>viprfs.client.secret_key</name>
     <value><ecs_object_user_secret_key></value>
   </property>
   <property>
     <name>viprfs.client.vipr.hostname</name>
     <value><ecs-endpoint></value>
   </property>
   <property>
     <name>viprfs.client.vipr.port</name>
     <value>9021</value>
   </property>
   ```
4. Authentication uses ECS object user access keys (simple auth); Kerberos integration is possible for secured Hadoop clusters — configure via ECS namespace HDFS auth settings
5. ECS presents HDFS namespace paths mapped to buckets; directory emulation is handled by the connector
6. Test: `hadoop fs -ls ecshdfs://<namespace>@<ecs-endpoint>/<bucket>/`

**HDFS considerations:**

| Consideration | Detail |
|---|---|
| Performance | ECS HDFS is not optimised for small random I/O; best suited for large sequential reads/writes (Spark workloads) |
| Authentication | S3 access keys are embedded in `core-site.xml` — store the file with restricted permissions; use secrets management integration if available |
| Namespace mapping | Each ECS namespace appears as a separate HDFS cluster identifier; paths are `ecshdfs://<namespace>@<ecs-endpoint>/<bucket>/` |
| Metadata search | HDFS access does not use ECS metadata search; queries must go through the ECS Query API |

## Metadata Search Integration

ECS supports custom object metadata tagging and a Metadata Search API (based on Elasticsearch) that allows querying objects by custom key-value tags across a namespace.

**Enable metadata search per namespace:**
1. Navigate to ECS Portal → Manage → Namespaces → select namespace → Edit
2. Enable **Metadata Search** — this provisions an Elasticsearch indexer for the namespace
3. Note: metadata search adds indexer capacity overhead; plan ECS node sizing with this enabled

**Tag objects with custom metadata on upload:**

```bash
# Upload an object with custom metadata tags
aws s3api put-object \
  --bucket analytics-prod-raw \
  --key data/2024/report.parquet \
  --body report.parquet \
  --metadata '{"project":"alpha","env":"prod","owner":"analytics-team"}' \
  --endpoint-url https://<ecs-endpoint>:9021 \
  --no-verify-ssl \
  --profile ecs
```

**Query objects by metadata tag (ECS Query API):**

```bash
# Search for objects with a custom metadata tag (requires metadata search enabled on namespace)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/object/namespaces/analytics-prod/buckets/analytics-prod-raw/query?query=project%3Dalpha" \
  | python3 -m json.tool

# URL-encoded query format: key=value -> key%3Dvalue
# Multiple conditions: key1=value1 AND key2=value2 -> key1%3Dvalue1%20AND%20key2%3Dvalue2
```

## External Authentication (LDAP/AD)

ECS can delegate IAM user authentication to an external LDAP or Active Directory service for namespace-level management access. Configure under ECS Portal → Namespace → Edit → Authentication Domain.

- Object users with S3 access keys always authenticate locally — LDAP integration applies to management console users only
- LDAP is configured per namespace; multiple namespaces can reference different LDAP domains
- Supported protocols: LDAP (TCP 389) and LDAPS (TCP 636)
- Map AD groups to ECS namespace roles in the Authentication Domain configuration

## CloudIQ Integration (ECS 3.9+)

ECS 3.9 introduced integration with Dell CloudIQ for cloud-based capacity analytics, proactive health alerts, and hardware lifecycle management.

- Configure CloudIQ connectivity in ECS Portal → Settings → CloudIQ
- CloudIQ provides multi-cluster capacity trending and forecasting alongside other Dell storage systems
- Proactive recommendations for capacity expansion are surfaced in the CloudIQ portal before utilisation thresholds are reached
- Hardware component health and end-of-service-life alerts are raised in CloudIQ automatically

## SNMP and Syslog Integration

ECS generates SNMP traps and syslog messages for hardware and service health events. Integrate with your monitoring platform for 24/7 alerting.

**Syslog configuration:**
```yaml
ECS Portal → Settings → Syslog
  - Syslog server: <SIEM-or-syslog-aggregator-IP>
  - Port: 514 (UDP or TCP)
  - Protocol: RFC 5424 or RFC 3164
```

**SNMP configuration:**
```yaml
ECS Portal → Settings → SNMP
  - SNMP version: v3 (recommended); v2c for legacy monitoring systems
  - Community string (v2c): <monitoring-community>
  - Trap destination: <monitoring-server-IP>:162
  - Trap types: node status, disk status, capacity threshold, replication status
```

**Key SNMP MIBs:** Download the ECS MIB file from ECS Portal → Settings → SNMP → Download MIB to import into your monitoring platform (Nagios, Zabbix, SolarWinds, etc.).

---

## See also

- [Ecs — How It Works](how-it-works/)
- [Ecs — Design Standards](design-standards/)
