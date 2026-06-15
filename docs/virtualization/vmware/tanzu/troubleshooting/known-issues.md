---
tags:
  - troubleshooting
  - tanzu
  - vmware
  - known-issues
---
# VMware Tanzu — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Tanzu Kubernetes Grid (TKG) and Supervisor cluster bugs, error codes, and workarounds.

*Applies to: Tanzu Kubernetes Grid 2.x / vSphere 7.x–8.x with Tanzu*
</div>

```text
┌───────────────────────────────────── Virtualization Vmware Tanzu ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Vmware: Virtualization Vmware Tanzu platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Virtualization Vmware Tanzu management console                  │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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


## Before you begin

- Supervisor control plane logs: `kubectl logs -n vmware-system-tkg <pod>` from the Supervisor context.
- TKG guest cluster logs: switch to workload cluster context and inspect `kube-apiserver` pods.
- Most Tanzu issues relate to NSX networking, storage policy assignment, or Content Library sync.

## Supervisor Cluster

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Supervisor API server unreachable on port 6443 | TKG 2.x | NSX load balancer VIP not allocated or NSX edge unreachable | Check NSX load balancer pool for Supervisor API VIP; verify NSX Edge connectivity | N/A |
| `Namespace quota exceeded` when creating TKG cluster | TKG 2.x | vSphere Namespace resource quota too restrictive | Increase vCPU/memory quota on vSphere Namespace in vSphere Client | N/A |
| Supervisor control plane node CrashLoopBackOff | TKG 2.x | etcd volume full (default thin-provision fills up) | Expand etcd PV on vSAN datastore; or clean up etcd compaction backlog | N/A |

## TKG Workload Clusters

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `TanzuKubernetesCluster stuck in Deleting` | TKG 2.x | Finalizer not removed due to CSI PV cleanup timeout | Manually remove finalizers: `kubectl edit tkc <name>` → remove `deletionFinalizers` | N/A |
| Worker nodes `NotReady` after cluster creation | TKG 2.x | CNI (Antrea) not initialized; Geneve UDP 6081 blocked | Verify UDP 6081 open between all worker nodes and Supervisor | N/A |
| Image pull fails: `Content Library item not found` | TKG 2.x | TKG OVA not subscribed in Content Library | Subscribe Content Library to VMware TKG OVA catalog; sync | N/A |

## Storage

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| PVC stuck in `Pending` — `no storageclass found` | TKG 2.x | Default StorageClass not set on TKG cluster | Annotate storage class as default: `kubectl annotate sc <name> storageclass.kubernetes.io/is-default-class=true` | N/A |
| vSAN CSI driver not binding PVC | TKG 2.x | Storage policy assigned to Namespace doesn't match cluster host's vSAN policy | Verify vSAN storage policy assigned to Namespace exists on all hosts in cluster | N/A |

## See also

- [VMware Tanzu — Common Issues](common-issues.md)
- [VMware NSX — Known Issues](../../nsx/troubleshooting/known-issues/)
- [VMware vCenter — Known Issues](../../vcenter/troubleshooting/known-issues/)
