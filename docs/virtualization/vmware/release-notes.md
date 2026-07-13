---
tags:
  - vmware
description: "Version history and release notes for VMware."
---
# VMware — Release Notes

*Applies to: VMware vSphere 7.x / 8.x*

<div class="kb-summary">
Version history and release notes for VMware.
</div>

![Release Notes](../../assets/vmware-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| vSphere 8.0 U3 | 2024-Q3 | vSphere 8.0 U3 — multi-product patch release | [Release Notes](#) |
| vSphere 8.0 U2 | 2024-Q1 | vSphere 8.0 U2 — vCenter HA improvements | [Release Notes](#) |
| vSphere 8.0 U1 | 2023-Q2 | vSphere 8.0 U1 — stability and security | [Release Notes](#) |
| vSphere 8.0 GA | 2022-Q4 | vSphere 8.0 GA — DPU offload, vSAN ESA | [Release Notes](#) |
| vSphere 7.0 U3 | 2022-Q1 | vSphere 7.0 U3 — lifecycle management LTS | [Release Notes](#) |

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
