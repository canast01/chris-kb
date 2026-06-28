---
tags:
  - security
---
# Venafi — Release Notes

<div class="kb-summary">
Version history and release notes for Venafi.
</div>

![Release Notes](../../assets/venafi-release-notes.svg)

## Before you begin

No special prerequisites — review the version table and cross-reference your deployed version before applying any update.

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 24.3 | 2024-Q3 | Venafi 24.3 — TLS Protect Cloud improvements | [Release Notes](#) |
| 24.1 | 2024-Q1 | Venafi 24.1 — Kubernetes cert-manager integration | [Release Notes](#) |
| 23.4 | 2023-Q4 | Venafi 23.4 — CodeSign Protect updates | [Release Notes](#) |
| 23.2 | 2023-Q2 | Venafi 23.2 — machine identity firewall | [Release Notes](#) |
| 22.4 | 2022-Q4 | Venafi 22.4 — TrustNet improvements | [Release Notes](#) |

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
