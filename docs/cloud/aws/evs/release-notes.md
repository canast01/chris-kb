---
tags:
  - aws
description: "Version history and release notes for AWS EVS."
---
# AWS EVS — Release Notes

*Applies to: AWS Elastic VMware Service*

<div class="kb-summary">
Version history and release notes for AWS EVS.
</div>

![Release Notes](../../../assets/evs-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 1.3 | 2024-Q3 | AWS EVS 1.3 — vSphere 8.0 U3 baseline | [Release Notes](#) |
| 1.2 | 2024-Q1 | AWS EVS 1.2 — SDDC interconnect improvements | [Release Notes](#) |
| 1.1 | 2023-Q3 | AWS EVS 1.1 — NSX 4.1 support | [Release Notes](#) |
| 1.0 | 2023-Q1 | AWS EVS 1.0 GA — VMware workloads on AWS bare metal | [Release Notes](#) |
| Preview | 2022-Q4 | AWS EVS preview — initial availability regions | [Release Notes](#) |

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
