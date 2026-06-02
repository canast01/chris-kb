# CloudIQ — Integrations


<div class="kb-summary">
Integrations reference covering Connectivity and Integration Points, Secure Connect Gateway, Email Notifications, Webhook Notifications, REST API Integration and 1 more sections.
</div>

```text
┌────────────────────────────────────── Dell CloudIQ Integrations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           CloudIQ integrates via REST API, webhooks, email, ITSM connectors, and SSO          │   │
│   │       Alert webhooks post to ServiceNow, Slack, or any HTTP endpoint on threshold breach      │   │
│   │       REST API exposes asset inventory, health scores, and metrics for custom dashboards      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    CloudIQ alert → webhook → ITSM ticket or Slack notification; REST API → BI/CMDB                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Alerting          │  │          API / Data         │  │           Identity          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │         Email alerts        │  │       CloudIQ REST API      │  │        SSO (SAML 2.0)       │   │
│   │        Webhook HTTP/S       │  │       Asset inventory       │  │         Dell account        │   │
│   │       ServiceNow conn.      │  │        Metrics export       │  │          RBAC roles         │   │
│   │        Slack webhook        │  │        Report export        │  │        MFA supported        │   │
│   │          PagerDuty          │  │           CSV/JSON          │  │         Org grouping        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    API token from CloudIQ settings → REST calls for health/capacity → CMDB or BI ingest               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │   Integration    │      Method      │      Trigger      │     Use case     │       Auth       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    ServiceNow    │     Webhook      │    Alert fires    │   Auto ticket    │     API key      │   │
│   │      Slack       │     Webhook      │    Alert fires    │  ChatOps notify  │   Webhook URL    │   │
│   │    Custom BI     │     REST API     │     Scheduled     │    Dashboards    │   Bearer token   │   │
│   │       CMDB       │     REST API     │     On-demand     │    Asset sync    │   Bearer token   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Webhook        = HTTP POST sent by CloudIQ to external URL when alert condition met                │
│    REST API       = CloudIQ public API; authenticated with OAuth bearer token; GET/POST               │
│    SSO            = SAML 2.0 identity federation; Dell accounts or corp IdP supported                 │
│    ServiceNow     = CloudIQ native connector creates incidents in ServiceNow on alert                 │
│    Report export  = PDF/CSV capacity and health reports downloadable or emailed on schedule           │
│    Org grouping   = Group systems by site/customer in CloudIQ for MSP multi-tenancy                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Email Notifications

CloudIQ sends alert notifications directly from Dell's mail infrastructure — no on-premises SMTP relay is required. Configure notification recipients in the CloudIQ portal under **Settings > Notifications > Email**.

- Add recipient email addresses per notification rule.
- Scope rules by system, severity (CRITICAL, WARNING, INFO), or CloudIQ tag.
- Test the notification configuration using the **Send Test** button in the notification rule.

## Webhook Notifications

CloudIQ supports outbound webhook delivery for CRITICAL alerts, enabling integration with Slack, Microsoft Teams, ServiceNow, or any HTTP endpoint that accepts a JSON POST.

Configure under **Settings > Notifications > Webhook**:

- **Endpoint URL**: the Slack incoming webhook URL, Teams connector URL, or ServiceNow REST API URL.
- **Method**: POST
- **Payload format**: CloudIQ sends a JSON body containing alert severity, system name, description, and timestamp.

## REST API Integration

Common integration patterns:

| Tool | Integration Method |
|---|---|
| Splunk | CloudIQ API poller script (Python) writing JSON events to Splunk HTTP Event Collector |
| Grafana | CloudIQ API data source via Grafana JSON API plugin or custom Python proxy |
| ServiceNow | CloudIQ webhook POST to ServiceNow inbound REST API for incident creation |
| Ansible | CloudIQ API queried in playbooks for health gate checks before storage maintenance tasks |

## ServiceNow Integration

CloudIQ can automatically create ServiceNow incidents for CRITICAL alerts via the webhook notification feature. Configure as follows:

1. In ServiceNow, create or identify an **Inbound REST API** endpoint or a scripted REST API that accepts a JSON POST and creates an incident.
2. In CloudIQ under **Settings > Notifications > Webhook**, add a new webhook with the ServiceNow REST API endpoint URL and any required authentication headers (e.g., Basic auth or OAuth token as a custom header).
3. Set the notification filter to **CRITICAL** severity to avoid flooding the ITSM tool with low-priority alerts.
4. Map the CloudIQ JSON payload fields (system name, alert description, severity) to ServiceNow incident fields in the ServiceNow scripted REST handler.
5. Test by triggering a test notification from CloudIQ and confirming the incident appears in ServiceNow.

For production environments, use a ServiceNow integration user with the minimum required roles (`itil` for incident creation) rather than a shared admin account.
