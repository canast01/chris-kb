# Aria Ops for Logs — Procedures


<div class="kb-summary">
Procedures reference covering Search Examples, Alerts Overview, Alert Types and Configuration, Alert Query Syntax, Alert Threshold Settings and 3 more sections.
</div>

## Search Examples

### Host Disconnect Events

```text
lost connectivity to the server
not responding
connection refused
```
```
┌──────────────────────────────── Aria Operations for Logs — Procedures ────────────────────────────────┐
│                                                                                                       │
│  Common operational procedures: add sources, rotate certs, manage disk, adjust alerts.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Add Log Source                │  │             Certificate Rotation            │   │
│   │     1. Install content pack if available     │  │    1. Generate new cert with correct SAN    │   │
│   │      2. Configure device syslog to vRLI      │  │        2. Import cert via VAMI → SSL        │   │
│   │     3. Verify events arriving in Explore     │  │        3. Restart loginsight service        │   │
│   │      4. Tag source: env/product fields       │  │     4. Verify sources still sending logs    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Disk and retention management prevent appliance from filling up during high-volume events.           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Disk Management                │  │               Alert Management              │   │
│   │       Monitor: Admin → System Monitor        │  │         Add: Queries → create alert         │   │
│   │        Archive: trigger manual export        │  │      Test: fire test from alert editor      │   │
│   │        Purge: reduce retention period        │  │       Route: map to webhook/email/SNow      │   │
│   │      Expand: add worker for more space       │  │     Suppress: noise via suppression rule    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI appliance · /storage disk · NFS archive target · vCenter · syslog sources                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Content pack      = Install before onboarding; provides parsers and dashboards for source            │
│  Explore           = vRLI real-time log viewer; used to confirm new sources are sending               │
│  Source tag        = Custom field on ingested events identifying environment or product               │
│  SAN cert          = Subject Alternative Name; FQDN of vRLI must be in cert SAN list                  │
│  loginsight service= Linux service restarted after cert change to apply new TLS cert                  │
│  System Monitor    = vRLI Admin section showing disk, CPU, RAM, and ingestion metrics                 │
│  Manual archive    = Trigger export of log data to NFS/S3 before disk fills                           │
│  Retention period  = Days of hot log data kept on disk; reduce to free space                          │
│  Worker node       = Add for more disk and processing; joins cluster automatically                    │
│  Alert suppression = Rule preventing noisy known-good events from firing notifications                │
│  Webhook route     = Notification channel sending HTTP POST to external system on alert               │
│  Alert test        = Manual trigger in alert editor; confirms notification delivery                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

### vMotion Failures

```text
vmotion
migration failed
VMotionFailed
```

### HA Events

```text
HA failover
ha.vm.restart
failover started
admission control
```

### DRS Events

```text
DRS
migration recommended
load balance
```

### Datastore Errors

```text
datastore
SCSI error
APD
PDL
NFS
VMFS
```

### vSAN Errors

```text
vsan
disk group
resync
object health
storage compliance
```

### NSX Errors

```text
nsx
transport node
edge
TEP
segment
```

### Time-Based Search Tips

- Always set a time range — start with the last 1 hour for active incidents
- Expand to 24 hours or 7 days when investigating intermittent issues
- Use the timeline view to identify event spikes
- Cross-reference vCenter event timestamps with host log timestamps

---

## Alerts Overview

Log-based alerts in Aria Operations for Logs (vRealize Log Insight) trigger notifications when query results meet defined thresholds. Alerts can fire via email, webhook, or integration with Aria Operations.

## Alert Types and Configuration

Alerts are created from saved queries. Navigate to **Interactive Analytics**, build your query, then click **Create Alert**.

```bash
# List all configured alerts via API
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/alerts \
  | python3 -m json.tool

# Get details of a specific alert
curl -sk -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/alerts/<alert-id>" \
  | python3 -m json.tool

# Disable an alert
curl -sk -X PUT -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/alerts/<alert-id>/state/DISABLED" \
  -H "Content-Type: application/json"

# Enable an alert
curl -sk -X PUT -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/alerts/<alert-id>/state/ENABLED" \
  -H "Content-Type: application/json"
```

## Alert Query Syntax

Alerts are built on the same query language used in Interactive Analytics:

```bash
# Alert on SSH failed logins (count > 10 in 5 min)
text contains "Failed password" AND hostname contains "prod-" 

# Alert on vCenter alarm events
appname = "vpxd" AND text contains "alarm" AND text contains "triggered"

# Alert on disk full events across all Linux hosts
text matches "No space left on device" AND source != "dev"

# Alert on firewall denies from specific subnet
text contains "DENY" AND text contains "10.0.1." AND appname = "pfsense"
```

## Alert Threshold Settings

| Threshold Type | Use Case | Example |
|---|---|---|
| Count | Fire when N events occur in time window | `> 10 in 5 minutes` |
| Rate of change | Fire when event rate increases sharply | `> 50% increase in 10 minutes` |
| Static (presence) | Fire when any matching event appears | Any occurrence of `"kernel panic"` |

## Notification Webhooks

Webhooks send alert payloads to external systems such as Teams, Slack, or custom endpoints.

```bash
# List configured notification destinations
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/notification/channels \
  | python3 -m json.tool

# Create a webhook notification channel
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/notification/channels \
  -H "Content-Type: application/json" \
  -d '{
    "type": "WEBHOOK",
    "name": "teams-alerts",
    "webhookUrl": "https://example.webhook.office.com/webhookb2/...",
    "contentType": "application/json",
    "body": "{\"text\": \"Alert: ${alertName} - ${hitCount} events\"}"
  }'

# Test a notification channel
curl -sk -X POST -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/notification/channels/<channel-id>/test"
```

Webhook payload variables:

| Variable | Value |
|---|---|
| `${alertName}` | Name of the alert |
| `${hitCount}` | Number of matching events |
| `${url}` | Deep link to alert in vRLI UI |
| `${fields}` | Extracted field values from the matching log |
| `${timestamp}` | Alert trigger time (epoch ms) |

## Alert Queries via API

```bash
# Run an ad-hoc alert query to test before creating an alert
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/events/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "text contains \"Failed password\"",
    "startTimeMillis": 1714950000000,
    "endTimeMillis": 1714953600000,
    "numResults": 100
  }' | python3 -m json.tool

# List active (recently triggered) alerts
curl -sk -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/alerts?status=ACTIVE" \
  | python3 -m json.tool
```

## Integration with Aria Operations

When integrated with Aria Operations (vROps), alerts in vRLI can create alerts/symptoms in the vROps console:

```bash
# Configure vROps integration from vRLI
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/operations-server-config \
  -H "Content-Type: application/json" \
  -d '{
    "serverHost": "<vrops-fqdn>",
    "serverPort": 443,
    "username": "admin",
    "password": "<password>",
    "enabled": true
  }'
```
