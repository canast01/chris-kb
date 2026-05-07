# Route 53

AWS Route 53 — DNS hosted zones, record management, health checks, and routing policies.
## Key Concepts

| Concept | Description |
|---|---|
| Hosted zone | Container for DNS records for a domain |
| Public hosted zone | Answers DNS queries from the internet |
| Private hosted zone | Answers DNS queries only within specified VPCs |
| Alias record | Route 53-specific record that maps to AWS resources (no TTL charge) |
| Health check | Monitors endpoints; drives failover routing policies |
| Routing policy | Simple, Weighted, Latency, Failover, Geolocation, Multivalue |

## Common CLI Commands

```bash
# List hosted zones
aws route53 list-hosted-zones \
  --query 'HostedZones[*].{Name:Name,ID:Id,Type:Config.PrivateZone}' --output table

# List records in a zone
aws route53 list-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --query 'ResourceRecordSets[*].{Name:Name,Type:Type,TTL:TTL}' --output table

# Create an A record
aws route53 change-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "app.example.com.",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{"Value": "10.0.1.100"}]
      }
    }]
  }'

# Update (UPSERT) a record — creates or replaces
aws route53 change-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "app.example.com.",
        "Type": "A",
        "TTL": 60,
        "ResourceRecords": [{"Value": "10.0.1.200"}]
      }
    }]
  }'

# Delete a record
# Use same structure as CREATE but with "Action": "DELETE" and exact matching values

# Check propagation status of a change
aws route53 get-change --id <change-id>
```

## Health Checks

```bash
# Create health check for an HTTP endpoint
aws route53 create-health-check \
  --caller-reference "app-hc-$(date +%s)" \
  --health-check-config '{
    "IPAddress": "10.0.1.100",
    "Port": 443,
    "Type": "HTTPS",
    "ResourcePath": "/health",
    "FullyQualifiedDomainName": "app.example.com",
    "RequestInterval": 30,
    "FailureThreshold": 3
  }'

# List health checks
aws route53 list-health-checks \
  --query 'HealthChecks[*].{ID:Id,Type:HealthCheckConfig.Type,Status:HealthCheckConfig.Type}' --output table

# Get health check status
aws route53 get-health-check-status --health-check-id <hc-id>
```

## Routing Policies

| Policy | Use Case |
|---|---|
| Simple | Single resource, no health checks |
| Weighted | A/B testing, gradual traffic shift (set weights 0–255) |
| Failover | Primary/secondary with health checks |
| Latency | Route to lowest-latency region |
| Geolocation | Route by country/continent |
| Multivalue | Return up to 8 healthy records (not a load balancer) |

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| DNS change not resolving | TTL cached | Wait for TTL expiry; test with `dig @8.8.8.8 <name>` |
| Record resolves to wrong IP | Route 53 propagation | `aws route53 get-change --id <id>` — wait for `INSYNC` |
| Private zone not resolving | VPC association | Check private hosted zone is associated with the querying VPC |
| Health check failing | Health check status | Review CloudWatch metric `HealthCheckStatus`; check endpoint response |
