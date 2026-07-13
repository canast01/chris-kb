---
tags:
  - operations
description: "Operational scripts: daily health snapshot, CSR auto-approval, node drain wrapper, etcd backup automation, pod restart loop detection, and namespace..."
---
# OpenShift — Scripts

<div class="kb-summary">
Operational scripts: daily health snapshot, CSR auto-approval, node drain wrapper, etcd backup automation, pod restart loop detection, and namespace resource summary.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

S: "scripts/" {shape: rectangle}
CH: "cluster-health-check.sh · CO / nodes / etcd / ·\nCoreDNS / ingress" {shape: rectangle}
AC: "auto-approve-csrs.sh · poll + approve · every 30s" {shape: rectangle}
EB: "etcd-backup.sh · SSH to master · copy tarball local" {shape: rectangle}
ND: "node-drain.sh · pre-check + · cordon + drain" {shape: rectangle}
PR: "pod-restart-detector.sh · find crash-looping ·\npods by threshold" {shape: rectangle}

S -> CH
S -> AC
S -> EB
S -> ND
S -> PR
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## cluster-health-check.sh

Checks cluster operators, node readiness, etcd pod count, CoreDNS, and ingress pods. Outputs PASS/FAIL per check. Exits 1 if any check fails.

```bash
#!/bin/bash
KUBECONFIG=${1:-$KUBECONFIG}
TS=$(date '+%Y-%m-%d %H:%M')
FAIL=0

pass() { echo "  PASS: $1"; }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

echo "=== OpenShift Cluster Health Check: $TS ==="
echo ""

echo "--- Cluster Version ---"
oc get clusterversion version --no-headers | awk '{print "  Version:", $2, "Available:", $3, "Progressing:", $4, "Degraded:", $5}'

echo ""
echo "--- Cluster Operators ---"
DEGRADED=$(oc get co --no-headers | awk '$4=="True" {print $1}')
PROGRESSING=$(oc get co --no-headers | awk '$3=="True" {print $1}')
[ -z "$DEGRADED" ] && pass "no degraded operators" || fail "DEGRADED: $DEGRADED"
[ -z "$PROGRESSING" ] && pass "no progressing operators" || echo "  INFO  PROGRESSING: $PROGRESSING"

echo ""
echo "--- Nodes ---"
NOT_READY=$(oc get nodes --no-headers | grep -v " Ready" | awk '{print $1}')
[ -z "$NOT_READY" ] && pass "all nodes Ready" || fail "NOT READY: $NOT_READY"

echo ""
echo "--- etcd Pods ---"
ETCD_COUNT=$(oc get pods -n openshift-etcd --no-headers | grep -c "^etcd-")
[ "$ETCD_COUNT" -eq 3 ] && pass "etcd pod count = 3" || fail "etcd pod count = $ETCD_COUNT (expected 3)"

echo ""
echo "--- CoreDNS ---"
DNS_NOT_RUNNING=$(oc get pods -n openshift-dns --no-headers | grep dns | grep -vc "Running")
[ "$DNS_NOT_RUNNING" -eq 0 ] && pass "all CoreDNS pods Running" || fail "$DNS_NOT_RUNNING CoreDNS pods not Running"

echo ""
echo "--- Ingress Controller ---"
INGRESS_NOT_RUNNING=$(oc get pods -n openshift-ingress --no-headers | grep -vc "Running")
[ "$INGRESS_NOT_RUNNING" -eq 0 ] && pass "all ingress pods Running" || fail "$INGRESS_NOT_RUNNING ingress pods not Running"

echo ""
echo "--- Unhealthy Pods (cluster-wide) ---"
UNHEALTHY=$(oc get pods --all-namespaces --no-headers | grep -cvE "Running|Completed|Succeeded")
[ "$UNHEALTHY" -eq 0 ] && pass "all pods Running/Completed" || { fail "unhealthy pod count = $UNHEALTHY"; oc get pods --all-namespaces | grep -vE "Running|Completed|Succeeded|NAMESPACE"; }

echo ""
echo "=== Result: $( [ $FAIL -eq 0 ] && echo PASS || echo "FAIL ($FAIL checks failed)" ) ==="
exit $FAIL
```


```text title="Expected output"
=== OpenShift Cluster Health Check: 2024-01-15 14:32 ===

--- Cluster Version ---
  Version: 4.13.12 Available: True Progressing: False Degraded: False

--- Cluster Operators ---
  PASS: no degraded operators
  INFO  PROGRESSING: openshift-apiserver

--- Nodes ---
  PASS: all nodes Ready

--- etcd Pods ---
  PASS: etcd pod count = 3

--- CoreDNS ---
  PASS: all CoreDNS pods Running

--- Ingress Controller ---
  PASS: all ingress pods Running

--- Unhealthy Pods (cluster-wide) ---
  PASS: all pods Running/Completed

=== Result: PASS ===
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "clusterversion"`** — Verify the cluster is OpenShift (not vanilla Kubernetes) and that the user has cluster-admin permissions.
    **`Unable to connect to the server: dial tcp: lookup api.cluster.local on 127.0.0.11:53: no such host`** — Ensure KUBECONFIG points to a valid kubeconfig file and the cluster API is reachable (check `oc status`).
    **`error: You must be logged in to the server (Unauthorized)`** — Re-authenticate with `oc login` or ensure the KUBECONFIG token has not expired.
