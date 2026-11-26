---
tags:
  - linux
description: "Version history and release notes for Linux."
---
# Linux — Release Notes

*Applies to: Linux (RHEL / Ubuntu / Debian)*

<div class="kb-summary">
Version history and release notes for Linux.
</div>

![Release Notes](../../assets/linux-release-notes.svg)

## Version History

!!! warning "Unverified version history"
    This table has not yet been checked against the vendor's official release
    notes. Treat the versions, dates and summaries below as unconfirmed until
    they are verified.

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| RHEL 9.4 | 2024-Q2 | RHEL 9.4 — kernel 5.14.0-427, FIPS 140-3 | Not yet verified |
| RHEL 9.3 | 2023-Q4 | RHEL 9.3 — image mode preview, toolbox v3 | Not yet verified |
| RHEL 9.2 | 2023-Q2 | RHEL 9.2 — OpenSSL 3.0.7, SELinux udica | Not yet verified |
| Ubuntu 24.04 | 2024-Q2 | Ubuntu 24.04 LTS — kernel 6.8, systemd 255 | Not yet verified |
| Ubuntu 22.04 | 2022-Q2 | Ubuntu 22.04 LTS — kernel 5.15, OpenSSL 3.0 | Not yet verified |

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
