# SnapMirror — Integrations


<div class="kb-summary">
> Part of the [SnapMirror Architecture](../index.md) reference.
</div>

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
