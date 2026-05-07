# ECS Troubleshooting
## Common Issues

| Symptom | Cause | Action |
|---|---|---|
| Node shows `DEGRADED` or offline in ECS Portal | Disk failure, NIC fault, or node OS crash | Check ECS Portal → Hardware for disk state; SSH to the node and check OS logs; replace failed disk via the guided procedure in the portal |
| Geo-replication lag growing between VDCs | WAN link saturation, remote VDC node issue, or replication group misconfiguration | Check ECS Portal → Geo Monitoring; review inter-site bandwidth utilisation; verify the remote VDC has healthy nodes |
| S3 `AccessDenied` despite correct credentials | IAM policy misconfiguration, wrong namespace, or bucket policy conflict | Confirm IAM user is assigned to the correct namespace; check bucket policy with `ecscli bucket get`; verify path-style vs virtual-hosted-style addressing |
| Capacity growing unexpectedly | Bucket versioning accumulating old versions, incomplete multipart uploads, or no lifecycle policy | Check versioning on buckets; list and abort incomplete MPUs via S3 API; add lifecycle policies to expire non-current versions |
| ECS Portal login fails (HTTP 503 or timeout) | Portal service down or certificate expired | SSH to node and restart ECS portal service; check TLS certificate expiry via ECS Portal → Settings → Certificates |
| Bucket quota exceeded — writes failing with `QuotaExceeded` | Bucket or namespace hard quota reached | Increase quota via ECS Portal → Buckets → Edit or expire old objects; review lifecycle rules |
| Object read returns `404` for a recently written object | Replication lag: object written to one VDC not yet visible on the reading VDC | Wait for replication to complete; check replication lag in Geo Monitoring; verify replication group consistency setting |
| `503 Service Unavailable` on S3 endpoint during steady state | Data service process down on some nodes, or cluster is in degraded mode | Check node health in portal; review ECS data service logs on affected nodes |
| WORM/CAS object deletion blocked | Object is within its retention period | This is expected behaviour; confirm retention period setting on the bucket; escalate to data owner to confirm |

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
