---
tags:
  - troubleshooting
  - pure1
  - pure-storage
  - known-issues
---
# Pure1 — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Pure1 issues covering array connectivity, portal access, and data display problems. Pure1 is a SaaS platform — most issues are phone-home connectivity from arrays.

*Applies to: Pure1 cloud portal*
</div>

```text
┌──────────────────────────────────────────────── Pure1 ────────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Cloud management portal — health, analytics, AI workload planning, licensing         │   │
│   │               Protocols: HTTPS (UI) · REST API · phonehome (HTTPS 443 outbound)               │   │
│   │             Management: Pure1 web portal · REST API · mobile app · alert webhooks             │   │
│   │            Array phonehome -> Pure1 ingest -> AI model -> health/capacity dashboard           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Collection         │  │       Phonehome agent       │  │     HTTPS out, per array    │   │
│   │          Analytics          │  │         AI/ML engine        │  │       Cloud-side model      │   │
│   │            Portal           │  │         Pure1 web UI        │  │       Fleet-wide view       │   │
│   │          Licensing          │  │        Evergreen mgmt       │  │     Capacity entitlement    │   │
│   │            Alerts           │  │       Webhook / email       │  │       Threshold based       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   Pure1 portal   │ Fleet management │     HTTPS 443     │     Pure SSO     │ SaaS; no on-prem │   │
│   │    Phonehome     │ Telemetry upload │   HTTPS 443 out   │    Array cert    │No inbound needed │   │
│   │    AI engine     │ Capacity predict │      Internal     │       N/A        │ Fleet-trained ML │   │
│   │     REST API     │Portal automation │     HTTPS 443     │    API token     │  Pipeline mgmt   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: FlashArray/FlashBlade -> phonehome HTTPS -> Pure cloud -> Pure1 portal                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Pure1        = Pure Storage SaaS management and analytics portal                                     │
│  Phonehome    = Purity outbound telemetry to Pure1 cloud (HTTPS 443)                                  │
│  Array registration = linking a FlashArray/Blade serial to a Pure1 org account                        │
│  Fleet        = all arrays registered to a Pure1 organization                                         │
│  AI prediction = Pure1 ML-based capacity runout and performance headroom forecast                     │
│  Health score = per-array composite score; drives SLA and proactive support                           │
│  Workload     = Pure1 per-volume performance and latency tracking entity                              │
│  Evergreen mgmt = Pure1 shows current entitlement, capacity usage, upgrade eligibility                │
│  Alert        = Pure1 threshold breach or anomaly notification (email/webhook)                        │
│  REST API     = Pure1 programmatic interface for fleet data and alert management                      │
│  Tagging      = user-defined labels on arrays in Pure1 for filtering/grouping                         │
│  Proxy        = optional on-prem proxy for phonehome if direct internet blocked                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Pure1 issues are either phone-home connectivity (array side) or portal access (browser side).
- Array connectivity: verify outbound TCP 443 from array management IP to `pure1.purestorage.com`.
- Portal issues: log in at `pure1.purestorage.com`; contact Pure Storage support if portal is unavailable.

## Array Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Array shows `Offline` in Pure1 | All | TCP 443 blocked from array management IP to pure1.purestorage.com | Open firewall; test: `curl -sk https://pure1.purestorage.com` from array management network | N/A |
| Array connected but data stale >24 hours | All | Intermittent network drops interrupting telemetry upload | Check network stability from array management IP; review firewall session table for timeouts | N/A |
| `puremessage test` returns `Connection failed` | Purity 6.x | Proxy required but not configured | Configure HTTP proxy on array: `purearray setattr --proxy http://<proxy>:<port>` | N/A |

## Portal Access

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Cannot log in to Pure1 portal | N/A | SSO federation issue or Pure1 outage | Try direct login at `pure1.purestorage.com`; check `status.purestorage.com` for outage | N/A |
| Array visible in Pure1 but showing no performance data | All | Array model not yet configured for full telemetry | Contact Pure support — some older models have limited telemetry | N/A |

## See also

- [Pure1 — Common Issues](common-issues.md)
- [Pure Storage FlashArray — Known Issues](../../flasharray/troubleshooting/known-issues/)
- [Pure Storage FlashBlade — Known Issues](../../flashblade/troubleshooting/known-issues/)
