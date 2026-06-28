---
tags:
  - srm
  - vmware
---
# VMware SRM — Release Notes

<div class="kb-summary">
Version history and release notes for VMware SRM.
</div>

![Release Notes](../../../assets/srm-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 9.0 | 2024-Q2 | SRM 9.0 — vSphere 8 native, REST-only management | [Release Notes](#) |
| 8.8 | 2023-Q4 | SRM 8.8 — vSAN stretched cluster DR improvements | [Release Notes](#) |
| 8.7 | 2023-Q1 | SRM 8.7 — policy-based protection groups | [Release Notes](#) |
| 8.6 | 2022-Q3 | SRM 8.6 — vSphere Replication 8.6 alignment | [Release Notes](#) |
| 8.5 | 2022-Q1 | SRM 8.5 — NFS array-based replication expansion | [Release Notes](#) |

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
