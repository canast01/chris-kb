---
tags:
  - troubleshooting
search:
  boost: 1.5
---
# OpenShift — Diagnostics

<div class="kb-summary">
Diagnostic tools and techniques: must-gather collection, oc adm inspect, Prometheus-based diagnostics, OVN network tracing, log aggregation, and etcd health assessment.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

A: "Issue Reported" {shape: rectangle}
B: "Collect must-gather\noc adm must-gather" {shape: rectangle}
C: "Review Operator Logs\noc describe co + pod logs" {shape: rectangle}
D: "D" {shape: rectangle}
E: "Review etcd Metrics\nWAL latency, DB size, leader" {shape: rectangle}
F: "F" {shape: rectangle}
G: "Network Trace\novn-trace / tcpdump / curl test" {shape: rectangle}
H: "Review Node Logs\noc adm node-logs\noc debug node" {shape: rectangle}
I: "I" {shape: rectangle}
J: "Open Support Case\nAttach must-gather + sos report" {shape: rectangle}
K: "Resolved" {shape: rectangle}

A -> B
B -> C
D -> E
F -> G
F -> H
E -> I
G -> I
I -> J
I -> K
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
mustgather: "must-gather" {shape: rectangle}
oc_adm_inspect_targeted: "oc adm inspect (Targeted)" {shape: rectangle}
metricsbased_diagnostics: "Metrics-Based Diagnostics" {shape: rectangle}
etcd_diagnostics: "etcd Diagnostics" {shape: rectangle}
network_diagnostics: "Network Diagnostics" {shape: rectangle}
log_aggregation: "Log Aggregation" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> mustgather: investigate
symptom -> oc_adm_inspect_targeted: investigate
symptom -> metricsbased_diagnostics: investigate
symptom -> etcd_diagnostics: investigate
symptom -> network_diagnostics: investigate
symptom -> log_aggregation: investigate
mustgather -> resolution
oc_adm_inspect_targeted -> resolution
metricsbased_diagnostics -> resolution
etcd_diagnostics -> resolution
network_diagnostics -> resolution
log_aggregation -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## must-gather

```bash
# Full cluster collection (required for Red Hat support cases)
oc adm must-gather --dest-dir=/tmp/must-gather

# Output location: /tmp/must-gather/must-gather.local.<timestamp>/
# Key directories:
#   cluster-info/        — cluster version, node info, co status
#   namespaces/<ns>/     — pod logs, events, resource YAML per namespace
#   etcd/                — etcd member list, endpoint status, DB info
#   network/             — OVN-K flows, NetworkPolicy state
#   audit_logs/          — API server audit logs

# Product-specific must-gather images
oc adm must-gather \
  --image=registry.redhat.io/ocs4/ocs-must-gather-rhel8         # ODF/OCS
oc adm must-gather \
  --image=registry.redhat.io/rhacm2/acm-must-gather-rhel8       # ACM
oc adm must-gather \
  --image=registry.redhat.io/openshift4/ose-network-tools-rhel9  # Network

# Restrict to specific namespace (faster for targeted issues)
oc adm must-gather --dest-dir=/tmp/mg \
  -- /usr/bin/gather_namespaces openshift-etcd

# Compress for upload to Red Hat support portal
tar czf must-gather-$(date +%F-%H%M).tar.gz /tmp/must-gather/

# Review top-level summary
ls /tmp/must-gather/must-gather.local.*/
cat /tmp/must-gather/must-gather.local.*/cluster-info/clusterversion
```


