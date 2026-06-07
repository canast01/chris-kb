# OpenShift — Diagnostics

<div class="kb-summary">
Diagnostic tools and techniques: must-gather collection, oc adm inspect, etcd diagnostics, network troubleshooting, and log collection from cluster components.
</div>

```text
┌──────────────────────────────────── OpenShift Diagnostics ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   must-gather: full cluster state in one command; attach to every Red Hat support case        │   │
│   │   oc adm inspect: targeted collection for one operator/namespace; faster than must-gather    │    │
│   │   etcd: health endpoints + Prometheus metrics; latency > 10ms P99 = disk IOPS problem        │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      must-gather            │  │      etcd Diagnostics        │  │     Network Diagnostics     │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  Full cluster state         │  │  endpoint health/status      │  │  oc exec curl between pods  │  │
│   │  Pod logs, events, configs  │  │  member list + latency       │  │  OVN-K pod status           │  │
│   │  ~10-20 min to collect      │  │  db size, compaction         │  │  DNS resolution test        │  │
│   │  Attach to support case     │  │  Prometheus metrics          │  │  NetworkPolicy debug        │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    must-gather  = Runs image that collects logs, configs, CRDs, and events from all namespaces        │
│    oc adm inspect= Collects resources from a specific operator or namespace; faster/targeted          │
│    etcdctl     = etcd CLI; available inside etcd pods via oc rsh or oc debug node                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## must-gather

```bash
# Full cluster collection (required for Red Hat support cases)
oc adm must-gather --dest-dir=/tmp/must-gather

# Saves to: /tmp/must-gather/must-gather.local.<timestamp>/

# Product-specific must-gather images
oc adm must-gather --image=registry.redhat.io/ocs4/ocs-must-gather-rhel8  # ODF
oc adm must-gather --image=registry.redhat.io/rhacm2/acm-must-gather-rhel8  # ACM

# Restrict to specific namespace (faster)
oc adm must-gather --dest-dir=/tmp/mg -- /usr/bin/gather_namespaces openshift-etcd

# Compress for upload
tar czf must-gather-$(date +%F).tar.gz /tmp/must-gather/
```

## oc adm inspect (Targeted)

```bash
# Collect specific operator
oc adm inspect clusteroperator/etcd --dest-dir=/tmp/etcd-inspect
oc adm inspect clusteroperator/ingress --dest-dir=/tmp/ingress-inspect
oc adm inspect clusteroperator/authentication --dest-dir=/tmp/auth-inspect

# Collect namespace
oc adm inspect namespace/openshift-monitoring --dest-dir=/tmp/monitoring
oc adm inspect namespace/openshift-dns --dest-dir=/tmp/dns

# Collect a specific resource
oc adm inspect deployment/prometheus-operator -n openshift-monitoring
```

## etcd Diagnostics

```bash
# Get etcd pod
ETCD_POD=$(oc get pod -n openshift-etcd -l etcd=true -o name | head -1)

# Helper function for etcdctl
etcdctl_cmd() {
  oc rsh -n openshift-etcd "$ETCD_POD" \
    etcdctl "$@" \
    --endpoints=https://localhost:2379 \
    --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
    --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(oc rsh -n openshift-etcd "$ETCD_POD" hostname).crt \
    --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(oc rsh -n openshift-etcd "$ETCD_POD" hostname).key
}

# Member list
etcdctl_cmd member list -w table

# Endpoint health
etcdctl_cmd endpoint health --cluster -w table

# Endpoint status (includes DB size and leader)
etcdctl_cmd endpoint status --cluster -w table

# Check P99 commit latency via Prometheus
# Query: histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m]))
# Alert if > 10ms

# Compact etcd if DB > 8 GB
REV=$(etcdctl_cmd endpoint status --write-out="json" | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['Status']['header']['revision'])")
etcdctl_cmd compact "$REV"
etcdctl_cmd defrag --cluster
```

## Network Diagnostics

```bash
# Test pod-to-pod connectivity
oc exec -n source-ns source-pod -- curl -v http://target-service.target-ns.svc.cluster.local

# Test DNS resolution from a pod
oc exec -n <ns> <pod> -- nslookup kubernetes.default.svc.cluster.local
oc exec -n <ns> <pod> -- cat /etc/resolv.conf

# Debug CoreDNS
oc get pods -n openshift-dns
oc logs -n openshift-dns -l dns.operator.openshift.io/daemonset-dns

# OVN-Kubernetes diagnostics
oc get pods -n openshift-ovn-kubernetes -o wide
oc logs -n openshift-ovn-kubernetes <ovnkube-master-pod> -c nbdb
oc logs -n openshift-ovn-kubernetes <ovnkube-node-pod> -c ovnkube-node

# Check NetworkPolicy is not blocking traffic
oc get networkpolicy -n <ns>
oc describe networkpolicy <np> -n <ns>

# Trace a connection (OVN flows)
oc debug node/<node>
chroot /host
ovn-trace --ovs "inport=<logical-port>" "eth.dst == <mac>, ip4.dst == <ip>"
```

## Node-Level Diagnostics

```bash
# Access node as root via debug pod
oc debug node/<node-name>
chroot /host

# Check container runtime
crictl ps                          # running containers
crictl pods                        # pod sandboxes
crictl info                        # runtime info
crictl logs <container-id>

# Check kubelet
systemctl status kubelet
journalctl -u kubelet -n 100 --no-pager

# Check disk usage
df -h
du -sh /var/lib/containers/*       # container layers
du -sh /var/log/pods/*             # pod logs consuming disk
```
