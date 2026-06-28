---
tags:
  - veeam
---
# Veeam Backup & Replication — Release Notes

<div class="kb-summary">
Version history and release notes for Veeam Backup & Replication.
</div>

![Release Notes](../../assets/veeam-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 12.2 | 2024-Q3 | Veeam 12.2 — Entra ID backup GA, CDP improvements | [Release Notes](#) |
| 12.1 | 2024-Q1 | Veeam 12.1 — malware detection, ZTNA integration | [Release Notes](#) |
| 12.0 | 2023-Q1 | Veeam 12.0 — immutable backup to S3 GA | [Release Notes](#) |
| 11a | 2022-Q1 | Veeam 11a — patch release, CDP stability | [Release Notes](#) |
| 11.0 | 2021-Q2 | Veeam 11.0 — CDP, Kubernetes support GA | [Release Notes](#) |

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
