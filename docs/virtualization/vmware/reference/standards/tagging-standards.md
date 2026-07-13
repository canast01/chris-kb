---
tags:
  - reference
description: "Consistent tagging supports ownership, billing, backup policy, patch scheduling, and compliance."
---
# VMware Tagging Standards

<div class="kb-summary">
Consistent tagging supports ownership, billing, backup policy, patch scheduling, and compliance.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

required_tags: "Required Tags" {shape: rectangle}
optional_tags: "Optional Tags" {shape: rectangle}
tagging_process: "Tagging Process" {shape: rectangle}

required_tags -> optional_tags: hardens
optional_tags -> tagging_process: hardens
```

## Required Tags

| Tag Category | Example Values |
|---|---|
| Application Owner | team-infra, team-app01 |
| Business Unit | finance, operations, it |
| Environment | prod, dev, test, infra |
| Criticality | critical, standard, low |
| Backup Policy | daily-30d, weekly-14d, none |
| Patch Group | patch-group-a, patch-group-b |
| Support Group | infra-team, app-team |

## Optional Tags

| Tag Category | Example Values |
|---|---|
| Compliance | pci, hipaa, gdpr |
| Temporary VM | true (include decommission date in notes) |
| Decommission Date | 2026-06-01 |

## Tagging Process

- Tags are applied at VM creation
- Owners are responsible for keeping tags current
- Tags are reviewed quarterly or as part of the access review process
