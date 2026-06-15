---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# Dell ECS — Diagnostics

<div class="kb-summary">
ECS diagnostic commands: authenticate to the Management REST API and check cluster node health with <code>GET /vdc/nodes</code>, inspect active alerts via <code>/vdc/alerts</code>, test the S3 data path with <code>aws s3api head-bucket</code> and <code>head-object</code>, SSH to individual nodes to inspect the storageos service and Cassandra ring health, check geo-replication lag via <code>/vdc/geo-replication/status</code>, and collect a support bundle via <code>POST /vdc/support-bundle</code> for Dell escalation.

*Applies to: ECS 3.x*
</div>

```text
┌────────────────────────────────────── Dell ECS — Diagnostics ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────┐      │
│   │  Start here: GET /vdc/nodes → all GOOD? → GET /vdc/alerts → identify failure domain       │       │
│   │  Node DEGRADED: SSH → systemctl status storageos → df -h /data/ → lsblk                   │       │
│   │  S3 access denied: check IAM user + bucket policy + addressing style + namespace           │      │
│   │  Geo-replication lag: nc -zv remote 9100 → check remote VDC health → WAN bandwidth        │       │
│   └────────────────────────────────────────────────────────────────────────────────────────────┘      │
│                                                                                                       │
│   ┌─────────────────────────────────────────┐  ┌──────────────────────────────────────────────┐       │
│   │          Management API Health          │  │           Node and Service Health            │       │
│   │   GET /vdc/nodes: GOOD | DEGRADED      │  │   systemctl status storageos caspian         │        │
│   │   GET /vdc/alerts: active fault list   │  │   df -h /data/: data partition usage         │        │
│   │   GET /vdc/capacity: provisioned/used  │  │   nodetool status: Cassandra ring (UN?)      │        │
│   │   GET /vdc/geo-replication/status: lag │  │   echo srvr | nc localhost 2181: ZK mode     │        │
│   │   GET /vdc/version: software version   │  │   lsblk: disk layout and state per node      │        │
│   └─────────────────────────────────────────┘  └──────────────────────────────────────────────┘       │
│                                                                                                       │
│   ┌─────────────────────────────────────────┐  ┌──────────────────────────────────────────────┐       │
│   │            S3 Data Path Tests           │  │       Geo-Replication Monitoring             │       │
│   │   aws s3 ls: list buckets (auth test)  │  │   GET /vdc/geo-replication/status: lag       │        │
│   │   aws s3api head-bucket: bucket exists │  │   nc -zv remote-vdc-node 9100: WAN port      │        │
│   │   aws s3api head-object: object access │  │   chronyc tracking: clock sync per node      │        │
│   │   get-bucket-policy: check policy      │  │   viprexec -v -cmd "free -h": cluster RAM    │        │
│   │   openssl s_client :9021: TLS check    │  │   Portal → Geo Monitoring: per-RG lag view   │        │
│   └─────────────────────────────────────────┘  └──────────────────────────────────────────────┘       │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ECS appliance nodes (x86) · 10/25 GbE backend network · commodity SAS drives                         │
│  ZooKeeper cluster (port 2181) · Cassandra metadata cluster · WAN link to remote VDC (port 9100)      │
│                                                                                                       │
│  Key terms:                                                                                           │
│  ECS                = Elastic Cloud Storage; Dell S3-compatible object store for unstructured data    │
│  VDC                = Virtual Data Center; group of ECS nodes at a single geographic site             │
│  Storage pool       = collection of nodes within a VDC; defines the erasure coding domain             │
│  Replication group  = links VDCs for geo-redundant object storage; 3-way replication                  │
│  Bucket             = top-level S3 namespace; equivalent to S3 bucket or Azure container              │
│  Erasure coding     = data protection scheme; default 12+4 provides 4-drive fault tolerance           │
│  Namespace          = tenant-level isolation; multiple tenants share a single ECS cluster             │
│  CAS                = Content Addressed Storage; fixed-content object storage with WORM support       │
│  Replication factor = number of VDC copies; 3-way geo-replication for maximum durability              │
│  Atmos API          = legacy Dell Atmos-compatible API; supported for migration from Atmos systems    │
│  HDFS connector     = ECS Hadoop connector; ECS appears as HDFS namespace for analytics jobs          │
│  Quota              = per-namespace or per-bucket storage quota; enforced as hard or soft limit       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TD
    A([ECS Issue Reported]) --> B[GET /vdc/nodes: cluster health\nGET /vdc/alerts: active alerts]
    B --> C{All nodes GOOD?}
    C -->|No — node DEGRADED| D[SSH to affected node\nsystemctl status storageos caspian]
    D --> E{Service running?}
    E -->|No| F[journalctl -u storageos: logs\ndf -h /data/ — disk full?\nRestart only if logs confirm safe]
    E -->|Yes| G[nodetool status: Cassandra ring\necho srvr | nc 2181: ZK mode\nlsblk: check for disk errors]
    C -->|Yes| H{S3 API functional?}
    H -->|No — 403 or 500| I[aws s3api head-bucket: auth check\nCheck IAM user + bucket policy\nVerify addr style and namespace]
    H -->|Yes| J{Geo-replication lag growing?}
    J -->|Yes| K[nc -zv remote-node 9100: WAN port\nGET /vdc/nodes: remote VDC health\nMonitor WAN bandwidth]
    J -->|No| L[Tail ECS logs for transient errors\ntail /var/log/ecs/*.log | grep ERR]
    F --> M[Collect support bundle\nPOST /vdc/support-bundle or Portal\nOpen Dell support case]
    G --> M
    I --> M
    K --> M
    L --> M

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,C,E,H,J dark
    class B,D,F,G,I,K,L action
    class M escalate
```

