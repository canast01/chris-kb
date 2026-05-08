# Aria Ops for Logs — Scripts

Scripts for Aria Operations for Logs target four use cases: cluster health monitoring, log source coverage auditing, alert definition management, and log queries via the REST API. The API base URL is `https://<vrli-fqdn>/api/v2` with HTTP Basic authentication.

---

## Cluster Health Check

```bash
#!/usr/bin/env bash
# Usage: ./vrli-health.sh <vrli-fqdn> <username> <password>
VRLI=$1; USER=$2; PASS=$3

echo "=== Cluster Nodes ==="
curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/cluster/nodes" | \
  jq -r '.nodes[] | "\(.hostname)\t\(.state)\t\(.role)\t\(.version)"' | \
  column -t

echo ""
echo "=== Ingestion Stats ==="
curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/cluster/stats" | \
  jq '{eventsPerSecond: .eventsIngested, diskUsedPct: .diskUsagePercent,
       totalDiskGB: .totalDiskSpaceGB, usedDiskGB: .usedDiskSpaceGB}'

echo ""
echo "=== Active Alerts (Critical) ==="
curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/alerts?severity=critical&status=active" | \
  jq -r '.alerts[] | "\(.name)\t\(.timestamp)"' | column -t
```

---

## Agent Coverage Report

Identifies agents that have not checked in within the last 30 minutes — potential connectivity or service failures.

```bash
#!/usr/bin/env bash
VRLI=$1; USER=$2; PASS=$3
THRESHOLD_MINS=30
THRESHOLD_MS=$((THRESHOLD_MINS * 60 * 1000))
NOW_MS=$(date +%s%3N)

echo "=== Agents not checked in within $THRESHOLD_MINS minutes ==="
curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/agents" | \
  jq --argjson now "$NOW_MS" --argjson thresh "$THRESHOLD_MS" \
  '.agents[] | select(($now - (.lastActive | tonumber)) > $thresh) |
   {host: .hostname, lastActive: .lastActive, state: .state}' | \
  jq -r '"STALE: \(.host) — last seen \(.lastActive)"'

echo ""
echo "=== All agents summary ==="
curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/agents" | \
  jq -r '.agents | length' | xargs -I{} echo "Total agents registered: {}"
```

---

## Query Recent Events via API

Use the API to search for log events programmatically (useful for automation and integration with incident management tools).

```bash
#!/usr/bin/env bash
# Search for authentication failures in the last hour
VRLI="vrli-prod-01.corp.local"
START=$(date -d "1 hour ago" +%s)000  # milliseconds
END=$(date +%s)000

curl -sk -u "admin:<password>" \
  -H "Content-Type: application/json" \
  -X POST "https://$VRLI/api/v2/events/ingest" \
  -d "{
    \"query\": \"Failed to authenticate OR authentication failure\",
    \"start-time\": $START,
    \"end-time\": $END,
    \"limit\": 100
  }" | jq '.events[] | {time: .timestamp, host: .fields.hostname, text: .text}'
```

---

## Bulk Alert Definition Export

Export all alert definitions to JSON for version control or migration to another cluster.

```bash
#!/usr/bin/env bash
VRLI=$1; USER=$2; PASS=$3
OUTPUT="vrli-alerts-$(date +%Y%m%d).json"

curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/alerts" | jq '.' > "$OUTPUT"
echo "Exported $(jq '.alerts | length' "$OUTPUT") alert definitions to $OUTPUT"
```

---

## Disk Usage Monitor with Warning

Sends a warning if any cluster node disk usage exceeds a threshold.

```bash
#!/usr/bin/env bash
VRLI=$1; USER=$2; PASS=$3; WARN_PCT=${4:-75}

STATS=$(curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/cluster/stats")
USED_PCT=$(echo "$STATS" | jq '.diskUsagePercent // 0' | tr -d '"')

echo "Cluster disk used: ${USED_PCT}%"
if (( $(echo "$USED_PCT > $WARN_PCT" | bc -l) )); then
  echo "WARNING: Disk usage exceeds ${WARN_PCT}% — expand storage or reduce retention"
  exit 1
else
  echo "OK: Disk usage within threshold"
fi
```

---

## Notification Channel Test

Test all configured notification channels and report pass/fail.

```bash
#!/usr/bin/env bash
VRLI=$1; USER=$2; PASS=$3

echo "=== Notification Channels ==="
curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/notification" | \
  jq -r '.notifications[] | "\(.name)\t\(.type)\t\(.enabled)"' | \
  column -t

# Test each enabled channel
curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/notification" | \
  jq -r '.notifications[] | select(.enabled == true) | .id' | \
  while read -r id; do
    RESULT=$(curl -sk -u "$USER:$PASS" -X POST \
      "https://$VRLI/api/v2/notification/$id/test" | jq -r '.status')
    echo "Channel $id: $RESULT"
  done
```

---

## ESXi Syslog Configuration (Bulk PowerCLI)

```powershell
# Configure all ESXi hosts to forward syslog to Aria Ops for Logs
$vrliTarget = "udp://vrli-prod-01.corp.local:514"

Get-VMHost | ForEach-Object {
    $esxcli = Get-EsxCli -VMHost $_ -V2
    $params = $esxcli.system.syslog.config.set.CreateArgs()
    $params.loghost = $vrliTarget
    $esxcli.system.syslog.config.set.Invoke($params) | Out-Null
    $esxcli.system.syslog.reload.Invoke() | Out-Null
    $cfg = $esxcli.system.syslog.config.get.Invoke()
    [PSCustomObject]@{
        Host = $_.Name
        RemoteHost = $cfg.RemoteHost
        Status = if ($cfg.RemoteHost -eq $vrliTarget) { "OK" } else { "MISMATCH" }
    }
} | Format-Table -AutoSize
```
