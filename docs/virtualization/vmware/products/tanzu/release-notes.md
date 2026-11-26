---
tags:
  - tanzu
  - vmware
description: "Version history and release notes for VMware Tanzu."
---
# VMware Tanzu — Release Notes

*Applies to: VMware Tanzu*

<div class="kb-summary">
Version history and release notes for VMware Tanzu.
</div>

![Release Notes](../../../../assets/tanzu-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 2.4 | 2024-Q3 | Tanzu 2.4 — Kubernetes 1.30 support | Not yet verified |
| 2.3 | 2024-Q1 | Tanzu 2.3 — Tanzu Kubernetes Grid 2.3 | Not yet verified |
| 2.2 | 2023-Q3 | Tanzu 2.2 — ClusterClass GA, Carvel tools update | Not yet verified |
| 2.1 | 2023-Q1 | Tanzu 2.1 — vSphere Namespace policy enhancements | Not yet verified |
| 2.0 | 2022-Q4 | Tanzu 2.0 — TKG rebrand, unified lifecycle | Not yet verified |

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
