# AWS AWS Config


<div class="kb-summary">
AWS AWS Config reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────────────── AWS Governance — AWS Config ─────────────────────────────────────┐
│                                                                                                       │
│  Config records resource inventory, tracks changes, and evaluates compliance rules.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Resource Recording              │  │                 Config Rules                │   │
│   │       Recorder: all or selected types        │  │         Managed: AWS pre-built rules        │   │
│   │         Configuration item: snapshot         │  │            Custom: Lambda-backed            │   │
│   │           Timeline: change history           │  │         Trigger: change or periodic         │   │
│   │          Delivery: S3 bucket + SNS           │  │        Result: Compliant/NonCompliant       │   │
│   │          Org aggregator: multi-acct          │  │           Conformance pack: bundle          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Recorder captures state; rules evaluate against that state; aggregator consolidates                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Remediation                  │  │                 Common Rules                │   │
│   │           Auto: SSM Automation doc           │  │       s3-bucket-public-read-prohibited      │   │
│   │            Manual: console review            │  │         ec2-instance-managed-by-ssm         │   │
│   │           Retry: on failure config           │  │              encrypted-volumes              │   │
│   │         EventBridge: trigger action          │  │      mfa-enabled-for-iam-console-access     │   │
│   │         Exceptions: suppress finding         │  │              cloudtrail-enabled             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Config service · S3 (history) · SNS · SSM (remediation) · Security Hub (findings)                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Configuration item= Point-in-time snapshot of resource state and relationships                       │
│  Recorder        = Config component capturing resource configuration changes                          │
│  Config rule     = Evaluates resources against desired configuration state                            │
│  Managed rule    = Pre-built rule maintained by AWS; parameterised                                    │
│  Custom rule     = Lambda function evaluating resource config with custom logic                       │
│  Conformance pack= YAML template bundling multiple Config rules and remediations                      │
│  Aggregator      = Collects Config data from multiple accounts/regions centrally                      │
│  Auto remediation= SSM Automation document triggered on NonCompliant finding                          │
│  Compliance score= % of resources Compliant across all evaluated rules                                │
│  Change trigger  = Rule evaluates when resource configuration changes                                 │
│  Periodic trigger= Rule evaluates on schedule (every 1/3/6/12/24 hours)                               │
│  Exception       = Suppresses a specific NonCompliant finding for a known reason                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── AWS Governance — AWS Config ─────────────────────────────────────┐
│                                                                                                       │
│  Config records resource inventory, tracks changes, and evaluates compliance rules.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Resource Recording              │  │                 Config Rules                │   │
│   │       Recorder: all or selected types        │  │         Managed: AWS pre-built rules        │   │
│   │         Configuration item: snapshot         │  │            Custom: Lambda-backed            │   │
│   │           Timeline: change history           │  │         Trigger: change or periodic         │   │
│   │          Delivery: S3 bucket + SNS           │  │        Result: Compliant/NonCompliant       │   │
│   │          Org aggregator: multi-acct          │  │           Conformance pack: bundle          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Recorder captures state; rules evaluate against that state; aggregator consolidates                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Remediation                  │  │                 Common Rules                │   │
│   │           Auto: SSM Automation doc           │  │       s3-bucket-public-read-prohibited      │   │
│   │            Manual: console review            │  │         ec2-instance-managed-by-ssm         │   │
│   │           Retry: on failure config           │  │              encrypted-volumes              │   │
│   │         EventBridge: trigger action          │  │      mfa-enabled-for-iam-console-access     │   │
│   │         Exceptions: suppress finding         │  │              cloudtrail-enabled             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Config service · S3 (history) · SNS · SSM (remediation) · Security Hub (findings)                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Configuration item= Point-in-time snapshot of resource state and relationships                       │
│  Recorder        = Config component capturing resource configuration changes                          │
│  Config rule     = Evaluates resources against desired configuration state                            │
│  Managed rule    = Pre-built rule maintained by AWS; parameterised                                    │
│  Custom rule     = Lambda function evaluating resource config with custom logic                       │
│  Conformance pack= YAML template bundling multiple Config rules and remediations                      │
│  Aggregator      = Collects Config data from multiple accounts/regions centrally                      │
│  Auto remediation= SSM Automation document triggered on NonCompliant finding                          │
│  Compliance score= % of resources Compliant across all evaluated rules                                │
│  Change trigger  = Rule evaluates when resource configuration changes                                 │
│  Periodic trigger= Rule evaluates on schedule (every 1/3/6/12/24 hours)                               │
│  Exception       = Suppresses a specific NonCompliant finding for a known reason                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS AWS Config notes for day-to-day infrastructure operations.

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
