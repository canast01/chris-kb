# AWS Permission Review

```
┌────────────────────────────────── AWS Identity — Permission Review ───────────────────────────────────┐
│                                                                                                       │
│  Quarterly IAM review: remove unused principals, trim over-privileged policies.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Review Scope                 │  │                    Tools                    │   │
│   │          IAM users: last-used date           │  │         Credential report: all users        │   │
│   │         Access keys: 90-day rotation         │  │         Access Analyzer: ext access         │   │
│   │           Roles: last assumed date           │  │            IAM last-accessed data           │   │
│   │           Policies: unused actions           │  │          CloudTrail: API usage data         │   │
│   │          Groups: membership correct          │  │          Security Hub: IAM findings         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Last-accessed data shows unused services; trim to what was actually used                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Remediation Actions              │  │                  Automation                 │   │
│   │          Delete: unused users/keys           │  │         Lambda: flag stale accounts         │   │
│   │         Disable: inactive keys first         │  │          Config: access-key-rotated         │   │
│   │         Trim: remove unused services         │  │         EventBridge: 90-day trigger         │   │
│   │         Detach: over-broad policies          │  │        Jira: auto-ticket per finding        │   │
│   │       Document: exceptions with expiry       │  │           Review: tracked in ITSM           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  IAM service · CloudTrail · Access Analyzer · Security Hub · Config · Lambda                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Credential report= CSV of all IAM users with password/key last-used dates                            │
│  Last-accessed data= Shows which AWS services a role/user has called in last 90 days                  │
│  Access Analyzer = Identifies IAM roles/S3/KMS accessible from outside the account                    │
│  Unused action   = API action granted by policy but never called in review period                     │
│  Stale account   = IAM user not logged in for > 90 days; candidate for deletion                       │
│  90-day trigger  = EventBridge rule firing when key age exceeds rotation threshold                    │
│  access-key-rotated= Config managed rule flagging keys older than specified days                      │
│  Over-privileged = Principal has more permissions than needed for their role                          │
│  Exception       = Documented justification for keeping broad permissions with expiry                 │
│  ITSM tracking   = Review findings tracked as tickets in ServiceNow or Jira                           │
│  Disable before delete= Inactivate key first; verify no breakage; then delete                         │
│  Security Hub findings= IAM-related CIS checks reported as findings in Security Hub                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Permission Review notes for day-to-day infrastructure operations.

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
