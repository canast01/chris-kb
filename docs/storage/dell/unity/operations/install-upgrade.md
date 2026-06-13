---
tags:
  - dell
  - operations
---
# Unity — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering Unity OE Version Matrix, Upgrade Paths, Hardware Refresh, EOL Tracking.

*Applies to: Unity XT*
</div>

```text
┌─────────────────────────────────── Dell Unity Install and Upgrade ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Initial install: rack Unity → cable SPs and DAEs → configure via Unisphere wizard       │   │
│   │       OE upgrade: download upgrade package → upload to Unity → health pre-check → commit      │   │
│   │      Rolling upgrade: SP B reboots first → SP A takes all I/O → SP B ready → SP A reboots     │   │
│   │            Non-disruptive: hosts continue I/O during upgrade; one SP always serving           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Health pre-check → upload OE package → commit → SP B upgrade/reboot → SP A upgrade/reboot          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Initial Install       │  │          OE Upgrade         │  │        Add Drives/DAE       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Rack and cable       │  │         Download OE         │  │        Cable new DAE        │   │
│   │           Power on          │  │       Upload to array       │  │        Rescan drives        │   │
│   │       Unisphere wizard      │  │        Pre-check run        │  │         Expand pool         │   │
│   │        Network config       │  │         SP B upgrade        │  │        FAST VP rebal        │   │
│   │          SCG enroll         │  │         SP A upgrade        │  │        Verify health        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    OE upgrade non-disruptive; hosts continue I/O; each SP takes ~15-20 min to reboot                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │    Operation     │     Duration     │     Disruptive    │     Rollback     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │ Initial install  │    2–4 hours     │  Yes (new system) │       N/A        │  Follow wizard   │   │
│   │    OE upgrade    │    30–60 min     │    No (rolling)   │  Prior OE image  │ Pre-check first  │   │
│   │     DAE add      │      15 min      │         No        │    Remove DAE    │ Rescan required  │   │
│   │    Drive add     │      5 min       │         No        │       N/A        │ Pool expand opt. │   │
│                                                                                                       │
│    Physical: SPE base unit; DAEs connect via SAS expansion cable from SP to first DAE chain           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OE             = Operating Environment; Unity OS upgrade package (.tgz file from Dell)             │
│    Rolling upgrade= SP B upgraded first while SP A serves I/O; then roles swap for SP A upgrade       │
│    Pre-check      = Automated health validation before upgrade commit; blocks on unresolved alerts    │
│    Unisphere wizard= Web-based initial configuration wizard; run once after first power-on            │
│    SPE            = Storage Processor Enclosure; base 2U chassis containing SP A and SP B             │
│    DAE            = Disk Array Enclosure; 2U or 4U expansion shelf; chained from SPE                  │
│    FAST VP rebal  = After adding drives, FAST VP distributes data across new capacity                 │
│    Pool expand    = Add drives to existing storage pool; capacity available after rescan              │
│    SCG enroll     = Register Unity with SCG after install for CloudIQ and phone-home support          │
│    Rollback OE    = If upgrade fails mid-way, Unity can revert to previous OE version                 │
│    SAS expansion  = Back-end SAS cabling between SPE and DAE; daisy-chain up to max DAEs              │
│    15-20 min reboot= Each SP reboot time during OE upgrade; I/O served by partner SP                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Unity OE Version Matrix

Unity OE (Operating Environment) releases follow a major.minor.patch scheme. Dell publishes end-of-support dates for each release; versions past their end-of-support date no longer receive security patches or bug fixes.

| Unity OE Version | Release | End of Primary Support | Notes |
|---|---|---|---|
| 5.4.x | 2024 | TBA | Current recommended release |
| 5.3.x | 2023 | TBA | Supported; upgrade to 5.4.x recommended |
| 5.2.x | 2022 | 2025 | Near end-of-support; plan upgrade |
| 5.1.x | 2021 | 2024 | End of primary support reached |
| 5.0.x | 2020 | 2023 | End of support; no further patches |
| 4.x and below | Pre-2020 | Expired | Must upgrade immediately |

Unity XT hardware is end-of-new-sales. Dell continues to support existing Unity XT systems under ProSupport contracts until the published hardware EOL date. The strategic migration path is to Dell PowerStore.

## Upgrade Paths

Unity OE supports **Non-Disruptive Upgrade (NDU)** — I/O continues from host perspective while each SP is restarted sequentially.

Supported upgrade path: any version within two major versions back can typically upgrade directly. Consult the Dell Unity Compatibility Matrix on the support portal for your specific version pair before beginning.

**Upgrade procedure:**

1. Run `uemcli /env/health show -filter "health.value ne OK"` and resolve all faults. Do not upgrade with a degraded pool or faulted SP.
2. Confirm both SPs are online and healthy: `uemcli /env/sp show`.
3. Confirm all replication sessions are in Active state: `uemcli /rep/session show`.
4. Download the OE upgrade package from [https://www.dell.com/support](https://www.dell.com/support) and verify the SHA256 checksum.
5. Upload the package to the array: **Unisphere > Maintenance > Software Upgrades > Upload Package**, or via `uemcli /sys/sw upload`.
6. Initiate the upgrade from Unisphere or `uemcli /sys/sw upgrade`. The system upgrades SP B first, then SP A. I/O continues via the active SP throughout.
7. Monitor upgrade progress in Unisphere. Each SP restart takes 10–20 minutes. Do not interrupt the process.
8. After completion, verify both SPs return to Normal state, confirm `uemcli /sys/sw show` shows the new version, and re-check all pools and replication sessions.

## Hardware Refresh

Dell Unity XT is end-of-new-sales. Organisations still running Unity XT should plan a migration to Dell PowerStore.

Migration options:

| Migration Method | Description | Best For |
|---|---|---|
| Dell Migration Services | Dell Professional Services migrates data using native replication or VPLEX | Large environments; minimal host downtime |
| Host-based migration | Applications quiesced, data mirrored to PowerStore volumes, host re-zoned | Small environments; full control over cutover |
| VPLEX non-disruptive migration | Unity LUN federated via VPLEX, then migrated behind VPLEX to PowerStore | Zero-downtime for VPLEX-connected environments |

Request a Dell-led migration assessment via your account team to determine the best approach for your workload mix.

## EOL Tracking

Monitor the following sources for Unity EOL announcements:

- Dell Support Portal: [https://www.dell.com/support](https://www.dell.com/support) — search for "Unity XT End of Life" under Product Notifications.
- Dell Technical Advisories: subscribe to email notifications for Unity XT product advisories.
- ProSupport contract renewal: EOL hardware loses ProSupport coverage at the hardware EOL date even if a support contract is active.

Maintain a lifecycle register that records each Unity system's hardware model, current OE version, ProSupport expiry date, and planned refresh date. Review and update the register quarterly.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
