# APEX Storage as a Service — Integrations

```text
┌─────────────────────────────────── Dell Apex STaaS — Integrations ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Apex integrations: VMware (vVols/VMFS), Kubernetes CSI, data protection, REST API       │   │
│   │          VMware: VASA provider for vVols; VMFS datastore via iSCSI or FC; SRM support         │   │
│   │          Kubernetes: Dell CSI driver; dynamic persistent volume provisioning for pods         │   │
│   │         Data protection: PowerProtect DD target, Avamar, or third-party via NFS/iSCSI         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    vCenter VASA → vVols per-VM policy · CSI driver → PVC provisioning · DD target → backup            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            VMware           │  │          Kubernetes         │  │       Data Protection       │   │
│   │         vVols / VASA        │  │       Dell CSI driver       │  │       PowerProtect DD       │   │
│   │        VMFS datastore       │  │         PVC dynamic         │  │         Avamar NDMP         │   │
│   │          SRM for DR         │  │         StorageClass        │  │          NetWorker          │   │
│   │         SPBM policy         │  │         Snapshot CSI        │  │        Cloud DR copy        │   │
│   │        vCenter plugin       │  │         Helm charts         │  │           REST API          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    VASA provider and CSI driver installed once; all subsequent provisioning is self-service           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Integration    │     Protocol     │    Key feature    │    Provision     │      Notes       │   │
│   │   VMware vVols   │     VASA 3.0     │   Per-VM policy   │    vCenter UI    │   SPBM driven    │   │
│   │    Kubernetes    │     CSI 1.x      │    Dynamic PVC    │   StorageClass   │  Dell CSI helm   │   │
│   │  PowerProt. DD   │   NFS/DD Boost   │    Dedup target   │   PPDM policy    │  DD Boost req.   │   │
│   │     REST API     │    HTTPS/JSON    │     Automation    │   Scripts/IaC    │   Apex portal    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: VASA provider VM on vCenter · CSI controller pod in K8s · DD appliance on-prem           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    vVols          = Virtual Volumes; per-VM storage objects; managed by VASA provider                 │
│    VASA           = vSphere APIs for Storage Awareness; enables per-VM storage policies               │
│    SPBM           = Storage Policy Based Management; assigns storage policy to each VM                │
│    VMFS           = vSphere File System; block-based datastore for VMware workloads                   │
│    SRM            = Site Recovery Manager; VMware DR orchestration using storage replication          │
│    CSI driver     = Container Storage Interface; Dell CSI plugin provisions K8s PVCs                  │
│    StorageClass   = Kubernetes resource defining storage tier and parameters for PVCs                 │
│    PVC            = PersistentVolumeClaim; K8s request for storage; CSI provisions it                 │
│    DD Boost       = Dell Data Domain protocol; deduplicated backup streams to DD target               │
│    PPDM           = PowerProtect Data Manager; Dell backup orchestration for DD targets               │
│    NDMP           = Network Data Management Protocol; Avamar backup of NAS file systems               │
│    Helm chart     = Kubernetes package manager chart; deploys Dell CSI driver components              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [APEX Storage as a Service](../../index.md) reference.

---

| Integration | Notes |
|---|---|
| APEX Console | Primary management interface for subscriptions, billing, capacity requests, and support cases |
| APEX REST API | `https://api.dell.com` — programmatic access to systems, subscriptions, capacity, and metrics |
| CloudIQ | Health scoring and alerting for APEX systems; APEX systems appear in CloudIQ by underlying hardware model |
| Secure Connect Gateway (SCG) | Telemetry pipeline from on-premises hardware to CloudIQ and Dell support |
| Dell field service | Hardware replacement and capacity additions are Dell-managed via APEX Console service requests |

## Notes on APEX Management Boundaries

| Task | Interface |
|---|---|
| Order / provision new APEX system | APEX Console (console.dell.com) |
| Resize contracted capacity | APEX Console → Subscription → Modify |
| Create / delete volumes | APEX Console or APEX Block API |
| Monitor health and alerts | CloudIQ (console.dell.com/cloudiq) |
| View billing / consumption | APEX Console → Billing or Subscription API |
| Performance metrics | APEX Block API or CloudIQ API |
| Firmware upgrades | Dell-managed (SaaS — no customer action required) |
| Hardware replacement | Dell field service — no customer CLI |
