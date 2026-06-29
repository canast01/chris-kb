---
tags:
  - troubleshooting
search:
  boost: 1.5
---
# OpenShift — Common Issues

<div class="kb-summary">
Troubleshooting guide for frequent OpenShift failures: CrashLoopBackOff, ImagePullBackOff, node NotReady, Pending pods, OOMKilled, etcd high latency, DNS failures, and degraded cluster operators.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "oc logs --previous\ncheck exit code" {shape: rectangle}
D: "OOMKilled\nIncrease memory limit" {shape: rectangle}
E: "App error\nCheck application logs" {shape: rectangle}
F: "SIGTERM timeout\nIncrease terminationGracePeriodSeconds" {shape: rectangle}
G: "oc describe pod Events\ncheck pull secret + image name" {shape: rectangle}
H: "Insufficient resources?\nSCC violation? PVC unbound?" {shape: rectangle}
I: "I" {shape: rectangle}
J: "kubelet / CRI-O status\nDiskPressure / NTP drift" {shape: rectangle}
K: "K" {shape: rectangle}
L: "oc describe co\ncheck operator pod logs" {shape: rectangle}
M: "etcd high latency\ndisk IOPS saturation" {shape: rectangle}
A: "Start: Pod or Node Issue" {shape: rectangle}

B -> C
C -> D
C -> E
C -> F
B -> G
B -> H
I -> J
K -> L
K -> M
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
crashloopbackoff: "CrashLoopBackOff" {shape: rectangle}
imagepullbackoff: "ImagePullBackOff" {shape: rectangle}
pending_pods_not_scheduling: "Pending Pods (Not Scheduling)" {shape: rectangle}
oomkilled: "OOMKilled" {shape: rectangle}
node_notready: "Node NotReady" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> crashloopbackoff: investigate
symptom -> imagepullbackoff: investigate
symptom -> pending_pods_not_scheduling: investigate
symptom -> oomkilled: investigate
symptom -> node_notready: investigate
diagnostic_flow -> resolution
crashloopbackoff -> resolution
imagepullbackoff -> resolution
pending_pods_not_scheduling -> resolution
oomkilled -> resolution
node_notready -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "CrashLoopBackOff" {shape: rectangle}
D2: "D2" {shape: rectangle}
R2: "Node NotReady" {shape: rectangle}
D3: "D3" {shape: rectangle}
R3: "ImagePullBackOff" {shape: rectangle}
D4: "D4" {shape: rectangle}
R4: "Pending Pods" {shape: rectangle}
D5: "D5" {shape: rectangle}
R5: "Cluster Operator Degraded" {shape: rectangle}
R6: "etcd High Latency" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}

D1 -> R1
D2 -> R2
D3 -> R3
D4 -> R4
D5 -> R5
R2 -> R6
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## CrashLoopBackOff

```bash
# 1. Check current logs
oc logs <pod> -n <ns>

# 2. Check previous container instance (the one that crashed)
oc logs <pod> -n <ns> --previous

# 3. Describe for events and last state
oc describe pod <pod> -n <ns>
# Look at: Events section → reason, message
# Look at: Last State → exitCode

# 4. Common exit codes:
#    exitCode 137 → OOMKilled: container killed by kernel OOM; see OOMKilled section
#    exitCode 1   → Application error; check app logs for exception/traceback
#    exitCode 127 → Command not found (CMD path wrong inside image)
#    exitCode 139 → Segmentation fault (SIGSEGV) — memory corruption or arch mismatch
#    exitCode 143 → SIGTERM not handled; terminationGracePeriodSeconds exceeded
#    "exec format error" → Image built for wrong CPU architecture (e.g. arm64 on x86 node)

# 5. Debug the image interactively (overrides entrypoint)
oc debug deployment/<name> -n <ns>

# 6. Check if a ConfigMap or Secret the pod depends on is missing
oc describe pod <pod> -n <ns> | grep -A5 "Reason\|Error\|Warning"
```


