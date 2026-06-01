# CloudIQ — Integrations (Monitoring)

<div class="kb-summary">
CloudIQ integrates natively with Dell storage arrays via the SCG, and outbound to ITSM and notification systems via the REST API and webhook connectors.
</div>

```
┌───────────────────────────────── CloudIQ — Architecture Integrations ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Supported Arrays               │              Notification Targets              │   │
│   │        PowerStore: native integration        │           Email: SMTP to ops mailbox           │   │
│   │        PowerScale: native integration        │        Webhook: Slack/Teams/ServiceNow         │   │
│   │        PowerFlex: native integration         │          API: REST for custom tooling          │   │
│   │         Unity XT: native integration         │       MyService360: support portal link        │   │
│   │         PowerMax: via Data Mobility          │         Aria Ops: CloudIQ adapter PAK          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Arrays push telemetry to cloudiq.dell.com · CloudIQ pushes alerts to webhook targets                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Native integration = Array firmware includes CloudIQ telemetry client; no agent needed               │
│  Data Mobility = PowerMax component handling CloudIQ registration and telemetry forwarding            │
│  Webhook = Outbound HTTP POST from CloudIQ when alert fires; JSON payload                             │
│  REST API = CloudIQ programmatic interface for retrieving health scores and alert data                │
│  MyService360 = Dell customer support portal; linked from CloudIQ for case creation                   │
│  Aria Ops PAK = Adapter package enabling Aria Operations to pull CloudIQ data on-prem                 │
│  SMTP notification = Email sent by CloudIQ when alert fires or score drops                            │
│  API token = Bearer token for CloudIQ REST API; generated in account settings                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────── CloudIQ — Architecture Integrations ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Supported Arrays               │              Notification Targets              │   │
│   │        PowerStore: native integration        │           Email: SMTP to ops mailbox           │   │
│   │        PowerScale: native integration        │        Webhook: Slack/Teams/ServiceNow         │   │
│   │        PowerFlex: native integration         │          API: REST for custom tooling          │   │
│   │         Unity XT: native integration         │       MyService360: support portal link        │   │
│   │         PowerMax: via Data Mobility          │         Aria Ops: CloudIQ adapter PAK          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Arrays push telemetry to cloudiq.dell.com · CloudIQ pushes alerts to webhook targets                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Native integration = Array firmware includes CloudIQ telemetry client; no agent needed               │
│  Data Mobility = PowerMax component handling CloudIQ registration and telemetry forwarding            │
│  Webhook = Outbound HTTP POST from CloudIQ when alert fires; JSON payload                             │
│  REST API = CloudIQ programmatic interface for retrieving health scores and alert data                │
│  MyService360 = Dell customer support portal; linked from CloudIQ for case creation                   │
│  Aria Ops PAK = Adapter package enabling Aria Operations to pull CloudIQ data on-prem                 │
│  SMTP notification = Email sent by CloudIQ when alert fires or score drops                            │
│  API token = Bearer token for CloudIQ REST API; generated in account settings                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
