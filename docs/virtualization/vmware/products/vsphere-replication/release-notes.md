---
tags:
  - vmware
  - vsphere-replication
description: "Version history and release notes for VMware vSphere Replication."
---
# VMware vSphere Replication — Release Notes

*Applies to: VMware vSphere 7.x / 8.x*

<div class="kb-summary">
Version history and release notes for VMware vSphere Replication.
</div>

![Release Notes](../../../../assets/vsphere-replication-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 8.8 | 2024-Q1 | vSphere Replication 8.8 — improved RPO granularity | [Release Notes](#) |
| 8.7 | 2023-Q3 | vSphere Replication 8.7 — vSAN replication improvements | [Release Notes](#) |
| 8.6 | 2022-Q4 | vSphere Replication 8.6 — SRM 8.6 alignment | [Release Notes](#) |
| 8.5 | 2022-Q2 | vSphere Replication 8.5 — cloud provider support | [Release Notes](#) |
| 8.4 | 2021-Q4 | vSphere Replication 8.4 — replication traffic compression | [Release Notes](#) |

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
