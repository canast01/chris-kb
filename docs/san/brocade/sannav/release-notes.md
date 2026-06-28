---
tags:
  - san
---
# Brocade SANnav — Release Notes

<div class="kb-summary">
Version history and release notes for Brocade SANnav.
</div>

![Release Notes](../../../assets/sannav-release-notes.svg)

```d2
direction: right

center: "SANnav" {shape: hexagon}
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
| 2.3.1 | 2024-Q3 | SANnav 2.3.1 — FOS 9.2.2 discovery support | [Release Notes](#) |
| 2.3.0 | 2024-Q1 | SANnav 2.3.0 — health dashboard improvements | [Release Notes](#) |
| 2.2.2 | 2023-Q3 | SANnav 2.2.2 — REST API v2 analytics | [Release Notes](#) |
| 2.2.1 | 2023-Q1 | SANnav 2.2.1 — scalability patch release | [Release Notes](#) |
| 2.2.0 | 2022-Q3 | SANnav 2.2.0 — Supportsave automation | [Release Notes](#) |

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
