# OpenShift — Procedures

<div class="kb-summary">
Common operational procedures: node drain and maintenance mode, scaling MachineSets, adding node roles, rotating certificates, and managing cluster configuration.
</div>

```text
┌────────────────────────────────── OpenShift Operational Procedures ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Always: health check before maintenance; cordon then drain; verify workloads rescheduled    │   │
│   │   Scale: edit MachineSet replicas (not manual node creation); approve CSRs after scale-out    │   │
│   │   Certs: cluster auto-rotates < 1 year; etcd peer certs need manual intervention if expired  │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Node Maintenance        │  │     Cluster Scaling          │  │   Certificate Rotation      │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  cordon → drain → work      │  │  Edit MachineSet replicas    │  │  Auto-rotated by cluster    │  │
│   │  Respect PodDisruptionBudge │  │  Approve new worker CSRs     │  │  Manual: oc adm ocp-certs   │  │
│   │  DaemonSets: --ignore-ds    │  │  Label/taint new nodes       │  │  etcd: special procedure    │  │
│   │  uncordon when done         │  │  ClusterAutoscaler for auto  │  │  kubeconfig: oc login again │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PDB          = PodDisruptionBudget; limits how many pods can be unavailable; drain respects it     │
│    MachineConfig= OS-level configuration object applied by MCO (files, kernel args, systemd units)    │
│    MachineSet   = Template for worker nodes; scale by editing replicas field                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Node Drain (Maintenance Mode)

```bash
# 1. Pre-check — ensure cluster is healthy
oc get co | grep -v "True.*False.*False"
oc get nodes

# 2. Cordon (mark unschedulable)
oc adm cordon <node-name>

# 3. Drain (evict pods)
oc adm drain <node-name> \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=60 \
  --timeout=300s
# --ignore-daemonsets: skip DaemonSet pods (they'll restart on the node)
# --delete-emptydir-data: allow pods with emptyDir volumes to be evicted

# 4. Verify workloads rescheduled
oc get pods --all-namespaces | grep <node-name>

# 5. Perform maintenance

# 6. Uncordon
oc adm uncordon <node-name>
oc get nodes   # verify Ready
```

## Scale Workers via MachineSet

```bash
# List MachineSets
oc get machineset -n openshift-machine-api

# Scale up
oc scale machineset <machineset-name> -n openshift-machine-api --replicas=5

# Monitor new machine provisioning
oc get machine -n openshift-machine-api -w
oc get nodes -w

# Approve new worker CSRs (if auto-approval not configured)
oc get csr | grep Pending
oc adm certificate approve <csr-name>
# Approve all pending at once:
oc get csr -o name | xargs oc adm certificate approve

# Scale down (deletes nodes gracefully)
oc scale machineset <machineset-name> -n openshift-machine-api --replicas=3
```

## Add New MachineSet

```bash
# Export existing MachineSet as template
oc get machineset <existing-ms> -n openshift-machine-api -o yaml > new-ms.yaml

# Edit: change name, zone/AZ, and any node-specific settings
# Key fields to update:
#   metadata.name
#   spec.selector.matchLabels.machine.openshift.io/cluster-api-machineset
#   spec.template.metadata.labels.machine.openshift.io/cluster-api-machineset
#   spec.template.spec.providerSpec.value.network (if different)

oc apply -f new-ms.yaml
oc get machineset -n openshift-machine-api
```

## Add Infra Node Role

```bash
# 1. Create infra MachineSet (copy from worker MS, add infra label)
# 2. Label existing or new node
oc label node <node> node-role.kubernetes.io/infra=""

# 3. Taint to prevent regular workloads
oc adm taint node <node> node-role.kubernetes.io/infra=reserved:NoSchedule

# 4. Move router (ingress controller) to infra nodes
oc patch ingresscontroller/default -n openshift-ingress-operator \
  --type=merge \
  -p '{"spec":{"nodePlacement":{"nodeSelector":{"matchLabels":{"node-role.kubernetes.io/infra":""}},"tolerations":[{"key":"node-role.kubernetes.io/infra","effect":"NoSchedule"}]}}}'

# 5. Move monitoring
cat <<EOF | oc apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    prometheusOperator:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: node-role.kubernetes.io/infra
        effect: NoSchedule
    prometheusK8s:
      nodeSelector:
        node-role.kubernetes.io/infra: ""
      tolerations:
      - key: node-role.kubernetes.io/infra
        effect: NoSchedule
EOF
```

## Certificate Rotation

```bash
# Check certificate expiry
oc -n openshift-kube-apiserver-operator get secret kube-apiserver-to-kubelet-signer \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate

# Force ingress cert rotation
oc patch secret router-certs-default -n openshift-ingress --type=json \
  -p='[{"op":"remove","path":"/data/tls.crt"}]'

# Rotate etcd peer certs (if expired)
# Use the etcd-cert-recovery procedure from Red Hat KCS
oc get po -n openshift-etcd | grep etcd

# After cert rotation: approve new CSRs
oc get csr | grep Pending
oc adm certificate approve <csr>
```

## Apply MachineConfig (OS Configuration)

```bash
# Example: add custom kernel argument
cat <<EOF | oc apply -f -
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: worker
  name: 99-worker-custom-kernel-arg
spec:
  kernelArguments:
  - hugepagesz=1G
  - hugepages=16
EOF

# Monitor MCO applying the config (nodes will drain+reboot one by one)
oc get mcp   # MachineConfigPool — watch UPDATED / UPDATING / DEGRADED
oc get nodes -w
```
