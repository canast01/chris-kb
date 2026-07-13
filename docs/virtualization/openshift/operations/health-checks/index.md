---
tags:
  - operations
description: "Daily cluster health routine: cluster operators, node status, etcd health, monitoring stack, networking, storage, certificate expiry, and resource..."
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


```text title="Expected output"
authentication                                       True        False        False      2d
dns                                                  True        True         False      2d
etcd                                                 True        False        False      2d
ingress                                              True        False        False      2d
kube-apiserver                                       True        False        False      2d
machine-config                                       True        False        False      2d
monitoring                                           True        False        False      2d
network                                              True        False        False      2d
storage                                              True        False        False      2d

Name:         authentication
Namespace:    openshift-authentication
Labels:       <none>
Annotations:  <none>
API Version:  config.openshift.io/v1
Kind:         ClusterOperator
Status:
  Conditions:
    Last Transition Time:  2024-01-15T08:32:14Z
    Message:               OAuth server deployment has 3 replicas, all available, all updated
    Reason:                AsExpected
    Status:                True
    Type:                  Available

NAME                                    READY   STATUS    RESTARTS   AGE
oauth-openshift-5d8c9f2b4-7k9m2        1/1     Running   0          2d
oauth-openshift-5d8c9f2b4-m3xp6        1/1     Running   0          2d
oauth-openshift-5d8c9f2b4-q2lw8        1/1     Running   0          2d
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "co"`** — Ensure you are connected to an OpenShift cluster (not vanilla Kubernetes) with `oc login` and verify API availability.
    **`Error from server (NotFound): namespaces "openshift-authentication" not found`** — Confirm the operator namespace exists with `oc get ns | grep openshift` and check that the cluster operator is actually installed.
    **`error: expected 'logs' subcommand or flag`** — Use the correct syntax `oc logs -n <namespace> <pod-name>` or `oc logs -n <namespace> deployment/<name>` without extra flags before the resource type.
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


```text title="Expected output"
NAME                    STATUS   ROLES           AGE    VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE
master-01.ocp.local     Ready    control-plane   45d    v1.27.6   10.0.1.10       <none>        Red Hat Enterprise Linux CoreOS 4.13.11
master-02.ocp.local     Ready    control-plane   45d    v1.27.6   10.0.1.11       <none>        Red Hat Enterprise Linux CoreOS 4.13.11
master-03.ocp.local     Ready    control-plane   45d    v1.27.6   10.0.1.12       <none>        Red Hat Enterprise Linux CoreOS 4.13.11
worker-01.ocp.local     Ready    worker          42d    v1.27.6   10.0.2.20       <none>        Red Hat Enterprise Linux CoreOS 4.13.11
worker-02.ocp.local     Ready    worker          42d    v1.27.6   10.0.2.21       <none>        Red Hat Enterprise Linux CoreOS 4.13.11

Conditions:
  Type                 Status  LastHeartbeatTime         Reason
  MemoryPressure       False   Wed Jan 10 14:32:15 2024  KubeletHasSufficientMemory
  DiskPressure         False   Wed Jan 10 14:32:15 2024  KubeletHasNoDiskPressure
  PIDPressure          False   Wed Jan 10 14:32:15 2024  KubeletHasSufficientPID
  Ready                True    Wed Jan 10 14:32:15 2024  KubeletReady

NAME                    CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
master-01.ocp.local     1240m        31%    8192Mi          52%
master-02.ocp.local     1156m        29%    7840Mi          50%
master-03.ocp.local     1312m        33%    8512Mi          54%
worker-01.ocp.local     2840m        71%    14336Mi         91%
worker-02.ocp.local     1920m        48%    9216Mi          59%

NAMESPACE              NAME                                    CPU(m)   MEMORY(Mi)
openshift-monitoring   prometheus-k8s-0                        892      2048
openshift-apiserver    apiserver-6d4f7c8b9e2a1f3g             645      1536
kube-system            etcd-master-01.ocp.local               512      768
openshift-etcd         etcd-member-master-02.ocp.local        478      704
monitoring             grafana-deployment-5f8c9d2e1a3b       234      512

NAME     CONFIG                                   UPDATED   UPDATING   DEGRADED   NODES-READY   NODES-UPDATED   NODES-AVAILABLE   NODES-DEGRADED
master   rendered-master-a1b2c3d4e5f6g7h8i9j0k   True      False      False      3             3                3                 0
worker   rendered-worker-x9y8z7w6v
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


```text title="Expected output"
pod/etcd-ip-192-168-100-10.ec2.internal
https://192.168.100.10:2379 is healthy: successfully committed proposal
https://192.168.100.11:2379 is healthy: successfully committed proposal
https://192.168.100.12:2379 is healthy: successfully committed proposal
+------------------------+------------------+---------+---------+----------+-----------+-----------+-----------+
| ENDPOINT               | ID               | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX |
+------------------------+------------------+---------+---------+----------+-----------+-----------+-----------+
| https://192.168.100.10:2379 | 8e9c42a7b1d5f3c2 | 3.5.9   | 2.1 GB  | true      | false     | 847       | 18492156  |
| https://192.168.100.11:2379 | 7f2d8c1a9e4b6k9l | 3.5.9   | 2.0 GB  | false     | false     | 847       | 18492156  |
| https://192.168.100.12:2379 | 6a3e9d2b8f5c7m1n | 3.5.9   | 2.2 GB  | false     | false     | 847       | 18492156  |
+------------------------+------------------+---------+---------+----------+-----------+-----------+-----------+
Finished defragmenting etcd member 8e9c42a7b1d5f3c2
```

!!! warning "Common errors"
    **`error: unable to connect to etcd: context deadline exceeded`** — Verify the etcd pod is running with `oc get pod -n openshift-etcd` and check network connectivity to the endpoint IP.
    **`x509: certificate signed by unknown authority`** — Ensure the cacert, cert, and key paths are correct and the certificates have not expired with `oc get secret -n openshift-etcd etcd-all-certs -o yaml`.
    **`etcdctl: command not found`** — The etcdctl binary is not available in the etcd pod image; use `oc debug node/<node-name>` and mount the etcd container to access the binary directly.
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


```text title="Expected output"
NAME                                      READY   STATUS    RESTARTS   AGE
ovnkube-master-7k9m2                      2/2     Running   0          8d
ovnkube-master-b4lx8                      2/2     Running   0          8d
ovnkube-master-c2p5q                      2/2     Running   0          8d
ovnkube-node-4jnxk                        1/1     Running   0          7d
ovnkube-node-8vqrs                        1/1     Running   0          7d
ovnkube-node-d6m9p                        1/1     Running   0          7d
...

