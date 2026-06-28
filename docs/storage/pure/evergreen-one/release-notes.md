---
tags:
  - pure
---
# Pure Evergreen//ONE — Release Notes

<div class="kb-summary">
Version history and release notes for Pure Evergreen//ONE.
</div>

![Release Notes](../../../assets/evergreen-one-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 2024.4 | 2024-Q4 | Evergreen//ONE 2024.4 — SLA expansion to NVMe-oF | [Release Notes](#) |
| 2024.2 | 2024-Q2 | Evergreen//ONE — latency guarantee update | [Release Notes](#) |
| 2023.4 | 2023-Q4 | Evergreen//ONE — capacity burst model revision | [Release Notes](#) |
| 2023.2 | 2023-Q2 | Evergreen//ONE — sustainability reporting GA | [Release Notes](#) |
| 2022.4 | 2022-Q4 | Evergreen//ONE — FlashBlade//S tier introduction | [Release Notes](#) |

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