```text title="Expected output"
$ oc adm must-gather --dest-dir=/tmp/must-gather
gathering data...
Gathering data for ns/openshift-etcd...
Gathering data for ns/openshift-apiserver...
Gathering data for ns/openshift-controller-manager...
Gathering data for ns/openshift-kube-apiserver...
Gathering data for ns/openshift-monitoring...
Gathering data for ns/openshift-network-operator...
Gathering data for ns/openshift-ovn-kubernetes...
Gathering data for ns/openshift-sdn...
Gathering data for ns/openshift-kube-scheduler...
Gathering data for ns/openshift-kube-controller-manager...
...
must-gather collection complete, output available in /tmp/must-gather/must-gather.local.20240315-143022/

$ tar czf must-gather-2024-03-15-1430.tar.gz /tmp/must-gather/

$ ls /tmp/must-gather/must-gather.local.*/
audit_logs  cluster-info  etcd  namespaces  network  nodes  pods

$ cat /tmp/must-gather/must-gather.local.20240315-143022/cluster-info/clusterversion
apiVersion: config.openshift.io/v1
kind: ClusterVersion
metadata:
  name: version
status:
  desired:
    image: quay.io/openshift-release-dev/ocp-release:4.14.8-x86_64
    version: 4.14.8
  history:
  - image: quay.io/openshift-release-dev/ocp-release:4.14.8-x86_64
    version: 4.14.8
    state: Completed
```

!!! warning "Common errors"
    **`error: unable to find image "registry.redhat.io/ocs4/ocs-must-gather-rhel8" locally`** — Ensure the cluster has pull credentials for registry.redhat.io and the image name matches your OCS/ODF version (e.g., ocs-must-gather-rhel9 for OCS 4.13+).
    **`error: open /tmp/must-gather: permission denied`** — Run the command with appropriate permissions or specify a writable destination directory (e.g., `--dest-dir=$HOME/must-gather`).
    **`error: unable to connect to the server: dial tcp: lookup api.cluster.example.com on 8.8.8.8:53: no such host`** — Verify kubeconfig is set correctly with `oc config current-context` and the cluster API endpoint is reachable.
## oc adm inspect (Targeted)

```bash
# Collect specific cluster operator state
oc adm inspect clusteroperator/etcd --dest-dir=/tmp/etcd-inspect
oc adm inspect clusteroperator/ingress --dest-dir=/tmp/ingress-inspect
oc adm inspect clusteroperator/authentication --dest-dir=/tmp/auth-inspect
oc adm inspect clusteroperator/kube-apiserver --dest-dir=/tmp/apiserver-inspect

# Collect full namespace (faster than must-gather for single namespace issues)
oc adm inspect namespace/openshift-monitoring --dest-dir=/tmp/monitoring
oc adm inspect namespace/openshift-dns --dest-dir=/tmp/dns

# Collect a specific resource
oc adm inspect deployment/prometheus-operator -n openshift-monitoring

# Inspect all failure events cluster-wide
oc get events --field-selector reason=Failed -A \
  --sort-by='.lastTimestamp'
```


