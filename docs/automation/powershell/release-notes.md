---
tags:
  - powershell
---
# PowerShell — Release Notes

<div class="kb-summary">
Version history and release notes for PowerShell.
</div>

![Release Notes](../../assets/powershell-release-notes.svg)

```d2
direction: right

center: "PowerShell" {shape: hexagon}
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
| 7.4 LTS | 2024-Q1 | PowerShell 7.4 LTS — .NET 8 baseline | [Release Notes](#) |
| 7.3 | 2022-Q4 | PowerShell 7.3 — tab completion improvements | [Release Notes](#) |
| 7.2 LTS | 2021-Q4 | PowerShell 7.2 LTS — .NET 6 baseline | [Release Notes](#) |
| 7.1 | 2020-Q4 | PowerShell 7.1 — ForEach-Object -Parallel GA | [Release Notes](#) |
| 7.0 | 2020-Q1 | PowerShell 7.0 GA — cross-platform LTS | [Release Notes](#) |

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