## Before you begin

- **Access:** Management REST API at `https://<ecs-node>:4443` (authenticate first to get a session token); SSH to ECS nodes as `admin`; ECS Portal admin account; S3 credentials (access key and secret key) for data path tests
- **Gather first:** ECS version (`GET /vdc/version`), active alerts (`GET /vdc/alerts`), VDC node list (`GET /vdc/nodes`), and the specific symptom — S3 HTTP error code, node state, or geo-replication lag percentage
- **Scope:** confirm whether the issue affects one node, one VDC, or geo-replication between VDCs — a single DEGRADED node is different from cluster-wide unavailability
- **Session tokens:** expire after 8 hours; re-authenticate with the `/login` endpoint if commands return 401

---

## Step 1 — Management API health check

```bash
# Authenticate to the ECS Management REST API
TOKEN=$(curl -sk -u "sysadmin:<password>" \
  -D - "https://<ecs-node>:4443/login" \
  | grep "X-SDS-AUTH-TOKEN" | awk '{print $2}' | tr -d '\r')

ECS="https://<ecs-node>:4443"

# VDC capacity — fields: totalProvisioned_gb, usedCapacity_gb, availableCapacity_gb
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/capacity" | python3 -m json.tool

# Node health — nodestatus: GOOD | DEGRADED | UNKNOWN
# All nodes must show GOOD before any planned change
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/nodes" | python3 -m json.tool

# Specific node details
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/nodes/<node-id>" | python3 -m json.tool

# Active alerts
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/alerts" | python3 -m json.tool

# ECS software version
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/version" | python3 -m json.tool

# Geo-replication status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/geo-replication/status" | python3 -m json.tool

# Replication groups (vpools)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/data-service/vpools" | python3 -m json.tool

# Dashboard zone health
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/dashboard/zones/localzone" | python3 -m json.tool

# Namespace list
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/object/namespaces" | python3 -m json.tool

# Bucket list for a namespace
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/object/bucket?namespace=<namespace>" | python3 -m json.tool

# Invalidate session
curl -sk -H "X-SDS-AUTH-TOKEN: $TOKEN" "$ECS/logout" > /dev/null
```

---

## Step 2 — S3 API diagnostics

```bash
S3_EP="https://<ecs-s3-endpoint>:9021"
PROFILE="--profile ecs --endpoint-url $S3_EP --no-verify-ssl"

# Test S3 connectivity (list buckets)
aws s3 ls $PROFILE

# Head a specific bucket (tests auth and bucket existence)
aws s3api head-bucket --bucket <bucket> $PROFILE

# Head a specific object (tests object existence and access)
aws s3api head-object --bucket <bucket> --key <object-key> $PROFILE

# List objects in a bucket
aws s3 ls s3://<bucket>/ $PROFILE

# List incomplete multipart uploads
aws s3api list-multipart-uploads --bucket <bucket> $PROFILE

# Get bucket versioning state
aws s3api get-bucket-versioning --bucket <bucket> $PROFILE

# Get bucket policy
aws s3api get-bucket-policy --bucket <bucket> $PROFILE

# Get object lock configuration
aws s3api get-object-lock-configuration --bucket <bucket> $PROFILE

# TLS certificate check on S3 endpoint
openssl s_client -connect <ecs-s3-endpoint>:9021 -servername <ecs-s3-endpoint> \
  </dev/null 2>/dev/null | openssl x509 -noout -dates -subject -issuer

# Test raw HTTP connectivity to S3 endpoint
curl -sv --max-time 10 "https://<ecs-s3-endpoint>:9021/" \
  --resolve "<ecs-s3-endpoint>:9021:<ecs-node-ip>" \
  --insecure 2>&1 | grep -E "< HTTP|Connected|SSL|certificate"
```

