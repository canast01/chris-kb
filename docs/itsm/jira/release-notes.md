---
tags:
  - jira
description: "Version history and release notes for Jira."
---
# Jira — Release Notes

*Applies to: Jira*

<div class="kb-summary">
Version history and release notes for Jira.
</div>

![Release Notes](../../assets/jira-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 9.17 | 2024-Q3 | Jira Software 9.17 — Backlog import improvements | [Release Notes](#) |
| 9.15 | 2024-Q2 | Jira Software 9.15 — roadmap planning update | [Release Notes](#) |
| 9.12 | 2024-Q1 | Jira Software 9.12 — plan capacity enhancements | [Release Notes](#) |
| 9.4 | 2023-Q1 | Jira Software 9.4 — LTS baseline | [Release Notes](#) |
| 9.0 | 2022-Q3 | Jira Software 9.0 — project template updates | [Release Notes](#) |

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
