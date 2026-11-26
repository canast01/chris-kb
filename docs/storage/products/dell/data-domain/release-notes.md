---
tags:
  - dell
description: "Version history and release notes for Dell Data Domain."
---
# Dell Data Domain — Release Notes

*Applies to: Dell EMC Storage*

<div class="kb-summary">
Version history and release notes for Dell Data Domain.
</div>

![Release Notes](../../../../assets/data-domain-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 8.1 | 2024-Q2 | Data Domain OS 8.1 — DD VE scale improvements | Not yet verified |
| 7.13 | 2023-Q3 | DDOS 7.13 — cloud tier Azure Gov support | Not yet verified |
| 7.12 | 2023-Q1 | DDOS 7.12 — DD3300 platform GA | Not yet verified |
| 7.11 | 2022-Q3 | DDOS 7.11 — DD9900 capacity expansion | Not yet verified |
| 7.10 | 2022-Q1 | DDOS 7.10 — Boost performance improvements | Not yet verified |

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
