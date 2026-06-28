---
tags:
  - ceph
---
# Ceph — Release Notes

<div class="kb-summary">
Version history and release notes for Ceph.
</div>

![Release Notes](../../assets/ceph-release-notes.svg)

```d2
direction: right

center: "Ceph" {shape: hexagon}
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
| 18.2 Reef | 2024-Q2 | Ceph 18.2 Reef — RGW multi-site active-active | [Release Notes](#) |
| 17.2 Quincy | 2023-Q2 | Ceph 17.2 Quincy — RBD fast-diff improvements | [Release Notes](#) |
| 16.2 Pacific | 2022-Q2 | Ceph 16.2 Pacific — cephadm orchestration GA | [Release Notes](#) |
| 15.2 Octopus | 2021-Q2 | Ceph 15.2 Octopus — object gateway enhancements | [Release Notes](#) |
| 14.2 Nautilus | 2020-Q2 | Ceph 14.2 Nautilus — mgr dashboard v2 | [Release Notes](#) |

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
