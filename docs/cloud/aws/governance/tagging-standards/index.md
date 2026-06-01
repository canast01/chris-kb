# AWS Tagging Standards


<div class="kb-summary">
AWS Tagging Standards reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────────── AWS Governance — Tagging Standards ──────────────────────────────────┐
│                                                                                                       │
│  Mandatory tag schema for cost allocation, compliance, ownership, and automation.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Mandatory Tags                │  │                Optional Tags                │   │
│   │          Environment: prod/dev/test          │  │             Version: release tag            │   │
│   │          Owner: team or alias email          │  │              Backup: true/false             │   │
│   │           CostCentre: finance code           │  │             Patch Group: for SSM            │   │
│   │          Application: workload name          │  │          DataClassification: level          │   │
│   │           ManagedBy: terraform/cfn           │  │           Expiry: sandbox TTL date          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Mandatory tags enforced by SCP and Config; optional tags enable automation                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Enforcement                  │  │              Naming Convention              │   │
│   │        SCP: deny without required tag        │  │          Keys: PascalCase standard          │   │
│   │          Config: required-tags rule          │  │         Values: lowercase kebab-case        │   │
│   │          Tag policy: org-level case          │  │            No spaces: use hyphens           │   │
│   │         IaC: tags block per resource         │  │          Max: 50 tags per resource          │   │
│   │         Remediation: auto-tag Lambda         │  │         Review: monthly compliance %        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Organizations (tag policies) · Config · SCP engine · Cost Explorer · S3 (CUR)                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Tag policy      = Organizations policy enforcing allowed tag values and case                         │
│  required-tags   = Config managed rule detecting resources missing mandatory tags                     │
│  PascalCase      = Tag key convention: Environment, CostCentre, Owner                                 │
│  kebab-case      = Tag value convention: prod, dev, finance-123                                       │
│  ManagedBy       = Tag indicating IaC tool owning the resource lifecycle                              │
│  DataClassification= Tag indicating sensitivity: public, internal, confidential                       │
│  Expiry tag      = Date after which sandbox resource is auto-deleted by Lambda                        │
│  Patch Group     = SSM tag linking instance to patch baseline                                         │
│  Auto-tag Lambda = EventBridge-triggered Lambda applying default tags on resource create              │
│  Tag compliance  = % of resources with all required tags; tracked in Config                           │
│  Cost allocation = Tags activated in Billing console appear in CUR and Cost Explorer                  │
│  IaC tags block  = Terraform/CloudFormation resource property ensuring tags at deploy                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Tagging Standards notes for day-to-day infrastructure operations.

## Where It Fits

Use this page for build work, support checks, troubleshooting, standards, and operational review.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Confirm service health. |  |  |
| Review alerts. |  |  |
| Check recent changes. |  |  |
| Confirm capacity and performance are within normal range. |  |  |

## Health Commands

~~~bash
# Add environment-specific commands here
~~~

## Common Issues

- Misconfiguration after change work.
- Missing access or permissions.
- Alert noise without clear ownership.
- Drift from documented standards.

## Operational Tasks


| Task | Command |
|---|---|
| Review current configuration. |  |
| Validate dependencies. |  |
| Record changes. |  |
| Confirm monitoring coverage. |  |

## Upgrade Notes

- Check release notes before upgrades.
- Validate backup or rollback options.
- Confirm maintenance window and communication plan.
- Test after the change.

## Best Practices


| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Document ownership. | Document ownership. |
| Use least privilege access. | Use least privilege access. |
| Validate changes after implementation. | Validate changes after implementation. |
