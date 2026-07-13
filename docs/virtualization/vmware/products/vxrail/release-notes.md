---
tags:
  - vxrail
description: "Version history and release notes for Dell VxRail."
---
# Dell VxRail — Release Notes

*Applies to: Dell VxRail 7.x / 8.x*

<div class="kb-summary">
Version history and release notes for Dell VxRail.
</div>

![Release Notes](../../../../assets/vxrail-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 8.0.300 | 2024-Q3 | VxRail 8.0.300 — ESXi 8.0 U3 baseline | [Release Notes](#) |
| 8.0.200 | 2024-Q1 | VxRail 8.0.200 — vSAN 8 U2 support | [Release Notes](#) |
| 8.0.100 | 2023-Q2 | VxRail 8.0 — full vSphere 8 lifecycle support | [Release Notes](#) |
| 7.0.481 | 2022-Q4 | VxRail 7.0.481 — ESXi 7.0 U3 LTS | [Release Notes](#) |
| 7.0.450 | 2022-Q1 | VxRail 7.0.450 — stability and driver updates | [Release Notes](#) |

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
