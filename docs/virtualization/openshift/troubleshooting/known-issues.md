---
tags:
  - troubleshooting
  - openshift
  - kubernetes
  - known-issues
---
# Red Hat OpenShift — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known OpenShift bugs, error codes, and workarounds covering cluster operators, OVN-Kubernetes networking, image registry, and upgrade issues.

*Applies to: OpenShift Container Platform 4.12–4.16*
</div>

```text
┌────────────────────────────────────────── Red Hat OpenShift ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Enterprise Kubernetes platform — control plane, operators, and workloads           │   │
│   │              Protocols: HTTPS (API/UI) · etcd gRPC · CRI-O · CNI (OVN-Kubernetes)             │   │
│   │             Management: oc CLI · web console · GitOps (ArgoCD) · OLM operator mgmt            │   │
│   │               User -> API server -> etcd -> scheduler -> kubelet -> pod running               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │        Control plane        │  │          API + etcd         │  │       3 masters for HA      │   │
│   │           Compute           │  │         Worker nodes        │  │      CRI-O container rt     │   │
│   │          Networking         │  │        OVN-Kubernetes       │  │     SDN + network policy    │   │
│   │           Storage           │  │         CSI drivers         │  │     PVC -> StorageClass     │   │
│   │          Operators          │  │         OLM managed         │  │     Day-2 config via CRD    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    API server    │ Cluster endpoint │     HTTPS 6443    │   OIDC / cert    │All ops route here│   │
│   │       etcd       │   State store    │    gRPC 2379/80   │       mTLS       │3 members (quorum)│   │
│   │       OLM        │Operator lifecycle│      Internal     │       RBAC       │  Manages op CSV  │   │
│   │      oc CLI      │Cluster management│    HTTPS (API)    │    kubeconfig    │ Extends kubectl  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: bare-metal/VM masters (3) + worker nodes -> OVN overlay -> storage CSI                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  etcd         = distributed key-value store; single source of truth for cluster state                 │
│  OLM          = Operator Lifecycle Manager; installs and updates operators from catalog               │
│  CRI-O        = OpenShift container runtime; OCI-compliant, replaces Docker                           │
│  OVN-Kubernetes = default SDN (replaces OpenShift SDN); uses OVS + OVN                                │
│  MachineConfig = operator managing node-level OS and kubelet configuration                            │
│  CSV          = ClusterServiceVersion; operator metadata including permissions                        │
│  CRD          = Custom Resource Definition; extends Kubernetes API for operators                      │
│  PVC          = Persistent Volume Claim; requests storage from a StorageClass                         │
│  StorageClass = CSI driver config defining backend and provisioner                                    │
│  ImageStream  = OpenShift abstraction for tracking container image versions                           │
│  Route        = OpenShift ingress object exposing services externally                                 │
│  Node NotReady = kubelet lost contact with API server or CRI-O is unhealthy                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Check all cluster operator status: `oc get co` — any `Degraded=True` blocks upgrades.
- `oc adm must-gather` collects all diagnostic data for Red Hat support.
- Cluster upgrade fails are almost always due to a degraded operator or certificate issue.

## Cluster Operators

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `authentication` operator degraded after certificate rotation | OCP 4.12+ | OAuth server certificate not trusted after rotation | Re-approve CSRs: `oc get csr | grep Pending | oc certificate approve` | N/A |
| `kube-apiserver` operator degraded: `revision stuck` | OCP 4.12+ | API server rollout blocked by unhealthy etcd pod | Check etcd pod health: `oc get pods -n openshift-etcd`; restart failed etcd pod | N/A |
| `machine-config` operator degraded after node change | OCP 4.x | MachineConfig pool not rendered cleanly | Check MCO: `oc describe mcp worker`; look for config render errors | N/A |

## Networking (OVN-Kubernetes)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Pod-to-pod traffic fails across nodes | OCP 4.12+ | OVN-Kubernetes Geneve (UDP 6081) blocked between nodes | Verify UDP 6081 open on all node NICs and any intermediate firewalls | N/A |
| Service ClusterIP unreachable from pods | OCP 4.x | OVN flow tables out of sync | Restart `ovnkube-node` DaemonSet on affected node: `oc delete pod -n openshift-ovn-kubernetes -l app=ovnkube-node --field-selector=spec.nodeName=<node>` | N/A |

## Image Registry and Builds

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `image-registry` operator degraded — storage not available | OCP 4.x | No persistent storage configured for internal registry | Configure PVC or S3 storage for registry: `oc patch configs.imageregistry.operator.openshift.io/cluster --patch '{"spec":{"storage":{"pvc":{"claim":""}}}}' --type=merge` | N/A |
| Build fails: `ImagePullBackOff` from internal registry | OCP 4.x | Registry service cert not trusted by node | Approve pending node CSRs; verify cluster CA trust bundle | N/A |

## Upgrades

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Upgrade stuck at 10% — `machine-config` not applied | OCP 4.x | Worker node reboot loop during MCO config application | Check node: `oc debug node/<node>`; inspect `/var/log/messages` for boot failure | N/A |
| `oc adm upgrade` blocked: `Upgradeable=False` | OCP 4.x | Cluster operator reporting blocker condition | `oc get co`; investigate the Degraded operator; resolve before proceeding | N/A |

## See also

- [OpenShift — Common Issues](common-issues/)
