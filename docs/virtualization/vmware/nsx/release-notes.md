---
tags:
  - nsx
  - nsx-4
  - vmware
---
# VMware NSX — Release Notes

<div class="kb-summary">
Version history and release notes for VMware NSX.
</div>

![Release Notes](../../../assets/nsx-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 4.1.2 | 2024-Q2 | Distributed SNAT, multi-site federation improvements | [Release Notes](#) |
| 4.1.1 | 2023-Q4 | NSX-T to NSX rebrand GA, L7 firewall enhancements | [Release Notes](#) |
| 4.0.1 | 2023-Q1 | NSX 4.0 — policy API convergence, EVPN support | [Release Notes](#) |
| 3.2.3 | 2022-Q3 | NSX-T 3.2 LTS — distributed firewall scale | [Release Notes](#) |
| 3.2.1 | 2022-Q1 | NSX-T 3.2.1 — malware prevention GA | [Release Notes](#) |

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
