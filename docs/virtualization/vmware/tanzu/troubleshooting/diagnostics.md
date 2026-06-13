---
tags:
  - tanzu
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Tanzu — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Collect Cluster Diagnostics, Supervisor Control Plane VM Access, TKG Cluster Events, Harbor Logs, Describe Stuck or Failing Pods and 3 more sections.

*Applies to: Tanzu 3.x*
</div>
```text
┌────────────────────────────── Virtualization Vmware Tanzu — Diagnostics ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Vmware diagnostics: log collection, health checks, and performance analysis          │   │
│   │          Tools: management CLI, REST API, vendor support bundle, and system event log         │   │
│   │          Performance: check I/O latency, throughput, queue depth, and cache hit rate          │   │
│   │       Collect support bundle before contacting vendor support to reduce time-to-resolve       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify issue → collect logs → run diagnostics → analyse → resolve                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Tanzu infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Tanzu platform overview and core concepts               │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Collect Cluster Diagnostics

```bash
# Tanzu diagnostics bundle (management cluster)
tanzu diagnostics collect --management-cluster

# kubectl cluster dump (workload cluster)
kubectl config use-context <cluster-context>
kubectl cluster-info dump --output-directory=/tmp/cluster-dump --all-namespaces
tar czf cluster-dump-$(date +%Y%m%d).tar.gz /tmp/cluster-dump/
```

---

## Supervisor Control Plane VM Access

```bash
# The Supervisor control plane VMs run on ESXi hosts — access via SSH
# Default SSH key is in vCenter:
# Workload Management → Supervisor → Control Plane VMs → SSH Key

# Get Supervisor control plane VM IPs from vCenter
# vCenter → Workload Management → Supervisor → Control Plane VMs

ssh -i ~/.ssh/supervisor_key root@<supervisor-control-plane-ip>

# Check Supervisor API server log:
journalctl -u kube-apiserver -f

# Check etcd:
journalctl -u etcd -f

# Check all Supervisor system pods:
kubectl get pods -n kube-system
kubectl get pods -n vmware-system-tkg
```

---

## TKG Cluster Events

```bash
# Get all events sorted by time (best first view for diagnosing recent issues)
kubectl get events -A --sort-by='.lastTimestamp' | tail -50

# Get events for a specific namespace
kubectl get events -n production --sort-by='.lastTimestamp'

# Get events for a specific pod
kubectl describe pod <pod-name> -n production | tail -30
```

---

## Harbor Logs

```bash
# If Harbor is deployed as OVA (VM-based):
ssh admin@harbor.example.local
docker-compose -f /opt/docker-compose.yml logs --tail=100 core
docker-compose -f /opt/docker-compose.yml logs --tail=100 registry
docker-compose -f /opt/docker-compose.yml logs --tail=100 nginx

# If Harbor is deployed on Kubernetes:
kubectl logs -n harbor \
  $(kubectl get pods -n harbor -l component=core -o jsonpath='{.items[0].metadata.name}') \
  --tail=100

kubectl logs -n harbor \
  $(kubectl get pods -n harbor -l component=registry -o jsonpath='{.items[0].metadata.name}') \
  --tail=100
```

---

## Describe Stuck or Failing Pods

```bash
# Describe pod — shows scheduling decisions, container state, events
kubectl describe pod <pod-name> -n <namespace>

# Get previous container logs (if container crashed and restarted)
kubectl logs <pod-name> -n <namespace> --previous

# Follow live logs
kubectl logs <pod-name> -n <namespace> -f

# Multi-container pods — specify container
kubectl logs <pod-name> -n <namespace> -c <container-name>
```

---

## CSI Driver Logs (for PVC Issues)

```bash
# vSphere CSI driver runs in vmware-system-csi namespace
kubectl get pods -n vmware-system-csi

# Check CSI controller logs:
kubectl logs -n vmware-system-csi \
  $(kubectl get pods -n vmware-system-csi -l app=vsphere-csi-controller -o jsonpath='{.items[0].metadata.name}') \
  -c vsphere-csi-controller --tail=100

# Check CSI node daemon logs (runs on each node):
kubectl logs -n vmware-system-csi \
  -l app=vsphere-csi-node \
  -c vsphere-csi-node --tail=50
```

---

## Pinniped Auth Failure Diagnostics

```bash
# Check Pinniped supervisor pods
kubectl get pods -n pinniped-supervisor
kubectl logs -n pinniped-supervisor \
  $(kubectl get pods -n pinniped-supervisor -l app=pinniped-supervisor -o jsonpath='{.items[0].metadata.name}') \
  --tail=50

# Check Pinniped concierge (per workload cluster)
kubectl get pods -n pinniped-concierge
kubectl logs -n pinniped-concierge \
  $(kubectl get pods -n pinniped-concierge -o jsonpath='{.items[0].metadata.name}') \
  --tail=50

# Test OIDC flow manually:
tanzu cluster kubeconfig get my-cluster
kubectl get pods -n default  # If this fails with auth error, check Pinniped logs
```

---

## Enable Verbose tanzu CLI Logging

```bash
# Run tanzu commands with verbose logging
TANZU_LOG_LEVEL=debug tanzu cluster create my-cluster --file config.yaml 2>&1 | tee tanzu-debug.log

# Or set log level via flag:
tanzu cluster list -v 9
```

---

## See also

- [Virtualization Vmware Tanzu — Common Issues](common-issues/)
- [Tanzu — Escalation](escalation/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
