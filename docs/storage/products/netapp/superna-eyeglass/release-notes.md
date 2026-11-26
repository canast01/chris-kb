---
tags:
  - netapp
description: "Version history and release notes for Superna Eyeglass."
---
# Superna Eyeglass — Release Notes

*Applies to: NetApp ONTAP 9.x*

<div class="kb-summary">
Version history and release notes for Superna Eyeglass.
</div>

![Release Notes](../../../../assets/superna-eyeglass-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 2.9 | 2024-Q2 | Eyeglass 2.9 — OneFS 9.7 failover support | Not yet verified |
| 2.8 | 2023-Q4 | Eyeglass 2.8 — ransomware defender improvements | Not yet verified |
| 2.7 | 2023-Q2 | Eyeglass 2.7 — multi-cluster DR orchestration | Not yet verified |
| 2.6 | 2022-Q4 | Eyeglass 2.6 — SyncIQ policy automation | Not yet verified |
| 2.5 | 2022-Q1 | Eyeglass 2.5 — configuration replication engine v2 | Not yet verified |

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
