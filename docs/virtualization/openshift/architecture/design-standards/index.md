---
tags:
  - architecture
description: "Node sizing guidelines, MachineSet design, storage class standards, network CIDR planning, and infrastructure node placement for production OpenShift..."
---
# OpenShift — Design Standards

<div class="kb-summary">
Node sizing guidelines, MachineSet design, storage class standards, network CIDR planning, and infrastructure node placement for production OpenShift clusters.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

A: "Cluster Sizing Tiers" {shape: rectangle}
B: "Compact\n3 control-plane\n0 dedicated workers" {shape: rectangle}
C: "Standard\n3 control-plane\n2+ workers" {shape: rectangle}
D: "Large\n3 control-plane\n100+ workers\n+ infra nodes" {shape: rectangle}
C1: "Worker MachineSet\ngeneral compute" {shape: rectangle}
D1: "Worker MachineSet\ncompute" {shape: rectangle}
D2: "Infra MachineSet\nrouter / monitoring / registry" {shape: rectangle}
D3: "Storage MachineSet\nODF / Ceph OSDs" {shape: rectangle}

A -> B
A -> C
A -> D
C -> C1
D -> D1
D -> D2
D -> D3
```

```d2
direction: down

cluster_sizing_tiers: "Cluster Sizing Tiers" {shape: rectangle}
node_sizing_reference: "Node Sizing Reference" {shape: rectangle}
infrastructure_nodes: "Infrastructure Nodes" {shape: rectangle}
etcd_disk_sizing_and_validation: "etcd Disk Sizing and Validation" {shape: rectangle}
network_cidr_planning: "Network CIDR Planning" {shape: rectangle}
storageclass_standards: "StorageClass Standards" {shape: rectangle}

cluster_sizing_tiers -> node_sizing_reference: hardens
node_sizing_reference -> infrastructure_nodes: hardens
infrastructure_nodes -> etcd_disk_sizing_and_validation: hardens
etcd_disk_sizing_and_validation -> network_cidr_planning: hardens
network_cidr_planning -> storageclass_standards: hardens
```

## Cluster Sizing Tiers

| Tier | Control plane | Workers | Use case |
|---|---|---|---|
| Compact | 3 (masters run workloads) | 0 | Lab, CI, edge; masters schedulable |
| Standard | 3 | 2–10 | Small production; no dedicated infra nodes |
| Standard + Infra | 3 | 2–10 + 3 infra | Production; platform components isolated |
| Large | 3 | 100+ | Enterprise; separate storage, infra, compute pools |

## Node Sizing Reference

| Role | vCPU | RAM | Boot disk | Notes |
|---|---|---|---|---|
| Master (small) | 8 | 32 GB | 120 GB SSD | Minimum; supports ≤25 workers |
| Master (medium) | 12 | 48 GB | 120 GB SSD | Supports 25–100 workers |
| Master (large) | 16 | 64 GB | 120 GB SSD | Supports 100+ workers |
| Infra | 4–8 | 16–32 GB | 120 GB | Router, monitoring, registry |
| Worker (general) | 4–16 | 16–64 GB | 120 GB | Size per workload profile |
| Storage (ODF) | 10 | 24 GB | 120 GB + OSD disks | ODF minimum 3 nodes × 3 disks |

## Infrastructure Nodes

Infrastructure nodes run platform components (ingress router, image registry, cluster monitoring, logging) and keep those workloads off general worker nodes. This reduces licensing impact (infra nodes do not consume OpenShift worker entitlements in some scenarios).

**Workloads that belong on infra nodes:**

- OpenShift Router (`openshift-ingress`)
- Internal Image Registry (`openshift-image-registry`)
- Cluster Monitoring stack (`openshift-monitoring`)
- Cluster Logging / Loki (`openshift-logging`)
- OAuth server (`openshift-authentication`)

```yaml
# MachineSet spec for infra pool (vSphere example)
apiVersion: machine.openshift.io/v1beta1
kind: MachineSet
metadata:
  name: cluster-infra-0
  namespace: openshift-machine-api
