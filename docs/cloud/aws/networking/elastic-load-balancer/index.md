# AWS Elastic Load Balancer


<div class="kb-summary">
AWS Elastic Load Balancer reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌────────────────────────────── Elastic Load Balancer — ALB / NLB / GWLB ───────────────────────────────┐
│                                                                                                       │
│  ELB distributes inbound traffic across targets; ALB for HTTP, NLB for TCP, GWLB for appliances.      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                ALB (Layer 7)                 │  │                NLB (Layer 4)                │   │
│   │          HTTP/HTTPS listener rules           │  │             TCP/UDP/TLS listener            │   │
│   │           Path/host/header routing           │  │        Static IP per AZ; EIP support        │   │
│   │      WAF integration; auth with Cognito      │  │       Ultra-low latency; millions RPS       │   │
│   │       Redirect/fixed-response actions        │  │        Preserve source IP to targets        │   │
│   │      Target: instance, IP, Lambda, ALB       │  │          Target: instance, IP, ALB          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Listeners route to target groups; health checks determine which targets receive traffic.             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Target Groups                 │  │             Health & Access Logs            │   │
│   │         Protocol: HTTP/HTTPS/TCP/UDP         │  │     Health check: path, interval, codes     │   │
│   │      Deregistration delay: drain conns       │  │       Access logs: S3 bucket delivery       │   │
│   │      Stickiness: LB or app-based cookie      │  │          Connection logs: NLB only          │   │
│   │     Slow start: ramp traffic to targets      │  │       CloudWatch metrics: RequestCount      │   │
│   │       Cross-zone load balancing option       │  │          Deletion protection toggle         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS regional ELB nodes per AZ · ENI attached to VPC subnets · Global backbone                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ALB             = Application Load Balancer; Layer 7; routes on HTTP attributes                      │
│  NLB             = Network Load Balancer; Layer 4; routes on TCP/UDP/TLS                              │
│  GWLB            = Gateway Load Balancer; routes traffic through third-party appliances               │
│  Listener        = Protocol+port entry point on the load balancer; holds routing rules                │
│  Rule            = ALB condition + action; evaluated in priority order per listener                   │
│  Target group    = Set of registered targets with a common health check configuration                 │
│  Stickiness      = Session affinity directing a client to the same target repeatedly                  │
│  Deregistration delay= Time targets drain existing connections after deregistration                   │
│  Cross-zone LB   = Distributes requests evenly across all targets in all enabled AZs                  │
│  Access logs     = Per-request records delivered to S3: time, client, target, response                │
│  WAF integration = ALB can enforce AWS WAF web ACL on inbound HTTP requests                           │
│  EIP on NLB      = Elastic IP assigned to NLB node per AZ; stable IP for allowlisting                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────── Elastic Load Balancer — ALB / NLB / GWLB ───────────────────────────────┐
│                                                                                                       │
│  ELB distributes inbound traffic across targets; ALB for HTTP, NLB for TCP, GWLB for appliances.      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                ALB (Layer 7)                 │  │                NLB (Layer 4)                │   │
│   │          HTTP/HTTPS listener rules           │  │             TCP/UDP/TLS listener            │   │
│   │           Path/host/header routing           │  │        Static IP per AZ; EIP support        │   │
│   │      WAF integration; auth with Cognito      │  │       Ultra-low latency; millions RPS       │   │
│   │       Redirect/fixed-response actions        │  │        Preserve source IP to targets        │   │
│   │      Target: instance, IP, Lambda, ALB       │  │          Target: instance, IP, ALB          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Listeners route to target groups; health checks determine which targets receive traffic.             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Target Groups                 │  │             Health & Access Logs            │   │
│   │         Protocol: HTTP/HTTPS/TCP/UDP         │  │     Health check: path, interval, codes     │   │
│   │      Deregistration delay: drain conns       │  │       Access logs: S3 bucket delivery       │   │
│   │      Stickiness: LB or app-based cookie      │  │          Connection logs: NLB only          │   │
│   │     Slow start: ramp traffic to targets      │  │       CloudWatch metrics: RequestCount      │   │
│   │       Cross-zone load balancing option       │  │          Deletion protection toggle         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS regional ELB nodes per AZ · ENI attached to VPC subnets · Global backbone                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ALB             = Application Load Balancer; Layer 7; routes on HTTP attributes                      │
│  NLB             = Network Load Balancer; Layer 4; routes on TCP/UDP/TLS                              │
│  GWLB            = Gateway Load Balancer; routes traffic through third-party appliances               │
│  Listener        = Protocol+port entry point on the load balancer; holds routing rules                │
│  Rule            = ALB condition + action; evaluated in priority order per listener                   │
│  Target group    = Set of registered targets with a common health check configuration                 │
│  Stickiness      = Session affinity directing a client to the same target repeatedly                  │
│  Deregistration delay= Time targets drain existing connections after deregistration                   │
│  Cross-zone LB   = Distributes requests evenly across all targets in all enabled AZs                  │
│  Access logs     = Per-request records delivered to S3: time, client, target, response                │
│  WAF integration = ALB can enforce AWS WAF web ACL on inbound HTTP requests                           │
│  EIP on NLB      = Elastic IP assigned to NLB node per AZ; stable IP for allowlisting                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Elastic Load Balancer notes for day-to-day infrastructure operations.

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