```text title="Expected output"
inspecting clusteroperator/etcd
  clusteroperator/etcd
  deployment/etcd-quorum-guard -n openshift-etcd
  statefulset/etcd -n openshift-etcd
  pod/etcd-ip-10-0-145-23.ec2.internal -n openshift-etcd
  pod/etcd-ip-10-0-156-44.ec2.internal -n openshift-etcd
  pod/etcd-ip-10-0-167-89.ec2.internal -n openshift-etcd
inspecting clusteroperator/ingress
  clusteroperator/ingress
  deployment/router-default -n openshift-ingress
  service/router-default -n openshift-ingress
inspecting clusteroperator/authentication
  clusteroperator/authentication
  deployment/oauth-openshift -n openshift-authentication
  pod/oauth-openshift-7d4f8c9b2-xk9mj -n openshift-authentication
inspecting clusteroperator/kube-apiserver
  clusteroperator/kube-apiserver
  kubeapiserver/cluster
  pod/kube-apiserver-ip-10-0-145-23.ec2.internal -n openshift-kube-apiserver
  pod/kube-apiserver-ip-10-0-156-44.ec2.internal -n openshift-kube-apiserver
inspecting namespace/openshift-monitoring
  namespace/openshift-monitoring
  deployment/prometheus-operator -n openshift-monitoring
  statefulset/prometheus-k8s -n openshift-monitoring
  pod/prometheus-operator-5c8d6f7b9-lmk2p -n openshift-monitoring
  pod/prometheus-k8s-0 -n openshift-monitoring
inspecting namespace/openshift-dns
  namespace/openshift-dns
  daemonset/dns-default -n openshift-dns
  pod/dns-default-4xk8m -n openshift-dns
  pod/dns-default-7jn2p -n openshift-dns
inspecting deployment/prometheus-operator -n openshift-monitoring
  deployment/prometheus-operator
  pod/prometheus-operator-5c8d6f7b9-lmk2p -n openshift-monitoring
NAMESPACE                    NAME                                              REASON    AGE
openshift-kube-apiserver     pod/kube-apiserver-ip-10-0-145-23.ec2.internal   Failed    12m
openshift-etcd               pod/etcd-ip-10-0-156-44.ec2.internal             Failed    8m
openshift-monitoring         pod/prometheus-k8s-0                              Failed    5m
openshift-ingress            pod/router-default-9k4lm                          Failed    3m
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "clusteroperator"`** — Verify you are connected to an OpenShift cluster (not vanilla Kubernetes) with `oc version` and check cluster API availability.
    **`error: unable to write to /tmp/etcd-inspect: permission denied`** — Run the command with appropriate permissions or specify a writable destination directory like `$HOME/inspect-output`.
    **`error: no resources found in openshift
## Metrics-Based Diagnostics

```bash
# Node resource usage
oc adm top nodes

# Pod memory usage across all namespaces sorted by highest memory
oc adm top pods -A --sort-by=memory | head -20

# Pod CPU usage across all namespaces sorted by highest CPU
oc adm top pods -A --sort-by=cpu | head -20

# Run a Prometheus instant query directly against the in-cluster Prometheus
oc exec -n openshift-monitoring prometheus-k8s-0 -- \
  promtool query instant http://localhost:9090 \
  'etcd_disk_wal_fsync_duration_seconds{quantile="0.99"}'

# etcd backend commit latency (should be < 25ms P99)
oc exec -n openshift-monitoring prometheus-k8s-0 -- \
  promtool query instant http://localhost:9090 \
  'histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m]))'

# OOM events on nodes (node-level memory pressure)
oc exec -n openshift-monitoring prometheus-k8s-0 -- \
  promtool query instant http://localhost:9090 \
  'kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}'

# API server error rate
oc exec -n openshift-monitoring prometheus-k8s-0 -- \
  promtool query instant http://localhost:9090 \
  'sum(rate(apiserver_request_total{code=~"5.."}[5m])) by (resource, verb)'
```


```text title="Expected output"
NAME                                    CPU(cores)   MEMORY(Mi)
master-0.example.com                    1245m        8932Mi
master-1.example.com                    1089m        8156Mi
worker-0.example.com                    892m         6234Mi
worker-1.example.com                    756m         5891Mi
worker-2.example.com                    634m         4127Mi

NAMESPACE                NAME                                    CPU(m)   MEMORY(Mi)
openshift-etcd           etcd-master-0                           892      1456
openshift-apiserver      apiserver-master-1                      756      2134
openshift-monitoring     prometheus-k8s-0                        634      3892
openshift-kube-scheduler scheduler-master-0                      445      892
openshift-controller-mgr controller-manager-master-2             389      1023
...

NAMESPACE                NAME                                    CPU(m)   MEMORY(Mi)
openshift-monitoring     prometheus-k8s-0                        1245     3892
openshift-etcd           etcd-master-0                           892      1456
openshift-apiserver      apiserver-master-1                      756      2134
openshift-kube-scheduler scheduler-master-0                      445      892
openshift-controller-mgr controller-manager-master-2             389      1023
...

