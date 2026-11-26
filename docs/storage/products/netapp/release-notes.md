---
tags:
  - netapp
description: "Version history and release notes for NetApp."
---
# NetApp — Release Notes

*Applies to: NetApp ONTAP 9.x*

<div class="kb-summary">
Version history and release notes for NetApp.
</div>

![Release Notes](../../../assets/netapp-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 2024.4 | 2024-Q4 | NetApp platform update — unified BlueXP UI | Not yet verified |
| 2024.2 | 2024-Q2 | NetApp — ONTAP 9.15, SnapCenter 6.0 alignment | Not yet verified |
| 2023.4 | 2023-Q4 | NetApp — AFF C-series capacity tier GA | Not yet verified |
| 2023.2 | 2023-Q2 | NetApp — BlueXP backup and recovery expansion | Not yet verified |
| 2022.4 | 2022-Q4 | NetApp — ONTAP S3 multi-protocol enhancement | Not yet verified |

## Key Terminology

**Major Version**
: A release containing significant new features or architectural changes; may require additional planning and testing.

**Patch Release**
: A targeted fix release that addresses bugs or security issues within a major/minor version.

**EOL (End of Life)**
: Date after which the vendor no longer provides updates, security patches, or technical support.

**Upgrade Path**
: The supported sequence of versions a system must traverse to reach a target version (some versions cannot be skipped).

## Upgrade Path

Review the vendor's official upgrade documentation and compatibility matrix before beginning any version change. Validate that all dependent components (OS, drivers, integration plugins) support the target version. Perform upgrades in a staged approach: dev/test environment first, then production. Capture a snapshot or backup immediately prior to the upgrade window. After the upgrade, run post-validation health checks and confirm all services are operating normally.