spec:
  replicas: 3
  selector:
    matchLabels:
      machine.openshift.io/cluster-api-machineset: cluster-infra-0
  template:
    metadata:
      labels:
        machine.openshift.io/cluster-api-machineset: cluster-infra-0
    spec:
      taints:
      - key: node-role.kubernetes.io/infra
        effect: NoSchedule
      metadata:
        labels:
          node-role.kubernetes.io/infra: ""
          node-role.kubernetes.io/worker: ""
      providerSpec:
        value:
          numCPUs: 8
          memoryMiB: 32768
          diskGiB: 120
```

```bash
# Label and taint infra nodes (manual, non-MachineSet path)
oc label node <node> node-role.kubernetes.io/infra=""
oc adm taint node <node> node-role.kubernetes.io/infra=reserved:NoSchedule

# Move ingress controller to infra nodes
oc patch ingresscontroller default -n openshift-ingress-operator \
  --type=merge -p '{"spec":{"nodePlacement":{"nodeSelector":{"matchLabels":{"node-role.kubernetes.io/infra":""}},"tolerations":[{"key":"node-role.kubernetes.io/infra","effect":"NoSchedule"}]}}}'

# Move monitoring stack to infra nodes (cluster-monitoring-config ConfigMap)
oc -n openshift-monitoring apply -f - <<'EOF'
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


```text title="Expected output"
node/worker-infra-01 labeled
node/worker-infra-01 tainted with node-role.kubernetes.io/infra=reserved:NoSchedule
ingresscontroller.operator.openshift.io/default patched
configmap/cluster-monitoring-config created
```

!!! warning "Common errors"
    **`error: node "<node>" not found`** — Replace `<node>` with the actual node hostname (e.g., `worker-infra-01`).
    **`Error from server (NotFound): ingresscontrollers.operator.openshift.io "default" not found`** — Verify the ingress operator is installed with `oc get ingresscontroller -n openshift-ingress-operator`.
    **`error: error validating "STDIN": error validating data: ValidationError(ConfigMap.data.config.yaml): invalid type for io.openshift.config.v1.ClusterMonitoringConfig: got "string", expected "object"`** — Remove the `config.yaml:` key and pipe the YAML object directly as the ConfigMap data value.
## etcd Disk Sizing and Validation

etcd is the most I/O-sensitive component. Slow disk causes fsync latency, leader elections, and cluster instability.

| Requirement | Value | Notes |
|---|---|---|
| Minimum IOPS | 500 sustained | For 4K random writes (fdatasync) |
| Recommended IOPS | 2,000+ | NVMe preferred |
| Minimum capacity | 10 GB | Practical baseline; 50 GB for large clusters |
| Recommended capacity | 50 GB | Handles compaction and defrag headroom |
| Max fsync latency | 10 ms | Above this threshold triggers leader re-elections |
| Disk type | SSD or NVMe | Spinning disk causes guaranteed instability |

```bash
# Validate etcd disk performance with fio (run on each master before install)
fio \
  --rw=write \
  --ioengine=sync \
  --fdatasync=1 \
  --directory=/var/lib/etcd \
  --size=22m \
  --bs=2300 \
  --name=etcd-fio

# Target: 99th-percentile fsync latency < 10ms
# Look for "fsync/fdatasync/sync_file_range" latency in output
# If p99 > 10ms — do not use that disk for etcd
```


```text title="Expected output"
etcd-fio: (g=0): rw=write, bs=(R) 2300B-2300B, (W) 2300B-2300B, ioengine=sync, iodepth=1
fio-3.28
Starting 1 process
etcd-fio: Laying out IO file (1 file / 22MiB)
etcd-fio: Opened 1 file, 22MiB
etcd-fio: IO Error: ENOSPC (No space left on device)

Run status group 0 (all jobs):
  WRITE: bw=8,456KiB/s (8,659kB/s), 8,456KiB/s-8,456KiB/s (8,659kB/s-8,659kB/s), io=18.2MiB (19.1MB), run=2203-2203msec

Disk stats (read/write):
  sda3: ios=0/9847, merge=0/0, ticks=0/18234, in_queue=18234, util=98.45%

fsync/fdatasync/sync_file_range:
  sync (usec): min=412, max=8923, avg=2156.34, stdev=1847.23, samples=7924
  percentiles (usec): 1.00=521, 5.00=612, 10.00=701, 20.00=892, 50.00=1834, 90.00=4521, 95.00=6234, 99.00=8156, 99.9=8891, 99.99=8923
```

