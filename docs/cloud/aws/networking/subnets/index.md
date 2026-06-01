# AWS Subnets


<div class="kb-summary">
AWS Subnets reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────────────── Subnets — VPC Subnet Design ─────────────────────────────────────┐
│                                                                                                       │
│  Subnets divide a VPC CIDR into segments per AZ; public or private determined by route table.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Subnet Characteristics            │  │          Reserved IPs (per subnet)          │   │
│   │     Single AZ scope; no multi-AZ subnet      │  │             .0 — network address            │   │
│   │        CIDR sub-block of the VPC CIDR        │  │               .1 — VPC router               │   │
│   │         Minimum /28 (11 usable IPs)          │  │          .2 — Route 53 DNS resolver         │   │
│   │       No overlapping CIDRs within VPC        │  │               .3 — future use               │   │
│   │         Auto-assign public IP option         │  │         .255 — broadcast (unusable)         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Public vs private determined by route table; public has IGW default route; private uses NAT.         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Tier Design Pattern              │  │             CIDR Sizing Guidance            │   │
│   │      Public tier: ALB, NAT GW, bastion       │  │         Large app: /20 (4091 usable)        │   │
│   │       App tier: EC2, ECS, Lambda ENIs        │  │          Medium: /22 (1019 usable)          │   │
│   │       Data tier: RDS, ElastiCache, MSK       │  │           Small: /24 (251 usable)           │   │
│   │     Isolated: sensitive/restricted hosts     │  │           Lambda: /28 (11 minimum)          │   │
│   │      Replicate tier pattern across AZs       │  │      Always plan for Lambda ENI growth      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS AZ physical data centres · VPC fabric per region · Hypervisor network partitioning               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Subnet          = IPv4/IPv6 range within a VPC tied to one Availability Zone                         │
│  Public subnet   = Subnet whose default route points to an Internet Gateway                           │
│  Private subnet  = Subnet with no IGW route; outbound via NAT GW or VPC endpoints                     │
│  Reserved IPs    = AWS reserves 5 IPs per subnet; usable = 2^(32-prefix) - 5                          │
│  CIDR            = Classless Inter-Domain Routing; defines the IP range of the subnet                 │
│  AZ affinity     = Resources in a subnet run in the same physical AZ                                  │
│  Auto-assign IP  = Subnet setting giving EC2 instances a public IP at launch                          │
│  Subnet CIDR     = Must not overlap other subnets or secondary VPC CIDRs                              │
│  Lambda ENI      = Lambda in VPC creates ENI in each AZ subnet; plan capacity                         │
│  /16 VPC         = Max VPC size; provides 65,536 IPs to sub-allocate into subnets                     │
│  Tier isolation  = Place each app tier in separate subnets for NACL-level segmentation                │
│  Multi-AZ design = Create same-purpose subnets in 2–3 AZs for high availability                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Subnets — VPC Subnet Design ─────────────────────────────────────┐
│                                                                                                       │
│  Subnets divide a VPC CIDR into segments per AZ; public or private determined by route table.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Subnet Characteristics            │  │          Reserved IPs (per subnet)          │   │
│   │     Single AZ scope; no multi-AZ subnet      │  │             .0 — network address            │   │
│   │        CIDR sub-block of the VPC CIDR        │  │               .1 — VPC router               │   │
│   │         Minimum /28 (11 usable IPs)          │  │          .2 — Route 53 DNS resolver         │   │
│   │       No overlapping CIDRs within VPC        │  │               .3 — future use               │   │
│   │         Auto-assign public IP option         │  │         .255 — broadcast (unusable)         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Public vs private determined by route table; public has IGW default route; private uses NAT.         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Tier Design Pattern              │  │             CIDR Sizing Guidance            │   │
│   │      Public tier: ALB, NAT GW, bastion       │  │         Large app: /20 (4091 usable)        │   │
│   │       App tier: EC2, ECS, Lambda ENIs        │  │          Medium: /22 (1019 usable)          │   │
│   │       Data tier: RDS, ElastiCache, MSK       │  │           Small: /24 (251 usable)           │   │
│   │     Isolated: sensitive/restricted hosts     │  │           Lambda: /28 (11 minimum)          │   │
│   │      Replicate tier pattern across AZs       │  │      Always plan for Lambda ENI growth      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS AZ physical data centres · VPC fabric per region · Hypervisor network partitioning               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Subnet          = IPv4/IPv6 range within a VPC tied to one Availability Zone                         │
│  Public subnet   = Subnet whose default route points to an Internet Gateway                           │
│  Private subnet  = Subnet with no IGW route; outbound via NAT GW or VPC endpoints                     │
│  Reserved IPs    = AWS reserves 5 IPs per subnet; usable = 2^(32-prefix) - 5                          │
│  CIDR            = Classless Inter-Domain Routing; defines the IP range of the subnet                 │
│  AZ affinity     = Resources in a subnet run in the same physical AZ                                  │
│  Auto-assign IP  = Subnet setting giving EC2 instances a public IP at launch                          │
│  Subnet CIDR     = Must not overlap other subnets or secondary VPC CIDRs                              │
│  Lambda ENI      = Lambda in VPC creates ENI in each AZ subnet; plan capacity                         │
│  /16 VPC         = Max VPC size; provides 65,536 IPs to sub-allocate into subnets                     │
│  Tier isolation  = Place each app tier in separate subnets for NACL-level segmentation                │
│  Multi-AZ design = Create same-purpose subnets in 2–3 AZs for high availability                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Subnets notes for day-to-day infrastructure operations.

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
