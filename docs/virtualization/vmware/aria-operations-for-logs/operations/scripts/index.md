# Aria Operations for Logs — Scripts Reference

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

```text
┌──────────────────────────── Aria Operations for Logs — Scripts Reference ─────────────────────────────┐
│                                                                                                       │
│  vRLI scripting uses REST API for config export/import, ingest, and query automation.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Common REST API Scripts            │  │          ESXi Syslog Config Script          │   │
│   │      GET /api/v1/config/export → backup      │  │       esxcli system syslog config set       │   │
│   │      POST /api/v1/config/import restore      │  │        --loghost=ssl://vRLI-FQDN:6514       │   │
│   │       POST /api/v1/events/ingest push        │  │         esxcli system syslog reload         │   │
│   │       GET /api/v1/cluster/nodes status       │  │       Apply via PowerCLI foreach host       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Disk and alert scripts automate routine operations for large-scale deployments.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Appliance Maintenance Scripts         │  │              Monitoring Scripts             │   │
│   │          df -h /storage: disk check          │  │        curl GET /api/v1/cluster/nodes       │   │
│   │          service loginsight restart          │  │       Parse JSON: check state==MASTER       │   │
│   │       find /storage -mtime +90 archive       │  │        Alert if disk > 80% threshold        │   │
│   │      netstat -tulpn: verify ports open       │  │       Cron: daily config export to NFS      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI Linux appliance · ESXi hosts · PowerCLI station · NFS for backup scripts                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Config export API = GET /api/v1/config/export; JSON backup of all vRLI settings                      │
│  Config import API = POST /api/v1/config/import; restore from config JSON backup                      │
│  Ingest API        = POST /api/v1/events/ingest; body: {events:[{text,fields,timestamp}]}             │
│  Cluster nodes API = GET /api/v1/cluster/nodes; returns state (MASTER/WORKER/etc)                     │
│  esxcli syslog     = ESXi command to configure log destination; run per-host or via PowerCLI          │
│  PowerCLI foreach  = Connect-VIServer then Get-VMHost | foreach {Invoke-EsxCli...}                    │
│  loginsight svc    = service loginsight restart; safe restart without data loss                       │
│  Cron config backup= Daily cron calling config export API and writing JSON to NFS                     │
│  Disk alert script = Checks df -h output; emails/pages if /storage >80% used                          │
│  SSL syslog URL    = ssl://vRLI-FQDN:6514 format used in esxcli loghost config                        │
│  Sessions API      = POST /api/v1/sessions with creds; returns sessionId for auth                     │
│  Bearer header     = Authorization: Bearer <sessionId> on subsequent API calls                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
#!/usr/bin/env bash
VRLI=$1; USER=$2; PASS=$3
OUTPUT="vrli-alerts-$(date +%Y%m%d).json"

curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/alerts" | jq '.' > "$OUTPUT"
echo "Exported $(jq '.alerts | length' "$OUTPUT") alert definitions to $OUTPUT"
```
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
```powershell
# Configure all ESXi hosts to forward syslog to Aria Ops for Logs
$vrliTarget = "udp://vrli-prod-01.example.local:514"

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