```text title="Expected output"
$ oc logs nginx-deployment-5d4b8c9f7-k2x9m -n production
2024-01-15T09:23:45.123Z [INFO] Starting nginx server
2024-01-15T09:23:46.456Z [INFO] Listening on 0.0.0.0:8080
2024-01-15T09:24:12.789Z [ERROR] Connection refused from 10.244.1.5:54321

$ oc logs nginx-deployment-5d4b8c9f7-k2x9m -n production --previous
2024-01-15T09:20:10.234Z [FATAL] Out of memory: cannot allocate 512MB
Killed

$ oc describe pod nginx-deployment-5d4b8c9f7-k2x9m -n production
Name:         nginx-deployment-5d4b8c9f7-k2x9m
Namespace:    production
Status:       CrashLoopBackOff
Events:
  Type     Reason     Age   Message
  ----     ------     ---   -------
  Normal   Created    2m    Created container nginx
  Warning  BackOff    1m    Back-off restarting failed container
  Warning  Failed     45s   Error: OOMKilled
Last State:
  Terminated
    Reason:       OOMKilled
    Exit Code:    137
    Started:      Mon, 15 Jan 2024 09:20:08 +0000
    Finished:     Mon, 15 Jan 2024 09:20:10 +0000

$ oc debug deployment/nginx-deployment -n production
Starting pod/nginx-deployment-debug, command was: /usr/sbin/nginx -g daemon off;
Pod IP: 10.244.2.15
If you don't see a command prompt, try entering 'sh'.
sh-4.4#

$ oc describe pod nginx-deployment-5d4b8c9f7-k2x9m -n production | grep -A5 "Reason\|Error\|Warning"
  Warning  Failed     45s   Error: OOMKilled
  Warning  BackOff    1m    Back-off restarting failed container
```

!!! warning "Common errors"
    **`Error from server (NotFound): pods "<pod>" not found`** — Verify the pod name and namespace with `oc get pods -n <ns>` and use the exact pod name.
    **`error: unable to upgrade connection: container not found ("<container>")`** — Ensure the pod is running (not in CrashLoopBackOff) before attempting `oc debug`; use `oc get pods -n <ns>` to check status.
    **`Error from server (Forbidden): pods is forbidden: User "system:serviceaccount:..." cannot get resource "pods"`** — Add RBAC permissions for the service account with `oc adm policy add-role-to-user view <user> -n <ns>`.
## ImagePullBackOff

```bash
# 1. Check which image and exact error
oc describe pod <pod> -n <ns>
# Events: Failed to pull image "quay.io/myapp:latest": ...

# 2. Common causes and fixes:
# a) Wrong image name/tag → fix image reference in deployment
# b) No pull secret for private registry:
oc create secret docker-registry registry-creds \
  --docker-server=quay.io \
  --docker-username=<user> \
  --docker-password=<token> \
  -n <ns>
oc secrets link default registry-creds --for=pull -n <ns>

# c) Registry unreachable → check network, proxy env vars, firewall
# d) Air-gapped: image not mirrored → mirror to internal registry and add ImageContentSourcePolicy
# e) Auth expired → re-create or rotate pull secret

# 3. Test pull manually on a node
oc debug node/<node> -- crictl pull <image>

# 4. Check global pull secret (applies to all namespaces)
oc get secret pull-secret -n openshift-config \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq .

# 5. Check ImageContentSourcePolicy for air-gapped mirror config
oc get imagecontentsourcepolicy
oc get imagecontentsourcepolicy -o yaml | grep -A5 mirrors
```


