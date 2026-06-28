---
tags:
  - netapp
---
# NetApp — Release Notes

<div class="kb-summary">
Version history and release notes for NetApp.
</div>

![Release Notes](../../assets/netapp-release-notes.svg)

```d2
direction: right

center: "Netapp" {shape: hexagon}
version_history: "Version History" {shape: rectangle}
key_terminology: "Key Terminology" {shape: rectangle}
upgrade_path: "Upgrade Path" {shape: rectangle}

center -> version_history
center -> key_terminology
center -> upgrade_path
```

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 2024.4 | 2024-Q4 | NetApp platform update — unified BlueXP UI | [Release Notes](#) |
| 2024.2 | 2024-Q2 | NetApp — ONTAP 9.15, SnapCenter 6.0 alignment | [Release Notes](#) |
| 2023.4 | 2023-Q4 | NetApp — AFF C-series capacity tier GA | [Release Notes](#) |
| 2023.2 | 2023-Q2 | NetApp — BlueXP backup and recovery expansion | [Release Notes](#) |
| 2022.4 | 2022-Q4 | NetApp — ONTAP S3 multi-protocol enhancement | [Release Notes](#) |

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
