---
tags:
  - terraform
description: "Version history and release notes for Terraform."
---
# Terraform — Release Notes

*Applies to: Terraform 1.x*

<div class="kb-summary">
Version history and release notes for Terraform.
</div>

![Release Notes](../../assets/terraform-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 1.9 | 2024-Q2 | Input variable validations on modules, provider iteration | Not yet verified |
| 1.8 | 2024-Q1 | Provider-defined functions, enhanced import blocks | Not yet verified |
| 1.7 | 2023-Q4 | Ephemeral values, write-only attributes | Not yet verified |
| 1.6 | 2023-Q3 | Test framework GA, stack configuration preview | Not yet verified |
| 1.5 | 2023-Q2 | Import block GA, config-driven import | Not yet verified |

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
