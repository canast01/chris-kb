# AWS Security Groups

```text
┌──────────────────────────── Security Groups — Stateful Instance Firewall ─────────────────────────────┐
│                                                                                                       │
│  Security groups act as virtual firewalls for ENIs; stateful — return traffic is automatic.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Security Group Characteristics        │  │                Rule Structure               │   │
│   │    Stateful: return traffic auto-allowed     │  │          Protocol: TCP/UDP/ICMP/All         │   │
│   │      Allow rules only; no explicit deny      │  │              Port or port range             │   │
│   │       Applied to ENI; multiple per ENI       │  │      Source/dest: CIDR or SG reference      │   │
│   │      All rules evaluated (no ordering)       │  │          Description field per rule         │   │
│   │     Default SG: allows all within group      │  │        Inbound and outbound rule sets       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Reference another SG as source/dest to allow traffic between grouped resources.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Best Practices                │  │               Common Patterns               │   │
│   │     Least privilege: minimal open ports      │  │       Web tier SG: 443 from 0.0.0.0/0       │   │
│   │     SG reference instead of CIDR ranges      │  │        App SG: port from web SG only        │   │
│   │       Prefix lists: managed CIDR sets        │  │         DB SG: 5432 from app SG only        │   │
│   │     Tag SGs: team, environment, purpose      │  │        Bastion SG: 22 from corp CIDR        │   │
│   │      Audit via Config rule: open rules       │  │       ELB SG: source ALB SG to targets      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS hypervisor network layer · ENI-level enforcement per EC2 host                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Security group  = Stateful virtual firewall applied to one or more ENIs                              │
│  ENI             = Elastic Network Interface; SGs attach here, not to instances directly              │
│  Stateful        = Connection tracking; return packets allowed without explicit outbound rule         │
│  Allow-only      = SGs have no deny rules; absence of allow = implicit deny                           │
│  SG reference    = Rule source/dest is another SG ID; allows dynamic group membership                 │
│  Default SG      = Created with each VPC; allows all inbound from same SG                             │
│  Prefix list     = Named collection of CIDRs usable as SG rule source/destination                     │
│  Rule evaluation = All rules processed; most permissive allow wins (no ordering)                      │
│  Chained SGs     = Web → app → DB using SG references creates least-privilege tiers                   │
│  Max per ENI     = Default 5 SGs per ENI; up to 16 with limit increase                                │
│  Inbound default = New custom SG has no inbound rules; all inbound denied                             │
│  Outbound default= New custom SG allows all outbound; restrict for compliance                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Security Groups notes for day-to-day infrastructure operations.

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
