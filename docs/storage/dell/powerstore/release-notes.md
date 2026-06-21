---
tags:
  - dell
---
# Dell PowerStore — Release Notes

<div class="kb-summary">
Version history and release notes for Dell PowerStore.
</div>

![Release Notes](../../../assets/powerstore-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 3.6 | 2024-Q3 | PowerStore 3.6 — AppsOn enhancements | [Release Notes](#) |
| 3.5 | 2024-Q1 | PowerStore 3.5 — NVMe-oF iSCSI offload | [Release Notes](#) |
| 3.2 | 2023-Q3 | PowerStore 3.2 — volume group remote replication | [Release Notes](#) |
| 3.0 | 2022-Q4 | PowerStore 3.0 — Metro volume replication GA | [Release Notes](#) |
| 2.1 | 2022-Q1 | PowerStore 2.1 — Kubernetes CSI improvements | [Release Notes](#) |

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
