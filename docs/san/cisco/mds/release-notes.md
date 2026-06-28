---
tags:
  - san
---
# Cisco MDS — Release Notes

<div class="kb-summary">
Version history and release notes for Cisco MDS.
</div>

![Release Notes](../../../assets/mds-release-notes.svg)

```d2
direction: right

center: "Cisco MDS" {shape: hexagon}
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
| 9.4(3) | 2024-Q3 | MDS NX-OS 9.4(3) — 64G FC GA | [Release Notes](#) |
| 9.4(2) | 2024-Q1 | MDS NX-OS 9.4(2) — CFS improvements | [Release Notes](#) |
| 9.3(2) | 2023-Q3 | MDS NX-OS 9.3(2) — IVR NAT enhancements | [Release Notes](#) |
| 9.3(1) | 2023-Q1 | MDS NX-OS 9.3(1) — Smart Zoning scale | [Release Notes](#) |
| 9.2(2) | 2022-Q3 | MDS NX-OS 9.2(2) — DPPM improvements | [Release Notes](#) |

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
