---
tags:
  - dell
---
# Dell PowerScale — Release Notes

*Applies to: Dell PowerScale (Isilon) 9.x*

<div class="kb-summary">
Version history and release notes for Dell PowerScale.
</div>

![Release Notes](../../../../assets/powerscale-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 9.7 | 2024-Q3 | OneFS 9.7 — SmartFlash NVMe tier GA | [Release Notes](#) |
| 9.6 | 2024-Q1 | OneFS 9.6 — SyncIQ policy improvements | [Release Notes](#) |
| 9.5 | 2023-Q3 | OneFS 9.5 — S3 protocol multi-bucket support | [Release Notes](#) |
| 9.4 | 2023-Q1 | OneFS 9.4 — DataAdvantage analytics | [Release Notes](#) |
| 9.3 | 2022-Q3 | OneFS 9.3 — SyncIQ SmartSync GA | [Release Notes](#) |

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
