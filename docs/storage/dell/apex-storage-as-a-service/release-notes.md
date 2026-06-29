---
tags:
  - dell
---
# Dell Apex Storage-as-a-Service — Release Notes

*Applies to: Dell EMC Storage*

<div class="kb-summary">
Version history and release notes for Dell Apex Storage-as-a-Service.
</div>

![Release Notes](../../../assets/apex-storage-as-a-service-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 2024.3 | 2024-Q3 | Apex STaaS 2024.3 — PowerMax NVMe tier addition | [Release Notes](#) |
| 2024.1 | 2024-Q1 | Apex STaaS 2024.1 — sustainability SLA module | [Release Notes](#) |
| 2023.3 | 2023-Q3 | Apex STaaS 2023.3 — PowerStore flex tier GA | [Release Notes](#) |
| 2023.1 | 2023-Q1 | Apex STaaS 2023.1 — burst capacity on-demand | [Release Notes](#) |
| 2022.3 | 2022-Q3 | Apex STaaS 2022.3 — PowerScale object tier | [Release Notes](#) |

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
