---
tags:
  - troubleshooting
  - netapp
  - ontap
  - known-issues
---
# NetApp ONTAP — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known ONTAP bugs, error codes, and workarounds covering NFS, SMB, SnapMirror, iSCSI, and cluster health.

*Applies to: ONTAP 9.12–9.15*
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
│    ONTAP              = NetApp storage OS; unified NAS, SAN, and object across AFF, FAS, ONTAP Selec  │
│    SVM                = Storage Virtual Machine; logical storage server with protocols, IP, and volu  │
│    Aggregate          = RAID group of disks; underpins FlexVols and FlexGroups within a node          │
│    FlexVol            = flexible thin-provisioned volume within an aggregate; most common container   │
│    FlexGroup          = scale-out volume spanning multiple aggregates; for very large NAS workloads   │
│    SnapMirror         = async or synchronous replication between ONTAP systems for DR and backup      │
│    SnapVault          = backup-oriented SnapMirror variant; independent retention at destination      │
│    FlexClone          = instant space-efficient writable clone of a volume or LUN from snapshot       │
│    Snapshot           = ONTAP space-efficient PiT copy; stored in .snapshot directory on NFS          │
│    ONTAP Mediator     = third-site quorum for SnapMirror SM-BC; prevents split-brain scenarios        │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN repli  │
│    vserver            = ONTAP CLI name for SVM; vserver show and vserver nfs show are common command  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Run `system health alert show` on the cluster for active alerts.
- EMS logs: `event log show -severity ERROR` — first point of diagnosis for all issues.
- AutoSupport uploads collect all diagnostic data: `system node autosupport invoke -node * -type all`.

## NFS

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| NFS client shows `Stale file handle` after SVM failover | ONTAP 9.x | Client cached old data LIF IP; NFS mount bound to specific LIF | Configure NFS clients to use DNS name (round-robin across LIFs) rather than IP | N/A |
| `NFSERR_ACCES` on NFS export despite correct permissions | ONTAP 9.x | Export policy rule client match uses CIDR but client IP outside range | Verify export policy rule client match exactly matches client subnet | N/A |
| NFS v4.1 delegation recall causing high latency | ONTAP 9.12 | Delegation recall storm during high-metadata workload | Disable NFSv4.1 delegations for affected SVM if workload is high-metadata: `vserver nfs modify -delegation disabled` | 9.13 |

## SMB / CIFS

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Access denied` on SMB share after AD password reset for service account | ONTAP 9.x | CIFS server machine account in AD out of sync | Re-join CIFS SVM to AD domain: `vserver cifs modify -domain-workgroup` | N/A |
| DFS namespace broken after SVM DR failover | ONTAP 9.x | DFS referral points to old SVM data LIF | Update DFS namespace targets to new data LIF IP post-failover | N/A |

## SnapMirror / Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| SnapMirror relationship stuck `Idle` — lag increasing | ONTAP 9.x | Intercluster LIF blocked; TCP 11104/11105 not reachable | Verify ports 11104/11105 open between intercluster LIFs | N/A |
| SnapMirror update fails: `Source volume is busy` | ONTAP 9.x | Snapshot retention prevents new Snapshot during update | Delete oldest Snapshot manually; or increase max Snapshot count | N/A |

## iSCSI / SAN

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| iSCSI initiator loses path after LIF migration | ONTAP 9.x | Host iSCSI session bound to old LIF IP | Rescan initiator: `iscsiadm -m session --rescan`; enable ALUA on host | N/A |
| LUN offline after node takeover | ONTAP 9.x | LUN not mapped on partner node's LIF | Verify igroups include both home and partner LIFs (required for multi-path) | N/A |

## See also

- [NetApp ONTAP — Common Issues](common-issues/)
- [NetApp SnapMirror — Known Issues](../../snapmirror/troubleshooting/known-issues.md)
- [NetApp SnapCenter — Known Issues](../../snapcenter/troubleshooting/known-issues.md)
