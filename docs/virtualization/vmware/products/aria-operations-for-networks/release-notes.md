---
tags:
  - aria-networks
  - vmware
---
# VMware Aria Operations for Networks — Release Notes

*Applies to: VMware Aria 8.x*

<div class="kb-summary">
Version history and release notes for VMware Aria Operations for Networks.
</div>

![Release Notes](../../../../assets/aria-operations-for-networks-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 6.13 | 2024-Q3 | Aria for Networks 6.13 — NSX 4.1 topology support | [Release Notes](#) |
| 6.11 | 2024-Q1 | Aria for Networks 6.11 — path tracing improvements | [Release Notes](#) |
| 6.9 | 2023-Q3 | Aria for Networks 6.9 — vRNI rebrand to Aria | [Release Notes](#) |
| 6.7 | 2023-Q1 | Aria for Networks 6.7 — AWS VPC flow log analysis | [Release Notes](#) |
| 6.5 | 2022-Q3 | vRNI 6.5 — application security planning | [Release Notes](#) |

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
