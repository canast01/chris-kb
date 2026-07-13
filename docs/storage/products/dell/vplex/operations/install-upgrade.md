---
tags:
  - dell
  - operations
description: "Install & Upgrade reference covering GeoSynchrony Version Matrix, Upgrade Paths, Hardware Lifecycle, EOL Tracking."
---
# Dell VPLEX — Install & Upgrade

<div class="kb-summary">
Install & Upgrade reference covering GeoSynchrony Version Matrix, Upgrade Paths, Hardware Lifecycle, EOL Tracking.

*Applies to: VPLEX*
</div>
![Dell VPLEX — Install & Upgrade](../../../../../assets/storage-dell-vplex-operations-install-upgrade.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## GeoSynchrony Version Matrix

VPLEX runs the GeoSynchrony software stack. Dell publishes end-of-support dates for each GeoSynchrony release. Running an unsupported version means no security patches, no bug fixes, and no Dell support for software issues.

| GeoSynchrony Version | Release | End of Primary Support | Notes |
|---|---|---|---|
| 6.2.x | 2023–2024 | TBA | Current recommended release |
| 6.1.x | 2022–2023 | TBA | Supported; upgrade to 6.2.x recommended |
| 6.0.x | 2021–2022 | 2024 | Near end-of-support; plan upgrade |
| 5.5.x | 2019–2021 | 2023 | End of primary support; no further patches |
| 5.4.x and below | Pre-2019 | Expired | Must upgrade immediately |

Check the current GeoSynchrony version: `ll /version/` in `vplexcli`.

## Upgrade Paths

GeoSynchrony upgrades follow a one-version-at-a-time path for major version jumps. Patch releases (6.1.x to 6.1.y) can typically be applied directly. Consult the Dell VPLEX Upgrade Guide for your specific version pair before beginning.

**Pre-upgrade checklist:**

1. Confirm the target GeoSynchrony release notes and verify compatibility with backend array firmware versions, VMware vSphere versions, and host OS multipath driver versions.
2. Verify that a valid Witness is configured and reachable from both Metro clusters.
3. Confirm all distributed devices are in a healthy sync state: `ll /distributed-storage/distributed-devices/*/health-indications/`
4. Confirm all consistency groups are healthy.
5. Take a VMS VM snapshot before beginning.

**Upgrade procedure (per cluster):**

1. Download the GeoSynchrony upgrade bundle from [https://www.dell.com/support](https://www.dell.com/support) and verify the checksum.
2. Upload the bundle to the VMS.
3. Upgrade one director at a time per engine using the rolling upgrade procedure in the VPLEX Upgrade Guide. Verify director health before proceeding to the next.
4. After all directors in a cluster are upgraded, confirm distributed device sync state and host connectivity.
5. Upgrade the VMS management software after all directors reach the new code level.
6. For Metro deployments, upgrade one cluster at a time; verify cross-cluster operation before upgrading the second cluster.
7. Post-upgrade: run `health-check --full` and validate all distributed devices show healthy status.

```d2
direction: right

preCheck: "Pre-upgrade checklist\nCompatibility matrix verified\nAll devices in-sync\nVMS snapshot taken" {shape: rectangle}
dl: "Download GeoSynchrony bundle\ndell.com/support\nVerify checksum" {shape: rectangle}
dir1A: "Upgrade director-1-1-A\nVerify health-state: ok" {shape: rectangle}
dir1B: "Upgrade director-1-1-B\nVerify health-state: ok" {shape: rectangle}
ddCheck1: "Confirm distributed device\nsync state after engine-1-1" {shape: rectangle}
nextEngine: "Repeat for next engine\n(if present" {shape: rectangle}
upgradeVms: "Upgrade VMS\nmanagement software" {shape: rectangle}
hcFull: "health-check --full\nNo warnings or errors" {shape: rectangle}
cluster2: "Upgrade Cluster-2\n(Metro — same sequence" {shape: rectangle}
done: "Upgrade complete\nUpdate lifecycle register" {shape: rectangle}

preCheck -> dl
dl -> dir1A
dir1A -> dir1B
dir1B -> ddCheck1
ddCheck1 -> nextEngine
nextEngine -> upgradeVms
upgradeVms -> hcFull
hcFull -> cluster2
cluster2 -> done
```

## Hardware Lifecycle

VPLEX hardware generations have fixed EOL dates. Key hardware end-of-sale and end-of-support milestones:

| Platform | Status | Notes |
|---|---|---|
| VPLEX VS2 (current director hardware) | Active | Supported under current ProSupport contracts |
| VPLEX GS400/GS200 (earlier directors) | End-of-sale | Support continuation per contract; check Dell EOL notices |

For hardware EOL, replacement options are:

- **VPLEX hardware refresh**: replace directors with current-generation hardware; software configuration is preserved.
- **Migration to alternative platform**: for environments where VPLEX functionality is replaced by storage-array-native replication (e.g., PowerStore Metro Node), contact the Dell account team for a migration assessment.

## EOL Tracking

- Subscribe to Dell product notifications for VPLEX at [https://www.dell.com/support](https://www.dell.com/support) to receive EOL announcements.
- Review the Dell Support Product EOL page quarterly.
- Maintain a lifecycle register for each VPLEX cluster recording: GeoSynchrony version, director hardware model, ProSupport contract expiry, and planned upgrade/refresh date.
- Coordinate VPLEX lifecycle events with backend array and host OS refresh cycles to avoid compatibility gaps.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Vplex — Procedures](../procedures/)
- [Vplex — Health Checks](../health-checks/)
- [Vplex — Deploy](../../deploy/)
