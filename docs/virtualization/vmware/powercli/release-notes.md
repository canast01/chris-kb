---
tags:
  - powercli
  - vmware
---
# VMware PowerCLI — Release Notes

<div class="kb-summary">
Version history and release notes for VMware PowerCLI.
</div>

![Release Notes](../../../assets/powercli-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 13.3 | 2024-Q3 | PowerCLI 13.3 — vSphere 8.0 U3 module updates | [Release Notes](#) |
| 13.2 | 2024-Q1 | PowerCLI 13.2 — New-VM template improvements | [Release Notes](#) |
| 13.1 | 2023-Q3 | PowerCLI 13.1 — VMware.PowerCLI umbrella module | [Release Notes](#) |
| 13.0 | 2023-Q1 | PowerCLI 13.0 — PowerShell 7.3 compatibility | [Release Notes](#) |
| 12.7 | 2022-Q3 | PowerCLI 12.7 — vSAN cmdlet additions | [Release Notes](#) |

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
