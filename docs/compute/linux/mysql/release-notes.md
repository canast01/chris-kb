---
tags:
  - linux
description: "Version history and release notes for MySQL."
---
# MySQL — Release Notes

*Applies to: Linux · MySQL 8.x*

<div class="kb-summary">
Version history and release notes for MySQL.
</div>

![Release Notes](../../../assets/mysql-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 8.4 LTS | 2024-Q2 | MySQL 8.4 LTS — new innovation release model | [Release Notes](#) |
| 8.2 | 2023-Q4 | MySQL 8.2 — Vector data type preview | [Release Notes](#) |
| 8.0.36 | 2024-Q1 | MySQL 8.0.36 — security and bug fix release | [Release Notes](#) |
| 8.0.34 | 2023-Q3 | MySQL 8.0.34 — JSON table improvements | [Release Notes](#) |
| 8.0.32 | 2023-Q1 | MySQL 8.0.32 — InnoDB parallel DDL | [Release Notes](#) |

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
