---
tags:
  - architecture
  - netapp
---
# SnapMirror — Integrations


<div class="kb-summary">
Part of the [SnapMirror Architecture](../index.md) reference.
</div>
```text
┌────────────────────────────────── NetApp SnapMirror — Integrations ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    SnapMirror integrations: VMware vSphere, Kubernetes CSI, backup software, and monitoring   │   │
│   │     Protocols: SnapMirror protocol (encrypted) · NFS/SMB/iSCSI at destination after break     │   │
│   │ API: ONTAP System Manager / SnapMirror CLI REST API enables automation and third-party tool i │   │
│   │             Plug-ins available for vCenter, OpenShift, Splunk, and SIEM platforms             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SnapMirror → REST API / plug-ins → VMware / K8s / backup / monitoring                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Async            │  │        Periodic sync        │  │         RPO: minutes        │   │
│   │             Sync            │  │           Zero RPO          │  │          Sub-ms lag         │   │
│   │            SM-BC            │  │        Active-active        │  │        Transparent FO       │   │
│   │            Vault            │  │        Long retention       │  │         Backup copy         │   │
│   │            Cloud            │  │         ONTAP → CVO         │  │       Cloud DR/backup       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │ Async SnapMirror │  DR replication  │    SM protocol    │   Certificate    │   RPO minutes    │   │
│   │ Sync SnapMirror  │  Zero-RPO sync   │    SM protocol    │   Certificate    │ StrictSync/Sync  │   │
│   │      SM-BC       │ Active-active SA │    SM protocol    │     Mediator     │    No RPO/RTO    │   │
│   │    SnapVault     │ Backup retention │    SM protocol    │   Certificate    │ Longer retentio  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Source ONTAP cluster · destination ONTAP cluster · intercluster LIFs · WAN link          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapMirror         = ONTAP replication; transfers only changed blocks after initial baseline sync  │
│    Intercluster LIF   = dedicated logical interface for SnapMirror traffic between clusters           │
│    SnapMirror policy  = defines schedule, retention, and transfer type (async/sync/vault)             │
│    Baseline transfer  = first full snapshot transfer establishing the SnapMirror relationship         │
│    Update             = incremental transfer; only sends new or changed blocks since last successfu...│
│    Snapmirror break   = breaks the DR relationship; activates destination volume for read-write       │
│    Resync             = re-establishes a broken SnapMirror relationship from the last common snapshot │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN volumes│
│    Mediator           = ONTAP Mediator; quorum service for SM-BC running on Linux VM at third site    │
│    SnapVault          = SnapMirror variant for backup retention; destination has independent schedule │
│    MirrorAndVault     = policy combining SnapMirror DR and SnapVault backup retention copies          │
│    Fanout             = single source volume replicating to multiple destination clusters simultane...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## SnapCenter Orchestration

SnapCenter uses SnapMirror to replicate application-consistent snapshots to a DR site. SnapCenter manages the full workflow: application quiesce, snapshot creation, SnapMirror update, and snapshot catalog registration. For DR failover, SnapCenter orchestrates `snapmirror break` on the destination, mounts the destination volume, and presents it to hosts — enabling application-consistent failover without manual intervention. SnapCenter also manages the resync and failback sequence post-recovery.

## SVM-DR for NAS Failover

SVM-DR replicates an entire data SVM — including all volumes, LIF configuration, NFS exports, CIFS shares, and local users — to a destination SVM. This enables complete NAS server failover where the destination SVM can be activated with the same share paths and permissions. SVM-DR is preferred over volume-level relationships where full NAS server recoverability is required, not just data. Superna Eyeglass can automate SVM-DR failover workflows for environments requiring automated NAS DR.

## SMBC for Transparent Host Failover

SnapMirror Business Continuity (SMBC) uses ONTAP consistency groups to replicate groups of volumes synchronously. Hosts access the LUNs via the same LUN path on both sites — both storage nodes present the same LUN identity. In the event of a source cluster failure, the ONTAP Mediator signals the destination cluster to begin serving I/O automatically, with no host-side path changes or reconfiguration required. SMBC is designed for SAN workloads (iSCSI, FC) where continuous availability is mandatory.

## Cloud Volumes ONTAP

SnapMirror replication operates natively between on-premises ONTAP clusters and Cloud Volumes ONTAP (CVO) instances in AWS, Azure, or GCP. This supports cloud-based DR scenarios where the destination is a CVO instance rather than a physical cluster. BlueXP manages the cloud replication relationship setup. SnapMirror policies and schedules function identically regardless of whether the destination is on-premises or cloud-hosted.

## REST API

ONTAP provides a REST API for programmatic SnapMirror relationship management. Use for automation, monitoring dashboards, and ITSM integration.

```bash
# List all SnapMirror relationships
GET /api/snapmirror/relationships

# Create a new SnapMirror relationship
POST /api/snapmirror/relationships

# Trigger an update on a specific relationship
PATCH /api/snapmirror/relationships/{uuid}

# Get transfer history
GET /api/snapmirror/relationships/{uuid}/transfers
```

Authenticate with HTTP Basic or cluster-scoped API tokens. Use the ONTAP REST API documentation at `https://<cluster-mgmt>/docs/api` for interactive exploration.
