---
tags:
  - dell
description: "Version history and release notes for Dell FOD."
---
# Dell FOD — Release Notes

*Applies to: Dell EMC Storage*

<div class="kb-summary">
Version history and release notes for Dell FOD.
</div>

![Release Notes](../../../../assets/fod-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 3.2 | 2024-Q2 | FOD 3.2 — PowerMax 10.1 feature enablement | [Release Notes](#) |
| 3.1 | 2023-Q3 | FOD 3.1 — online license activation improvements | [Release Notes](#) |
| 3.0 | 2022-Q4 | FOD 3.0 — REST API license management | [Release Notes](#) |
| 2.5 | 2022-Q1 | FOD 2.5 — multi-array batch activation | [Release Notes](#) |
| 2.4 | 2021-Q2 | FOD 2.4 — license audit report export | [Release Notes](#) |

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
