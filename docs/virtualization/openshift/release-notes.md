---
tags:
  - openshift
description: "Version history and release notes for OpenShift."
---
# OpenShift — Release Notes

*Applies to: OpenShift 4.x*

<div class="kb-summary">
Version history and release notes for OpenShift.
</div>

![Release Notes](../../assets/openshift-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 4.16 | 2024-Q2 | OpenShift 4.16 — Kubernetes 1.29, tech preview updates | Not yet verified |
| 4.15 | 2024-Q1 | OpenShift 4.15 — RHCOS improvements, ACM 2.10 | Not yet verified |
| 4.14 | 2023-Q4 | OpenShift 4.14 — LTS, HyperShift GA | Not yet verified |
| 4.13 | 2023-Q2 | OpenShift 4.13 — hosted control planes preview | Not yet verified |
| 4.12 | 2022-Q4 | OpenShift 4.12 — LVM operator GA, Tekton 1.9 | Not yet verified |

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