### Workflow: S3 Access Denied

1. Confirm the access key and secret key are correct (secret keys cannot be retrieved from ECS — if lost, rotate)
2. Confirm the object user exists in the correct namespace: `ecscli user list-object-users --namespace <ns>`
3. Check the bucket policy: `aws s3api get-bucket-policy --bucket <bucket> $PROFILE`
4. Check the bucket ACL: `aws s3api get-bucket-acl --bucket <bucket> $PROFILE`
5. Verify the S3 request is using the correct addressing style (path-style vs virtual-hosted-style)
6. Check that the bucket exists in the expected namespace: `ecscli bucket get --namespace <ns> --name <bucket>`

---

## Step 3 — Node-level SSH diagnostics

```bash
# SSH to an ECS node
ssh admin@<ecs-node>

# ECS service health
systemctl status storageos     # Main ECS data service
systemctl status caspian       # ECS fabric agent

# Check across all nodes simultaneously
viprexec -v -cmd "systemctl is-active storageos"
viprexec -v -cmd "systemctl is-active caspian"

# Disk diagnostics
df -h /data/                                           # Data partition usage
df -h                                                  # All disk mounts
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,STATE             # Disk layout, type, state
viprexec -v -cmd "df -h /data/"                        # Check across all cluster nodes

# System resources
uptime
free -h
viprexec -v -cmd "free -h"
ps aux | grep -E "storageos|caspian|java" | grep -v grep
```

### Cassandra (metadata store)

```bash
# Ring status: UN = Up/Normal | DN = Down | UJ = Joining | UL = Leaving
/opt/storageos/tools/nodetool status

# Compaction activity (high compaction = elevated metadata latency)
/opt/storageos/tools/nodetool compactionstats

# Heap usage (heap pressure = GC pauses = slow metadata responses)
/opt/storageos/tools/nodetool info | grep -iE "heap|load"

# Flush Cassandra memtables (can help if writes are stalled)
/opt/storageos/tools/nodetool flush

# Node info (token, DC, rack, load)
/opt/storageos/tools/nodetool ring
```

### ZooKeeper (cluster coordination)

```bash
# Mode should be 'leader' on one node and 'follower' on all others
echo "srvr" | nc localhost 2181 | grep Mode

# Outstanding requests should be near zero during steady state
echo "stat" | nc localhost 2181 | grep outstanding

# Connection count (elevated connections may indicate a stuck client)
echo "stat" | nc localhost 2181 | grep connections

# List all ZK nodes in the ensemble
echo "conf" | nc localhost 2181
```

### NTP and clock sync

```bash
chronyc tracking
timedatectl status
# All nodes should agree within 100ms; mismatched clocks cause geo-replication errors
viprexec -v -cmd "date"
```

### Network connectivity

```bash
# Test inter-node connectivity on the data network
ping -c 4 <other-ecs-node-data-ip>

# Test WAN connectivity to remote VDC nodes (geo-replication port)
nc -zv <remote-vdc-node> 9100

# Test KMIP connectivity (if encryption at rest with external KMS is configured)
nc -zv <kmip-server> 5696
```

### Workflow: Node Marked DEGRADED

1. `GET /vdc/nodes` — identify which node is DEGRADED and its node ID
2. `GET /vdc/alerts` — check for disk or NIC failure alerts correlated with the node
3. SSH to the affected node: `ssh admin@<ecs-node>`
4. `systemctl status storageos` — confirm whether the ECS service is running
5. `df -h /data/` — check if the data partition is full or unmounted
6. `lsblk` — identify any disks showing error state in the OS
7. Check system log: `journalctl -xe | grep -iE "disk|error|fault" | tail -50`
8. If a disk failure is confirmed: initiate disk replacement via **ECS Portal → Hardware → Disks → Replace Disk**
9. Monitor rebuild progress in **ECS Portal → Hardware → Disks** until the new disk shows `GOOD`

---

## Step 4 — Geo-replication diagnostics

```bash
# Current geo-replication status (all replication groups)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/geo-replication/status" | python3 -m json.tool

# Replication groups (vpools)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/data-service/vpools" | python3 -m json.tool
```

### Workflow: Geo-Replication Lag Growing

