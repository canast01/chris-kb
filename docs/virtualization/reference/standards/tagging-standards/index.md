# VMware Tagging Standards

Consistent tagging supports ownership, billing, backup policy, patch scheduling, and compliance.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│               Required Tags — Applied at VM Creation                     │
├─────────────────────┬────────────────────────────────────────────────────┤
│   Tag Category      │  Values                                            │
├─────────────────────┼────────────────────────────────────────────────────┤
│ Environment         │ prod │ dev │ test │ uat │ infra                    │
│ Application Owner   │ team-infra │ team-app01 │ team-db                  │
│ Business Unit       │ finance │ operations │ it                          │
│ Criticality         │ critical │ standard │ low                          │
│ Backup Policy       │ daily-30d │ weekly-14d │ none                      │
│ Patch Group         │ patch-group-a │ patch-group-b                      │
│ Support Group       │ infra-team │ app-team                              │
├─────────────────────┴────────────────────────────────────────────────────┤
│  Applied at: VM creation  │  Reviewed: quarterly  │  Owner: responsible  │
│  Enforcement: Backup tool uses Backup Policy tag for job scoping         │
└──────────────────────────────────────────────────────────────────────────┘
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
