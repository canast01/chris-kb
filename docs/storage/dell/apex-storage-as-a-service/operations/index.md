---
tags:
  - dell
  - operations
---
# APEX Storage as a Service — Operations

<div class="kb-summary">
APEX Storage as a Service — Operations reference: CLI Reference, Health Checks, Procedures, Install & Upgrade, and 2 more.
</div>

```text
┌──────────────────────────────────── Dell Apex STaaS — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Apex day-2 operations: volume provisioning, capacity management, snapshots, alerts      │   │
│   │         Provisioning: Apex Console or REST API; create volumes, exports, map to hosts         │   │
│   │       Capacity: monitor committed vs used in CloudIQ; raise SR to expand committed tier       │   │
│   │           Snapshots: schedule via Apex Console; crash-consistent; clone for dev/test          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Provision → map to host → monitor CloudIQ → snapshot → capacity review → expand                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Provisioning        │  │          Monitoring         │  │        Data Services        │   │
│   │        Create volume        │  │        CloudIQ health       │  │       Snapshot sched.       │   │
│   │         Map to host         │  │        Capacity usage       │  │         Clone volume        │   │
│   │       Create NFS exp.       │  │        Performance IO       │  │         Replication         │   │
│   │        Expand volume        │  │         Alert review        │  │         Thin reclaim        │   │
│   │         Delete/unmap        │  │        Billing report       │  │         Compression         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All hardware ops (firmware, replacement) are Dell responsibility; open SR via Apex Console         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │   Apex Console   │     Key field     │      Verify      │      Notes       │   │
│   │    Create vol    │ Storage>Volumes  │     Size/tier     │  Host sees vol   │    Thin prov.    │   │
│   │     Map host     │  Storage>Hosts   │      IQN/WWN      │     Host LUN     │   Multipath on   │   │
│   │     Snapshot     │  Data Svc>Snap   │      Schedule     │    Snap count    │  Retention set   │   │
│   │   Capacity SR    │    Support>SR    │   Current/target  │    SR created    │  Dell responds   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: array controllers · host HBA/NIC · multipath driver on each host                         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Thin provisioning = Volume allocated to host at requested size; storage used only on write         │
│    Host mapping     = Associate host IQN (iSCSI) or WWN (FC) to a volume or export                    │
│    NFS export       = File storage share; mount on Linux/VMware via NFS protocol                      │
│    Snapshot sched.  = Automated recurring snapshot policy; retain N snapshots                         │
│    Clone            = Writable copy of a volume or snapshot; used for dev/test                        │
│    Thin reclaim     = Return unused thin-provisioned blocks to pool (UNMAP/TRIM)                      │
│    CloudIQ health   = AI-driven health score; monitors controller, drives, fans, thermals             │
│    Performance IO   = IOPS and throughput graphs per volume in CloudIQ                                │
│    Billing report   = Apex Console monthly view of committed + burst usage by tier                    │
│    SR (Service Req) = Support request to Dell; used for hardware issues and capacity expands          │
│    Compression      = Inline data compression reducing physical footprint on array                    │
│    Replication      = Async or sync copy of volumes to secondary Apex or PowerStore                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
</div>