## auto-approve-csrs.sh

Polls `oc get csr` every 30 seconds and approves all Pending CSRs. Useful during UPI installs or node replacement operations. Runs until Ctrl-C.

```bash
#!/bin/bash
INTERVAL=30

echo "[$(date '+%H:%M:%S')] CSR auto-approver started — polling every ${INTERVAL}s (Ctrl+C to stop)"

while true; do
  TS="[$(date '+%H:%M:%S')]"
  PENDING=$(oc get csr --no-headers 2>/dev/null | awk '/Pending/ {print $1}')
  if [ -n "$PENDING" ]; then
    COUNT=$(echo "$PENDING" | wc -l | tr -d ' ')
    echo "$TS Approving $COUNT pending CSR(s): $(echo $PENDING | tr '\n' ' ')"
    echo "$PENDING" | xargs oc adm certificate approve
    echo "$TS Approved."
  else
    echo "$TS No pending CSRs."
  fi
  sleep "$INTERVAL"
done
```


```text title="Expected output"
[14:32:18] CSR auto-approver started — polling every 30s (Ctrl+C to stop)
[14:32:18] Approving 2 pending CSR(s): csr-8xk9m csr-lq2p7 
certificatesigningrequest.certificates.k8s.io/csr-8xk9m approved
certificatesigningrequest.certificates.k8s.io/csr-lq2p7 approved
[14:32:18] Approved.
[14:32:48] No pending CSRs.
[14:33:18] No pending CSRs.
[14:33:48] Approving 1 pending CSR(s): csr-9vr4n 
certificatesigningrequest.certificates.k8s.io/csr-9vr4n approved
[14:33:48] Approved.
[14:34:18] No pending CSRs.
```

!!! warning "Common errors"
    **`error: unable to connect to the server: dial tcp: lookup api.cluster.local on [IP]: no such host`** — Ensure KUBECONFIG is set correctly and the cluster API endpoint is reachable: `export KUBECONFIG=/path/to/kubeconfig`.
    **`error: You must be logged in to the server (Unauthorized)`** — Re-authenticate with the cluster using `oc login` or verify your service account token has sufficient permissions.
    **`xargs: oc: No such file or directory`** — Add the oc binary to your PATH or use the full path to oc (e.g., `/usr/local/bin/oc`).
## etcd-backup.sh

SSHes to master-0 (auto-detected or supplied), runs `cluster-backup.sh`, copies the tarball to a local path, and verifies the backup file is larger than 100 KB.

```bash
#!/bin/bash
MASTER=${1:-$(oc get nodes -l node-role.kubernetes.io/master -o name 2>/dev/null | head -1 | cut -d/ -f2)}
LOCAL_DIR=${2:-/tmp/etcd-backup-$(date +%F)}

[ -z "$MASTER" ] && { echo "ERROR: no master node found or supplied"; exit 1; }

echo "Master node : $MASTER"
echo "Local backup: $LOCAL_DIR"
mkdir -p "$LOCAL_DIR"

REMOTE_DIR="/home/core/assets/backup"

echo "Running cluster-backup.sh on $MASTER via SSH..."
ssh -o StrictHostKeyChecking=no "core@$MASTER" \
  "sudo /usr/local/bin/cluster-backup.sh $REMOTE_DIR"

echo "Copying backup files to $LOCAL_DIR..."
scp -o StrictHostKeyChecking=no \
  "core@$MASTER:$REMOTE_DIR/snapshot_*.db" \
  "core@$MASTER:$REMOTE_DIR/static_kuberesources_*.tar.gz" \
  "$LOCAL_DIR/"

SNAPSHOT=$(ls "$LOCAL_DIR"/snapshot_*.db 2>/dev/null | head -1)
[ -z "$SNAPSHOT" ] && { echo "ERROR: snapshot file not found in $LOCAL_DIR"; exit 1; }

SIZE=$(stat -f%z "$SNAPSHOT" 2>/dev/null || stat -c%s "$SNAPSHOT")
MIN_SIZE=$((100 * 1024))
if [ "$SIZE" -lt "$MIN_SIZE" ]; then
  echo "ERROR: snapshot file too small (${SIZE} bytes) — backup may be corrupt"
  exit 1
fi

echo "Backup verified: $(ls -lh "$SNAPSHOT")"
echo "Backup path   : $LOCAL_DIR"
```


