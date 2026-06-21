---
tags:
  - pure
---
# Pure FlashBlade — Release Notes

<div class="kb-summary">
Version history and release notes for Pure FlashBlade.
</div>

![Release Notes](../../../assets/flashblade-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 4.4.10 | 2024-Q3 | Purity//FB 4.4 — S3 multi-region replication | [Release Notes](#) |
| 4.3.7 | 2024-Q1 | Purity//FB 4.3 — rapid restore throughput | [Release Notes](#) |
| 4.2.10 | 2023-Q3 | Purity//FB 4.2 — NFS v4.1 GA on FlashBlade//S | [Release Notes](#) |
| 4.1.14 | 2023-Q1 | Purity//FB 4.1 — FlashBlade//S platform GA | [Release Notes](#) |
| 3.3.6 | 2022-Q3 | Purity//FB 3.3 — SMB 3.1.1 Continuous Availability | [Release Notes](#) |

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