NAME                      READY   STATUS    RESTARTS   AGE
dns-default-7h2kl         1/1     Running   0          8d
dns-default-m8qpn         1/1     Running   0          8d
dns-default-x5r3j         1/1     Running   0          8d

Server:		172.30.0.10
Address:	172.30.0.10#53

Name:	kubernetes.default.svc.cluster.local
Address: 172.30.0.1

Server:		172.30.0.10
Address:	172.30.0.10#53

Name:	registry.redhat.io
Address: 52.204.18.75

NAME                              READY   STATUS    RESTARTS   AGE
router-default-5m7np              1/1     Running   0          8d
router-default-9k2lq              1/1     Running   0          8d

200

Name:                  ingress
Namespace:             openshift-ingress-operator
Labels:               
Annotations:          
Status:               Available
Message:              
Reason:               AsExpected
```

!!! warning "Common errors"
    **`Error from server (NotFound): deployments.apps "myapp" not found`** — Verify the deployment name and namespace with `oc get deployments -n mynamespace` before running debug.
    **`Server: [::1] / Address: ::1#53 (connection timeout)`** — Ensure CoreDNS pods are running with `oc get pods -n openshift-dns` and check pod logs with `oc logs -n openshift-dns <pod-name>`.
    **`curl: (7) Failed to connect to console-openshift-console.apps.<cluster>.<base> port 443: Name or address not known`** — Replace `<cluster>.<base>` with your actual cluster domain (e.g., `oc whoami --show-console` to verify the correct URL).
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


