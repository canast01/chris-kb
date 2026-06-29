---
tags:
  - netapp
---
# NetApp SnapMirror — Release Notes

*Applies to: NetApp ONTAP 9.x · SnapMirror*

<div class="kb-summary">
Version history and release notes for NetApp SnapMirror.
</div>

![Release Notes](../../../assets/snapmirror-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 9.15.1 | 2024-Q4 | SnapMirror active sync — asymmetric access GA | [Release Notes](#) |
| 9.14.1 | 2024-Q1 | SnapMirror cloud — S3 endpoint expansion | [Release Notes](#) |
| 9.13.1 | 2023-Q3 | FlexGroup SnapMirror active sync support | [Release Notes](#) |
| 9.12.1 | 2023-Q1 | SnapMirror business continuity v2 enhancements | [Release Notes](#) |
| 9.11.1 | 2022-Q3 | SnapMirror active sync — VMFS datastores GA | [Release Notes](#) |

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
