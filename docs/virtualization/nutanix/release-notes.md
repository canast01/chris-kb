---
tags:
  - nutanix
---
# Nutanix — Release Notes

<div class="kb-summary">
Version history and release notes for Nutanix.
</div>

![Release Notes](../../assets/nutanix-release-notes.svg)

```d2
direction: right

center: "Nutanix AHV" {shape: hexagon}
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
| 6.8 | 2024-Q3 | AOS 6.8 — NCI improvements, 3-node edge scaling | [Release Notes](#) |
| 6.7 | 2024-Q1 | AOS 6.7 — Flow Network Security enhancements | [Release Notes](#) |
| 6.6 | 2023-Q3 | AOS 6.6 — Objects 4.0 S3 multipart upload | [Release Notes](#) |
| 6.5 | 2023-Q1 | AOS 6.5 LTS — Prism Central scale improvements | [Release Notes](#) |
| 6.1 | 2022-Q1 | AOS 6.1 — Nutanix Files WORM GA | [Release Notes](#) |

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
