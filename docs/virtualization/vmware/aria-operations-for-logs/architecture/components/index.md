# Aria Ops for Logs — Components

## Ingestion Overview

Aria Operations for Logs (vRLI) receives log data via syslog (UDP/TCP/TLS) and via the Log Insight Agent. Sources include ESXi hosts, vCenter, NSX, Linux/Windows VMs, and network devices. Log forwarding and filtering reduce noise and storage consumption.

## Syslog Configuration

vRLI listens on the following ports by default:

| Protocol | Port | TLS |
|---|---|---|
| Syslog UDP | 514 | No |
| Syslog TCP | 514 | No |
| Syslog TCP/TLS | 6514 | Yes |
| CFapi (agent) | 9000 | No |
| CFapi TLS (agent) | 9543 | Yes |

```bash
# Verify vRLI is listening on syslog ports
ss -tlnup | grep -E "514|9000|9543"

# Test syslog delivery from a Linux source
logger -n <vrli-fqdn> -P 514 --tcp "Test syslog message from $(hostname)"

# Send a test event via UDP
echo "<13>May  7 10:00:00 testhost test: Hello vRLI" | nc -u <vrli-fqdn> 514

# Verify event arrived in vRLI (query API)
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/events/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "text contains \"Hello vRLI\"",
    "startTimeMillis": '"$(date -d '5 minutes ago' +%s000)"',
    "endTimeMillis": '"$(date +%s000)"'
  }' | python3 -m json.tool
```

## ESXi Syslog Configuration

```bash
# Configure ESXi host to forward syslog to vRLI
esxcli system syslog config set --loghost="udp://<vrli-fqdn>:514"
esxcli system syslog reload

# Verify current syslog configuration
esxcli system syslog config get

# Open firewall rule for syslog on ESXi
esxcli network firewall ruleset set --ruleset-id=syslog --enabled=true
esxcli network firewall refresh
```

## Log Insight Agent Deployment

The Log Insight Agent supports structured log collection from Linux and Windows hosts with filtering and tag enrichment.

```bash
# Download the agent installer from vRLI UI or appliance
curl -sk -O https://<vrli-fqdn>/api/v1/agent/packages/types/RPM

# Install on Linux (RHEL/CentOS)
rpm -ivh VMware-Log-Insight-Agent-*.rpm

# Configure the agent
cat > /var/lib/loginsight-agent/liagent.ini << 'EOF'
[server]
hostname=<vrli-fqdn>
proto=cfapi
port=9000
ssl=no

[logging]
debug_level=0
EOF

# Start and enable the agent
systemctl start liagentd
systemctl enable liagentd

# Check agent status
systemctl status liagentd
tail -50 /var/log/loginsight-agent/liagent.log
```

## Agent Configuration for Custom Log Paths

```ini
# /var/lib/loginsight-agent/liagent.ini additions for custom logs

[filelog|nginx-access]
directory=/var/log/nginx
include=access.log
event_marker=^\d{1,3}\.\d{1,3}

[filelog|app-errors]
directory=/opt/myapp/logs
include=error*.log
tags={"app_name": "myapp", "env": "prod"}
```

## Log Forwarding

vRLI can forward processed logs to another syslog endpoint or another vRLI cluster:

```bash
# List existing forwarder configurations
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/forwarders \
  | python3 -m json.tool

# Create a forwarder to a SIEM (e.g., Splunk)
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/forwarders \
  -H "Content-Type: application/json" \
  -d '{
    "name": "splunk-siem",
    "host": "splunk-hec.example.com",
    "port": 514,
    "protocol": "TCP",
    "sslEnabled": false,
    "workerCount": 4
  }'

# Test a forwarder connection
curl -sk -X POST -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/forwarders/<forwarder-id>/test"
```

## Filtering and Ingestion Control

Filters can drop noisy log streams before they reach storage, reducing licence consumption and storage costs.

```bash
# List all ingestion filters
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/filters \
  | python3 -m json.tool

# Create a drop filter (discard heartbeat messages)
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/filters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "drop-heartbeats",
    "action": "DROP",
    "conditions": [
      {"fieldName": "text", "operator": "CONTAINS", "value": "heartbeat"}
    ]
  }'
```

Ingestion filter actions:

| Action | Effect |
|---|---|
| `DROP` | Discard matching events — they are never stored |
| `TAG` | Add a field/tag to matching events before storage |
| `ROUTE` | Send matching events to a specific dataset |

---

## Dashboards Overview

Dashboards in Aria Operations for Logs provide persistent, shareable views of log data. They are composed of widgets that display query results, field histograms, and time-series counts. Dashboards are useful for operational monitoring and compliance reporting.

## Creating Dashboards

Dashboards are created via the UI at **Dashboards > New Dashboard**, or via the API:

```bash
# List existing dashboards
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/dashboards \
  | python3 -m json.tool

# Create a new dashboard
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/dashboards \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security Events",
    "shared": true,
    "widgets": []
  }' | python3 -m json.tool

# Clone an existing dashboard
curl -sk -X POST -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/dashboards/<dashboard-id>/clone" \
  -H "Content-Type: application/json" \
  -d '{"name": "Security Events - Copy"}'
```

## Log Widgets

Widgets are the building blocks of a dashboard. Each widget runs a query against ingested log data.

Widget types available:

| Widget Type | Description | Best Used For |
|---|---|---|
| Event Count Over Time | Bar chart of event frequency | Volume monitoring, spike detection |
| Field Table | Table of extracted field values | IP/hostname/user-based summaries |
| Field Distribution | Pie or bar chart of field values | Top-N analysis |
| Text | Free text for labels and notes | Section headers, instructions |
| Log Count | Single number tile | KPI / SLA metrics |

```bash
# Add a widget to a dashboard
curl -sk -X POST -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/dashboards/<dashboard-id>/widgets" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Failed SSH Logins",
    "widgetType": "EVENT_COUNT_OVER_TIME",
    "query": "text contains \"Failed password\"",
    "timeRange": "LAST_1_HOUR"
  }'
```

## Field Extraction

Custom fields are extracted from log messages using regex. Extracted fields can be used in widgets, alerts, and queries.

```bash
# Create a custom extracted field
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/fields \
  -H "Content-Type: application/json" \
  -d '{
    "name": "source_ip",
    "displayName": "Source IP",
    "regex": "from ([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})",
    "regexFlags": [],
    "discoverable": true
  }'

# List all custom extracted fields
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/fields \
  | python3 -m json.tool

# Verify a regex extraction against sample log text
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/fields/test \
  -H "Content-Type: application/json" \
  -d '{
    "regex": "from ([0-9.]+)",
    "sample": "sshd: Failed password for root from 192.168.1.10 port 44231"
  }' | python3 -m json.tool
```

Field extraction reference:

| Log Format | Extraction Approach | Example Regex |
|---|---|---|
| Key=value pairs | Named group on value | `user=(\S+)` |
| JSON logs | Use built-in JSON parser | — (automatic) |
| Apache/Nginx access logs | Use built-in content pack | — (content pack) |
| Syslog RFC5424 | Structured data auto-parsed | — (automatic) |
| Custom app logs | Regex per field | `\[ERROR\] (.+)` |

## Time Range Settings

Dashboard time range controls all widgets unless a widget overrides it:

```bash
# Set dashboard default time range via API
curl -sk -X PUT -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/dashboards/<dashboard-id>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security Events",
    "defaultTimeRange": "LAST_6_HOURS"
  }'
```

Available time range values:

| Value | Description |
|---|---|
| `LAST_5_MINUTES` | Last 5 minutes |
| `LAST_1_HOUR` | Last 1 hour |
| `LAST_6_HOURS` | Last 6 hours |
| `LAST_24_HOURS` | Last 24 hours |
| `LAST_7_DAYS` | Last 7 days |
| `CUSTOM` | User-specified start and end timestamps |

## Dashboard Sharing and Export

```bash
# Share a dashboard with all users
curl -sk -X PUT -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/dashboards/<dashboard-id>" \
  -H "Content-Type: application/json" \
  -d '{"shared": true}'

# Export all dashboards to JSON (for backup or migration)
curl -sk -u admin:<password> \
  https://<vrli-fqdn>/api/v1/dashboards \
  | python3 -m json.tool > vrli-dashboards-backup.json

# Import dashboards from JSON
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/dashboards/import \
  -H "Content-Type: application/json" \
  -d @vrli-dashboards-backup.json
```