1. **ECS Portal → Geo Monitoring** — identify which replication group has growing lag and which VDC is behind
2. Confirm the remote VDC is healthy: `GET /vdc/nodes` against the remote VDC endpoint
3. Check WAN bandwidth utilisation on the inter-site link at the time lag started growing
4. Confirm port 9100 is reachable between VDCs: `nc -zv <remote-vdc-node> 9100`
5. Check for alerts on the remote VDC: `GET /vdc/alerts` against the remote VDC endpoint
6. If the remote VDC is healthy and WAN is not saturated: check ECS data service logs for replication errors
7. If the WAN link is saturated: adjust replication group bandwidth throttle in **ECS Portal → Replication → Bandwidth Management**

```bash
# Search for geo-replication errors in service logs
grep -r "replication" /var/log/ecs/ | grep -iE "error|failed|timeout" | tail -50

# Check for time sync drift between VDC sites (mismatched clocks cause geo-rep errors)
viprexec -v -cmd "date"
chronyc tracking
```

---

## Step 5 — Support bundle collection

```bash
# ECS software version
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/version" | python3 -m json.tool

# Node list and health status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/nodes" | python3 -m json.tool

# Active alerts
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/alerts" | python3 -m json.tool

# VDC capacity
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/capacity" | python3 -m json.tool

# Replication group status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/data-service/vpools" | python3 -m json.tool

# Namespace and bucket inventory
ecscli namespace list
ecscli bucket list --namespace <affected-namespace>
ecscli bucket get --namespace <affected-namespace> --name <affected-bucket>

# Generate support bundle (mandatory for Sev1/Sev2)
curl -s -k -X POST \
  -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "$ECS/vdc/support-bundle" | python3 -m json.tool
# Alternatively: ECS Portal → Support → Collect Logs
```

**Information to prepare before the call:**

| Item | Detail |
|---|---|
| ECS software version | From `GET /vdc/version` |
| Number of VDCs and nodes per VDC | Topology description |
| Replication group configuration | Mode (sync/async), VDC pairing |
| Approximate time the issue started | As precise as possible |
| Recent changes | Upgrades, network changes, new buckets, IAM changes in the 48h before the issue |
| Error messages | From ECS Portal, S3 client logs, and application logs |
| Impact | Which namespaces/buckets/applications are affected |

---

## Log locations

| Log | Location | Content |
|---|---|---|
| ECS data service log | `/var/log/ecs/` on each node | Object I/O, erasure coding, replication errors, chunk placement |
| ECS portal / management log | `/var/log/ecs-portal/` or `journalctl -u ecs-portal` | API requests, portal events, authentication failures |
| ECS fabric agent log | `/opt/emc/caspian/fabric/agent/logs/agent.log` | Node lifecycle, upgrade, and fabric events |
| OS system log | `/var/log/messages` or `journalctl -xe` | Node OS events, hardware errors, kernel messages |
| Cassandra log | `/opt/storageos/db/logs/system.log` | Metadata store events, compaction, GC events |
| ZooKeeper log | `/opt/storageos/zookeeper/logs/zookeeper.log` | Cluster coordination events |
| Geo-replication log | ECS Portal → Logs → Geo Replication | Replication job status and per-object replication errors |
| Audit log | ECS Portal → Monitoring → Audit | Admin actions — create/modify/delete namespace, bucket, IAM |

```bash
# Tail ECS data service log for real-time error monitoring
tail -f /var/log/ecs/*.log | grep -iE "error|exception|failed|degraded"

# Tail fabric agent log
tail -f /opt/emc/caspian/fabric/agent/logs/agent.log

# Journalctl for ECS services
journalctl -u storageos -f --no-pager
journalctl -u caspian -f --no-pager

# Search Cassandra log for recent errors
journalctl -u cassandra --since "1 hour ago" | grep -iE "error|exception|heap"
```

---

## See also

- [ECS — Common Issues](common-issues/)
- [ECS — Escalation](escalation/)
- [ECS — Health Checks](../operations/health-checks/)

## Verify resolution

- `GET /vdc/nodes` returns all nodes with `nodestatus: GOOD`
- `GET /vdc/alerts` returns empty or only previously acknowledged alerts
- `aws s3api head-bucket --bucket <bucket> $PROFILE` returns HTTP 200 (no 403 or 500 errors)
- `GET /vdc/geo-replication/status` shows replication lag is stable or decreasing
- `/opt/storageos/tools/nodetool status` shows all nodes as `UN` (Up/Normal) on the affected node
- `systemctl is-active storageos && systemctl is-active caspian` returns `active` on all cluster nodes