etcd_disk_wal_fsync_duration_seconds{instance="10.0.1.15:2379",job="prometheus-k8s"} => 0.0234 @1699564892.123

histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m])) => 0.0189 @1699564892.123

kube_pod_container_status_last_terminated_reason{reason="OOMKilled",pod="worker-pod-xyz",namespace="default"} => 2 @1699564892.123

{resource="pods",verb="create"} => 0.00234 @1699564892.123
{resource="nodes",verb="get"} => 0.00089 @1699564892.123
```

!!! warning "Common errors"
    **`error: metrics not available yet`** — Wait 2-3 minutes after cluster startup for Prometheus to collect initial metrics, then retry the query.
    **`Error executing remote command: command terminated with exit code 1`** — Verify the prometheus-k8s-0 pod is running with `oc get pod -n openshift-monitoring prometheus-k8s-0` and check pod logs with `oc logs -n openshift-monitoring prometheus-k8s-0`.
    **`error: unable to connect to the server: dial tcp: lookup prometheus-k8s-0 on [IP]: no such host`** — Ensure you are connected to the correct cluster context with `oc config current-context` and the openshift-monitoring namespace exists.
## etcd Diagnostics

```bash
# Get etcd pod
ETCD_POD=$(oc get pod -n openshift-etcd -l etcd=true -o name | head -1)

# Helper function for etcdctl inside the etcd pod
etcdctl_cmd() {
  oc rsh -n openshift-etcd "$ETCD_POD" \
    etcdctl "$@" \
    --endpoints=https://localhost:2379 \
    --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
    --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(oc rsh -n openshift-etcd "$ETCD_POD" hostname).crt \
    --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(oc rsh -n openshift-etcd "$ETCD_POD" hostname).key
}

# Member list — verify all 3 masters are members
etcdctl_cmd member list -w table

# Endpoint health — all endpoints should be healthy
etcdctl_cmd endpoint health --cluster -w table

# Endpoint status — DB SIZE, IS LEADER, RAFT_TERM
etcdctl_cmd endpoint status --cluster -w table

# Compact and defrag if DB > 8 GB
REV=$(etcdctl_cmd endpoint status --write-out="json" | \
  python3 -c "import sys,json; print(json.load(sys.stdin)[0]['Status']['header']['revision'])")
etcdctl_cmd compact "$REV"
etcdctl_cmd defrag --cluster
```


```text title="Expected output"
pod/etcd-ip-10-0-1-45.ec2.internal
+------------------+---------+-------+----------+-----+----------+
| ID               | STATUS  | NAME  | PEER URL | ... | LEARNER  |
+------------------+---------+-------+----------+-----+----------+
| 8f3c2a1b5d9e4f6 | started | etcd0 | https... |     | false    |
| 7e2b1a9c4d8f3e5 | started | etcd1 | https... |     | false    |
| 6d1a0b8c3e7f2d4 | started | etcd2 | https... |     | false    |
+------------------+---------+-------+----------+-----+----------+
https://10.0.1.45:2379 is healthy: successfully committed proposal: took = 12.456ms
https://10.0.1.46:2379 is healthy: successfully committed proposal: took = 11.234ms
https://10.0.1.47:2379 is healthy: successfully committed proposal: took = 13.891ms
+------------------+----------+--------+--------+--------+
| ENDPOINT         | ID       | VERSION | DB SIZE | IS LEADER |
+------------------+----------+--------+--------+--------+
| https://10.0.1.45:2379 | 8f3c2a1b | 3.5.9   | 2.1 GB  | true      |
| https://10.0.1.46:2379 | 7e2b1a9c | 3.5.9   | 2.0 GB  | false     |
| https://10.0.1.47:2379 | 6d1a0b8c | 3.5.9   | 2.2 GB  | false     |
+------------------+----------+--------+--------+--------+
compacted revision 4521847
Finished defragmenting etcd member [8f3c2a1b5d9e4f6] in 8.234s
Finished defragmenting etcd member [7e2b1a9c4d8f3e5] in 7.891s
Finished defragmenting etcd member [6d1a0b8c3e7f2d4] in 8.456s
```

!!! warning "Common errors"
    **`error: unable to match a volume mount in pod openshift-etcd/etcd-ip-10-0-1-45.ec2.internal for /etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/`** — Verify the certificate path exists in the pod with `oc rsh -n openshift-etcd <pod> ls -la /etc/kubernetes/static-pod-certs/secrets/` and adjust the path if using a different OpenShift version.
    **`Error: context deadline exceeded`** — The etcd cluster is overloaded or unhealthy; check member health with `etcdctl_cmd member list` and verify all three masters are running before retrying.
    **`Error: failed to dial default: context deadline exceeded`** — Ensure network connectivity between the control plane nodes and that the etcd service is listening on port 2379 with `oc rsh -n openshift-et
