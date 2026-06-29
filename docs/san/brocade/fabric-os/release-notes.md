---
tags:
  - san
---
# Brocade Fabric OS — Release Notes

*Applies to: Brocade FOS 9.x*

<div class="kb-summary">
Version history and release notes for Brocade Fabric OS.
</div>

![Release Notes](../../../assets/fabric-os-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 9.2.2 | 2024-Q3 | FOS 9.2.2 — 64G FC speed support | [Release Notes](#) |
| 9.2.1 | 2024-Q1 | FOS 9.2.1 — security hardening patches | [Release Notes](#) |
| 9.2.0 | 2023-Q3 | FOS 9.2.0 — zoning scalability improvements | [Release Notes](#) |
| 9.1.1 | 2023-Q1 | FOS 9.1.1 — FICON MIHPTO enhancements | [Release Notes](#) |
| 9.1.0 | 2022-Q3 | FOS 9.1.0 — 64G long distance SFP support | [Release Notes](#) |

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
