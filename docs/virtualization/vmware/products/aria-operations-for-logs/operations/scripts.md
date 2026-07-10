---
tags:
  - aria-logs
  - operations
  - vmware
---
# Aria Operations for Logs — Scripts Reference

*Applies to: VMware Aria 8.x*
![Aria Operations for Logs — Scripts Reference](../../../../../assets/virtualization-vmware-aria-operations-for-logs-operations-sc.svg)

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


```text title="Expected output"
=== Cluster Nodes ===
vrli-node-01.corp.local  ALIVE  MASTER  8.14.0.21045
vrli-node-02.corp.local  ALIVE  REPLICA  8.14.0.21045
vrli-node-03.corp.local  ALIVE  REPLICA  8.14.0.21045

=== Ingestion Stats ===
{
  "eventsPerSecond": 487293,
  "diskUsedPct": 73.4,
  "totalDiskGB": 2048,
  "usedDiskGB": 1502.7
}

=== Active Alerts (Critical) ===
Disk Space Critical Threshold Exceeded  2024-01-15T09:42:18Z
High Memory Pressure on Master Node     2024-01-15T08:31:05Z
Replication Lag Detected                2024-01-15T07:19:42Z
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present in script, but ensure your VRLI instance certificate is trusted or use `-k`).
    **`jq: parse error: Cannot index number with string "hostname"`** — Verify the API endpoint returns the expected JSON structure by running `curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/cluster/nodes" | jq '.'` to inspect raw output.
    **`curl: (7) Failed to connect to <vrli-fqdn> port 443: Connection refused`** — Confirm VRLI service is running and accessible at the provided FQDN with `curl -sk https://$VRLI/api/health` before running the full script.
```bash
#!/usr/bin/env bash
VRLI=$1; USER=$2; PASS=$3
OUTPUT="vrli-alerts-$(date +%Y%m%d).json"

curl -sk -u "$USER:$PASS" "https://$VRLI/api/v2/alerts" | jq '.' > "$OUTPUT"
echo "Exported $(jq '.alerts | length' "$OUTPUT") alert definitions to $OUTPUT"
```

```text title="Expected output"
Exported 247 alert definitions to vrli-alerts-20240115.json
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host`** — Verify the VRLI hostname is correct and resolvable (e.g., `nslookup $VRLI`).
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure the API credentials are correct; a 401/403 response returns HTML instead of JSON.
    **`command not found: jq`** — Install jq on the system with `apt-get install jq` or `yum install jq`.
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

```text title="Expected output"
Cluster disk used: 68%
OK: Disk usage within threshold
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification (already present in the script, so verify the VRLI hostname/IP is correct and reachable).
    **`jq: command not found`** — Install jq on the system with `apt-get install jq` (Debian/Ubuntu) or `yum install jq` (RHEL/CentOS).
    **`bc: command not found`** — Install bc with `apt-get install bc` or `yum install bc` to enable floating-point arithmetic comparison.
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

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## See also

- [Aria Operations for Logs — CLI Reference](../cli-reference/)
- [Aria Ops for Logs — Procedures](../procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
