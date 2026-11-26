---
tags:
  - vcenter
  - vmware
  - vsphere-8
description: "Version history and release notes for VMware vCenter."
---
# VMware vCenter — Release Notes

*Applies to: VMware vCenter 7.x / 8.x*

<div class="kb-summary">
Version history and release notes for VMware vCenter.
</div>

![Release Notes](../../../../assets/vcenter-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 8.0 U3 | 2024-Q3 | vCenter HA improvements, SDDC Manager integration | Not yet verified |
| 8.0 U2 | 2024-Q1 | Reduced footprint appliance, converged management | Not yet verified |
| 8.0 U1 | 2023-Q2 | vCenter Server 8.0 U1 stability and security patches | Not yet verified |
| 8.0 GA | 2022-Q4 | vCenter 8 GA — vSphere Distributed Services Engine | Not yet verified |
| 7.0 U3 | 2022-Q1 | vCenter 7.0 U3 — end of gen LTS baseline | Not yet verified |

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

Upgrade vCenter Server using the VMware vCenter Server Installer or VAMI. Always upgrade vCenter before ESXi hosts. Ensure the target version is compatible with all managed hosts using the [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com/). Snapshot the vCenter appliance VM before beginning. Post-upgrade, verify vCenter HA and Plugin compatibility.
