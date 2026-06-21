---
tags:
  - python
---
# Python — Release Notes

<div class="kb-summary">
Version history and release notes for Python.
</div>

![Release Notes](../../assets/python-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
| 3.13 | 2024-Q4 | Python 3.13 — free-threaded mode, JIT compiler preview | [Release Notes](#) |
| 3.12 | 2023-Q4 | Python 3.12 — improved error messages, f-string updates | [Release Notes](#) |
| 3.11 | 2022-Q4 | Python 3.11 — 10-60 % speed improvements | [Release Notes](#) |
| 3.10 | 2021-Q4 | Python 3.10 — structural pattern matching | [Release Notes](#) |
| 3.9 | 2020-Q4 | Python 3.9 — dict union operators, type hints | [Release Notes](#) |

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
