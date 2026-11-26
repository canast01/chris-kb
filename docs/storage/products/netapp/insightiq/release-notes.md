---
tags:
  - netapp
description: "Version history and release notes for NetApp InsightIQ."
---
# NetApp InsightIQ — Release Notes

*Applies to: NetApp ONTAP 9.x*

<div class="kb-summary">
Version history and release notes for NetApp InsightIQ.
</div>

![Release Notes](../../../../assets/insightiq-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 5.1 | 2024-Q2 | InsightIQ 5.1 — OneFS 9.7 compatibility | Not yet verified |
| 5.0 | 2023-Q3 | InsightIQ 5.0 — new performance baselines engine | Not yet verified |
| 4.1 | 2022-Q4 | InsightIQ 4.1 — cluster comparison dashboards | Not yet verified |
| 4.0 | 2022-Q1 | InsightIQ 4.0 — REST API for report export | Not yet verified |
| 3.2 | 2021-Q3 | InsightIQ 3.2 — long-term capacity trending | Not yet verified |

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