```text title="Expected output"
Name:         my-app-pod-5d8f9
Namespace:    production
Status:       ImagePullBackOff
Events:
  Type     Reason                 Age                From               Message
  ----     ------                 ---                ----               -------
  Normal   Scheduled              2m45s              default-scheduler  Successfully assigned production/my-app-pod-5d8f9 to worker-node-03
  Warning  Failed                 2m30s              kubelet            Failed to pull image "quay.io/myapp:latest": rpc error: code = Unknown desc = failed to pull and unpack image "quay.io/myapp:latest": failed to resolve reference "quay.io/myapp:latest": unexpected status code [manifests latest]: 401

secret/registry-creds created
secretlink.authorization.openshift.io/default-registry-creds-pull created

{
  "auths": {
    "quay.io": {
      "auth": "dXNlcjp0b2tlbjEyMzQ1Ng=="
    },
    "registry.redhat.io": {
      "auth": "c2VydmljZWFjY291bnQ6cGFzc3dvcmQ="
    }
  }
}

NAME                                                 AGE
registry-mirror.io-imagecontentsourcepolicy         14d
quay-io-imagecontentsourcepolicy                    8d

apiVersion: config.openshift.io/v1
kind: ImageContentSourcePolicy
metadata:
  name: quay-io-imagecontentsourcepolicy
spec:
  repositoryDigestMirrors:
  - mirrors:
    - mirror.internal.corp:5000/quay-mirror
    source: quay.io
```

!!! warning "Common errors"
    **`Failed to pull image "quay.io/myapp:latest": unexpected status code [manifests latest]: 401`** — Create a pull secret with valid credentials and link it to the service account using `oc secrets link default registry-creds --for=pull -n <ns>`.
    **`rpc error: code = Unknown desc = failed to resolve reference`** — Verify the image tag exists in the registry and the node has network connectivity to the registry; check firewall rules and proxy environment variables with `oc debug node/<node>`.
    **`ImagePullBackOff`** — Check the pod events with `oc describe pod <pod> -n <ns>` to see the exact pull error, then address the root cause (auth, network, or image availability).
## Pending Pods (Not Scheduling)

```bash
# 1. Check events — scheduling failure reason is always in events
oc describe pod <pod> -n <ns>

# a) Insufficient resources: "0/6 nodes are available: Insufficient cpu"
oc adm top nodes
oc get nodes -o json | \
  jq '.items[] | {name: .metadata.name, cpu: .status.allocatable.cpu, mem: .status.allocatable.memory}'

# b) SCC violation: "unable to validate against any security context constraint"
oc adm policy scc-subject-review -f pod.yaml
oc adm policy add-scc-to-user anyuid -z <sa> -n <ns>

# c) Taint/toleration mismatch: "node(s) had untolerated taint"
oc describe node <node> | grep Taint
# Add toleration to pod spec if intentional; otherwise investigate node taints

# d) NodeAffinity mismatch: "node(s) didn't match nodeAffinity"
oc get nodes --show-labels | grep <required-label>

# e) PVC not bound: pod stays Pending until PVC is Bound
oc get pvc -n <ns>
oc describe pvc <name> -n <ns>
# Common: wrong StorageClass or no provisioner available

# f) Topology constraint: PodTopologySpreadConstraints too strict
oc get pod <pod> -n <ns> -o jsonpath='{.spec.topologySpreadConstraints}'
```


```text title="Expected output"
Name:         nginx-app-5d4c9f2b1
Namespace:    production
Status:       Pending
Events:
  Type     Reason            Age   From               Message
  ----     ------            ---   ----               -------
  Warning  FailedScheduling  2m    default-scheduler  0/6 nodes are available: Insufficient cpu.

NAME                 CPU    MEMORY
worker-01.lab.local  2400m  7776Mi
worker-02.lab.local  2400m  7776Mi
worker-03.lab.local  2400m  7776Mi

NAME                 CPU    MEMORY
worker-01.lab.local  2400m  7776Mi
worker-02.lab.local  2400m  7776Mi
worker-03.lab.local  2400m  7776Mi

RESOURCE   ALLOWED  MATCHED  TEMPLATE
scc        anyuid   false    -

pod "nginx-app-5d4c9f2b1" is forbidden: unable to validate against any security context constraint: [spec.securityContext.runAsUser: Invalid value: 1000: must be in ranges [0-65535]]

Name:        worker-04.lab.local
Taints:      gpu=true:NoSchedule,workload=batch:NoExecute

NAME             STATUS   ROLES    AGE   VERSION   LABELS
worker-01.lab.local   Ready    worker   45d   4.12.5    kubernetes.io/hostname=worker-01.lab.local,disktype=ssd
worker-02.lab.local   Ready    worker   45d   4.12.5    kubernetes.io/hostname=worker-02.lab.local,disktype=ssd

NAME                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
app-data-pvc        Pending                                             10Gi       RWO            fast-ssd       3m
database-pvc        Bound    pvc-a7f2c8d1-9e4b-4a2c-b1f3-8c9d2e1f5a6b  50Gi       RWO            standard       12h

[{"maxSkew":1,"topologyKey":"kubernetes.io/hostname","whenUnsatisfiable":"DoNotSchedule"}]
```

