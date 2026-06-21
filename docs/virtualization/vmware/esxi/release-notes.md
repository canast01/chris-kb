---
tags:
  - esxi
  - vmware
  - vsphere-8
---
# VMware ESXi — Release Notes

<div class="kb-summary">
Version history and release notes for VMware ESXi.
</div>

![Release Notes](../../../assets/esxi-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 8.0 U3 | 2024-Q3 | Security hardening, NVMe-oF initiator improvements | [Release Notes](#) |
| 8.0 U2 | 2024-Q1 | TPM 2.0 attestation enhancements, vTPM migration | [Release Notes](#) |
| 8.0 U1 | 2023-Q2 | ESXi 8.0 U1 — driver compatibility and stability | [Release Notes](#) |
| 8.0 GA | 2022-Q4 | ESXi 8 GA — Intel TDX, AMD SEV-SNP support | [Release Notes](#) |
| 7.0 U3 | 2022-Q1 | ESXi 7.0 U3 — lifecycle LTS baseline | [Release Notes](#) |

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