```text title="Expected output"
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                    STORAGECLASS   REASON   AGE
pvc-a1b2c3d4-e5f6-7890-abcd-ef1234567890   100Gi      RWO            Delete           Bound    openshift-monitoring/prometheus-k8s              gp3-csi                5d
pvc-b2c3d4e5-f6a7-8901-bcde-f12345678901   50Gi       RWO            Delete           Bound    openshift-logging/elasticsearch-cdm-xyz          gp3-csi                3d
pvc-c3d4e5f6-a7b8-9012-cdef-123456789012   20Gi       RWX            Retain           Released                                           gp3-csi                7d
pvc-d4e5f6a7-b8c9-0123-defg-234567890123   10Gi       RWO            Delete           Failed                                             gp3-csi    ProvisioningFailed   2d

NAME                                    STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
prometheus-k8s-db-0                     Bound    pvc-a1b2c3d4-e5f6-7890-abcd-ef1234567890   100Gi      RWO            gp3-csi        5d
elasticsearch-cdm-xyz-0                 Bound    pvc-b2c3d4e5-f6a7-8901-bcde-f12345678901   50Gi       RWO            gp3-csi        3d
test-app-pvc                            Pending                                                                        gp3-csi        12h

NAME                                              READY   STATUS    RESTARTS   AGE
aws-ebs-csi-driver-controller-5d8f7c9b4-xyz12    2/2     Running   0          8d
aws-ebs-csi-driver-node-2xk9m                    3/3     Running   1          8d
aws-ebs-csi-driver-node-4lp6n                    3/3     Running   0          8d
aws-ebs-csi-driver-node-7qr8s                    3/3     Running   2          8d
csi-snapshot-controller-0                        1/1     Running   0          8d

NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
gp3-csi (default)    ebs.csi.aws.com         Delete          WaitForFirstConsumer   true                   45d
standard             kubernetes.io/aws-ebs   Delete          Immediate             false                  45d

Name:                  storage
Namespace:             openshift-cluster-storage-operator
Labels:                <none>
Annotations:           <none>
API Version:           config.openshift.io/v1
Kind:                  ClusterOperator
Status:
  Conditions:
  - Last Transition Time:  2024-01-15T14:32:18Z
    Message:               
    Reason:                As
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


```text title="Expected output"
===== OpenShift Health Check Thu Jan 16 14:32:18 UTC 2025 =====
PASS  ClusterVersion not Degraded
PASS  All ClusterOperators healthy
PASS  All nodes Ready
PASS  MachineConfigPools not Degraded
FAIL  No unhealthy pods
      openshift-apiserver/apiserver-5d7c9f2b1
      openshift-controller-manager/controller-manager-wx8kl
PASS  etcd all endpoints healthy
PASS  OVN-Kubernetes pods Running
PASS  CoreDNS pods Running
PASS  No Pending PVCs
FAIL  Monitoring stack Running
      prometheus-operator-6f4d8c2k9
      thanos-querier-7b2e1a9m3

===== Result: 8 PASS / 2 FAIL =====
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "clusterversion"`** — Verify you are connected to an OpenShift cluster (not vanilla Kubernetes) with `oc api-resources | grep clusterversion`.
    **`error: unable to upgrade connection: container not found`** — Ensure the etcd pod is running with `oc get pods -n openshift-etcd -l etcd=true` and verify pod name matches the rsh command.
    **`KUBECONFIG: command not found`** — Set the KUBECONFIG variable before running the script: `export KUBECONFIG=/path/to/kubeconfig && bash ocp-health.sh`.
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


```text title="Expected output"
Connecting to etcd pod etcd-master-01...
60 / 60 Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
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


```text title="Expected output"
NAME                                    CPU(cores)   MEMORY(bytes)
worker-01.prod.internal                 2847m        18432Mi
worker-02.prod.internal                 1923m        12288Mi
worker-03.prod.internal                 3156m        21504Mi
master-01.prod.internal                 892m         8192Mi
master-02.prod.internal                 756m         7680Mi

NAMESPACE            NAME                                    CPU(cores)   MEMORY(bytes)
openshift-etcd       etcd-master-01.prod.internal            287m         892Mi
openshift-monitoring prometheus-operator-5d8f4c7b9d-kx2m9    156m         512Mi
openshift-apiserver  apiserver-5f7c9e2a1b-9qr3k              234m         1024Mi
kube-system          coredns-558bd4d5db-7x9m2                89m          256Mi
openshift-ingress    router-default-7c8f2e1a-5b6k            178m         768Mi
...

NAMESPACE            NAME                                    MEMORY(bytes)
openshift-etcd       etcd-master-02.prod.internal            1456Mi
openshift-monitoring prometheus-k8s-0                        2048Mi
openshift-apiserver  apiserver-5f7c9e2a1b-9qr3k              1024Mi
openshift-monitoring alertmanager-main-0                     512Mi
kube-system          coredns-558bd4d5db-7x9m2                768Mi
...

Conditions:
  Type                 Status  LastHeartbeatTime         LastTransitionTime        Reason                       Message
  Ready                True    Wed, 15 Jan 2025 14:32:15 +0000   Wed, 15 Jan 2025 09:12:00 +0000   KubeletReady            kubelet is posting ready status
  MemoryPressure       False   Wed, 15 Jan 2025 14:32:15 +0000   Wed, 15 Jan 2025 09:12:00 +0000   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         False   Wed, 15 Jan 2025 14:32:15 +0000   Wed, 15 Jan 2025 09:12:00 +0000   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure          False   Wed, 15 Jan 2025 14:32:15 +0000   Wed, 15 Jan 2025 09:12:00 +0000   KubeletHasSufficientPID      kubelet has sufficient PID available

Entering debug shell. Type 'exit' to return.
sh-4.4# journalctl -u kubelet --since "1 hour ago" | tail -50
Jan 15 14:28:34 worker-01.prod.internal kubelet[2847]: I0115 14:28:34.562891    2847 kubelet.go:1234] Starting kubelet v4.12.5
Jan 15 14:29:12 worker-01.prod.internal kubelet[
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
