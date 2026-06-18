---
tags:
  - troubleshooting
  - dell-aiops
  - dell
  - known-issues
---
# Dell AIOps — Known Issues and Error Codes

<div class="kb-summary">
Dell AIOps is a SaaS analytics layer on CloudIQ. All operational issues relate to CloudIQ connectivity or portal access — see Dell CloudIQ known issues for full coverage.

*Applies to: Dell AIOps / CloudIQ AIOps*
</div>

```text
┌──────────────────────────────────────── Dell AIOps / CloudIQ ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        AI-driven storage observability — telemetry, anomaly detection, recommendations        │   │
│   │                 Protocols: HTTPS (collector) · REST API · syslog · SMTP alerts                │   │
│   │          Management: CloudIQ web portal · REST API · email digest · Slack integration         │   │
│   │            Array telemetry -> CloudIQ ingest -> ML model -> anomaly alert -> action           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Collection         │  │       Array telemetry       │  │       Pushed via HTTPS      │   │
│   │          Analytics          │  │      ML anomaly engine      │  │     Cloud-side AI model     │   │
│   │           Alerting          │  │      Notification rules     │  │     Email / Slack / API     │   │
│   │         Integration         │  │      ServiceNow / ITSM      │  │     Auto-incident create    │   │
│   │          Inventory          │  │        Asset catalog        │  │     Contracts + versions    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  CloudIQ cloud   │ Analytics portal │     HTTPS 443     │     Dell SSO     │ SaaS; no on-prem │   │
│   │   Array agent    │  Telemetry push  │   HTTPS 443 out   │     API key      │  Outbound only   │   │
│   │     ML model     │Anomaly detection │      Internal     │       N/A        │ Fleet-trained ML │   │
│   │  ITSM connector  │Incident creation │     HTTPS REST    │  OAuth / token   │ServiceNow / Jira │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: Dell arrays (PowerStore/Unity/PowerMax) -> CloudIQ SaaS portal -> IT ops team              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CloudIQ      = Dell SaaS analytics platform for storage and compute observability                    │
│  AIOps        = AI for IT Operations; ML-driven anomaly detection and root-cause                      │
│  Telemetry    = array performance and capacity metrics pushed to CloudIQ hourly                       │
│  Anomaly      = ML-detected deviation from baseline; scored by impact level                           │
│  Health score = composite 0-100 metric per array; lower means more issues                             │
│  Recommendation = CloudIQ suggested action to improve efficiency or fix anomaly                       │
│  Proactive alert = early warning before threshold breach causes outage                                │
│  Connectivity = CloudIQ requires outbound HTTPS from array/proxy to Dell cloud                        │
│  Asset tag    = Dell serial used to associate array with a CloudIQ tenant                             │
│  Digest       = scheduled email summary of health scores and top anomalies                            │
│  Bandwidth throttle = CloudIQ limits telemetry rate to avoid impacting array perf                     │
│  SaaS         = CloudIQ is fully cloud-hosted; no on-premises deployment option                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Dell AIOps is fully SaaS-based; no on-premises AIOps software exists.
- All AIOps data flows through CloudIQ; connectivity and data issues are CloudIQ issues.

## Connectivity and Data

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| AIOps recommendations not appearing | AIOps | Array not sending telemetry to CloudIQ | Verify array phone-home (TCP 443 to cloudiq.dell.com); see [CloudIQ Known Issues](../../cloudiq/troubleshooting/known-issues/) | N/A |
| AIOps portal shows stale predictions | AIOps | CloudIQ data lag (up to 24h for analytics engine refresh) | Wait 24 hours; if persistent, contact Dell support | N/A |

## See also

- [Dell CloudIQ — Known Issues](../../cloudiq/troubleshooting/known-issues.md)