```text title="Expected output"
Master node : master-0.example.com
Local backup: /tmp/etcd-backup-2024-01-15
Running cluster-backup.sh on master-0.example.com via SSH...
etcd snapshot start time       : 2024-01-15 14:32:18.456789
etcd snapshot finish time      : 2024-01-15 14:32:45.123456
snapshot db size               : 1.2 GB
static kube resources size     : 245 MB
Copying backup files to /tmp/etcd-backup-2024-01-15...
snapshot_2024-01-15_143218.db                                100%  1.2GB   8.5MB/s   02:24
static_kuberesources_2024-01-15_143245.tar.gz                100%  245MB   6.2MB/s   00:40
Backup verified: -rw-r--r-- 1 core core 1.2G Jan 15 14:32 /tmp/etcd-backup-2024-01-15/snapshot_2024-01-15_143218.db
Backup path   : /tmp/etcd-backup-2024-01-15
```

!!! warning "Common errors"
    **`ERROR: no master node found or supplied`** — Ensure the OpenShift cluster is accessible via `oc` and at least one master node is labeled with `node-role.kubernetes.io/master`.
    **`Permission denied (publickey,gssapi-keyexchange)`** — Verify SSH key-based authentication is configured for the `core` user on the master node, or add the public key to `~/.ssh/authorized_keys`.
    **`ERROR: snapshot file not found in /tmp/etcd-backup-2024-01-15`** — Check that `/usr/local/bin/cluster-backup.sh` exists and executed successfully on the master node by running it manually via SSH.
## node-drain.sh

```bash
#!/bin/bash
NODE=$1
[ -z "$NODE" ] && { echo "Usage: $0 <node-name>"; exit 1; }

echo "=== Pre-drain health check ==="
DEGRADED=$(oc get co --no-headers | awk '$4=="True" {print $1}')
[ -n "$DEGRADED" ] && { echo "ABORT: degraded operators: $DEGRADED"; exit 1; }

echo "Cordoning $NODE..."
oc adm cordon "$NODE"

echo "Draining $NODE..."
oc adm drain "$NODE" \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=60 \
  --timeout=300s

echo ""
echo "$NODE drained successfully."
echo "After maintenance, run:"
echo "  oc adm uncordon $NODE"
echo "  oc get node $NODE"
```


```text title="Expected output"
=== Pre-drain health check ===
Cordoning worker-node-03...
node/worker-node-03 cordoned
Draining worker-node-03...
WARNING: ignoring DaemonSet-managed Pods: openshift-monitoring/node-exporter-abc12, openshift-sdn/sdn-9xk4l
evicting pod default/app-deployment-5d4c7f8b9-lmn2o
evicting pod kube-system/coredns-558bd4d5db-pq7rs
pod/app-deployment-5d4c7f8b9-lmn2o evicted
pod/coredns-558bd4d5db-pq7rs evicted

worker-node-03 drained successfully.
After maintenance, run:
  oc adm uncordon worker-node-03
  oc get node worker-node-03
```

!!! warning "Common errors"
    **`error: unable to drain node "worker-node-03", aborting command:there are pending pods when an error is occurred: default/stuck-pod-xyz`** — Add `--force` flag or manually delete the blocking pod with `oc delete pod stuck-pod-xyz -n default --grace-period=0 --force` before draining.
    **`ABORT: degraded operators: authentication,ingress`** — Wait for operators to recover with `oc get co -w` or investigate root cause with `oc describe co <operator-name>` before attempting drain.
    **`error: node "worker-node-04" not found`** — Verify the node name exists with `oc get nodes` and use the correct node identifier.
## pod-restart-detector.sh

```bash
#!/bin/bash
THRESHOLD=${1:-5}

echo "Pods with > $THRESHOLD restarts:"
oc get pods --all-namespaces -o json | \
  jq -r '.items[] | select(.status.containerStatuses != null) |
    .metadata.namespace + "/" + .metadata.name + " restarts=" +
    (.status.containerStatuses[0].restartCount | tostring)' | \
  awk -F'restarts=' -v t="$THRESHOLD" '$2+0 > t {print}' | \
  sort -t= -k2 -rn
```


```text title="Expected output"
Pods with > 5 restarts:
openshift-monitoring/prometheus-operator restarts=47
openshift-apiserver/apiserver-5d8f2c9b4-kx7nm restarts=23
openshift-etcd/etcd-master-01.example.com restarts=18
openshift-kube-controller-manager/kube-controller-manager-master-02 restarts=12
kube-system/coredns-558bd4d5db-9m2k4 restarts=8
```

