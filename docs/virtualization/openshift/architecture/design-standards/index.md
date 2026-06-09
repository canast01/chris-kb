# OpenShift — Design Standards

<div class="kb-summary">
Node sizing guidelines, MachineSet design, storage class standards, network CIDR planning, and infrastructure node placement for production OpenShift clusters.
</div>

```text
┌───────────────────────────────────── OpenShift Design Standards ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Master nodes: 3× fixed, never scale; size for etcd (IOPS-sensitive); dedicated infra nodes  │   │
│   │   Worker nodes: MachineSets; autoscale or manual; separate compute/infra/storage roles         │  │
│   │   Storage: define StorageClasses before workloads; default SC must exist for PVC binding       │  │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Masters (3 fixed)      │  │    Workers / MachineSets     │  │    Infra Nodes (3+)         │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  8 vCPU / 32 GB RAM min     │  │  4–16 vCPU depending on WL  │  │  4 vCPU / 16 GB RAM min     │   │
│   │  120 GB etcd disk (SSD)     │  │  Separate MachineSet / AZ   │  │  Router, monitoring, reg    │   │
│   │  Low latency to etcd        │  │  Labels + taints for roles   │  │  Taint: infra=reserved      │  │
│   │  Never schedule workloads   │  │  Autoscaler: min/max/target  │  │  Separate from worker WL    │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    MachineSet     = Template for a group of worker nodes; edit replicas to scale horizontally         │
│    StorageClass   = Defines how PVCs are provisioned (provisioner, reclaim policy, binding mode)      │
│    Infra node     = Worker with infra role; runs platform components, not user workloads              │
│    ClusterAutoscaler= Scales MachineSets based on pending pods; configures min/max per MachineSet     │
│    CIDR           = Classless Inter-Domain Routing; set clusterNetwork + serviceNetwork at install    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Node Sizing Reference

| Role | vCPU | RAM | Boot disk | Notes |
|---|---|---|---|---|
| Master | 8 | 32 GB | 120 GB SSD | etcd IOPS-sensitive; no workloads |
| Infra | 4–8 | 16–32 GB | 120 GB | Router, monitoring, registry |
| Worker (general) | 4–16 | 16–64 GB | 120 GB | Size per workload profile |
| Storage (ODF) | 10 | 24 GB | 120 GB + OSD disks | ODF minimum per node |

## Network CIDR Planning

Set at install time — cannot change after cluster creation.

```yaml
# install-config.yaml snippet
networking:
  clusterNetwork:
  - cidr: 10.128.0.0/14       # Pod network — must not overlap with node/service
    hostPrefix: 23             # /23 per node = 512 pod IPs per node
  serviceNetwork:
  - 172.30.0.0/16             # Service ClusterIP range
  machineNetwork:
  - cidr: 192.168.100.0/24   # Node network (your infrastructure)
  networkType: OVNKubernetes
```

| Network | Default CIDR | Notes |
|---|---|---|
| Pod (clusterNetwork) | 10.128.0.0/14 | Avoid overlap with infra; change if conflicting |
| Service (serviceNetwork) | 172.30.0.0/16 | ClusterIP range; kube-dns uses this |
| Node (machineNetwork) | site-specific | Must match your VM/bare-metal network |

## StorageClass Standards

```yaml
# Default StorageClass (must exist for dynamic PVC binding)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: thin-csi
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: csi.vsphere.volume.vmware.com
parameters:
  datastoreurl: "ds:///vmfs/volumes/<uuid>/"
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

| Storage Class | Use case | Reclaim | Binding mode |
|---|---|---|---|
| `thin-csi` (default) | General workloads on vSphere | Delete | WaitForFirstConsumer |
| `thick-csi` | Databases, etcd snapshots | Retain | Immediate |
| `ocs-storagecluster-ceph-rbd` | ODF block (RWO) | Delete | Immediate |
| `ocs-storagecluster-cephfs` | ODF shared filesystem (RWX) | Delete | Immediate |

## MachineSet Design

```yaml
# MachineSet template (vSphere example)
apiVersion: machine.openshift.io/v1beta1
kind: MachineSet
metadata:
  name: cluster-worker-0
  namespace: openshift-machine-api
spec:
  replicas: 3
  selector:
    matchLabels:
      machine.openshift.io/cluster-api-machineset: cluster-worker-0
  template:
    spec:
      taints: []          # Add infra taint for infra nodes
      metadata:
        labels:
          node-role.kubernetes.io/worker: ""
```

```bash
# Scale MachineSet
oc scale machineset cluster-worker-0 -n openshift-machine-api --replicas=5

# List MachineSets
oc get machineset -n openshift-machine-api

# Add ClusterAutoscaler
oc apply -f clusterautoscaler.yaml
oc apply -f machineautoscaler.yaml   # References MachineSet + min/max
```

## Infra Node Configuration

```bash
# Label and taint infra nodes
oc label node <node> node-role.kubernetes.io/infra=""
oc adm taint node <node> node-role.kubernetes.io/infra=reserved:NoSchedule NoExecute

# Move ingress controller to infra nodes
oc patch ingresscontroller default -n openshift-ingress-operator \
  --type=merge -p '{"spec":{"nodePlacement":{"nodeSelector":{"matchLabels":{"node-role.kubernetes.io/infra":""}},"tolerations":[{"key":"node-role.kubernetes.io/infra","effect":"NoSchedule"}]}}}'

# Move monitoring to infra nodes
oc apply -f cluster-monitoring-config.yaml   # configMap: cluster-monitoring-config
```
