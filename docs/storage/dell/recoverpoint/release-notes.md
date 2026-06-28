---
tags:
  - dell
---
# Dell RecoverPoint — Release Notes

<div class="kb-summary">
Version history and release notes for Dell RecoverPoint.
</div>

![Release Notes](../../../assets/recoverpoint-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 6.0 | 2024-Q2 | RecoverPoint 6.0 — VMAX/PowerMax 10 support | [Release Notes](#) |
| 5.3 | 2023-Q2 | RecoverPoint 5.3 — PowerStore replication GA | [Release Notes](#) |
| 5.2 | 2022-Q2 | RecoverPoint 5.2 — cloud copy target support | [Release Notes](#) |
| 5.1 | 2021-Q4 | RecoverPoint 5.1 — scale-out splitter support | [Release Notes](#) |
| 5.0 | 2021-Q1 | RecoverPoint 5.0 — VMware vSphere 7 support | [Release Notes](#) |

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
