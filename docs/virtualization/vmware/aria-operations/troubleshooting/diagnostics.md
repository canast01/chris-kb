---
tags:
  - aria-operations
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Operations — Diagnostics

<div class="kb-summary">
Aria Operations (vROps) diagnostic commands: check cluster service health with cluster-mgmt-cli, query the REST API health endpoint, inspect analytics.log and collector.log for errors, check adapter collection status, verify disk space on data nodes, generate the vcops-support bundle for VMware SRs.

*Applies to: VMware Aria Operations 8.x (vRealize Operations Manager)*
</div>
![Aria Operations — Diagnostics](../../../../assets/virtualization-vmware-aria-operations-troubleshooting-diagno.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "GET /suite-api/api/health\ncluster-mgmt-cli status" {shape: rectangle}
D: "grep adapter-name /var/log/vmware/vcops/collector.log\nTest adapter from vROps UI → Administration → Adapters" {shape: rectangle}
E: "GET /api/resources?page=0\nCompare count before and after last collection" {shape: rectangle}
F: "GET /api/alerts?pageSize=10\nCheck analytics.log for alert engine errors" {shape: rectangle}
G: "cluster-mgmt-cli status\nVAMI → Administration → Cluster Management" {shape: rectangle}
H: "df -h /storage/db\nCheck analytics partition usage" {shape: rectangle}
I: "I" {shape: rectangle}
J: "journalctl -u vmware-vcops -n 100\nCheck disk space: df -h /storage/db" {shape: rectangle}
K: "cluster-mgmt-cli status\nCheck replica node heartbeat" {shape: rectangle}
L: "grep ERROR collector.log | tail -50\nCheck adapter credential or TLS error" {shape: rectangle}
M: "Check adapter last collection time in vROps UI\nAdministration → Solutions → Adapter Instances" {shape: rectangle}
N: "grep ERROR analytics.log | tail -50\nCheck for OOM: grep OutOfMemory analytics.log" {shape: rectangle}
O: "Check NTP sync on all nodes\ntimedatectl; chronyc tracking" {shape: rectangle}
P: "Check /storage/db partition\nVAMI → Administration → Disk Usage" {shape: rectangle}
Q: "Collect vcops-support bundle\nvcops-support gen" {shape: rectangle}
R: "Open VMware SR\nmysupport.vmware.com" {shape: rectangle}
A: "Aria Operations Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> K
D -> L
E -> M
F -> N
G -> O
H -> P
J -> Q
K -> Q
L -> Q
M -> Q
N -> Q
O -> Q
P -> Q
Q -> R
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_cluster_service_status: "Step 1 — Check cluster service status" {shape: rectangle}
step_2_query_rest_api_health: "Step 2 — Query REST API health" {shape: rectangle}
step_3_inspect_log_files: "Step 3 — Inspect log files" {shape: rectangle}
step_4_check_adapter_collection_stat: "Step 4 — Check adapter collection status" {shape: rectangle}
step_5_check_vrops_cluster_node_heal: "Step 5 — Check vROps cluster node health" {shape: rectangle}
step_6_check_disk_space_and_performa: "Step 6 — Check disk space and performance" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_cluster_service_status: investigate
symptom -> step_2_query_rest_api_health: investigate
symptom -> step_3_inspect_log_files: investigate
symptom -> step_4_check_adapter_collection_stat: investigate
symptom -> step_5_check_vrops_cluster_node_heal: investigate
symptom -> step_6_check_disk_space_and_performa: investigate
step_1_check_cluster_service_status -> resolution
step_2_query_rest_api_health -> resolution
step_3_inspect_log_files -> resolution
step_4_check_adapter_collection_stat -> resolution
step_5_check_vrops_cluster_node_heal -> resolution
step_6_check_disk_space_and_performa -> resolution
```

## Before you begin

- **Access:** vROps admin UI credentials; SSH to the master node (`admin` user); VAMI access at port 5480
- **Gather first:** the specific symptom (adapter showing no data, UI alert for node health, resource count dropped, specific alert not firing), the adapter or resource type affected, and when the issue started
- **Scope:** confirm whether the issue affects one adapter instance, one resource type, or the entire vROps cluster

---

## Step 1 — Check cluster service status

```bash
# SSH to the vROps master node
ssh admin@<vrops-master-ip>

# Check cluster node roles and health
cluster-mgmt-cli status
# Expected output:
# MASTER_NODE: ONLINE
# REPLICA_NODE: ONLINE (synchronized)
# DATA_NODES: all ONLINE
# Problem: any node OFFLINE or DEGRADED

# Check vROps service status
systemctl status vmware-vcops
# Expected: active (running)

# Recent service events
journalctl -u vmware-vcops -n 100 --no-pager

# Disk space on the analytics and log partitions
df -h
# Expected: /storage/db < 80%; /var/log < 80%
# Problem: /storage/db > 85% = risk of analytics failure

# Check NTP sync (time drift causes cluster join failures and alert timing issues)
chronyc tracking | grep "System time"
timedatectl status
```

---

## Step 2 — Query REST API health

```bash
# Get API auth token (admin credentials)
TOKEN=$(curl -sk -X POST \
  "https://<vrops-master-ip>/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","authSource":"LOCAL"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('token',''))")

echo $TOKEN
# Expected: token string; empty = auth failed

# Cluster health check (per-service component status)
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://<vrops-master-ip>/suite-api/api/health" | python3 -m json.tool
# Expected: all components online

# Resource count (drop indicates collection stopped)
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://<vrops-master-ip>/suite-api/api/resources?pageSize=1" \
  | python3 -c "import json,sys; print('Total resources:', json.load(sys.stdin).get('total','unknown'))"

# Active alerts (high count = analytics engine may be generating floods)
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://<vrops-master-ip>/suite-api/api/alerts?pageSize=10" \
  | python3 -c "import json,sys; print('Active alerts:', json.load(sys.stdin).get('total','unknown'))"

# Adapter instances and their collection status
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://<vrops-master-ip>/suite-api/api/adapterinstances" \
  | python3 -c "
import json,sys
for ai in json.load(sys.stdin).get('adapterInstancesInfoDto', []):
    print(ai.get('id',''), '|', ai.get('name',''), '|', ai.get('collectorStatus',''))
"
# Problem: collectorStatus = Data Receiving/No Data = adapter collecting or not
```

---

## Step 3 — Inspect log files

```bash
# Analytics engine errors (OOM, processing failures, alert engine)
grep -i "ERROR\|Exception\|OutOfMemory\|FATAL" \
  /var/log/vmware/vcops/analytics.log | tail -50

# Adapter collection errors (adapter auth, TLS, timeout)
grep -i "ERROR\|Exception\|fail\|timeout" \
  /var/log/vmware/vcops/collector.log | tail -50

# Filter for a specific adapter by name (e.g., vCenter adapter)
grep -i "VMware vCenter" /var/log/vmware/vcops/collector.log | tail -30

# Follow analytics log in real time during a failing operation
tail -f /var/log/vmware/vcops/analytics.log | grep -i "error\|warn\|exception"

# Check for heap OOM errors specifically (common on undersized vROps nodes)
grep "OutOfMemoryError" /var/log/vmware/vcops/analytics.log | tail -20
# If present: check heap allocation in VAMI → Administration → JVM Memory
```

---

## Step 4 — Check adapter collection status

```bash
# Via vROps UI (most informative):
# Navigate to: Administration → Solutions → Adapter Instances
# For each adapter instance, check:
# - Status: Collection State (collecting/not collecting)
# - Last Updated: should be within the collection interval (typically 5 minutes)
# - Messages: shows adapter-specific error if collection failed

# Test adapter credentials from vROps UI:
# Click adapter → Test Connection
# This runs a live connectivity test from the vROps collector to the source

# Via collector.log — find the last collection attempt for vCenter adapter
grep "vCenter" /var/log/vmware/vcops/collector.log | \
  grep -i "Start collection\|End collection\|error" | tail -30

# Check if collection is happening every 5 minutes (expected interval)
grep "Start collection" /var/log/vmware/vcops/collector.log | \
  tail -10 | awk '{print $1, $2}'
# Expected: entries every 5 minutes per adapter instance
```

---

## Step 5 — Check vROps cluster node health

```bash
# Detailed node status
cluster-mgmt-cli status
# Shows: node ID, role, state, heartbeat timestamp

# Check replica node heartbeat (loss of replica = HA risk)
cluster-mgmt-cli -cmd showclusterstate
# Expected: all nodes in ONLINE state; masterNodeId matches the master

# Verify all nodes have NTP in sync (time drift > 5 minutes breaks cluster communication)
for node in <master-ip> <replica-ip> <data-node-ip>; do
  echo "=== $node ==="
  ssh admin@$node "chronyc tracking | grep 'System time'"
done

# Check VAMI for disk allocation per node
# Browse to: https://<vrops-node-ip>:5480
# Navigate to: Administration → Disk Usage
# Alert: /storage/db > 85% used

# Restart vROps service if analytics engine is stuck (safe for planned restart)
systemctl restart vmware-vcops
# Allow 5–10 minutes for full service startup; monitor with:
journalctl -u vmware-vcops -f
```

---

## Step 6 — Check disk space and performance

```bash
# Storage partitions specific to vROps
df -h /storage/db       # analytics data; should be < 80%
df -h /var/log          # log partition
df -h /data             # vROps data files

# Large log files that can be safely removed (keep last 7 days)
find /var/log/vmware/vcops/ -name "*.log.*" -mtime +7 | head -20
find /var/log/vmware/vcops/ -name "*.log.*" -mtime +7 -delete

# Check analytics DB size
du -sh /storage/db/
du -sh /storage/db/casa/  # CASA analytics store

# vROps JVM heap usage (if analytics.log shows OOM)
# Browse to: https://<vrops-master-ip>:5480
# Navigate to: Administration → JVM Memory Configuration
# Recommended: heap size = 70% of node RAM for dedicated nodes

# Check for core dump files
find / -name "core.*" -size +100M 2>/dev/null
```

---

## Step 7 — Collect support bundle for VMware SR

```bash
# Via SSH on the master node (recommended method)
ssh admin@<vrops-master-ip>
vcops-support gen
# Output: /tmp/vcops-support-<timestamp>.zip
# Includes: all cluster logs, analytics DB snapshot, configuration, node states

# Download the bundle
scp admin@<vrops-master-ip>:/tmp/vcops-support-*.zip ./

# Via VAMI (if SSH is unavailable)
# Browse to: https://<vrops-master-ip>:5480
# Navigate to: Administrator → Support → Generate Support Bundle → Download

# Include in VMware SR:
# - vcops-support ZIP bundle
# - vROps version: vROps UI → Administration → About
# - Node count and node IPs (master, replica, data nodes)
# - Adapter instance name and adapter type that is failing
# - Resource type and count that is missing or wrong
# - Time window when data stopped appearing
```

---

## Log locations

| Component | Path | What to look for |
|---|---|---|
| Analytics engine | `/var/log/vmware/vcops/analytics.log` | OOM errors, alert engine failures, processing |
| Adapter collector | `/var/log/vmware/vcops/collector.log` | Per-adapter collection attempts and failures |
| vROps service | `journalctl -u vmware-vcops` | Service start/stop/crash events |
| CASA data store | `/storage/db/casa/` | Analytics data files (size only; don't modify) |
| Cluster state | `cluster-mgmt-cli status` | Node roles and heartbeat state |

---

## See also

- [Aria Operations — Common Issues](../common-issues/)
- [Aria Operations — Escalation](../escalation/)

## Verify resolution

- `GET /suite-api/api/health` returns all components online with no degraded nodes
- `cluster-mgmt-cli status` shows master and all replica/data nodes ONLINE
- `grep -i error /var/log/vmware/vcops/collector.log | wc -l` shows no new errors after fixing adapter credentials
- Adapter instance collection state shows "Data Receiving" and last updated time is within the collection interval
- Resource count returned by `GET /api/resources?pageSize=1` matches expected inventory size
