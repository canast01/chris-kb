# Tanzu — Diagnostics

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
ssh admin@harbor.corp.local
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
