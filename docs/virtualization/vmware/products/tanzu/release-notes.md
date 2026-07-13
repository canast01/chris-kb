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

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 2.4 | 2024-Q3 | Tanzu 2.4 — Kubernetes 1.30 support | [Release Notes](#) |
| 2.3 | 2024-Q1 | Tanzu 2.3 — Tanzu Kubernetes Grid 2.3 | [Release Notes](#) |
| 2.2 | 2023-Q3 | Tanzu 2.2 — ClusterClass GA, Carvel tools update | [Release Notes](#) |
| 2.1 | 2023-Q1 | Tanzu 2.1 — vSphere Namespace policy enhancements | [Release Notes](#) |
| 2.0 | 2022-Q4 | Tanzu 2.0 — TKG rebrand, unified lifecycle | [Release Notes](#) |

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
