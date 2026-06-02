# AWS NAT Gateway


<div class="kb-summary">
AWS NAT Gateway reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌──────────────────────────── NAT Gateway — Private Subnet Outbound Access ─────────────────────────────┐
│                                                                                                       │
│  NAT Gateway enables private subnet instances to reach the internet without being reachable.          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              NAT Gateway Types               │  │                 Traffic Flow                │   │
│   │         Public: EIP, routes via IGW          │  │         Private subnet → route table        │   │
│   │       Private: VPC-to-VPC routing only       │  │          Route: 0.0.0.0/0 → NAT GW          │   │
│   │          Managed: HA within one AZ           │  │           NAT GW → IGW → internet           │   │
│   │      Up to 100 Gbps; 55,000 conns/host       │  │      Response: IGW → NAT GW → instance      │   │
│   │          No port 25 (SMTP) allowed           │  │       Inbound blocked: no unsolicited       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Deploy one NAT Gateway per AZ; route each AZ private subnet to its own NAT GW for HA.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  HA Pattern                  │  │                    Costs                    │   │
│   │       One NAT GW per AZ (3 for 3 AZs)        │  │           Hourly charge per NAT GW          │   │
│   │      Each AZ private route → local NAT       │  │          Data processing fee per GB         │   │
│   │       AZ failure: other AZs unaffected       │  │      Data transfer out: standard rates      │   │
│   │      No cross-AZ NAT GW sharing (cost)       │  │      Private NAT: no data transfer fee      │   │
│   │     NAT instance: cheaper but manual HA      │  │       Consider VPC endpoints to reduce      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS managed network infrastructure per AZ · Elastic IP from AWS pool · Regional backbone             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Public NAT GW   = NAT Gateway with an EIP; routes outbound through IGW to internet                   │
│  Private NAT GW  = NAT Gateway without EIP; used for private VPC-to-VPC routing                       │
│  SNAT            = Source NAT; replaces instance private IP with NAT GW EIP                           │
│  Connection tracking= NAT GW maintains state table mapping flows to return traffic                    │
│  Idle timeout    = NAT GW drops TCP connections idle for 350 seconds                                  │
│  Port exhaustion = >55,000 simultaneous connections to same dest IP:port causes drops                 │
│  NAT instance    = EC2-based alternative; user-managed; cheaper but no built-in HA                    │
│  Private subnet  = Subnet with no IGW route; relies on NAT GW for internet access                     │
│  AZ isolation    = Each AZ should have its own NAT GW for fault isolation                             │
│  VPC endpoint    = Alternative to NAT for AWS service access; no internet required                    │
│  Bandwidth limit = 100 Gbps max throughput; scales automatically up to limit                          │
│  Data processing = Per-GB charge applies for all traffic passing through NAT Gateway                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS NAT Gateway notes for day-to-day infrastructure operations.

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
