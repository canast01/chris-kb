---
tags:
  - windows
---
# SQL Server — Release Notes

<div class="kb-summary">
Version history and release notes for SQL Server.
</div>

![Release Notes](../../../assets/sql-server-release-notes.svg)

```d2
direction: right

center: "SQL Server" {shape: hexagon}
version_history: "Version History" {shape: rectangle}
key_terminology: "Key Terminology" {shape: rectangle}
upgrade_path: "Upgrade Path" {shape: rectangle}

center -> version_history
center -> key_terminology
center -> upgrade_path
```

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 2022 CU14 | 2024-Q4 | SQL Server 2022 CU14 — Query Store enhancements | [Release Notes](#) |
| 2022 CU10 | 2024-Q1 | SQL Server 2022 CU10 — security and performance | [Release Notes](#) |
| 2022 GA | 2022-Q4 | SQL Server 2022 GA — Azure Synapse Link | [Release Notes](#) |
| 2019 CU25 | 2023-Q4 | SQL Server 2019 CU25 — HA improvements | [Release Notes](#) |
| 2019 GA | 2019-Q4 | SQL Server 2019 GA — Big Data Clusters | [Release Notes](#) |

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
