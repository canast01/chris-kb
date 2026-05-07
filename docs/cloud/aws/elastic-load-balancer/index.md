# Elastic Load Balancer

AWS Elastic Load Balancing — ALB (Application), NLB (Network), and GLB (Gateway) load balancer management.
## Load Balancer Types

| Type | Layer | Use Case |
|---|---|---|
| ALB | Layer 7 | HTTP/HTTPS routing, path/host-based rules, microservices |
| NLB | Layer 4 | TCP/UDP, ultra-low latency, static IP, TLS passthrough |
| GLB | Layer 3 | Inline traffic inspection (firewalls, IDS/IPS) |
| CLB | Layer 4/7 | Legacy — migrate to ALB or NLB |

## Common CLI Commands

```bash
# List load balancers
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[*].{Name:LoadBalancerName,Type:Type,DNS:DNSName,State:State.Code}' \
  --output table

# List target groups
aws elbv2 describe-target-groups \
  --query 'TargetGroups[*].{Name:TargetGroupName,Protocol:Protocol,Port:Port,HealthCheck:HealthCheckPath}' \
  --output table

# Check target health
aws elbv2 describe-target-health \
  --target-group-arn <tg-arn> \
  --query 'TargetHealthDescriptions[*].{Target:Target.Id,Port:Target.Port,State:TargetHealth.State,Reason:TargetHealth.Reason}' \
  --output table

# List listeners on an ALB
aws elbv2 describe-listeners \
  --load-balancer-arn <alb-arn> \
  --query 'Listeners[*].{Port:Port,Protocol:Protocol,DefaultAction:DefaultActions[0].Type}' \
  --output table

# Describe ALB rules (routing)
aws elbv2 describe-rules \
  --listener-arn <listener-arn> \
  --query 'Rules[*].{Priority:Priority,Conditions:Conditions,Actions:Actions[0].Type}' \
  --output table
```

## Health Check Configuration

```bash
# Modify target group health check settings
aws elbv2 modify-target-group \
  --target-group-arn <tg-arn> \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3 \
  --health-check-timeout-seconds 5

# Register a target manually
aws elbv2 register-targets \
  --target-group-arn <tg-arn> \
  --targets Id=<instance-id>,Port=8080

# Deregister a target (for maintenance)
aws elbv2 deregister-targets \
  --target-group-arn <tg-arn> \
  --targets Id=<instance-id>
```

## Access Logs

```bash
# Enable ALB access logs (requires S3 bucket with correct permissions)
aws elbv2 modify-load-balancer-attributes \
  --load-balancer-arn <alb-arn> \
  --attributes Key=access_logs.s3.enabled,Value=true \
               Key=access_logs.s3.bucket,Value=<log-bucket> \
               Key=access_logs.s3.prefix,Value=alb-logs
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Targets unhealthy | `describe-target-health` | Verify health check path returns 200; check SG allows ALB to reach instances |
| 504 Gateway Timeout | Target not responding | Instance processing too slowly; increase timeout or fix app |
| 502 Bad Gateway | App response invalid | App returning wrong HTTP format; check app logs |
| SSL certificate error | Certificate on listener | Verify ACM cert is valid and attached to the HTTPS listener |
| Uneven traffic distribution | Sticky sessions? | Check if session stickiness is enabled on target group |
