---
tags:
  - security
---
# CyberArk — Release Notes

<div class="kb-summary">
Version history and release notes for CyberArk.
</div>

![Release Notes](../../assets/cyberark-release-notes.svg)

```d2
direction: right

center: "Cyberark" {shape: hexagon}
version_history: "Version History" {shape: rectangle}
key_terminology: "Key Terminology" {shape: rectangle}
upgrade_path: "Upgrade Path" {shape: rectangle}

center -> version_history
center -> key_terminology
center -> upgrade_path
```

## Before you begin

No special prerequisites — review the version table and cross-reference your deployed version before applying any update.


## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 14.2 | 2024-Q3 | CyberArk 14.2 — PAM360 integration improvements | [Release Notes](#) |
| 14.0 | 2024-Q1 | CyberArk 14.0 — CORA AI launch | [Release Notes](#) |
| 13.2 | 2023-Q3 | CyberArk 13.2 — EPM Mac Apple Silicon support | [Release Notes](#) |
| 13.0 | 2023-Q1 | CyberArk 13.0 — Identity Security platform | [Release Notes](#) |
| 12.6 | 2022-Q3 | CyberArk 12.6 — Conjur Cloud GA | [Release Notes](#) |

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