## Network Diagnostics

```bash
# Test pod-to-service connectivity
oc exec -n source-ns source-pod -- \
  curl -v http://target-service.target-ns.svc.cluster.local

# Test DNS resolution from a pod
oc exec -n <ns> <pod> -- nslookup kubernetes.default.svc.cluster.local
oc exec -n <ns> <pod> -- cat /etc/resolv.conf

# Debug CoreDNS
oc get pods -n openshift-dns
oc logs -n openshift-dns -l dns.operator.openshift.io/daemonset-dns --tail=30

# OVN-Kubernetes diagnostics
oc get pods -n openshift-ovn-kubernetes -o wide
oc logs -n openshift-ovn-kubernetes <ovnkube-master-pod> -c nbdb --tail=50
oc logs -n openshift-ovn-kubernetes <ovnkube-node-pod> -c ovnkube-node --tail=50

# OVN flow trace — determine why traffic is dropped
oc exec -n openshift-ovn-kubernetes ovnkube-node-<hash> -- \
  ovn-trace --ovs "inport=<logical-port>" \
  "eth.dst == <mac>, ip4.src == <src-ip>, ip4.dst == <dst-ip>, tcp.dst == 80"

# Capture packets on a node for offline analysis
oc debug node/<node>
chroot /host
tcpdump -i ens192 -w /host/tmp/capture.pcap host <target-ip> and port 443
# Copy pcap off node:
oc cp <debug-pod>:/host/tmp/capture.pcap /tmp/capture.pcap

# Check NetworkPolicy is not blocking traffic
oc get networkpolicy -n <ns>
oc describe networkpolicy <np> -n <ns>
```


```text title="Expected output"
Trying 10.217.4.52...
* Connected to target-service.target-ns.svc.cluster.local (10.217.4.52) port 80 (#0)
> GET / HTTP/1.1
< HTTP/1.1 200 OK
< Content-Length: 1234

Server: 10.217.4.52:8080
Address: 10.217.4.52#53

Name:	kubernetes.default.svc.cluster.local
Address: 10.96.0.1

nameserver 10.96.0.10
nameserver 10.96.0.11
search default.svc.cluster.local svc.cluster.local cluster.local

NAME                    READY   STATUS    RESTARTS   AGE
dns-default-5x7kj       1/1     Running   0          12d
dns-default-9m2lp       1/1     Running   0          12d
dns-default-b4c8n       1/1     Running   0          12d

2024-01-15T14:32:18.456Z [INFO] 192.168.1.45 - 53 "A IN kubernetes.default.svc.cluster.local. udp 54 false 512" NOERROR qr,aa,rd 97 0.002s
2024-01-15T14:32:19.123Z [INFO] 192.168.1.46 - 53 "A IN target-service.target-ns.svc.cluster.local. udp 62 false 512" NOERROR qr,aa,rd 105 0.001s

NAME                              READY   STATUS    RESTARTS   AGE   IP             NODE
ovnkube-master-4xz9p              3/3     Running   2          8d    10.0.128.4     worker-1
ovnkube-master-7k2lm              3/3     Running   1          8d    10.0.128.5     worker-2
ovnkube-node-8b9qx                3/3     Running   0          8d    10.0.129.10    worker-3
ovnkube-node-c5d2r                3/3     Running   0          8d    10.0.129.11    worker-4

2024-01-15T14:35:42.789Z [INFO] NBDB: Listening on 0.0.0.0:6641
2024-01-15T14:35:43.012Z [INFO] NBDB: Cluster state: active
2024-01-15T14:35:44.234Z [INFO] NBDB: 3 databases synchronized

2024-01-15T14:36:01.456Z [INFO] ovnkube-node: Setting up br-int bridge
2024-01-15T14:36:02.789Z [INFO] ovnkube-node: Configuring logical port for pod source-pod
2024-01-15T14:36:03.123Z [INFO] ovnkube-node: Flow rules installed: 247 total

 0. inport == "source-ns_source-pod" (source-ns_source-pod), priority 100
 1. eth.dst == fa:16:3e:ab:
```
## Log Aggregation

