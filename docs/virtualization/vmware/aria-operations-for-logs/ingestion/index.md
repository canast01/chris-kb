# Aria Operations for Logs — Ingestion

## Overview

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
