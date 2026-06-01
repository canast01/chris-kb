# AWS Network ACLs


<div class="kb-summary">
AWS Network ACLs reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```bash
┌────────────────────────────── Network ACLs — Stateless Subnet Firewall ───────────────────────────────┐
│                                                                                                       │
│  Network ACLs provide stateless subnet-level traffic filtering; processed in rule-number order.       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             NACL Characteristics             │  │                Rule Structure               │   │
│   │     Stateless: return traffic needs rule     │  │      Rule number: 1–32766 (lower first)     │   │
│   │    Applies to whole subnet (not instance)    │  │          Protocol: TCP/UDP/ICMP/All         │   │
│   │      Default NACL: allow all in and out      │  │         Port range: single or range         │   │
│   │       Custom NACL: deny all by default       │  │               Source/dest CIDR              │   │
│   │        One NACL per subnet; reusable         │  │            Action: Allow or Deny            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  NACLs evaluate each packet independently; security groups track connection state instead.            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Common Use Patterns              │  │            NACL vs Security Group           │   │
│   │      Block specific IPs across all VMs       │  │       NACL: subnet boundary; stateless      │   │
│   │      Ephemeral return ports: 1024–65535      │  │       SG: instance boundary; stateful       │   │
│   │     Explicit deny before wildcard allow      │  │        Use both for defence in depth        │   │
│   │      Inbound + matching outbound rules       │  │        NACL cannot reference SG by ID       │   │
│   │      Low rule numbers: highest priority      │  │      SG: no explicit deny; default deny     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS VPC data plane · Hypervisor-enforced packet filtering at subnet boundary                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Stateless       = Each packet evaluated independently; no connection state tracked                   │
│  Rule number     = Lower numbers processed first; first match terminates evaluation                   │
│  * rule          = Implicit deny-all catch-all at the end; cannot be removed                          │
│  Ephemeral ports = 1024–65535; required in outbound rules for TCP response traffic                    │
│  Inbound rules   = Filter traffic entering the subnet from outside                                    │
│  Outbound rules  = Filter traffic leaving the subnet; needed for return traffic                       │
│  Default NACL    = VPC-default NACL allows all inbound and outbound traffic                           │
│  Custom NACL     = New NACL denies all traffic until rules are explicitly added                       │
│  CIDR block      = IP address range in NACL rule; can be /32 for a single IP                          │
│  Subnet association= A subnet can only be associated with one NACL at a time                          │
│  Defence in depth= Use NACLs + security groups together for layered network security                  │
│  Allow before deny= Implicit deny; explicit allow rules required for desired traffic                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Network ACLs notes for day-to-day infrastructure operations.

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