!!! warning "Common errors"
    **`etcd-fio: IO Error: ENOSPC (No space left on device)`** — Ensure /var/lib/etcd has at least 50GB free space before running the test.
    **`fio: command not found`** — Install fio with `yum install fio` (RHEL/CentOS) or `apt-get install fio` (Ubuntu).
    **`Permission denied`** — Run the fio command with `sudo` or as root user since /var/lib/etcd requires elevated privileges.
## Network CIDR Planning

Set at install time — cannot change after cluster creation without reinstalling.

```yaml
# install-config.yaml networking section
networking:
  clusterNetwork:
  - cidr: 10.128.0.0/14       # Pod network; /14 = ~262,144 addresses
    hostPrefix: 23             # /23 per node = 510 pod IPs per node
  serviceNetwork:
  - 172.30.0.0/16             # Service ClusterIP range; ~65,534 services
  machineNetwork:
  - cidr: 192.168.100.0/24   # Node network — must match your infrastructure
  networkType: OVNKubernetes
```

| Network | Default CIDR | Purpose | Overlap risk |
|---|---|---|---|
| Pod (clusterNetwork) | `10.128.0.0/14` | Pod IP allocation across all nodes | Must not overlap node or service network |
| Service (serviceNetwork) | `172.30.0.0/16` | ClusterIP / headless service IPs | Must not overlap pod or node network |
| Node (machineNetwork) | site-specific | VM / bare-metal NIC addresses | Must be routable from your infrastructure |

**OVN-Kubernetes MTU considerations:**

OVN uses Geneve encapsulation for cross-node traffic. Geneve header overhead is ~100 bytes. Set cluster MTU to: `physical NIC MTU − 100`.

| Physical MTU | OVN cluster MTU to configure | Notes |
|---|---|---|
| 1500 (standard Ethernet) | 1400 | Default; works everywhere |
| 9000 (jumbo frames) | 8900 | Requires jumbo frames end-to-end |
| 1600 (cloud) | 1500 | Check cloud provider MTU |

```bash
# Check current network MTU setting
oc get network.operator cluster -o jsonpath='{.spec.defaultNetwork.ovnKubernetesConfig.mtu}'

# Verify pod interface MTU on a node
oc debug node/<node> -- ip link show eth0
```


```text title="Expected output"
1500

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 52:54:00:a1:2f:8c brd ff:ff:ff:ff:ff:ff
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 52:54:00:b3:4d:9e brd ff:ff:ff:ff:ff:ff
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "network.operator"`** — Verify the cluster-network-operator is installed with `oc get clusteroperator cluster-network-operator`.
    **`Error from server (NotFound): nodes "<node>" not found`** — Replace `<node>` with an actual node name from `oc get nodes`.
**VLAN segmentation recommendation:**

Separate VLANs for: (1) machine/node network, (2) storage network (iSCSI/NFS/ODF replication), (3) cluster API/management. Avoids broadcast domain pollution and simplifies firewall rules.

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

| Storage Class | Provisioner | Access mode | Reclaim | Use case |
|---|---|---|---|---|
| `thin-csi` (default) | vSphere CSI | RWO | Delete | General workloads on vSphere |
| `thick-csi` | vSphere CSI | RWO | Retain | Databases, etcd snapshots |
| `ocs-storagecluster-ceph-rbd` | ODF / Ceph RBD | RWO | Delete | High-performance block storage |
| `ocs-storagecluster-cephfs` | ODF / CephFS | RWX | Delete | Shared filesystems, NFS replacement |
| `nfs-client` | NFS subdir | RWX | Delete | Simple shared storage, legacy workloads |

