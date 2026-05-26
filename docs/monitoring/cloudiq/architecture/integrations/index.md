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
## Supported Dell Platforms

| Platform | Collection Method | Data Available |
|---|---|---|
| PowerMax / VMAX | HTTPS via Unisphere | Performance, capacity, SRDF state, health |
| PowerStore | HTTPS via REST API | Volume health, capacity, performance |
| PowerScale (Isilon) | SSH / OneFS REST API | Cluster capacity, node health, quotas |
| Unity XT | HTTPS via Unisphere | Pool capacity, SP health, replication status |
| PowerFlex (VxFlex OS) | HTTPS REST API | Cluster health, volume capacity |
| Data Domain | HTTPS REST API | Dedup savings, capacity, replication |

## ITSM Integrations

| Integration | Mechanism | Use Case |
|---|---|---|
| ServiceNow | REST outbound (CloudIQ connector) | Auto-create incidents on Critical alerts |
| Email | SMTP relay via CloudIQ cloud | Alert notifications to DL or individual |
| Webhook | HTTPS POST (custom) | PagerDuty, Slack, or custom endpoint |

### ServiceNow Setup

1. In CloudIQ portal: **Settings → Notifications → ServiceNow**
2. Enter ServiceNow instance URL, username, and password (or OAuth token)
3. Map CloudIQ severity levels to ServiceNow Priority values
4. Test with a manually triggered notification

## REST API

CloudIQ provides a REST API for programmatic access to fleet metrics:

```bash
# Get API token (OAuth client credentials)
curl -X POST https://cloudiq.dell.com/auth/token \
  -d "grant_type=client_credentials&client_id=<id>&client_secret=<secret>"

# List all systems and health scores
curl -H "Authorization: Bearer <token>" \
  https://cloudiq.dell.com/v1/storage-systems

# Get capacity for a specific system
curl -H "Authorization: Bearer <token>" \
  "https://cloudiq.dell.com/v1/storage-systems/{id}/capacity"
```
