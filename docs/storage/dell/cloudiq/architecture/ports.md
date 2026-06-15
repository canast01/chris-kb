---
tags:
  - cloudiq
  - dell
  - networking
  - firewall
  - ports
  - monitoring
---
# Dell CloudIQ — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell CloudIQ. CloudIQ is Dell's SaaS analytics and health monitoring platform. All Dell storage arrays that participate in CloudIQ must reach the CloudIQ cloud service via outbound HTTPS.

*Applies to: CloudIQ (SaaS)*
</div>

```text
┌──────────────────────────────────────────── Dell CloudIQ ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              CloudIQ: AI-powered cloud storage management and analytics platform              │   │
│   │                Protocols: HTTPS REST API · SMTP alerts · SCG telemetry protocol               │   │
│   │                                   Management: CloudIQ portal                                  │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │          Collection         │  │         SCG adapter         │  │       Array telemetry       │   │
│   │          Transport          │  │         HTTPS tunnel        │  │       Encrypted relay       │   │
│   │          Analytics          │  │         AIOps engine        │  │        Health scoring       │   │
│   │           Alerting          │  │        Email/webhook        │  │       Threshold rules       │   │
│   │          Reporting          │  │      Capacity forecast      │  │        Trend analysis       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │       Config      │       Auth       │      Notes       │   │
│   │   SCG gateway    │ Telemetry relay  │     On-prem VM    │   Certificate    │   One per site   │   │
│   │   CloudIQ SaaS   │ Analytics portal │    Managed SaaS   │      OAuth2      │   Dell-hosted    │   │
│   │     REST API     │    Automation    │    Token-based    │       JWT        │   GraphQL also   │   │
│   │   Alert engine   │  Notifications   │   Threshold rule  │  Email/webhook   │   Configurable   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: CloudIQ SaaS (cloud-hosted) · SCG gateways on-prem · connected Dell arrays               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CloudIQ            = Dell SaaS AIOps; monitors PowerStore, Unity, PowerMax, PowerScale arrays      │
│    SCG                = Secure Connect Gateway; on-prem agent that relays telemetry to CloudIQ        │
│    Health score       = composite 0-100 metric for array wellness; drops when alert conditions fire   │
│    Proactive rec.     = AI-generated recommendations for firmware, config, and capacity actions       │
│    Capacity IQ        = CloudIQ module; forecasts when arrays will reach configured capacity thresho  │
│    Performance IQ     = CloudIQ module; identifies latency anomalies and I/O bottlenecks over time    │
│    Wellness           = overall system health dashboard; aggregates all monitored arrays in one view  │
│    API token          = CloudIQ personal access token; use for REST and GraphQL API authentication    │
│    Webhook alert      = HTTP POST to external SIEM/ticketing endpoint on CloudIQ alert trigger        │
│    Workload planner   = CloudIQ tool for predicting impact of planned workload migrations             │
│    Tag                = user-defined key-value label applied to arrays for grouping and portal filte  │
│    Site               = logical grouping of arrays by physical location within CloudIQ hierarchy      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## How It Works

CloudIQ is a SaaS service — no on-premise CloudIQ server exists. Storage arrays send telemetry outbound to `cloudiq.dell.com`. Admin access is via browser to `cloudiq.dell.com` directly.

## Outbound — Array to CloudIQ (Required for Participation)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Storage array management IP | cloudiq.dell.com, *.dell.com | Telemetry upload, capacity and health data |

This applies to all CloudIQ-participating arrays:
- Dell PowerStore
- Dell PowerScale
- Dell PowerMax / VMAX
- Dell Unity XT
- Dell Data Domain / PowerProtect DD
- Dell ECS

## Admin Access (SaaS — No On-Prem Rules Needed)

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | cloudiq.dell.com | Admin browser access to CloudIQ dashboards |

## Firewall Summary

| From | To | Ports | Notes |
|---|---|---|---|
| All managed arrays (mgmt IPs) | cloudiq.dell.com | 443 | Required for CloudIQ participation — outbound only |
| Admin browsers | cloudiq.dell.com | 443 | SaaS access — no on-prem rules needed |

## Verify

```bash
# From array management network — test CloudIQ connectivity
curl -sk -o /dev/null -w "%{http_code}" https://cloudiq.dell.com/
# Expected: 200 or 302
```

## See also

- [Dell CloudIQ — Architecture](how-it-works/)
- [Dell PowerStore — Ports](../../powerstore/architecture/ports/)
- [Dell PowerScale — Ports](../../powerscale/architecture/ports/)