```bash
# Node journal logs via oc adm (no SSH required)
oc adm node-logs <node> -u crio --since=1h
oc adm node-logs <node> -u kubelet --since=2h

# All nodes at once for a specific service
oc adm node-logs --role=master -u etcd | tail -200

# Platform component logs
oc logs -n openshift-monitoring alertmanager-main-0 --tail=100
oc logs -n openshift-monitoring prometheus-k8s-0 --tail=100 -c prometheus

# Cluster Logging Operator (if deployed): query Loki
oc get pods -n openshift-logging
oc logs -n openshift-logging -l component=collector --tail=50

# Get all failure events across all namespaces sorted by time
oc get events -A \
  --field-selector reason=Failed \
  --sort-by='.lastTimestamp' | tail -30

# Get all Warning events cluster-wide
oc get events -A \
  --field-selector type=Warning \
  --sort-by='.lastTimestamp' | tail -50
```


```text title="Expected output"
oc adm node-logs <node> -u crio --since=1h
-- Logs begin at Wed 2024-01-17 14:32:18 UTC, end at Wed 2024-01-17 15:47:22 UTC. --
Jan 17 14:45:33 worker-node-02.ocp.local crio[2847]: time="2024-01-17T14:45:33.521847Z" level=info msg="PullImage" image.name="quay.io/openshift-release-dev/ocp-v4.13.5:cli"
Jan 17 15:12:09 worker-node-02.ocp.local crio[2847]: time="2024-01-17T15:12:09.847291Z" level=warn msg="ImagePull timeout" image.name="registry.redhat.io/rhel8/rhel:8.7" duration=45.2s
Jan 17 15:33:44 worker-node-02.ocp.local crio[2847]: time="2024-01-17T15:33:44.193012Z" level=error msg="Failed to create container" container.id="a7f2c9e1" error="OCI runtime error"

oc adm node-logs <node> -u kubelet --since=2h
Jan 17 13:47:51 worker-node-02.ocp.local kubelet[1924]: I0117 13:47:51.234567 1924 kubelet.go:2847] SyncLoop (PERM_DENIED): "kube-system/coredns-558bd4d5db-7xk2m"
Jan 17 14:22:18 worker-node-02.ocp.local kubelet[1924]: W0117 14:22:18.456789 1924 pod_workers.go:1456] Error syncing pod, skipping: failed to "CreatePodSandbox" for "default/nginx-deployment-66b6c48dd5-9m4kl"
Jan 17 15:01:33 worker-node-02.ocp.local kubelet[1924]: E0117 15:01:33.789012 1924 remote_runtime.go:432] RunPodSandbox from runtime service failed: rpc error: code = Unavailable desc = connection refused

oc adm node-logs --role=master -u etcd | tail -200
Jan 17 15:40:22 master-node-01.ocp.local etcd[3847]: {"level":"info","ts":"2024-01-17T15:40:22.123456Z","caller":"rafthttp/peer.go:345","msg":"peer connected","remote-peer-id":"8e9f2c1a3b5d7e9f","remote-peer-version":"3.5.7"}
Jan 17 15:41:05 master-node-01.ocp.local etcd[3847]: {"level":"warn","ts":"2024-01-17T15:41:05.654321Z","caller":"etcdserver/raft.go:456","msg":"apply request took too long","took":"2.847s","expected-duration":"100ms"}
Jan 17 15:42:18
```
## Node-Level Diagnostics

