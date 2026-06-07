# OpenShift — How It Works

<div class="kb-summary">
Control plane components, etcd quorum, API server request flow, scheduler decisions, and how the operator pattern manages cluster resources.
</div>

```text
┌────────────────────────────── OpenShift — Control Plane & Request Flow ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   All cluster changes go through kube-apiserver → etcd; controllers reconcile desired state   │   │
│   │   Operators extend this loop: watch CRDs, reconcile managed resources, report Conditions       │  │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    kubectl/oc → kube-apiserver → etcd (persist) → controllers (reconcile) → kubelet (execute)         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      kube-apiserver         │  │           etcd              │  │       Scheduler             │   │
│   │      ─────────────          │  │      ─────────────          │  │      ─────────────          │   │
│   │  REST gateway for all ops   │  │  Distributed KV store       │  │  Assigns pods to nodes      │   │
│   │  AuthN + AuthZ (RBAC)       │  │  Raft consensus (3 or 5)    │  │  Taints, tolerations        │   │
│   │  Admission webhooks         │  │  TLS mutual auth            │  │  Resource requests/limits   │   │
│   │  Resource validation        │  │  Snapshot + compaction      │  │  Affinity / anti-affinity   │   │
│   │  Watch/notify subscribers   │  │  Full cluster state here    │  │  Pod priority classes       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    etcd         = Key-value store holding ALL cluster state; losing quorum = cluster non-functional   │
│    Raft         = Consensus algorithm; requires majority (2/3 or 3/5) for writes; odd node count      │
│    Operator     = Kubernetes controller that manages a specific application via CRD watch-reconcile   │
│    CRO          = Cluster-scoped resource; ClusterOperator tracks built-in component health           │
│    MachineConfig= OS-level config (files, units, kernel args) applied by MCO to RHCOS nodes           │
│    OVN-Kubernetes= Default CNI in OCP 4.x; SDN deprecated; uses OVN/OVS for pod networking            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Control Plane Components

| Component | Role | Notes |
|---|---|---|
| `kube-apiserver` | REST gateway; all operations go through it | Front-end for etcd; validates, persists |
| `etcd` | Distributed KV store; cluster state | 3-node Raft quorum; must have majority |
| `kube-scheduler` | Assigns pods to nodes | Considers resources, taints, affinity |
| `kube-controller-manager` | Runs built-in controllers (Deployment, Node, etc.) | Reconciliation loop per resource type |
| `openshift-apiserver` | Extends kube-apiserver for OCP-specific resources | Routes, BuildConfigs, DeploymentConfigs |
| `cluster-version-operator` | Manages OCP version and cluster operator lifecycle | Drives upgrades, reports ClusterVersion |

## etcd Quorum Rules

```text
# etcd needs majority to accept writes
# 3-node cluster: need 2/3 alive
# 5-node cluster: need 3/5 alive (can lose 2)

# Never run 2 or 4 etcd members — split-brain risk
# Masters ARE the etcd nodes in standard OCP (co-located)
```

| Cluster size | Can tolerate failure of | Write quorum |
|---|---|---|
| 3 members | 1 member | 2 |
| 5 members | 2 members | 3 |

## Operator Pattern

Every OpenShift component is managed by a cluster operator. The pattern:

```text
1. CRD defines desired state (spec)
2. Operator watches CRD instances
3. Operator reconciles actual → desired
4. Operator reports status via Conditions
```

```bash
# Check cluster operator health
oc get clusteroperators
oc get co                          # short form

# Example output
NAME                    VERSION   AVAILABLE   PROGRESSING   DEGRADED
authentication          4.14.5    True        False         False
dns                     4.14.5    True        False         False
etcd                    4.14.5    True        False         False
kube-apiserver          4.14.5    True        False         False

# Any DEGRADED=True is a problem
oc describe co <operator-name>     # Conditions, message, and events
```

## Node Types

| Type | Role | Typical labels |
|---|---|---|
| Master | Control plane (etcd + API + scheduler) | `node-role.kubernetes.io/master` |
| Worker | General compute | `node-role.kubernetes.io/worker` |
| Infra | Monitoring, router, registry | `node-role.kubernetes.io/infra` |
| Storage | ODF/Ceph OSDs | `cluster.ocs.openshift.io/openshift-storage` |

```bash
# View node roles
oc get nodes -o wide
oc get nodes --show-labels | grep node-role

# Move infra workloads off worker nodes
oc label node <infra-node> node-role.kubernetes.io/infra=""
oc adm taint node <infra-node> node-role.kubernetes.io/infra=reserved:NoSchedule
```

## Networking (OVN-Kubernetes)

```text
Pod traffic flow:
  Pod → OVS (host) → OVN Logical Switch → OVN Router → external
  East-west: OVN handles pod-to-pod routing on the logical network
  North-south: via OpenShift Router (HAProxy) or LoadBalancer service
```

```bash
# Check network operator
oc get network.operator cluster -o yaml | grep -E "type:|clusterNetwork"

# Inspect OVN-K components
oc get pods -n openshift-ovn-kubernetes
oc get pods -n openshift-multus
```