```bash
# Check StorageClasses and which is default
oc get sc
# NAME             PROVISIONER                    RECLAIMPOLICY   VOLUMEBINDINGMODE
# thin-csi (default) csi.vsphere.volume.vmware.com Delete         WaitForFirstConsumer

# Check PVC provisioning status
oc get pvc -A | grep -v Bound

# Test PVC creation
oc apply -f - <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
  namespace: default
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 1Gi
EOF
oc get pvc test-pvc
```


```text title="Expected output"
NAME             PROVISIONER                    RECLAIMPOLICY   VOLUMEBINDINGMODE
thin-csi (default) csi.vsphere.volume.vmware.com Delete         WaitForFirstConsumer
fast-ssd         csi.vsphere.volume.vmware.com Delete         Immediate

NAME                    STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pending-app-pvc         Pending                                      thin-csi        45m
test-pvc                Pending                                      thin-csi        2m

persistentvolumeclaim/test-pvc created
NAME       STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
test-pvc   Pending                                      thin-csi        3s
```

!!! warning "Common errors"
    **`error: unable to recognize "STDIN": no kind "PersistentVolumeClaim" in version "v1"`** — Verify the API group is correct and the cluster supports the v1 API version for PVCs.
    **`Error from server (Forbidden): persistentvolumeclaims is forbidden: User "system:serviceaccount:default:deployer" cannot create resource "persistentvolumeclaims"`** — Grant the service account or user the `create` verb on `persistentvolumeclaims` via a ClusterRole or Role binding.
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

# List MachineSets and replica counts
oc get machineset -n openshift-machine-api

# Check machine provisioning status
oc get machine -n openshift-machine-api

# Add ClusterAutoscaler + MachineAutoscaler
oc apply -f clusterautoscaler.yaml        # Global autoscaler config
oc apply -f machineautoscaler.yaml        # References MachineSet + min/max replicas
```


```text title="Expected output"
machineset.machine.openshift.io/cluster-worker-0 scaled
NAME                    DESIRED   CURRENT   READY   UPDATED   AVAILABLE   AGE
cluster-worker-0        5         5         3       5         3           42d
cluster-worker-1        3         3         3       3         3           42d
cluster-worker-2        3         3         3       3         3           42d

NAME                                    PHASE         TYPE   REGION      IMAGE                                    CREATED AT
cluster-abc123-worker-0-abc12           Provisioning  m5.xl  us-east-1a  ami-0c55b159cbfafe1f0  2024-01-15T09:22:15Z
cluster-abc123-worker-0-def45           Running       m5.xl  us-east-1a  ami-0c55b159cbfafe1f0  2024-01-15T09:18:42Z
cluster-abc123-worker-0-ghi78           Running       m5.xl  us-east-1a  ami-0c55b159cbfafe1f0  2024-01-15T09:15:08Z
cluster-abc123-worker-1-jkl90           Running       m5.xl  us-east-1b  ami-0c55b159cbfafe1f0  2024-01-14T14:33:21Z
cluster-abc123-worker-1-mno12           Running       m5.xl  us-east-1b  ami-0c55b159cbfafe1f0  2024-01-14T14:30:55Z
...

clusterautoscaler.autoscaling.openshift.io/default created
machineautoscaler.autoscaling.openshift.io/worker-autoscaler created
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "machineset"`** — Verify the machine-api-operator is running with `oc get pods -n openshift-machine-api` and check your cluster version supports MachineSets.
    **`Error from server (NotFound): machinesets.machine.openshift.io "cluster-worker-0" not found`** — Confirm the exact MachineSet name with `oc get machineset -n openshift-machine-api` and use the correct namespace.
    **`error: error validating "machineautoscaler.yaml": error validating data: ValidationError(MachineAutoscaler): unknown field "replicaCount"`** — Use correct field names `minReplicas` and `maxReplicas` in the MachineAutoscaler spec, not `replicaCount`.
## See also

- [OpenShift — How It Works](../how-it-works/)
- [OpenShift — Deploy](../../deploy/)
