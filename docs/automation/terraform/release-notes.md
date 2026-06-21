---
tags:
  - terraform
---
# Terraform — Release Notes

<div class="kb-summary">
Version history and release notes for Terraform.
</div>

![Release Notes](../../assets/terraform-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 1.9 | 2024-Q2 | Input variable validations on modules, provider iteration | [Release Notes](#) |
| 1.8 | 2024-Q1 | Provider-defined functions, enhanced import blocks | [Release Notes](#) |
| 1.7 | 2023-Q4 | Ephemeral values, write-only attributes | [Release Notes](#) |
| 1.6 | 2023-Q3 | Test framework GA, stack configuration preview | [Release Notes](#) |
| 1.5 | 2023-Q2 | Import block GA, config-driven import | [Release Notes](#) |

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
