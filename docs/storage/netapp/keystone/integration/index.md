# NetApp Keystone Integration


<div class="kb-summary">
NetApp Keystone Integration reference covering ActiveIQ Digital Advisor, Keystone Collector, REST API, ITSM Integration, CloudOps Integration.
</div>

```text
┌──────────────────────────────────── NetApp Keystone — Integration ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Integrations: VMware (VAAI/VASA), Kubernetes (Trident), AWS/Azure blending          │   │
│   │           VAAI: hardware offload for clone, zero, lock operations from ESXi to ONTAP          │   │
│   │           VASA: Storage Policy-Based Management; maps service levels to VM policies           │   │
│   │             Trident: CSI driver for Kubernetes; dynamic PVC provisioning on ONTAP             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    App -> vSphere/K8s -> VAAI/VASA/Trident -> ONTAP SVM -> aggregate -> physical                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            VMware           │  │          Kubernetes         │  │            Cloud            │   │
│   │         VAAI NAS/SAN        │  │         Trident CSI         │  │        Cloud Volumes        │   │
│   │        VASA provider        │  │         StorageClass        │  │        BlueXP hybrid        │   │
│   │        SPBM policies        │  │         PVC dynamic         │  │        SnapMirror S3        │   │
│   │       VVOL datastores       │  │         NFS/iSCSI PV        │  │         Backup cloud        │   │
│   │        vCenter plugin       │  │        Astra Control        │  │          Cloud Sync         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Trident needs ONTAP SVM admin credentials; deploys as DaemonSet in k8s cluster                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Integration    │    Mechanism     │      Protocol     │       Auth       │      Notes       │   │
│   │       VAAI       │ ESXi HW offload  │      NFS/SCSI     │       n/a        │  Vendor plugin   │   │
│   │       VASA       │  Storage policy  │       HTTPS       │     SSL cert     │  vVols capable   │   │
│   │     Trident      │    CSI driver    │      REST API     │    SVM creds     │   K8s operator   │   │
│   │      BlueXP      │   Hybrid cloud   │       HTTPS       │      OAuth2      │    Cloud mgmt    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ESXi hosts connect to ONTAP data LIFs via NFS VLAN or FC fabric                          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VAAI          = vStorage APIs for Array Integration; offloads clone/lock to array                  │
│    VASA          = vSphere APIs for Storage Awareness; storage capability profiles                    │
│    SPBM          = Storage Policy-Based Management; VM tier via vCenter policy                        │
│    vVol          = Virtual Volume; per-VM ONTAP object; VM-level QoS and snapshot                     │
│    Trident       = NetApp CSI driver; creates NFS/iSCSI PVs from ONTAP                                │
│    StorageClass  = Kubernetes resource; maps to Trident backend (SVM + protocol)                      │
│    PVC           = PersistentVolumeClaim; K8s request for storage; Trident fulfils                    │
│    Astra Control = NetApp app-aware backup/DR for Kubernetes workloads                                │
│    Cloud Volumes = ONTAP as managed service on AWS/Azure/GCP (CVO/CVS)                                │
│    BlueXP        = Unified NetApp cloud manager; controls on-prem and cloud ONTAP                     │
│    SnapMirror S3 = Replication to/from S3-compatible targets for data mobility                        │
│    Cloud Sync    = NetApp SaaS data migration/sync; NFS, SMB, S3, HDFS                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Authenticate via ActiveIQ API tokens generated in the BlueXP portal. Tokens are scoped to the customer account and expire on a configurable schedule.

## ITSM Integration

Integrate Keystone consumption data with ServiceNow CMDB or similar ITSM platforms for:

- Asset and capacity records that reflect actual Keystone-managed hardware
- Monthly consumption report import for chargeback automation
- Alert generation from BlueXP webhooks to trigger ServiceNow incidents on capacity threshold breaches

Use the Keystone REST API to pull monthly consumption reports and push them to ServiceNow via its REST API or integration hub.

## CloudOps Integration

For hybrid cloud strategies, Keystone Flex extends the subscription model to Cloud Volumes ONTAP (CVO) instances in AWS, Azure, or GCP. A unified Keystone subscription can cover both on-premises Keystone STaaS and cloud CVO capacity under the same committed/burst billing model, with a single BlueXP dashboard view of total consumption across on-premises and cloud.
