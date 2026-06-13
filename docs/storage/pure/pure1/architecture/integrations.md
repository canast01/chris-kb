---
tags:
  - architecture
  - pure
---
# Pure1 — Integrations

<div class="kb-summary">
Pure1 integrates natively with FlashArray and FlashBlade via Purity OS telemetry, and outbound to ITSM systems, notification channels, and the Pure1 REST API for automation.
</div>

```text
┌────────────────────────────────── Pure1 — Architecture Integrations ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Array Sources                 │              Notification Targets              │   │
│   │       FlashArray//X (native phonehome)       │              Email: ops-storage@               │   │
│   │       FlashArray//C (native phonehome)       │           Webhook: ServiceNow/Slack            │   │
│   │       FlashBlade//S (native phonehome)       │                 Pure1 REST API                 │   │
│   │       FlashBlade//E (native phonehome)       │             Aria Ops Pure adapter              │   │
│   │            Pure Cloud Block Store            │             SIEM via syslog proxy              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Purity phonehome built-in · TCP 443 outbound from array · Pure cloud forwards alerts                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Native phonehome = Purity OS built-in; no additional agent or gateway needed                         │
│  Pure Cloud Block Store = FlashArray in AWS/Azure; also connected to Pure1                            │
│  REST API = Pure1 API for fleet-wide metric retrieval and management                                  │
│  Webhook = Pure1 outbound POST to webhook URL on proactive alert                                      │
│  ServiceNow = Pure1 alert forwarded as incident via webhook                                           │
│  Slack = Pure1 alert posted to storage team channel via webhook                                       │
│  Aria Ops adapter = PAK file pulling Pure1/FlashArray metrics into VMware Aria Operations             │
│  SIEM proxy = Script forwarding Pure1 API alerts to syslog for SIEM ingestion                         │
│  Pure1 API token = OAuth token for REST API; generated in Pure1 account settings                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
