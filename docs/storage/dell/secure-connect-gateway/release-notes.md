---
tags:
  - dell
---
# Dell Secure Connect Gateway — Release Notes

<div class="kb-summary">
Version history and release notes for Dell Secure Connect Gateway.
</div>

![Release Notes](../../../assets/secure-connect-gateway-release-notes.svg)

```d2
direction: right

center: "Secure Connect Gateway" {shape: hexagon}
version_history: "Version History" {shape: rectangle}
key_terminology: "Key Terminology" {shape: rectangle}
upgrade_path: "Upgrade Path" {shape: rectangle}

center -> version_history
center -> key_terminology
center -> upgrade_path
```

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 5.16 | 2024-Q3 | SCG 5.16 — PowerMax 10.1 telemetry support | [Release Notes](#) |
| 5.14 | 2024-Q1 | SCG 5.14 — virtual edition scale improvements | [Release Notes](#) |
| 5.12 | 2023-Q3 | SCG 5.12 — REST API v2 | [Release Notes](#) |
| 5.10 | 2023-Q1 | SCG 5.10 — automated alert routing | [Release Notes](#) |
| 5.8 | 2022-Q3 | SCG 5.8 — proactive monitoring expansion | [Release Notes](#) |

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
