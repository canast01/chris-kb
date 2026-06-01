# AWS Internet Gateway


<div class="kb-summary">
AWS Internet Gateway reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌──────────────────────────── Internet Gateway — VPC Internet Connectivity ─────────────────────────────┐
│                                                                                                       │
│  IGW provides bidirectional internet access for public subnets; performs NAT for Elastic IPs.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 IGW Function                 │  │        Requirements for Public Access       │   │
│   │      Horizontally scaled; HA by design       │  │           IGW attached to the VPC           │   │
│   │     No bandwidth limits or single points     │  │         Route table: 0.0.0.0/0 → IGW        │   │
│   │        1-to-1 NAT: EIP ↔ private IPv4        │  │         Subnet must be marked public        │   │
│   │       No NAT needed for IPv6 (native)        │  │      Instance needs EIP or auto-assign      │   │
│   │        Supports IPv4 and IPv6 traffic        │  │        Security group allows inbound        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  IGW enables inbound and outbound internet; Egress-only IGW for IPv6 outbound-only traffic.           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Egress-Only IGW (IPv6)            │  │              Related Components             │   │
│   │        Allows IPv6 outbound from VPC         │  │       NAT Gateway: IPv4 private subnet      │   │
│   │       Blocks inbound IPv6 connections        │  │       Route tables: per-subnet control      │   │
│   │      No EIP needed; uses instance IPv6       │  │        Elastic IP: static public IPv4       │   │
│   │     Attach to VPC; add route table rule      │  │      Security groups + NACLs: firewall      │   │
│   │         Free; no hourly/data charges         │  │        VPC Flow Logs: traffic capture       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS edge network · Regional backbone · ENIs on VPC subnet boundary infrastructure                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IGW             = Internet Gateway; horizontally scaled, redundant VPC component                     │
│  Public subnet   = Subnet whose route table has a default route (0.0.0.0/0) to an IGW                 │
│  Elastic IP      = Static public IPv4 address allocated to an AWS account                             │
│  1-to-1 NAT      = IGW translates EIP ↔ private IPv4 for inbound and outbound traffic                 │
│  Egress-only IGW = IPv6-only gateway allowing outbound but blocking inbound connections               │
│  Default route   = 0.0.0.0/0 or ::/0 route pointing to IGW for internet-bound traffic                 │
│  Attached state  = IGW must be in attached state to the VPC for traffic to flow                       │
│  Auto-assign IP  = Subnet setting that gives instances a public IP at launch from pool                │
│  IPv6 native     = No NAT needed; instances get globally routable /128 IPv6 address                   │
│  VPC routing     = Route table entries direct traffic; longest prefix match decides                   │
│  NAT Gateway     = Managed service for private subnet IPv4 outbound; not the IGW itself               │
│  HA design       = Single IGW is HA; do not run multiple IGWs for redundancy                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Internet Gateway notes for day-to-day infrastructure operations.

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