!!! warning "Common errors"
    **`0/6 nodes are available: Insufficient cpu`** — Increase resource requests in the pod spec, add worker nodes, or evict low-priority workloads using `oc delete pod` on non-critical pods.
    **`unable to validate against any security context constraint`** — Add the appropriate SCC to the service account with `oc adm policy add-scc-to-user <scc-name> -z <sa-name> -n <namespace>`.
    **`node(s) had untolerated taint`** — Add matching tolerations to the pod spec under `spec.tolerations` or remove the taint from the node with `oc adm taint nodes <node-name> <key>=<value>:<effect>-`.
## OOMKilled

```bash
# 1. Identify which container OOMKilled
oc describe pod <pod> -n <ns>
# Last State: Terminated  Reason: OOMKilled

# 2. Check memory usage vs limit
oc adm top pods <pod> -n <ns> --containers

# 3. Check Prometheus for historical memory usage
# Query: container_memory_working_set_bytes{pod="<pod>", namespace="<ns>"}

# 4. Increase memory limit
oc set resources deployment <name> -n <ns> \
  --containers=<container> \
  --limits=memory=2Gi \
  --requests=memory=512Mi

# 5. If limit is already generous: profile the app for memory leak
#    Look for unbounded caches, connection leaks, recursive structures
```


```text title="Expected output"
Name:                 api-server-5d8c9b2f
Namespace:            production
Status:               Running
Last State:           Terminated
  Reason:             OOMKilled
  Exit Code:          137
  Started:            2024-01-15T14:32:18Z
  Finished:           2024-01-15T14:35:42Z

POD                    NAME              CPU(cores)   MEMORY(bytes)
api-server-5d8c9b2f   api-container     245m         1847Mi
api-server-5d8c9b2f   sidecar           12m          128Mi

deployment.apps/api-server resource requirements updated
```

!!! warning "Common errors"
    **`Error from server (NotFound): pods "<pod>" not found`** — Verify the pod name and namespace with `oc get pods -n <ns>` before running describe.
    **`error: the server doesn't have a resource type "top"`** — Enable metrics-server on the cluster with `oc apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`.
    **`Error from server (NotFound): deployments.apps "<name>" not found`** — Confirm the deployment exists in the target namespace and use the correct resource type (deployment, statefulset, daemonset, etc.).
## Node NotReady

```bash
# 1. Check node conditions
oc describe node <node>
# Conditions section: MemoryPressure, DiskPressure, PIDPressure, Ready

# 2. Check kubelet and CRI-O on the node
oc debug node/<node>
chroot /host
systemctl status kubelet
systemctl status crio
journalctl -u kubelet -n 50 --no-pager
journalctl -u crio -n 50 --no-pager

# 3. Check disk usage (DiskPressure threshold default: 85%)
df -h /
df -h /var

# 4. Check OVN-K network pods on the node
oc get pods -n openshift-ovn-kubernetes \
  --field-selector=spec.nodeName=<node>

# 5. Check NTP (etcd elections require < 1s time skew between masters)
chroot /host chronyc tracking
chronyc sources -v

# 6. If node stuck NotReady after reboot:
oc get machineconfigpool -w
# MCO may be applying a MachineConfig — wait for it to complete
```


