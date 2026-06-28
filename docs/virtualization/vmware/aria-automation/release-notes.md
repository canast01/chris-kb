---
tags:
  - aria-automation
  - vmware
---
# VMware Aria Automation — Release Notes

<div class="kb-summary">
Version history and release notes for VMware Aria Automation.
</div>

![Release Notes](../../../assets/aria-automation-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 8.18 | 2024-Q3 | Aria Automation 8.18 — Day 2 actions catalog | [Release Notes](#) |
| 8.16 | 2024-Q1 | Aria Automation 8.16 — Terraform provider updates | [Release Notes](#) |
| 8.14 | 2023-Q3 | Aria Automation 8.14 — plugin extensibility GA | [Release Notes](#) |
| 8.12 | 2023-Q1 | Aria Automation 8.12 — vRA rebrand to Aria | [Release Notes](#) |
| 8.10 | 2022-Q3 | vRA 8.10 — ABX action enhancements | [Release Notes](#) |

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
