# OpenShift — Scripts

<div class="kb-summary">
Operational scripts: daily health snapshot, CSR auto-approval, node drain wrapper, etcd backup cron, pod restart loop detection, and namespace resource summary.
</div>

```text
┌──────────────────────────────────── OpenShift Operational Scripts ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Scripts collect state, automate repetitive tasks, and provide consistent health output      │   │
│   │   Run health-check.sh daily; etcd-backup.sh pre-upgrade; csr-approve.sh during scale-out     │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Health & Monitoring     │  │     Node Operations          │  │     Backup & Recovery       │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  health-check.sh            │  │  node-drain.sh               │  │  etcd-backup.sh             │  │
│   │  co-watch.sh                │  │  csr-approve.sh              │  │  verify-backup.sh           │  │
│   │  pod-restart-detector.sh    │  │  ns-resource-summary.sh      │  │  copy-backup-to-s3.sh       │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    KUBECONFIG   = Path to kubeconfig file; scripts should accept as env var or parameter              │
│    jq           = JSON processor; used to parse oc -o json output                                     │
│    CSR          = Certificate Signing Request; new worker nodes submit these to join cluster          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## health-check.sh

```bash
#!/bin/bash
# OpenShift cluster health snapshot
# Usage: ./health-check.sh [kubeconfig-path]

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
UNHEALTHY=$(oc get pods --all-namespaces --no-headers | grep -vE "Running|Completed|Succeeded" | wc -l)
[ "$UNHEALTHY" -eq 0 ] && echo "  OK: all pods running" || { echo "  UNHEALTHY POD COUNT: $UNHEALTHY"; oc get pods --all-namespaces | grep -vE "Running|Completed|Succeeded|NAMESPACE"; FAIL=$((FAIL+1)); }

echo ""
echo "--- Resource Pressure ---"
oc adm top nodes 2>/dev/null || echo "  metrics-server not available"

echo ""
echo "=== Result: $( [ $FAIL -eq 0 ] && echo PASS || echo "FAIL ($FAIL issues)" ) ==="
exit $FAIL
```

## csr-approve.sh

```bash
#!/bin/bash
# Auto-approve pending CSRs (use during scale-out)
# Usage: ./csr-approve.sh [--watch]

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

## node-drain.sh

```bash
#!/bin/bash
# Safe node drain with pre/post checks
# Usage: ./node-drain.sh <node-name>

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

echo "$NODE drained. Verify workloads, then run:"
echo "  oc adm uncordon $NODE"
```

## etcd-backup.sh

```bash
#!/bin/bash
# Run etcd backup on a master node via oc debug
# Usage: ./etcd-backup.sh <master-node> <local-backup-dir>

MASTER=${1:-$(oc get nodes -l node-role.kubernetes.io/master -o name | head -1 | cut -d/ -f2)}
BACKUP_DIR=${2:-/tmp/etcd-backup-$(date +%F)}

mkdir -p "$BACKUP_DIR"

echo "Running etcd backup on $MASTER..."
oc debug node/"$MASTER" -- chroot /host /usr/local/bin/cluster-backup.sh /home/core/backup

echo "Copying backup files..."
oc rsync "$MASTER":/home/core/backup/ "$BACKUP_DIR"/

echo "Backup files:"
ls -lh "$BACKUP_DIR"/
echo "Done: $BACKUP_DIR"
```

## pod-restart-detector.sh

```bash
#!/bin/bash
# Find pods with high restart counts (potential crash loops)
# Usage: ./pod-restart-detector.sh [threshold]

THRESHOLD=${1:-5}

echo "Pods with > $THRESHOLD restarts:"
oc get pods --all-namespaces -o json | \
  jq -r '.items[] | select(.status.containerStatuses != null) |
    .metadata.namespace + "/" + .metadata.name + " restarts=" +
    (.status.containerStatuses[0].restartCount | tostring)' | \
  awk -F'restarts=' -v t="$THRESHOLD" '$2+0 > t {print}' | \
  sort -t= -k2 -rn
```
