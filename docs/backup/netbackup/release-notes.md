---
tags:
  - netbackup
---
# Veritas NetBackup — Release Notes

*Applies to: NetBackup 10.x*

<div class="kb-summary">
Version history and release notes for Veritas NetBackup.
</div>

![Release Notes](../../assets/netbackup-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 10.4 | 2024-Q3 | NetBackup 10.4 — workload accelerator enhancements | [Release Notes](#) |
| 10.3 | 2024-Q1 | NetBackup 10.3 — Flex Scale HA improvements | [Release Notes](#) |
| 10.2 | 2023-Q3 | NetBackup 10.2 — cloud-first policy management | [Release Notes](#) |
| 10.1 | 2023-Q1 | NetBackup 10.1 — Kubernetes CSI snapshot backup | [Release Notes](#) |
| 10.0 | 2022-Q2 | NetBackup 10.0 GA — containerised media server | [Release Notes](#) |

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
