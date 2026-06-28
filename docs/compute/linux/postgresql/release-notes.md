---
tags:
  - linux
---
# PostgreSQL — Release Notes

<div class="kb-summary">
Version history and release notes for PostgreSQL.
</div>

![Release Notes](../../../assets/postgresql-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 17 | 2024-Q4 | PostgreSQL 17 — incremental backup, MERGE improvements | [Release Notes](#) |
| 16 | 2023-Q4 | PostgreSQL 16 — logical replication from standby | [Release Notes](#) |
| 15 | 2022-Q4 | PostgreSQL 15 — MERGE command, improved sorting | [Release Notes](#) |
| 14 | 2021-Q4 | PostgreSQL 14 — pipeline mode, ranges multirange | [Release Notes](#) |
| 13 | 2020-Q4 | PostgreSQL 13 — partitioned table improvements | [Release Notes](#) |

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
