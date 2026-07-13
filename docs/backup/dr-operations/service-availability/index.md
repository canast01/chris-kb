---
tags:
  - dr
description: "Service Availability Monitoring reference covering Availability Calculation, Uptime Monitoring Tools, Azure Monitor — Availability Test, AWS Route 53..."
---
# Service Availability Monitoring

<div class="kb-summary">
Service Availability Monitoring reference covering Availability Calculation, Uptime Monitoring Tools, Azure Monitor — Availability Test, AWS Route 53 Health Checks, Availability Incident Tracking and 1 more sections.
</div>

```d2
direction: down

availability_calculation: "Availability Calculation" {shape: rectangle}
aws_route_53_health_checks: "AWS Route 53 Health Checks" {shape: rectangle}
availability_incident_tracking: "Availability Incident Tracking" {shape: rectangle}
reporting: "Reporting" {shape: rectangle}

availability_calculation -> aws_route_53_health_checks: uses
aws_route_53_health_checks -> availability_incident_tracking: uses
availability_incident_tracking -> reporting: uses
```

## Availability Calculation

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


```text title="Expected output"
{
    "HealthCheck": {
        "Id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "CallerReference": "1699564823",
        "HealthCheckConfig": {
            "Type": "HTTPS",
            "FullyQualifiedDomainName": "app-host.example.com",
            "Port": 443,
            "ResourcePath": "/health",
            "RequestInterval": 30,
            "FailureThreshold": 3
        },
        "HealthCheckVersion": 1
    }
}
[
    {
        "Region": "us-east-1",
        "Status": "Success"
    },
    {
        "Region": "us-west-2",
        "Status": "Success"
    },
    {
        "Region": "eu-west-1",
        "Status": "Success"
    },
    {
        "Region": "ap-southeast-1",
        "Status": "Success"
    }
]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidInput) when calling the CreateHealthCheck operation: Invalid health check configuration` | Ensure the JSON is valid and the FullyQualifiedDomainName is a resolvable hostname without the `<>` brackets. |
    | `An error occurred (InvalidHealthCheckId) when calling the GetHealthCheckStatus operation: The health check ID '<id>' does not exist` | Replace `<id>` with the actual health check ID returned from the create command output. |
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