```bash
# Access node as root via debug pod
oc debug node/<node-name>
chroot /host

# Check container runtime
crictl ps                          # running containers
crictl pods                        # pod sandboxes
crictl info                        # CRI-O runtime info
crictl logs <container-id>         # container logs via CRI-O

# Check kubelet
systemctl status kubelet
journalctl -u kubelet -n 100 --no-pager

# Check disk usage (high disk → DiskPressure → pod evictions)
df -h /
df -h /var
du -sh /var/lib/containers/*       # container image layers
du -sh /var/log/pods/*             # pod logs on disk

# Check current MachineConfig state
rpm-ostree status                  # RHCOS OS version + pending changes
systemctl --failed                 # any failed systemd units
```


```text title="Expected output"
Starting pod/node-debug-4x8kp ...
Pod IP: 10.0.128.45
If you don't see a command prompt with '#', try pressing enter.
sh-4.4# chroot /host
sh-4.4# crictl ps
CONTAINER           IMAGE                                    CREATED             STATE               NAME                      ATTEMPT             POD ID
a7f2c9e1b4d6e      quay.io/openshift-release-dev/ocp-v4.12:latest  2 minutes ago       Running             openshift-apiserver     0                   b9c3e2f1a5d8k
c4b1d9e2f3a6h      registry.redhat.io/ubi8/ubi:latest       5 minutes ago       Running             etcd                      0                   d2e5f8a1b3c9m
sh-4.4# crictl pods
POD ID              CREATED             STATE               NAME                      NAMESPACE           ATTEMPT             RUNTIME
b9c3e2f1a5d8k      2 minutes ago       Ready               openshift-apiserver-pod  openshift-apiserver 0                   cri-o
d2e5f8a1b3c9m      5 minutes ago       Ready               etcd-pod                  openshift-etcd      0                   cri-o
sh-4.4# systemctl status kubelet
● kubelet.service - Kubernetes Kubelet
   Loaded: loaded (/etc/systemd/system/kubelet.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2h 45m ago
   Main PID: 2847 (kubelet)
   Tasks: 28
   Memory: 512.3M
sh-4.4# df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       100G   78G   22G  78% /
sh-4.4# df -h /var
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda3       100G   78G   22G  78% /var
sh-4.4# du -sh /var/lib/containers/*
45G     /var/lib/containers/storage
sh-4.4# rpm-ostree status
State: idle
Deployments:
● rhcos-412.86.202401151234
    Version: 412.86.202401151234
    Timestamp: 2024-01-15T12:34:00Z
    Commit: 8f3a2b1c9e4d5f6a7b8c9d0e1f2a3b4c
sh-4.4# systemctl --failed
0 loaded units listed.
```

!!! warning "Common errors"
    **`chroot: can't execute '/bin/bash': No such file or directory`** — Use `sh` instead of `bash` or verify the host filesystem is properly mounted by checking `ls /host/bin`.
    **`error: unable to get pod logs: rpc error: code = Unavailable desc = connection error: desc = "error reading from server: EOF"`** — Restart the CRI-O service with `systemctl restart crio` or check if the container runtime socket is accessible
---

## See also

- [OpenShift — Common Issues](../common-issues/)
- [OpenShift — Escalation](../escalation/)

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
