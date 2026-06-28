---
tags:
  - operations
---
# OpenShift — Health Checks

<div class="kb-summary">
Daily cluster health routine: cluster operators, node status, etcd health, monitoring stack, networking, storage, certificate expiry, and resource pressure. Run before and after every change.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
health_check_triage_flow: "Health Check Triage Flow" {shape: rectangle}
cluster_operator_health: "Cluster Operator Health" {shape: rectangle}
node_health: "Node Health" {shape: rectangle}
etcd_health: "etcd Health" {shape: rectangle}
networking_health: "Networking Health" {shape: rectangle}
storage_health: "Storage Health" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> health_check_triage_flow
health_check_triage_flow -> cluster_operator_health
cluster_operator_health -> node_health
node_health -> etcd_health
etcd_health -> networking_health
networking_health -> storage_health
storage_health -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Health Check Triage Flow

```mermaid
graph TD
    A["Start: scheduled\nhealth check"]:::dark --> B{"CVO status\noc get clusterversion"}:::dark
    B -->|"Progressing=True\nor Degraded=True"| B1["Investigate CVO\noc describe clusterversion"]:::red
    B -->|"Available=True"| C{"Cluster Operators\noc get co"}:::blue
    C -->|"Any Degraded=True"| C1["Investigate CO\noc describe co <name>"]:::red
    C -->|"All healthy"| D{"Nodes\noc get nodes"}:::blue
    D -->|"NotReady node"| D1["Describe node\ncheck kubelet/conditions"]:::red
    D -->|"All Ready"| E{"etcd\nendpoint health"}:::green
    E -->|"Endpoint unhealthy\nor db > 8 GB"| E1["etcd triage\ncheck leader, defrag"]:::red
    E -->|"All healthy"| F{"Networking\novn+dns pods"}:::green
    F -->|"Pods not Running"| F1["Restart pod\ncheck ovn logs"]:::red
    F -->|"All Running"| G{"Storage\npv/pvc status"}:::orange
    G -->|"Pending PVCs\nor Failed PVs"| G1["Check CSI driver\ncheck storageclass"]:::red
    G -->|"All healthy"| H["HEALTHY\nlog result"]:::teal

    classDef dark fill:#374151,color:#fff
    classDef blue fill:#2563eb,color:#fff
    classDef green fill:#15803d,color:#fff
    classDef orange fill:#b45309,color:#fff
    classDef teal fill:#164e63,color:#fff
    classDef red fill:#991b1b,color:#fff
```

## Cluster Operator Health

`oc get co` output columns: `NAME  VERSION  AVAILABLE  PROGRESSING  DEGRADED  SINCE  MESSAGE`

Healthy state: `AVAILABLE=True  PROGRESSING=False  DEGRADED=False`

| Column value | Meaning | Action |
|---|---|---|
| `AVAILABLE=False` | Operator not serving its function | Describe CO; check pods in operator namespace |
| `PROGRESSING=True` (> 30 min) | Stuck update or rollout | Describe CO; check operator pod logs |
| `DEGRADED=True` | Config or runtime error | Describe CO; read `message` field for root cause |
| `SINCE` > expected upgrade window | Operator took unusually long | Compare to previous upgrade history |

```bash
# Full CO status — healthy cluster shows no output from this command
oc get co | grep -v "True.*False.*False" | grep -v "^NAME"

# Investigate specific degraded operator
oc describe co authentication
# Read the "Conditions:" block; "message:" field explains the failure

# Check operator pod logs (namespace varies by operator)
oc get pods -n openshift-authentication
oc logs -n openshift-authentication deployment/oauth-openshift --tail=100

# Key operators and their namespaces
# authentication    → openshift-authentication
# dns               → openshift-dns
# etcd              → openshift-etcd
# ingress           → openshift-ingress
# kube-apiserver    → openshift-kube-apiserver
# machine-config    → openshift-machine-config-operator
# monitoring        → openshift-monitoring
# network           → openshift-ovn-kubernetes
# storage           → openshift-cluster-csi-drivers
```

## Node Health

