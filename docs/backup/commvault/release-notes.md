---
tags:
  - commvault
---
# Commvault — Release Notes

<div class="kb-summary">
Version history and release notes for Commvault.
</div>

![Release Notes](../../assets/commvault-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 11.32 | 2024-Q3 | Commvault 11.32 — AI-assisted anomaly recovery | [Release Notes](#) |
| 11.30 | 2024-Q1 | Commvault 11.30 — Metallic integration updates | [Release Notes](#) |
| 11.28 | 2023-Q3 | Commvault 11.28 — Air Gap Protect GA | [Release Notes](#) |
| 11.26 | 2023-Q1 | Commvault 11.26 — Kubernetes operator improvements | [Release Notes](#) |
| 11.24 | 2022-Q3 | Commvault 11.24 — Ransomware protection update | [Release Notes](#) |

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
