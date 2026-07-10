---
tags:
  - netapp
---
# NetApp Keystone — Release Notes

*Applies to: NetApp ONTAP 9.x*

<div class="kb-summary">
Version history and release notes for NetApp Keystone.
</div>

![Release Notes](../../../../assets/keystone-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| STaaS v3 | 2024-Q3 | Keystone STaaS v3 — AFF C-series tier addition | [Release Notes](#) |
| STaaS v2 | 2023-Q4 | Keystone STaaS v2 — NVMe tier GA, burst on-demand | [Release Notes](#) |
| STaaS v1.2 | 2023-Q1 | Keystone 1.2 — co-location expansion regions | [Release Notes](#) |
| STaaS v1.1 | 2022-Q3 | Keystone 1.1 — SLA reporting dashboard | [Release Notes](#) |
| STaaS v1.0 | 2022-Q1 | Keystone STaaS v1.0 GA | [Release Notes](#) |

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