!!! warning "Common errors"
    **`jq: error (at <stdin>:1): Cannot index null with string "containerStatuses"`** — Add a null check: `select(.status.containerStatuses != null and (.status.containerStatuses | length) > 0)` before accessing the array.
    **`awk: syntax error in pattern near line 1`** — Ensure `$THRESHOLD` is passed as a numeric value; quote the entire awk script or use `awk -v t="$THRESHOLD"` without embedded shell variables.
## csr-approve.sh

```bash
#!/bin/bash
WATCH=${1:-""}

approve_pending() {
  PENDING=$(oc get csr --no-headers | grep Pending | awk '{print $1}')
  if [ -n "$PENDING" ]; then
    echo "Approving CSRs: $PENDING"
    echo "$PENDING" | xargs oc adm certificate approve
  else
    echo "No pending CSRs"
  fi
}

if [ "$WATCH" = "--watch" ]; then
  echo "Watching for CSRs every 10s (Ctrl+C to stop)..."
  while true; do approve_pending; sleep 10; done
else
  approve_pending
fi
```


```text title="Expected output"
No pending CSRs
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "csr"`** — Ensure you are connected to a valid OpenShift cluster with `oc login` and have appropriate RBAC permissions.
    **`error: You must be logged in to the server (Unauthorized)`** — Authenticate to the OpenShift cluster using `oc login <cluster-url>` with valid credentials.
## health-check.sh

Legacy version — minimal output, good for cron + email alerting.

```bash
#!/bin/bash
KUBECONFIG=${1:-$KUBECONFIG}
TS=$(date '+%Y-%m-%d %H:%M')
FAIL=0

check() { local label=$1; shift; echo -n "[$label] "; "$@" && echo "OK" || { echo "FAIL"; FAIL=$((FAIL+1)); }; }

echo "=== OpenShift Health Check: $TS ==="
echo ""

echo "--- Cluster Operators ---"
DEGRADED=$(oc get co --no-headers | awk '$4=="True" {print $1}')
PROGRESSING=$(oc get co --no-headers | awk '$3=="True" {print $1}')
[ -z "$DEGRADED" ] && echo "  OK: no degraded operators" || { echo "  DEGRADED: $DEGRADED"; FAIL=$((FAIL+1)); }
[ -z "$PROGRESSING" ] && echo "  OK: no progressing operators" || echo "  PROGRESSING: $PROGRESSING"

echo ""
echo "--- Nodes ---"
NOTREADY=$(oc get nodes --no-headers | grep -v " Ready" | awk '{print $1}')
[ -z "$NOTREADY" ] && echo "  OK: all nodes Ready" || { echo "  NOT READY: $NOTREADY"; FAIL=$((FAIL+1)); }

echo ""
echo "--- Unhealthy Pods ---"
UNHEALTHY=$(oc get pods --all-namespaces --no-headers | grep -cvE "Running|Completed|Succeeded")
[ "$UNHEALTHY" -eq 0 ] && echo "  OK: all pods running" || { echo "  UNHEALTHY POD COUNT: $UNHEALTHY"; oc get pods --all-namespaces | grep -vE "Running|Completed|Succeeded|NAMESPACE"; FAIL=$((FAIL+1)); }

echo ""
echo "--- Resource Pressure ---"
oc adm top nodes 2>/dev/null || echo "  metrics-server not available"

echo ""
echo "=== Result: $( [ $FAIL -eq 0 ] && echo PASS || echo "FAIL ($FAIL issues)" ) ==="
exit $FAIL
```


```text title="Expected output"
=== OpenShift Health Check: 2024-01-15 14:32 ===

--- Cluster Operators ---
  OK: no degraded operators
  OK: no progressing operators

--- Nodes ---
  OK: all nodes Ready

--- Unhealthy Pods ---
  OK: all pods running

--- Resource Pressure ---
NAME                                    CPU(cores)   MEMORY(Mi)
worker-01.prod.internal                 1240m        8192Mi
worker-02.prod.internal                 892m         6144Mi
master-01.prod.internal                 1456m        12288Mi
master-02.prod.internal                 1389m        11520Mi
master-03.prod.internal                 1512m        12800Mi

=== Result: PASS ===
```

!!! warning "Common errors"
    **`error: Unable to connect to the server: dial tcp: lookup api.cluster.local on 10.0.2.2:53: no such host`** — Verify KUBECONFIG points to a valid cluster config file and the API server is reachable.
    **`error: the server doesn't have a resource type "co"`** — Ensure you are running against OpenShift 4.x (not Kubernetes); older OpenShift versions use `clusteroperators` instead of `co`.
    **`error: metrics-server not available`** — Install the metrics-server addon with `oc apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml` to enable resource usage reporting.
---

## See also

- [OpenShift — CLI Reference](../cli-reference/)
- [OpenShift — Procedures](../procedures/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
