# Dell ECS — Health Checks

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Log in to ECS Portal → Dashboard and review the Alerts panel | | Triage by severity |
| ECS Portal → Dashboard → Capacity | | |
| Query `GET /vdc/nodes` via the Management REST API | `GET /vdc/nodes` | All nodes should report `GOOD`; a `DEGRADED` or offline node requires immediate investigation |
| Query `GET /vdc/capacity` to retrieve current cluster capacity metrics | `GET /vdc/capacity` | |
| ECS Portal → Geo Monitoring | | |
| Confirm the S3 endpoint is responding | `HEAD` | |
| Review bucket-level capacity for fast-growing buckets | | Identify any namespace where week-over-week growth is accelerating beyond expected rates |

## Health Check

Run these checks before any planned change or as first-response steps when investigating node, replication, or S3 access issues.

- [ ] ECS Portal → Hardware → Nodes: all nodes show `GOOD`; no nodes are `DEGRADED` or offline
- [ ] `GET /vdc/nodes` — programmatic confirmation that all nodes report healthy status
- [ ] `GET /vdc/capacity` — cluster is below 80% used; free capacity is sufficient to absorb a node rebuild if needed
- [ ] `GET /vdc/alerts` — no active alerts of `ERROR` or `CRITICAL` severity
- [ ] ECS Portal → Geo Monitoring — all VDC replication groups are in sync with zero or near-zero lag
- [ ] ECS Portal → Hardware → Disks: no disks in `FAILED` or `SUSPECT` state
- [ ] S3 endpoint functional test: a `ListBuckets` or `HeadBucket` request completes within expected latency
- [ ] `ecscli namespace list` — all expected namespaces are present and accessible

```bash
# Authenticate to the ECS Management REST API (returns X-SDS-AUTH-TOKEN)
curl -s -k -u "sysadmin:<password>" \
  "https://<ecs-node>:4443/login" -D -

# Retrieve VDC capacity (total, used, available, percent full)
curl -s -k -H "X-SDS-AUTH-TOKEN: <token>" \
  "https://<ecs-node>:4443/vdc/capacity"

# List all nodes and their health status
curl -s -k -H "X-SDS-AUTH-TOKEN: <token>" \
  "https://<ecs-node>:4443/vdc/nodes"

# Retrieve active alerts for the VDC
curl -s -k -H "X-SDS-AUTH-TOKEN: <token>" \
  "https://<ecs-node>:4443/vdc/alerts"

# Test S3 endpoint — list buckets for a namespace using a valid access key
aws s3 ls s3:// --endpoint-url https://<s3-endpoint>:9021 \
  --no-verify-ssl

# List namespaces via ecscli
ecscli namespace list

# List buckets in a specific namespace
ecscli bucket list --namespace <namespace>
```

## Pre-Change Checklist

- [ ] All nodes online and healthy
- [ ] No active alerts at ERROR or CRITICAL level
- [ ] Replication health OK (no lag or failed replication)
- [ ] Capacity below 75%
- [ ] S3 endpoint responding

## Health Summary Table

| Check | Expected | Action if Not Met |
|---|---|---|
| Node state | All ONLINE | Investigate offline nodes |
| Capacity | < 75% | Plan expansion |
| Replication | No lag/failures | Check network and replication group |
| S3 endpoint | Reachable | Check load balancer and node services |
| Alerts | None critical | Resolve before changes |
