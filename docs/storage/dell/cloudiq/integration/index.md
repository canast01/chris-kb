# Dell CloudIQ Integration
## Secure Connect Gateway

The Secure Connect Gateway (SCG) is the primary telemetry feed for CloudIQ. SCG is a virtual appliance (OVA) deployed on-premises that collects telemetry from registered Dell systems and forwards it encrypted to `cloudiq.dell.com:443` over HTTPS.

Key configuration points:

- Deploy one SCG per site or per network segment where Dell systems reside.
- Register each storage system with SCG using the system's management IP and credentials.
- SCG sends telemetry outbound only — no inbound firewall rules are required.
- If outbound traffic must traverse a proxy, configure the proxy in SCG under **Settings > Proxy**. The proxy must allow HTTPS to `cloudiq.dell.com` and `esrs3.emc.com` on port 443.
- Telemetry collection interval is typically every 5 minutes for health and performance data.

```bash
# Verify SCG can reach Dell endpoints
curl -k https://cloudiq.dell.com
curl -k https://esrs3.emc.com
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

Example Slack integration: create an incoming webhook in Slack and paste the URL into CloudIQ as a webhook notification target with a filter for CRITICAL severity.

## REST API Integration

CloudIQ exposes a versioned REST API for programmatic access to health, capacity, performance, and alert data. Authenticate using OAuth2 client credentials.

```bash
# Step 1: Get an access token
ACCESS_TOKEN=$(curl -s -X POST "https://cloudiq.dell.com/auth/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=<client_id>&client_secret=<client_secret>" \
  | jq -r '.access_token')

# Step 2: Use the token in subsequent API calls
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://cloudiq.dell.com/cloudiq/rest/v1/storage-systems" | jq .
```

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
