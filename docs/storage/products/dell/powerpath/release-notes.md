---
tags:
  - dell
---
# Dell PowerPath — Release Notes

*Applies to: Dell PowerPath 7.x*

<div class="kb-summary">
Version history and release notes for Dell PowerPath.
</div>

![Release Notes](../../../../assets/powerpath-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 6.4 | 2024-Q2 | PowerPath 6.4 — RHEL 9.4 / SLES 15 SP5 support | [Release Notes](#) |
| 6.3 | 2023-Q3 | PowerPath 6.3 — PowerStore 3.0 multipath support | [Release Notes](#) |
| 6.2 | 2022-Q4 | PowerPath 6.2 — NVMe-oF multipath GA | [Release Notes](#) |
| 6.1 | 2022-Q1 | PowerPath 6.1 — Windows Server 2022 support | [Release Notes](#) |
| 6.0 | 2021-Q2 | PowerPath 6.0 — CLI management improvements | [Release Notes](#) |

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
