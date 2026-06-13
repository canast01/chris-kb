---
tags:
  - netapp
  - operations
---
# SnapCenter — Install & Upgrade


<div class="kb-summary">
Part of the [SnapCenter Operations](../index.md) reference.
</div>
```text
┌─────────────────────────────── NetApp SnapCenter — Install and Upgrade ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SnapCenter installation and upgrade: deployment and version management procedures       │   │
│   │         Pre-upgrade: back up configuration, check compatibility, review release notes         │   │
│   │      Upgrade: rolling upgrade preserves service; non-disruptive on dual-controller arrays     │   │
│   │           Post-upgrade: verify all services running; run health check; notify users           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Plan → backup config → upgrade staging → upgrade production → validate                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │          Windows VM         │  │       Central control       │   │
│   │           Plug-in           │  │          Host agent         │  │        App-consistent       │   │
│   │            Policy           │  │       Schedule/retain       │  │         Backup rule         │   │
│   │        Resource group       │  │       Grouped targets       │  │        Shared policy        │   │
│   │           Recovery          │  │       Volume/LUN/file       │  │       Granular restore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   SQL plug-in    │  MSSQL backups   │       HTTPS       │   Windows auth   │  App-consistent  │   │
│   │  Oracle plug-in  │  Oracle backups  │       HTTPS       │       SSH        │ RMAN integratio  │   │
│   │  VMware plug-in  │  VM/VMDK backup  │   HTTPS/vCenter   │   vCenter SSO    │   vSphere API    │   │
│   │ SAP HANA plug-in │   HANA backups   │       HTTPS       │     SAP auth     │   Backint API    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapCenter         = NetApp backup orchestration; coordinates app-consistent snapshots via plug-ins│
│    Plug-in            = host-side agent; quiesces application before snapshot: SQL, Oracle, VMware    │
│    Resource group     = set of resources sharing a backup policy and schedule in SnapCenter           │
│    Policy             = SnapCenter object defining snapshot frequency, retention, and replication t...│
│    App-consistent     = snapshot taken after DB quiesce; guarantees crash-consistent recovery         │
│    Clone lifecycle    = SnapCenter clone: create from snapshot, provision to host, then delete        │
│    FlexClone          = underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone      │
│    Vault policy       = SnapCenter policy that also replicates snapshots to SnapVault destination     │
│    Mirror policy      = SnapCenter policy that replicates snapshots via SnapMirror to DR cluster      │
│    RBAC               = SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles  │
│    SMF                = SnapCenter MySQL database storing job history, policies, and resource configs │
│    SnapCenter API     = REST API on port 8143; full feature coverage for automation workflows         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## SnapCenter Version Matrix

| SnapCenter Version | Release Date | Supported ONTAP Versions | End of Support |
|---|---|---|---|
| SnapCenter 4.7 | Oct 2021 | ONTAP 9.7–9.10 | Oct 2023 |
| SnapCenter 4.8 | Apr 2022 | ONTAP 9.7–9.11 | Apr 2024 |
| SnapCenter 4.9 | Sep 2022 | ONTAP 9.7–9.12 | Sep 2024 |
| SnapCenter 5.0 | Mar 2023 | ONTAP 9.8–9.13 | Mar 2025 |
| SnapCenter 6.0 | Oct 2023 | ONTAP 9.10–9.14 | Oct 2025 |
| SnapCenter 6.1 | Jun 2024 | ONTAP 9.11–9.15 | Jun 2026 |

Always verify the exact compatibility matrix in the [NetApp Interoperability Matrix Tool (IMT)](https://imt.netapp.com/matrix/imt.html) before upgrading. SnapCenter also has separate compatibility tables for each application plugin (Oracle, SQL Server, Exchange, SAP HANA, VMware).

## ONTAP Compatibility

- SnapCenter requires ONTAP 9.x; exact minimum version depends on features used (SnapMirror Business Continuity, vVols, etc.)
- SnapCenter 6.x requires ONTAP 9.10.1 or later for all features; some features (SnapMirror active sync, REST-only operations) require 9.12+
- The SnapCenter Plug-in for VMware vSphere follows its own version matrix and must be compatible with both the SnapCenter Server version and the vSphere version

## Upgrade Paths

SnapCenter supports in-place upgrades. Upgrade path:

1. Back up the MySQL repository: `C:\Program Files\NetApp\SnapCenter\MySQL Data\`
2. Record all resource groups, policies, schedules, and RBAC configurations (export from GUI or API)
3. Download the new SnapCenter Server installer from [mysupport.netapp.com](https://support.netapp.com)
4. Run the installer on the SnapCenter Server — it performs an in-place upgrade
5. After server upgrade, update all plugin packages via Settings → Hosts → select all → Update Plug-in
6. Update SnapCenter Plug-in for VMware OVA if deployed (download new OVA, deploy, deregister old OVA, register new OVA with vCenter)
7. Verify all resource groups, schedules, and job history are intact
8. Run a manual backup job on a representative resource group to confirm end-to-end functionality

**Never skip minor versions** — upgrade from 5.0 → 6.0 → 6.1, not 5.0 → 6.1 directly, unless the upgrade guide explicitly supports it.

## EOL Tracking

- SnapCenter follows roughly a 6-month release cadence
- End-of-support typically 2 years from release date
- Plan upgrades before end-of-support to ensure access to bug fixes and security patches
- Application plugin EOL is tied to the SnapCenter Server version — upgrading the server implicitly requires plugin upgrades

## Refresh Planning

| Trigger | Action |
|---|---|
| SnapCenter version approaching end-of-support | Plan upgrade within 3 months of EOL date |
| ONTAP upgraded beyond SnapCenter supported range | Upgrade SnapCenter before or concurrently with ONTAP upgrade |
| Windows Server OS reaching EOL | Migrate SnapCenter Server to new Windows Server VM |
| vSphere version upgrade | Verify SnapCenter Plug-in for VMware compatibility; upgrade OVA if needed |
| Application plugin (Oracle/SQL) version change | Verify IMT for plugin-to-SnapCenter-Server compatibility |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
