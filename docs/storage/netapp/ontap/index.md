---
tags:
  - netapp
---
# NetApp ONTAP

<div class="kb-summary">
NetApp ONTAP knowledge base — architecture, operations, security, and troubleshooting for AFF, FAS, and ONTAP Select platforms.
</div>
```text
┌──────────────────────────────────────────── NetApp ONTAP ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          ONTAP: enterprise unified storage operating system for NAS, SAN, and object          │   │
│   │                    Protocols: NFS v3/v4.1 · SMB · iSCSI · FC · NVMe-oF · S3                   │   │
│   │                          Management: ONTAP System Manager / ONTAP CLI                         │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Cluster           │  │        HA node pairs        │  │          Scale-out          │   │
│   │             SVM             │  │        Virtual server       │  │       Protocol access       │   │
│   │          Aggregate          │  │         RAID groups         │  │         Storage pool        │   │
│   │           FlexVol           │  │         Thin volume         │  │        Data container       │   │
│   │          SnapMirror         │  │         Replication         │  │          Async/Sync         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       SVM        │ Tenant isolation │   All protocols   │  Kerberos/NTLM   │  Virtual server  │   │
│   │    SnapMirror    │  DR replication  │    SM protocol    │   Certificate    │  Async or sync   │   │
│   │    FlexClone     │  Instant clone   │      Internal     │    Admin role    │ Space-efficient  │   │
│   │      SM-BC       │ Zero-RPO active- │    SM protocol    │     Mediator     │     SAN only     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: AFF/FAS HA node pairs · cluster network · client access network · MetroCluster           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ONTAP              = NetApp storage OS; unified NAS, SAN, and object across AFF, FAS, ONTAP Select │
│    SVM                = Storage Virtual Machine; logical storage server with protocols, IP, and vol...│
│    Aggregate          = RAID group of disks; underpins FlexVols and FlexGroups within a node          │
│    FlexVol            = flexible thin-provisioned volume within an aggregate; most common container   │
│    FlexGroup          = scale-out volume spanning multiple aggregates; for very large NAS workloads   │
│    SnapMirror         = async or synchronous replication between ONTAP systems for DR and backup      │
│    SnapVault          = backup-oriented SnapMirror variant; independent retention at destination      │
│    FlexClone          = instant space-efficient writable clone of a volume or LUN from snapshot       │
│    Snapshot           = ONTAP space-efficient PiT copy; stored in .snapshot directory on NFS          │
│    ONTAP Mediator     = third-site quorum for SnapMirror SM-BC; prevents split-brain scenarios        │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN repl...│
│    vserver            = ONTAP CLI name for SVM; vserver show and vserver nfs show are common commands │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Health checks, procedures, CLI reference, scripts, and lifecycle.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Security configuration, hardening, and access control.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic steps, and escalation paths.</span></a>
</div>