```text title="Expected output"
NAME                 STATUS   ROLES           AGE   VERSION
worker-01.ocp.local  NotReady worker,worker-cnf 45d   v1.27.6+f67aeb3

Conditions:
  Type                 Status  LastHeartbeatTime         Reason
  MemoryPressure       False   Wed Jan 10 14:32:15 2024  KubeletHasSufficientMemory
  DiskPressure         True    Wed Jan 10 14:32:15 2024  KubeletHasDiskPressure
  PIDPressure          False   Wed Jan 10 14:32:15 2024  KubeletHasSufficientPID
  Ready                False   Wed Jan 10 14:32:15 2024  KubeletNotReady

Filesystem     Size  Used Avail Use% Mounted on
/dev/sda3      100G  87G  13G  87%  /
/dev/sda4      50G  42G  8G   84%  /var

NAME                                      READY   STATUS    RESTARTS   AGE
ovnkube-node-8xf7m                        1/1     Running   0          12d
ovn-controller-5qp2k                      1/1     Running   2          8d

Reference ID : 8d4a8c2f.1704879135
Leap status  : Normal
System time  : 0.000234567 seconds slow of NTP time
RMS offset   : 0.000456789 seconds

NAME                    CONFIG                                        UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT   UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
master                  rendered-master-a1b2c3d4e5f6g7h8i9j0k1l2   True      False      False      3               3                   3                     0                      45d
worker                  rendered-worker-x9y8z7w6v5u4t3s2r1q0p9o8   False     True       False      5               4                   4                     0                      45d
```

!!! warning "Common errors"
    **`error: unable to connect to the server: dial tcp: lookup <node>: no such host`** — Replace `<node>` with the actual node name from `oc get nodes`.
    **`chroot: cannot change root directory to /host: No such file or directory`** — Ensure you are running `oc debug node/<node>` first and waiting for the debug pod to start before executing chroot.
    **`Unit kubelet.service could not be found.`** — The kubelet service may not be installed or the node OS differs; verify the node is RHCOS and check `/etc/systemd/system/kubelet.service.d/` for custom configurations.
## etcd High Latency

High disk I/O latency causes etcd to miss heartbeat deadlines, leading to leader elections, slow API responses, and cascading CrashLoopBackOff on etcd pods.

```bash
# Get etcd pod name
ETCD_POD=$(oc get pod -n openshift-etcd -l etcd=true -o name | head -1)

# Check endpoint status: DB SIZE and RAFT_APPLIED_INDEX
oc rsh -n openshift-etcd "$ETCD_POD" \
  etcdctl endpoint status --cluster --write-out=table \
  --endpoints=https://localhost:2379 \
  --cacert=/etc/kubernetes/static-pod-certs/configmaps/etcd-serving-ca/ca-bundle.crt \
  --cert=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).crt \
  --key=/etc/kubernetes/static-pod-certs/secrets/etcd-all-certs/etcd-peer-$(hostname).key

# Check P99 WAL fsync latency via Prometheus
# Alert threshold: > 10ms P99
# Query: etcd_disk_wal_fsync_duration_seconds{quantile="0.99"}

# Check disk latency on the etcd node
oc debug node/<master-node>
chroot /host
# Use iostat to identify disk saturation:
iostat -x 1 5 | grep -E "Device|sd|nvme"

# Defrag etcd if DB size > 8 GB
oc rsh -n openshift-etcd "$ETCD_POD" \
  etcdctl defrag --cluster \
  --endpoints=https://localhost:2379 \
  --cacert=... --cert=... --key=...
```


```text title="Expected output"
pod/etcd-ip-10-0-1-42.ec2.internal

+------------------------+------------------+---------+---------+-----------+
|       ENDPOINT         |        ID        | VERSION | DB SIZE | RAFT INDEX|
+------------------------+------------------+---------+---------+-----------+
| https://10.0.1.42:2379 | 8e4c5d7f9a2b1c3e |   3.5.9 | 7.2 GB  | 2847561   |
| https://10.0.1.51:2379 | 4a6b8c2d5e9f1a3b |   3.5.9 | 7.1 GB  | 2847561   |
| https://10.0.1.63:2379 | 9f1e2d3c4b5a6e7d |   3.5.9 | 7.3 GB  | 2847561   |
+------------------------+------------------+---------+---------+-----------+

Starting debug pod on master-0.ocp.example.com ...
Pod IP: 10.128.0.45
chroot /host
Device     r/s     w/s     rkB/s     wkB/s   await svctm  %util
sda       12.4    45.2    156.8   1024.3   18.5   2.1   12.1
nvme0n1   8.1     38.9    102.4    892.1   16.2   1.8    8.9

Defragmentation started on member 8e4c5d7f9a2b1c3e
Defragmentation finished for member 8e4c5d7f9a2b1c3e
```