```bash
# Overview: STATUS, ROLES, AGE, VERSION
oc get nodes -o wide

# Healthy output: all STATUS=Ready, VERSION identical across nodes
# Unhealthy indicators: NotReady, SchedulingDisabled (cordoned)

# Detailed node conditions
oc describe node <node-name>
# Watch for in "Conditions:" section:
#   MemoryPressure=True   → node running low on memory; pods may be evicted
#   DiskPressure=True     → disk usage > eviction threshold; clear logs/images
#   PIDPressure=True      → too many processes; check for runaway workloads
#   Ready=False           → kubelet not communicating; check kubelet service

# Resource usage per node
oc adm top nodes
# Alert if CPU or MEMORY% > 85% sustained

# Top pods across cluster
oc adm top pods --all-namespaces --sort-by=cpu | head -20
oc adm top pods --all-namespaces --sort-by=memory | head -20

# Check MachineConfigPool — MCO-driven node config status
oc get mcp
# UPDATED=False or DEGRADED=True: node failed to apply MachineConfig
oc describe mcp worker     # See which node is blocking
```

## etcd Health

etcd is the cluster database. A degraded etcd member or high write latency can cause API instability and failed writes across the cluster.

```bash
# Get an etcd pod name
ETCD_POD=$(oc get pod -n openshift-etcd -l etcd=true -o name | head -1)

# Endpoint health (all 3 members must be healthy)
oc rsh -n openshift-etcd $ETCD_POD \
  etcdctl endpoint health \
  --endpoints=https://localhost:2379 \
  --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
  --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).crt \
  --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).key

# Expected output per member:
# https://192.168.100.10:2379 is healthy: successfully committed proposal

# Endpoint status — DB size, leader, raft index
oc rsh -n openshift-etcd $ETCD_POD \
  etcdctl endpoint status --cluster -w table \
  --endpoints=https://localhost:2379 \
  --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
  --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).crt \
  --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).key
# Columns: ENDPOINT | ID | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX
# DB SIZE: alert if > 8 GB; defrag if so

# Defrag etcd (do on non-leader members first, then leader last)
oc rsh -n openshift-etcd $ETCD_POD \
  etcdctl defrag \
  --endpoints=https://<member-ip>:2379 \
  --cacert=... --cert=... --key=...

# P99 commit latency via Prometheus
# histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m]))
# Alert threshold: > 0.01 (10 ms)
```

## Networking Health

```bash
# OVN-Kubernetes pods (SDN data plane)
oc get pods -n openshift-ovn-kubernetes
# Expected: ovnkube-master-* and ovnkube-node-* all Running
# ovnkube-node runs as DaemonSet — one pod per node

# CoreDNS (service DNS)
oc get pods -n openshift-dns
# Expected: dns-default-* Running on every node (DaemonSet)

# Test DNS resolution from inside a pod
oc debug deployment/myapp -n mynamespace -- nslookup kubernetes.default.svc.cluster.local
# Expected: Server: 172.30.0.10 / Address: <ClusterIP of kubernetes service>

# Test external DNS from pod
oc debug deployment/myapp -n mynamespace -- nslookup registry.redhat.io

# Ingress (router) health
oc get pods -n openshift-ingress
# Expected: router-default-* Running

# Test ingress route
curl -k -o /dev/null -w "%{http_code}" https://console-openshift-console.apps.<cluster>.<base>
# Expected: 200 or 302

# Check ingress operator
oc describe co ingress
```

## Storage Health

```bash
# PersistentVolume status
oc get pv
# STATUS column: Bound=in use, Available=free, Released=PVC deleted (data retained), Failed=error
# Any Released or Failed PVs → investigate; Released PVs with retain policy need manual cleanup

# PersistentVolumeClaim status across all namespaces
oc get pvc -A
# STATUS: Bound=OK, Pending=provisioner cannot fulfill request → check CSI driver and StorageClass

# CSI driver pods
oc get pods -n openshift-cluster-csi-drivers
# All pods Running; operator pods and node-level driver pods

# Check default StorageClass
oc get sc
# At least one (default) StorageClass required for dynamic provisioning

# Storage operator status
oc describe co storage
```

## Run This Routine

Run in order — each check gates the next.

