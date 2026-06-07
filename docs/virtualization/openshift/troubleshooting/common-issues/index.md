# OpenShift — Common Issues

<div class="kb-summary">
Troubleshooting guide for frequent OpenShift failures: CrashLoopBackOff, ImagePullBackOff, node NotReady, Pending pods, OOMKilled, and degraded cluster operators.
</div>

```text
┌──────────────────────────────────── OpenShift Common Issues ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   First: check events (oc get events) and logs (oc logs); 90% of issues visible there        │    │
│   │   Node NotReady: check kubelet and CRI-O status on node; network plugin issues common        │    │
│   │   Operator Degraded: check operator pod logs and Conditions message on the CO object         │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Pod Failures           │  │      Node Issues             │  │    Operator / Platform      │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  CrashLoopBackOff           │  │  NotReady: kubelet/CRI-O     │  │  Degraded CO: check pods   │   │
│   │  ImagePullBackOff           │  │  NotSchedulable: cordoned    │  │  Progressing long: upgrade?│   │
│   │  OOMKilled: mem limits      │  │  DiskPressure: disk full     │  │  etcd high latency: IOPS   │   │
│   │  Pending: no resources/SCC  │  │  NTP drift: etcd elections   │  │  DNS failures: CoreDNS pod │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Back-off     = Exponential delay between restart attempts; resets if pod runs > 10 minutes         │
│    OOMKilled    = Container exceeded memory limit; kernel killed it; increase limit or fix leak       │
│    DiskPressure = Node disk > eviction threshold; kubelet starts evicting pods                        │
│    Taint        = Node property that repels pods without matching toleration                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## CrashLoopBackOff

```bash
# Symptoms: pod restarts repeatedly; STATUS = CrashLoopBackOff

# 1. Check current logs
oc logs <pod> -n <ns>

# 2. Check previous container instance (the one that crashed)
oc logs <pod> -n <ns> --previous

# 3. Describe for events
oc describe pod <pod> -n <ns>
# Look at: Events section → reason, message
# Look at: Last State → exitCode (OOMKilled=137, generic crash=1, segfault=139)

# 4. Common causes:
#    exitCode 137 → OOMKilled (see OOMKilled section)
#    exitCode 1   → application error; check logs for exception/traceback
#    exitCode 127 → command not found (CMD not in image)
#    "exec format error" → wrong image architecture

# 5. Debug the image interactively
oc debug deployment/<name> -n <ns>
```

## ImagePullBackOff

```bash
# Symptoms: pod stays in ImagePullBackOff; can't pull container image

# 1. Check which image and error
oc describe pod <pod> -n <ns>
# Events: Failed to pull image "quay.io/myapp:latest": ...

# Common causes and fixes:
# a) Wrong image name/tag → fix image reference in deployment
# b) No pull secret → oc create secret docker-registry registry-creds ...
#                      oc secrets link default registry-creds --for=pull -n <ns>
# c) Registry unreachable → check network, proxy, firewall
# d) Air-gap: image not mirrored → mirror image to internal registry
# e) Auth expired → re-create or rotate pull secret

# 2. Test pull manually on a node
oc debug node/<node> -- crictl pull <image>

# 3. Check global pull secret
oc get secret pull-secret -n openshift-config -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq .
```

## Pending Pods (Not Scheduling)

```bash
# Symptoms: pod stays in Pending state

# 1. Check events
oc describe pod <pod> -n <ns>
# Events will show scheduling failure reason

# Common causes:
# a) Insufficient resources: "0/6 nodes are available: Insufficient cpu"
#    → Check: oc adm top nodes; reduce requests or add nodes

# b) SCC violation: "unable to validate against any security context constraint"
#    → Check: oc adm policy scc-subject-review -f pod.yaml
#    → Grant SCC: oc adm policy add-scc-to-user anyuid -z <sa> -n <ns>

# c) Taint/toleration mismatch: "node(s) had untolerated taint"
#    → Check: oc describe node | grep Taint
#    → Add toleration to pod spec

# d) NodeAffinity mismatch: "node(s) didn't match nodeAffinity"
#    → Check label requirements in pod spec
#    → oc get nodes --show-labels

# e) PVC pending: PVC not bound (wrong StorageClass, no provisioner)
#    → oc get pvc -n <ns>
#    → oc describe pvc <name> -n <ns>
```

## OOMKilled

```bash
# Symptoms: pod exits with exitCode 137; pod describes "OOMKilled"

# 1. Check which container OOMKilled
oc describe pod <pod> -n <ns>
# Last State: Terminated  Reason: OOMKilled

# 2. Check container memory limits vs actual usage
oc adm top pods <pod> -n <ns> --containers

# 3. Fix: increase memory limit in deployment
oc set resources deployment <name> -n <ns> \
  --containers=<container> \
  --limits=memory=2Gi \
  --requests=memory=512Mi

# 4. If limit is already high: check for memory leak in application
```

## Node NotReady

```bash
# Symptoms: oc get nodes shows node as NotReady

# 1. Check node conditions
oc describe node <node>
# Look at: Conditions section → MemoryPressure, DiskPressure, PIDPressure, Ready

# 2. Check kubelet and CRI-O on the node
oc debug node/<node>
chroot /host
systemctl status kubelet
systemctl status crio
journalctl -u kubelet -n 50
journalctl -u crio -n 50

# 3. Check disk usage
df -h

# 4. Check OVN-K network pods on the node
oc get pods -n openshift-ovn-kubernetes --field-selector=spec.nodeName=<node>

# 5. Check NTP (etcd elections require time sync)
chroot /host chronyc tracking
```

## Cluster Operator Degraded

```bash
# Symptoms: oc get co shows DEGRADED=True for an operator

# 1. Get detailed status
oc describe co <operator-name>
# Conditions section → message field has root cause

# 2. Check operator pod logs
oc get pods -n openshift-<operator-name>
oc logs -n openshift-<operator-name> -l app=<operator-pod>

# 3. Common operator issues:
# dns operator degraded → check coredns pods in openshift-dns
# ingress operator degraded → check router pods in openshift-ingress
# monitoring operator degraded → check prometheus pods; likely PVC issue
# authentication degraded → check oauth server pods; LDAP connectivity
```
