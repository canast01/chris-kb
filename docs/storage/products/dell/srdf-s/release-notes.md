---
tags:
  - dell
description: "Version history and release notes for Dell SRDF/S."
---
# Dell SRDF/S — Release Notes

*Applies to: Dell EMC Storage*

<div class="kb-summary">
Version history and release notes for Dell SRDF/S.
</div>

![Release Notes](../../../../assets/srdf-s-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 10.1 | 2024-Q3 | SRDF/S 10.1 — 1 ms synchronous replication target | [Release Notes](#) |
| 10.0 | 2023-Q3 | SRDF/S 10.0 — PowerMax 350F GA | [Release Notes](#) |
| 9.2 | 2022-Q3 | SRDF/S 9.2 — Metro witness improvements | [Release Notes](#) |
| 9.1 | 2021-Q4 | SRDF/S 9.1 — Active/Active Metro enhancements | [Release Notes](#) |
| 9.0 | 2021-Q1 | SRDF/S 9.0 — HYPERMAX OS 9.0 alignment | [Release Notes](#) |

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
