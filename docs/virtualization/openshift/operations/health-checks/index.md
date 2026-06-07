# OpenShift — Health Checks

<div class="kb-summary">
Daily cluster health routine: cluster operators, node status, etcd health, monitoring stack, certificate expiry, and resource pressure. Run before and after every change.
</div>

```text
┌──────────────────────────────────── OpenShift Daily Health Check ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Run each morning; any DEGRADED operator or NotReady node = investigate before changes       │   │
│   │   etcd: check latency and member count; cert expiry: alert > 30 days warning                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │    Cluster Operators        │  │      Nodes & Workloads       │  │   etcd & Certificates       │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  All Available=True         │  │  All nodes Ready             │  │  3 members healthy          │  │
│   │  None Degraded=True         │  │  No pods CrashLoopBackOff    │  │  db size < 8 GB             │  │
│   │  None Progressing long      │  │  Resource pressure checked   │  │  Certs > 30 days remaining  │  │
│   │  Version matches expected   │  │  Pending PVCs = 0            │  │  etcd latency < 10ms P99    │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Alert thresholds:                                                                                  │
│    DEGRADED operator → investigate immediately; any NotReady node > 5 min → page on-call              │
│    etcd P99 commit latency > 10ms → investigate disk IOPS; db > 8 GB → compact immediately            │
│    Certificate < 30 days → schedule rotation; < 7 days → emergency rotation                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Run This Routine

Run in order — each check gates the next.

```bash
#!/bin/bash
# OpenShift Daily Health Check

echo "=== 1. Cluster Operators ==="
oc get co | grep -v "True.*False.*False" | grep -v "^NAME"
# Expected: empty (all operators Available=True, Progressing=False, Degraded=False)

echo "=== 2. Node Status ==="
oc get nodes -o wide
# Expected: all Ready; no NotReady

echo "=== 3. Unhealthy Pods ==="
oc get pods --all-namespaces | grep -vE "Running|Completed|Succeeded"
# Expected: empty (or only expected Pending/Terminating)

echo "=== 4. etcd Health ==="
ETCD_POD=$(oc get pod -n openshift-etcd -l etcd=true -o name | head -1)
oc rsh -n openshift-etcd $ETCD_POD \
  etcdctl endpoint health --cluster \
  --endpoints=https://localhost:2379 \
  --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
  --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).crt \
  --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).key
# Expected: all endpoints healthy

echo "=== 5. etcd DB Size ==="
oc rsh -n openshift-etcd $ETCD_POD \
  etcdctl endpoint status --cluster -w table \
  --endpoints=https://localhost:2379 \
  --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
  --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).crt \
  --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).key
# DB SIZE column should be < 8 GB

echo "=== 6. Resource Pressure ==="
oc adm top nodes
# Check CPU and memory; no node > 85%

echo "=== 7. Certificate Expiry ==="
oc -n openshift-config-managed get secret kube-controller-manager-client-cert-key \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate
# Alert if < 30 days

echo "=== 8. Monitoring Stack ==="
oc get pods -n openshift-monitoring | grep -v Running
# All monitoring pods should be Running
```

## Cluster Operator Checks

```bash
# Full CO status
oc get co

# Investigate degraded operator
oc describe co <operator-name>
# Look at: Conditions section → message field explains the issue

# Common operators and what they manage
# authentication     → OAuth server, kubeadmin secret
# dns                → CoreDNS pods in openshift-dns
# etcd               → etcd cluster
# ingress            → OpenShift Router (HAProxy)
# kube-apiserver     → kube-apiserver pods on masters
# machine-config     → MCO daemon on all nodes
# monitoring         → Prometheus, Alertmanager, Grafana
# network            → OVN-Kubernetes, Multus
# storage            → CSI driver operator
```

## etcd Performance Check

```bash
# Check P99 commit latency (should be < 10ms)
oc rsh -n openshift-etcd $ETCD_POD \
  etcdctl check perf --endpoints=https://localhost:2379 ...

# Monitor etcd via Prometheus
# Metric: etcd_disk_backend_commit_duration_seconds_bucket
# Query in Prometheus: histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m]))
```

## Node Resource Check

```bash
# Resource usage
oc adm top nodes
oc adm top pods --all-namespaces --sort-by=cpu | head -20
oc adm top pods --all-namespaces --sort-by=memory | head -20

# Check node conditions (Pressure states)
oc describe nodes | grep -A5 "Conditions:"
# Watch for: MemoryPressure, DiskPressure, PIDPressure = True
```
