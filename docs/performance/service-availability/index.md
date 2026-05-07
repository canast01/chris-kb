# Service Availability Monitoring

## Availability Calculation

```
Availability % = (Total time - Downtime) / Total time × 100

99.9%  → 8.7 hours downtime/year (43.8 min/month)
99.95% → 4.4 hours downtime/year (21.9 min/month)
99.99% → 52 minutes downtime/year (4.4 min/month)
```

## Synthetic Monitoring (External Probes)

```bash
# HTTP health check — confirm endpoint returns 200
curl -o /dev/null -s -w "%{http_code} %{time_total}s\n" https://<app>/health

# TCP port check
nc -zv <host> 443 2>&1 | grep -E "succeeded|failed"

# DNS resolution check
dig +short <hostname> @8.8.8.8

# Script: check multiple services
for endpoint in "https://app1/health" "https://app2/health"; do
    code=$(curl -o /dev/null -s -w "%{http_code}" "$endpoint")
    if [ "$code" != "200" ]; then
        echo "ALERT: $endpoint returned $code"
    fi
done
```

## Uptime Monitoring Tools

| Tool | Method | Notes |
|---|---|---|
| Prometheus Blackbox Exporter | HTTP/TCP/ICMP probes from internal | Integrates with Grafana |
| Zabbix | HTTP/TCP/ICMP + agent checks | All-in-one monitoring |
| Pingdom / UptimeRobot | External HTTP probes | External visibility; SLA reporting |
| Azure Monitor / Application Insights | App-level availability tests | Built-in for Azure workloads |
| AWS CloudWatch | Route 53 health checks | Native for AWS endpoints |

## Azure Monitor — Availability Test

```bash
# Create an availability test (ping test)
az monitor app-insights web-test create \
  -g <rg> \
  --app-insights <ai-name> \
  -n <test-name> \
  --defined-web-test-kind ping \
  --locations '[{"Id":"us-east-az"}]' \
  --url "https://<app>/health" \
  --frequency 300 \
  --timeout 30
```

## AWS Route 53 Health Checks

```bash
# Create HTTP health check
aws route53 create-health-check \
  --caller-reference "$(date +%s)" \
  --health-check-config '{
    "Type": "HTTPS",
    "FullyQualifiedDomainName": "<app-host>",
    "Port": 443,
    "ResourcePath": "/health",
    "RequestInterval": 30,
    "FailureThreshold": 3
  }'

# Get health check status
aws route53 get-health-check-status --health-check-id <id> \
  --query 'HealthCheckObservations[*].{Region:Region,Status:StatusReport.Status}'
```

## Availability Incident Tracking

```markdown
Incident:       APP-2026-042
Service:        ERP Application
Start time:     2026-05-05 14:23 UTC
End time:       2026-05-05 15:07 UTC
Downtime:       44 minutes
SLO impact:     Monthly budget: 43.8 min — budget consumed 100%
Root cause:     Database connection pool exhausted due to slow query
Detection:      Monitoring alert fired at 14:24 (1 min after start)
Resolution:     Restarted connection pool; fixed query index
```

## Reporting

| Report | Frequency | Audience |
|---|---|---|
| Availability dashboard | Real-time | Operations team |
| Monthly SLO compliance | Monthly | Management, service owners |
| Incident post-mortem | After each P1/P2 | Management, tech leads |
| Quarterly availability trend | Quarterly | CISO, IT management |