!!! warning "Common errors"
    **`error: unable to match a pod using the provided selectors: etcd=true`** — Verify the label selector with `oc get pod -n openshift-etcd --show-labels` and update the label name if it differs (e.g., `app=etcd` or `k8s-app=etcd`).
    **`x509: certificate signed by unknown authority`** — Ensure the certificate paths are correct and the pod is running with proper mounted secrets by checking `oc describe pod $ETCD_POD -n openshift-etcd` for volume mounts.
    **`error: node "<master-node>" not found`** — Replace `<master-node>` with an actual node name from `oc get nodes -l node-role.kubernetes.io/master` (e.g., `master-0.ocp.example.com`).
## DNS Failures

```bash
# 1. Check CoreDNS pods (one per node via DaemonSet)
oc get pods -n openshift-dns -o wide
# All should be Running; any Pending or Error needs investigation

# 2. Test DNS from within a pod
oc debug -n <ns> -- nslookup <service>.<ns>.svc.cluster.local
oc debug -n <ns> -- nslookup kubernetes.default.svc.cluster.local

# 3. Check CoreDNS logs for forwarding errors
oc logs -n openshift-dns \
  -l dns.operator.openshift.io/daemonset-dns --tail=50

# 4. Verify DNS ConfigMap (Corefile)
oc get configmap dns-default -n openshift-dns -o yaml
# Check upstream forwarder configuration

# 5. Check /etc/resolv.conf inside a pod
oc exec -n <ns> <pod> -- cat /etc/resolv.conf
# Should show: nameserver 172.30.0.10 (cluster DNS service IP)

# 6. Verify DNS service is running
oc get svc -n openshift-dns
# dns-default ClusterIP should be the IP in /etc/resolv.conf
```


```text title="Expected output"
NAME                    READY   STATUS    RESTARTS   AGE     IP            NODE
dns-default-abcd1       1/1     Running   0          7d      10.128.0.5    worker-1.example.com
dns-default-efgh2       1/1     Running   0          7d      10.128.1.8    worker-2.example.com
dns-default-ijkl3       1/1     Running   2          6d23h   10.128.2.12   master-0.example.com

Server:         172.30.0.10
Address:        172.30.0.10#53

Name:   nginx.default.svc.cluster.local
Address: 10.129.0.45

Server:         172.30.0.10
Address:        172.30.0.10#53

Name:   kubernetes.default.svc.cluster.local
Address: 172.30.0.1

[INFO] plugin/reload: Running configuration MD5 = 1a2b3c4d5e6f7g8h
[INFO] 10.128.0.15:54321 - 16384 "A" "nginx.default.svc.cluster.local." udp 54 false 2 0.001234s
[INFO] 10.128.1.22:45678 - 16384 "A" "kubernetes.default.svc.cluster.local." udp 54 false 2 0.000891s

apiVersion: v1
kind: ConfigMap
metadata:
  name: dns-default
  namespace: openshift-dns
data:
  Corefile: |
    .:5353 {
        errors
        health :8080
        ready :8081
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
        }
        forward . 8.8.8.8 8.8.4.4
        cache 30
    }

nameserver 172.30.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:2

NAME          TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
dns-default   ClusterIP   172.30.0.10   <none>        53/UDP    45d
```

!!! warning "Common errors"
    **`error: unable to forward to node "worker-1.example.com": error when getting node: nodes "worker-1.example.com" not found`** — Use the exact node name from `oc get nodes` instead of the FQDN.
    **`nslookup: can't resolve 'nginx.default.svc.cluster.local': No answer`** — Verify the service exists with `oc get svc -n default` and check CoreDNS logs for forwarding errors.
    **`nameserver 10.0.0.1`** — The resolver is pointing to the host DNS instead of the cluster DNS (172.30.0.10); restart the pod or check the CNI plugin configuration.
