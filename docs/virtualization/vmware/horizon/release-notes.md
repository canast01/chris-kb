---
tags:
  - horizon
  - vmware
---
# VMware Horizon — Release Notes

<div class="kb-summary">
Version history and release notes for VMware Horizon.
</div>

![Release Notes](../../../assets/horizon-release-notes.svg)

```d2
direction: right

center: "Horizon" {shape: hexagon}
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
| 8 2312 | 2024-Q1 | Horizon 2312 — Windows 11 23H2 gold image support | [Release Notes](#) |
| 8 2309 | 2023-Q4 | Horizon 2309 — App Volumes 4.10 integration | [Release Notes](#) |
| 8 2306 | 2023-Q2 | Horizon 2306 — Teams media optimisation improvements | [Release Notes](#) |
| 8 2303 | 2023-Q1 | Horizon 2303 — RDSH scaling enhancements | [Release Notes](#) |
| 8 2212 | 2022-Q4 | Horizon 2212 — Blast Extreme protocol update | [Release Notes](#) |

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