```bash
#!/bin/bash
# OpenShift Cluster Health Check
# Usage: KUBECONFIG=/path/to/kubeconfig bash ocp-health.sh

PASS=0
FAIL=0

check() {
  local label="$1"
  local result="$2"
  if [[ -z "$result" ]]; then
    echo "PASS  $label"
    ((PASS++))
  else
    echo "FAIL  $label"
    echo "      $result"
    ((FAIL++))
  fi
}

echo "===== OpenShift Health Check $(date) ====="

# 1. Cluster Version
CV=$(oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Degraded")].status}')
check "ClusterVersion not Degraded" "$([ "$CV" = "True" ] && echo "ClusterVersion Degraded=True")"

# 2. Cluster Operators
CO_BAD=$(oc get co --no-headers | grep -v "True\s*False\s*False" | awk '{print $1}')
check "All ClusterOperators healthy" "$CO_BAD"

# 3. Nodes Ready
NODES_BAD=$(oc get nodes --no-headers | grep -v " Ready " | awk '{print $1}')
check "All nodes Ready" "$NODES_BAD"

# 4. MachineConfigPools not Degraded
MCP_BAD=$(oc get mcp --no-headers | awk '$4=="True"{print $1}')
check "MachineConfigPools not Degraded" "$MCP_BAD"

# 5. Unhealthy pods (excluding Completed/Succeeded)
PODS_BAD=$(oc get pods -A --no-headers | grep -vE "Running|Completed|Succeeded" | awk '{print $1"/"$2}' | head -10)
check "No unhealthy pods" "$PODS_BAD"

# 6. etcd endpoint health
ETCD_POD=$(oc get pod -n openshift-etcd -l etcd=true -o name | head -1)
ETCD_OUT=$(oc rsh -n openshift-etcd $ETCD_POD \
  etcdctl endpoint health --cluster \
  --endpoints=https://localhost:2379 \
  --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
  --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).crt \
  --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).key \
  2>&1 | grep -v "is healthy")
check "etcd all endpoints healthy" "$ETCD_OUT"

# 7. OVN-Kubernetes pods Running
OVN_BAD=$(oc get pods -n openshift-ovn-kubernetes --no-headers | grep -v Running | awk '{print $1}')
check "OVN-Kubernetes pods Running" "$OVN_BAD"

# 8. CoreDNS pods Running
DNS_BAD=$(oc get pods -n openshift-dns --no-headers | grep -v Running | awk '{print $1}')
check "CoreDNS pods Running" "$DNS_BAD"

# 9. No Pending PVCs
PVC_PEND=$(oc get pvc -A --no-headers | grep Pending | awk '{print $1"/"$2}')
check "No Pending PVCs" "$PVC_PEND"

# 10. Monitoring stack Running
MON_BAD=$(oc get pods -n openshift-monitoring --no-headers | grep -v Running | grep -v Completed | awk '{print $1}')
check "Monitoring stack Running" "$MON_BAD"

echo ""
echo "===== Result: $PASS PASS / $FAIL FAIL ====="
[ $FAIL -gt 0 ] && exit 1 || exit 0
```

## etcd Performance Check

```bash
# Check P99 commit latency (should be < 10ms = 0.010 s)
# Via Prometheus (preferred):
# histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m]))

# Via etcdctl check perf (generates load — do not run on production during peak)
oc rsh -n openshift-etcd $ETCD_POD \
  etcdctl check perf \
  --endpoints=https://localhost:2379 \
  --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
  --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).crt \
  --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).key

# If latency is high: check disk IOPS on master nodes
# etcd requires SSD with > 500 IOPS sustained write performance
# VMware: ensure vSAN or NVMe-backed datastore; avoid spinning disk
```

## Node Resource Check

```bash
# Resource usage per node
oc adm top nodes
oc adm top pods --all-namespaces --sort-by=cpu | head -20
oc adm top pods --all-namespaces --sort-by=memory | head -20

# Check node conditions (Pressure states)
oc describe nodes | grep -A5 "Conditions:"
# Watch for: MemoryPressure, DiskPressure, PIDPressure = True

# Check kubelet log on a specific node
oc debug node/<node-name> -- chroot /host journalctl -u kubelet --since "1 hour ago" | tail -50

# Image disk usage on a node (can cause DiskPressure)
oc debug node/<node-name> -- chroot /host crictl images | sort -k4 -h | tail -20
# Remove unused images: crictl rmi --prune
```

---

## See also

- [OpenShift — Common Issues](../../troubleshooting/common-issues/)
- [OpenShift — Procedures](../procedures/)
- [OpenShift — CLI Reference](../cli-reference/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