## Cluster Operator Degraded

```bash
# 1. Get detailed status
oc describe co <operator-name>
# Conditions section → message field has root cause

# 2. Check operator pod logs
oc get pods -n openshift-<operator-name>
oc logs -n openshift-<operator-name> -l app=<operator-pod> --tail=100

# 3. Common operator degraded scenarios:
# dns degraded → check coredns pods in openshift-dns; check upstream DNS reachability
# ingress degraded → check router pods in openshift-ingress; check wildcard cert expiry
# monitoring degraded → check prometheus pods; likely PVC full or OOM
# authentication degraded → OAuth pods failing; check LDAP/OIDC connectivity
# storage degraded → CSI driver pods; check underlying storage system

# 4. Check if Progressing is stuck (often indicates upgrade issue)
oc get co | grep -v "True.*False.*False"
# Any CO with Available=False, Degraded=True, or Progressing=True for > 15 min

# 5. Force operator to reconcile (redeploy its managed pods)
oc rollout restart deployment/<operator-pod> -n openshift-<operator-ns>
```


```text title="Expected output"
$ oc describe co dns
Name:         dns
Namespace:    
Labels:       <none>
Annotations:  <none>
API Version:  config.openshift.io/v1
Kind:         ClusterOperator
Metadata:
  Creation Timestamp:  2024-01-15T09:22:33Z
  Generation:          47
  Resource Version:    8934521
  UID:                 a7c2f1e9-8b3d-4a6f-91c2-5e8d3f2a1b9c
Status:
  Conditions:
  - Last Transition Time:  2024-01-15T14:18:22Z
    Message:              DNS controller successfully rolled out coredns
    Reason:               AsExpected
    Status:               True
    Type:                 Available
  - Last Transition Time:  2024-01-15T14:18:22Z
    Message:              DNS controller successfully rolled out coredns
    Reason:               AsExpected
    Status:               False
    Type:                 Degraded
  - Last Transition Time:  2024-01-15T14:18:22Z
    Message:              DNS controller successfully rolled out coredns
    Reason:               AsExpected
    Status:               False
    Type:                 Progressing
  Related Objects:
  - Group:      apps
    Name:       dns-default
    Namespace:  openshift-dns
    Resource:   deployments
  Version:      4.13.8

$ oc get pods -n openshift-dns
NAME                    READY   STATUS    RESTARTS   AGE
dns-default-5f8c2d9b-k7m9l   1/1     Running   0          2d14h
dns-default-5f8c2d9b-n3x6p   1/1     Running   0          2d14h

$ oc logs -n openshift-dns -l app=dns-default --tail=100
2024-01-15T14:18:15.234Z [INFO] coredns: CoreDNS-1.10.1
2024-01-15T14:18:15.456Z [INFO] plugin/reload: Running CoreDNS-1.10.1
2024-01-15T14:18:22.891Z [INFO] Successfully loaded Corefile configuration
2024-01-15T14:18:23.012Z [INFO] Ready to accept queries

$ oc get co | grep -v "True.*False.*False"
NAME                                       AVAILABLE   DEGRADED   PROGRESSING   SINCE   VERSION
authentication                             True        False      False         2d      4.13.8
cloud-credential                           True        False      False         2d      4.13.8
cluster-autoscaler                         True        False      False         2d      4.13.8
dns                                        True        False      False         2d      4.13.8
etcd                                       True        False      False         2d      4.13.8
...

$ oc rollout restart deployment/dns-default -n openshift-dns
deployment.apps/dns-default restarted
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "co"`** — Use the full resource name `oc describe clusteroperator
---

## See also

- [OpenShift — Diagnostics](../diagnostics/)
- [OpenShift — Escalation](../escalation/)
- [OpenShift — Health Checks](../../operations/health-checks/)

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
