# Dell ECS — Diagnostics

> Diagnostic procedures and log analysis for Dell ECS.

## Diagnostic Commands

```bash
# Authenticate to the ECS Management REST API
curl -s -k -u "sysadmin:<password>" \
  "https://<ecs-node>:4443/login" -D -

# Set the auth token variable from the response header
TOKEN="<X-SDS-AUTH-TOKEN value>"

# Get VDC capacity (total, used, available)
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/capacity" | python3 -m json.tool

# List all nodes and health status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/nodes" | python3 -m json.tool

# Get active alerts for the VDC
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/alerts" | python3 -m json.tool

# List all namespaces
ecscli namespace list

# List buckets in a namespace
ecscli bucket list --namespace <namespace>

# Get bucket metadata (versioning, quota, replication group)
ecscli bucket get --namespace <namespace> --name <bucket>

# List incomplete multipart uploads for a bucket (S3 API via awscli)
aws s3api list-multipart-uploads \
  --endpoint-url https://<ecs-s3-endpoint> \
  --bucket <bucket>

# Test S3 connectivity with a simple HEAD request
curl -sv --max-time 10 \
  https://<ecs-s3-endpoint>/<bucket>/<object> \
  --aws-sigv4 "aws:amz:<region>:s3" \
  -u "<access_key>:<secret_key>"

# Check geo-replication status for a specific replication group
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/data-service/vpools" | python3 -m json.tool
```

## Log Locations

| Log | Location | Content |
|---|---|---|
| ECS data service log | `/var/log/ecs/` on each node | Object I/O, erasure coding, replication errors |
| ECS management service log | `/var/log/ecs-portal/` | API requests, portal events |
| OS system log | `/var/log/messages` or `journalctl` | Node OS events, hardware errors |
| Geo-replication log | ECS Portal → Logs → Geo Replication | Replication job status and errors |
| Audit log | ECS Portal → Monitoring → Audit | Administrative actions |

ECS also supports syslog forwarding (configure under ECS Portal → Settings → Syslog) — forward to your SIEM for centralised log analysis.

## Before Calling Support

Gather the following before opening a Dell Support case:

```bash
# ECS software version
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/version" | python3 -m json.tool

# Node list and health status
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/nodes" | python3 -m json.tool

# Active alerts
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/alerts" | python3 -m json.tool

# VDC capacity
curl -s -k -H "X-SDS-AUTH-TOKEN: $TOKEN" \
  "https://<ecs-node>:4443/vdc/capacity" | python3 -m json.tool
```

Also collect:
- ECS Portal → Support → Collect Logs (generates a support bundle per node)
- Replication group name and VDC topology description
- Approximate time window the issue started
- Description of any recent changes (upgrades, new buckets, IAM changes, network changes)
- Output of `ecscli namespace list` and the affected namespace/bucket names
