---
tags:
  - aws
  - networking
---
# AWS Route 53


<div class="kb-summary">
AWS Route 53 reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌────────────────────────────────── Route 53 — DNS & Traffic Routing ───────────────────────────────────┐
│                                                                                                       │
│  Route 53 provides authoritative DNS, health checks, and intelligent traffic routing policies.        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Hosted Zones                 │  │                 Record Types                │   │
│   │      Public: authoritative for internet      │  │               A: IPv4 address               │   │
│   │       Private: VPC-internal resolution       │  │              AAAA: IPv6 address             │   │
│   │         Zone delegation: NS records          │  │         CNAME: canonical name alias         │   │
│   │       DNSSEC: signing for public zones       │  │         Alias: AWS resource pointer         │   │
│   │       Transfer lock: prevent hijacking       │  │         MX/TXT/SRV/CAA record types         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Routing policies control how Route 53 responds; health checks remove unhealthy endpoints.            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Routing Policies               │  │                Health Checks                │   │
│   │        Simple: single value returned         │  │        Endpoint: HTTP/HTTPS/TCP check       │   │
│   │          Weighted: percentage split          │  │       Calculated: combine child checks      │   │
│   │       Failover: primary/secondary pair       │  │        CloudWatch alarm: metric-based       │   │
│   │        Latency: lowest latency region        │  │          Interval: 30s or 10s fast          │   │
│   │       Geolocation/Geoproximity routing       │  │       SNS alert on health state change      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  100+ globally distributed Route 53 edge locations · Anycast IP infrastructure                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Hosted zone     = Container for DNS records for a domain; public or private scoped                   │
│  Alias record    = Route 53 extension mapping a DNS name to an AWS resource endpoint                  │
│  TTL             = Time-to-live; how long resolvers cache a DNS response in seconds                   │
│  Weighted policy = Splits traffic by weight ratio, e.g. 70/30 for canary deployments                  │
│  Failover policy = Routes to primary; falls back to secondary when health check fails                 │
│  Latency policy  = Routes to AWS region with lowest latency for the client                            │
│  Geolocation     = Routes based on geographic location of the requesting resolver                     │
│  Geoproximity    = Routes based on distance; bias shifts boundary toward a region                     │
│  Private zone    = Hosted zone that resolves only within associated VPCs                              │
│  DNSSEC          = Signs zone records; resolvers validate signature chain to root                     │
│  Health check    = Route 53 probe; removes unhealthy endpoints from DNS responses                     │
│  Resolver        = Inbound/outbound endpoints for hybrid DNS query forwarding                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Route 53 notes for day-to-day infrastructure operations.

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

```bash
# Add environment-specific commands here
```

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
