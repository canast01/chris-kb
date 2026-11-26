---
tags:
  - security
description: "Version history and release notes for CyberArk."
---
# CyberArk — Release Notes

*Applies to: CyberArk PAS 12.x*

<div class="kb-summary">
Version history and release notes for CyberArk.
</div>

![Release Notes](../../../assets/cyberark-release-notes.svg)

## Before you begin

No special prerequisites — review the version table and cross-reference your deployed version before applying any update.

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 14.2 | 2024-Q3 | CyberArk 14.2 — PAM360 integration improvements | Not yet verified |
| 14.0 | 2024-Q1 | CyberArk 14.0 — CORA AI launch | Not yet verified |
| 13.2 | 2023-Q3 | CyberArk 13.2 — EPM Mac Apple Silicon support | Not yet verified |
| 13.0 | 2023-Q1 | CyberArk 13.0 — Identity Security platform | Not yet verified |
| 12.6 | 2022-Q3 | CyberArk 12.6 — Conjur Cloud GA | Not yet verified |

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
