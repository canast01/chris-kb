# AWS Route Tables


<div class="kb-summary">
AWS Route Tables reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌───────────────────────────────── Route Tables — VPC Traffic Routing ──────────────────────────────────┐
│                                                                                                       │
│  Route tables control how traffic is directed within a VPC; each subnet has one route table.          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Route Table Types               │  │             Route Entry Targets             │   │
│   │    Main: default for unassociated subnets    │  │      Internet Gateway: public internet      │   │
│   │     Custom: explicit subnet association      │  │        NAT Gateway: private outbound        │   │
│   │      Gateway: edge routing for IGW/VGW       │  │         TGW: transit gateway routing        │   │
│   │        Local: VPC CIDR always present        │  │          VPC Peering: peer VPC CIDR         │   │
│   │        One route table per subnet max        │  │       Virtual Private Gateway: VPN/DX       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Longest prefix match determines which route applies; local VPC route cannot be deleted.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Common Patterns                │  │              Route Propagation              │   │
│   │        Public subnet: 0.0.0.0/0 → IGW        │  │       VGW propagation: VPN BGP routes       │   │
│   │       Private subnet: 0.0.0.0/0 → NAT        │  │      TGW route tables: segment traffic      │   │
│   │       On-prem: 10.0.0.0/8 → VGW or TGW       │  │       Blackhole: drop matching traffic      │   │
│   │       VPC peering: specific peer CIDRs       │  │      Active routes: propagated + static     │   │
│   │      Middlebox: route via appliance ENI      │  │      Edge RT: service insertion at IGW      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS VPC hypervisor routing fabric · Transit Gateway physical nodes per region                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Route table     = Set of rules (routes) that determine where network traffic is directed             │
│  Local route     = VPC CIDR route always present; allows inter-subnet communication                   │
│  Main route table= Default table applied to subnets not explicitly associated elsewhere               │
│  Gateway RT      = Special route table associated with IGW or VGW for edge routing                    │
│  Longest prefix  = Most specific matching route wins; /32 beats /24 beats /0                          │
│  Route propagation= VGW or TGW automatically populates routes from BGP advertisements                 │
│  Blackhole route = Route pointing to a deleted or non-existent target; drops traffic                  │
│  Middlebox route = Traffic directed through a network appliance ENI for inspection                    │
│  TGW route table = Transit Gateway has its own route tables separate from VPC tables                  │
│  VGW             = Virtual Private Gateway; attachment point for VPN and Direct Connect               │
│  Active route    = Route in active use; a route can be static or propagated                           │
│  Subnet association= Linking a subnet to a specific route table; overrides main table                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Route Tables notes for day-to-day infrastructure operations.

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
