---
tags:
  - netapp
  - operations
---
# ONTAP — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering ONTAP Version Matrix, Upgrade Paths, EOL Tracking, Refresh Planning.
</div>
```text
┌───────────────────────────────── NetApp ONTAP — Install and Upgrade ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          ONTAP installation and upgrade: deployment and version management procedures         │   │
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


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## ONTAP Version Matrix

| Release | GA Date | Full Support End | Limited Support End | Notes |
|---|---|---|---|---|
| ONTAP 9.10.1 | Dec 2021 | Dec 2023 | Dec 2025 | P4 — limited support only |
| ONTAP 9.11.1 | Jun 2022 | Jun 2024 | Jun 2026 | P4 — limited support only |
| ONTAP 9.12.1 | Dec 2022 | Dec 2024 | Dec 2026 | P4 — approaching end |
| ONTAP 9.13.1 | Jun 2023 | Jun 2025 | Jun 2027 | Active — full support |
| ONTAP 9.14.1 | Dec 2023 | Dec 2025 | Dec 2027 | Active — recommended baseline |
| ONTAP 9.15.1 | Jun 2024 | Jun 2026 | Jun 2028 | Active — current latest |

Verify exact dates on the [NetApp Product Lifecycle page](https://support.netapp.com/) before planning any upgrade.

## Upgrade Paths

ONTAP follows a major.minor.patch versioning model. Upgrade rules:

- **Within the same minor release**: patch upgrades are always supported (e.g., 9.14.1 → 9.14.1P4)
- **Adjacent minor releases**: direct upgrade supported (e.g., 9.13.1 → 9.14.1)
- **Skipping minor releases**: generally not supported; must step through intermediate versions (e.g., 9.11.1 → 9.12.1 → 9.13.1)
- **Automated Non-Disruptive Upgrade (ANDU)**: preferred method; orchestrated by ONTAP itself, upgrades one node at a time via takeover/giveback
- Always check the [ONTAP Upgrade Advisor in BlueXP](https://bluexp.netapp.com) for the exact recommended path and any pre-upgrade blockers before beginning

```text
9.10.1 → 9.11.1 → 9.12.1 → 9.13.1 → 9.14.1 → 9.15.1
         (patch updates within each minor release are always allowed)
```

**Pre-upgrade checks:**
1. All SnapMirror relationships healthy; lag within RPO
2. No aggregates above 90% capacity
3. No failed or degraded RAID groups
4. AutoSupport delivering successfully
5. HA storage failover enabled on all pairs (`storage failover show`)

## EOL Tracking

- Monitor the NetApp Support lifecycle calendar quarterly
- Plan upgrades before limited support end dates — limited support means no new bug fixes, only existing fixes available
- Align ONTAP upgrades with SnapCenter compatibility — SnapCenter has its own supported ONTAP version matrix (see SnapCenter lifecycle)
- Track end-of-availability (EOA) for hardware platforms; an EOA platform still runs ONTAP but cannot be added to the fleet

## Refresh Planning

| Trigger | Action |
|---|---|
| ONTAP reaching limited support | Plan upgrade to current GA release within 6 months |
| Hardware EOA announced | Plan platform replacement within 18–24 months |
| Performance headroom <20% | Evaluate node addition or platform refresh |
| Aggregate disk count at shelf max | Add shelf or plan migration to larger-capacity drives |
| SnapMirror destination ONTAP < source | Upgrade destination first before upgrading source |

Refresh projects should be tracked in a capacity and lifecycle register updated quarterly. Use the Active IQ / BlueXP risk advisor to surface hardware and firmware advisories that can trigger unplanned refresh requirements.
