---
tags:
  - troubleshooting
  - cloudiq
  - dell
  - known-issues
---
# Dell CloudIQ — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known CloudIQ bugs, error codes, and workarounds. CloudIQ is a SaaS platform — most issues are phone-home connectivity from on-premises arrays or SaaS portal access.

*Applies to: Dell CloudIQ SaaS*
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


## Before you begin

- CloudIQ phone-home uses outbound TCP 443 from array management IPs to `cloudiq.dell.com` and `esrs.dell.com`.
- Array connectivity issues show as `Array offline` in CloudIQ portal.
- Portal issues: check `status.dell.com` for CloudIQ outage status.

## Array Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Array shows `Offline` in CloudIQ | Any | TCP 443 blocked from array management IP to cloudiq.dell.com | Open firewall; verify: `curl -sk https://cloudiq.dell.com` from array management network | N/A |
| Data stale in CloudIQ despite array healthy | Any | ESRS gateway connectivity intermittent | Check ESRS gateway (on-premises connector) status; restart ESRS gateway service | N/A |
| Array registered but no metrics visible | Any | Initial data collection takes up to 24 hours | Wait 24 hours post-registration before raising issue | N/A |

## Portal

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Login failed` to cloudiq.dell.com | N/A | SSO provider (Dell SSO) unavailable | Check `status.dell.com`; try alternate browser; clear cookies | N/A |
| Alert emails not arriving | N/A | Notification rule disabled or email filter | Check CloudIQ → Notification Rules; verify email not in spam | N/A |

## See also

- [Dell CloudIQ — Common Issues](common-issues.md)
- [Dell PowerStore — Known Issues](../../powerstore/troubleshooting/known-issues/)
