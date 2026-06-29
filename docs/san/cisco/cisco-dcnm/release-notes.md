---
tags:
  - san
---
# Cisco DCNM — Release Notes

*Applies to: Cisco MDS / NX-OS*

<div class="kb-summary">
Version history and release notes for Cisco DCNM.
</div>

![Release Notes](../../../assets/cisco-dcnm-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 12.2 | 2024-Q2 | DCNM 12.2 — fabric controller convergence | [Release Notes](#) |
| 12.1 | 2023-Q3 | DCNM 12.1 — vPC enhancements | [Release Notes](#) |
| 12.0 | 2022-Q4 | DCNM 12.0 — rebrand to Nexus Dashboard Fabric Controller | [Release Notes](#) |
| 11.5 | 2022-Q1 | DCNM 11.5 — LAN fabric improvements | [Release Notes](#) |
| 11.4 | 2021-Q2 | DCNM 11.4 — REST API v1 expansion | [Release Notes](#) |

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
