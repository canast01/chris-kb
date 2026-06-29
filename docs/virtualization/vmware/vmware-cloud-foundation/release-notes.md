---
tags:
  - vcf
  - vmware
---
# VMware Cloud Foundation — Release Notes

*Applies to: VMware vSphere 7.x / 8.x*

<div class="kb-summary">
Version history and release notes for VMware Cloud Foundation.
</div>

![Release Notes](../../../assets/vmware-cloud-foundation-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 5.2 | 2024-Q3 | VCF 5.2 — consolidated architecture GA | [Release Notes](#) |
| 5.1.1 | 2024-Q1 | VCF 5.1.1 — NSX 4.1, vSAN 8 U2 alignment | [Release Notes](#) |
| 5.1 | 2023-Q3 | VCF 5.1 — vSphere 8 U1 integrated baseline | [Release Notes](#) |
| 5.0 | 2022-Q4 | VCF 5.0 — NSX-T to NSX rebrand, single pane | [Release Notes](#) |
| 4.5 | 2022-Q1 | VCF 4.5 — vSphere 7 LTS, lifecycle management | [Release Notes](#) |

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
