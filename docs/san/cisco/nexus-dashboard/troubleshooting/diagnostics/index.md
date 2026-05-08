# Nexus Dashboard — Diagnostics

> Part of the [Nexus Dashboard](../../) reference.

---

## Overview

This page covers diagnostic procedures and log collection steps for investigating Nexus Dashboard platform issues, NDFC fabric management problems, and NDI telemetry issues. It also covers how to collect the support bundle for Cisco TAC escalation.

---

## Log Locations

### Platform Logs (ndadmin CLI)

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# View platform-level logs
acs system logs --tail 100

# Filter by component
acs system logs --component ndfc --tail 100
acs system logs --component ndi --tail 100
acs system logs --component security --tail 100

# Show audit log entries (user activity)
acs system logs --component audit --tail 50
```

### Kubernetes Pod Logs (Application Level)

```bash
# List all namespaces used by ND apps
kubectl get namespaces | grep -E "ndfc|ndi|nd-platform"

# Get NDFC server logs
kubectl logs -n ndfc deployment/ndfc-server --tail=100

# Get NDFC discovery logs
kubectl logs -n ndfc deployment/ndfc-discovery-manager --tail=100

# Get NDFC performance manager logs
kubectl logs -n ndfc deployment/ndfc-pm --tail=100

# Get NDI logs
kubectl logs -n ndi deployment/ndi-anomaly-engine --tail=100

# Get Keycloak (authentication) logs
kubectl logs -n nd-platform deployment/nd-keycloak --tail=100 | grep -i "error\|fail\|login"

# Get Nginx ingress logs (HTTP request details)
kubectl logs -n nd-platform deployment/nd-nginx --tail=100

# Get previous container logs (crash recovery)
kubectl logs -n ndfc deployment/ndfc-server --previous --tail=100
```

---

## Generating a TAC Support Bundle

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Generate support bundle — includes all platform logs, cluster state,
# Kubernetes events, node resource state, and app logs
acs techsupport --output /tmp/nd-support-$(date +%Y%m%d).tar.gz

# Monitor generation (may take 5-15 minutes)
# The command blocks until complete

# Transfer to your workstation
scp ndadmin@nd-dc1-1.corp.example.com:/tmp/nd-support-$(date +%Y%m%d).tar.gz ./

# For NDFC-specific issues, also collect the NDFC support bundle
kubectl exec -n ndfc deployment/ndfc-server -- \
  /usr/local/ndfc/sbin/collect-support.sh --output /tmp/ndfc-support.tar.gz
kubectl cp ndfc/$(kubectl get pod -n ndfc -l app=ndfc-server -o jsonpath='{.items[0].metadata.name}'):/tmp/ndfc-support.tar.gz ./ndfc-support-$(date +%Y%m%d).tar.gz
```

---

## Cluster Diagnostics

### Node Resource State

```bash
# CPU and memory usage per node
acs system resources

# Detailed Kubernetes node metrics
kubectl top nodes

# Per-pod resource usage (most memory/CPU hungry pods)
kubectl top pods --all-namespaces --sort-by=memory | head -20

# Node disk usage
kubectl get nodes -o wide
# SSH to each node and check:
df -h
du -sh /data/
```

### Kubernetes Events

```bash
# Recent cluster events (shows pod failures, scheduling issues, etc.)
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -50

# Events in a specific namespace
kubectl get events -n ndfc --sort-by='.lastTimestamp' | tail -20
```

### etcd Health

```bash
# Check etcd cluster health
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health

# Check etcd leader
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint status --write-out=table

# Expected: one LEADER, two followers for a 3-node cluster
```

---

## NDFC Diagnostics

### Discovery Issues

```bash
# Check discovery manager logs for a specific switch
kubectl logs -n ndfc deployment/ndfc-discovery-manager --tail=500 \
  | grep "<switch-ip>"

# Test SSH from ND data network
acs network test --host <switch-ip> --port 22

# Test SNMP v3
kubectl exec -n ndfc deployment/ndfc-server -- \
  snmpget -v3 -u ndfc_poll -l authPriv -a SHA -A <auth-pass> \
  -x AES -X <priv-pass> <switch-ip> sysDescr.0

# Trigger a manual rediscovery via API
TOKEN=$(curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"admin","userPasswd":"<pass>","domain":"local"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -X POST \
  "https://nd-dc1.corp.example.com/appcenter/cisco/ndfc/api/v1/san/fabrics/rediscover" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"fabricName":"DC1-FABRIC-A","rediscoverAll":false,"switchSerialNumbers":["<serial>"]}'
```

### Zoning Issues

```bash
# Check NDFC zone manager logs
kubectl logs -n ndfc deployment/ndfc-zone-manager --tail=200 \
  | grep -i "error\|fail\|conflict"

# Verify zone consistency on a specific MDS switch (NX-OS CLI)
# From a terminal to the switch:
show zoneset active vsan <vsan-id>
show zone status vsan <vsan-id>
show zone merge-failure vsan <vsan-id>
```

### Database Diagnostics

```bash
# Connect to NDFC database (PostgreSQL)
kubectl exec -n ndfc deployment/ndfc-server -- \
  psql -U postgres -c "\l"
# Lists databases: ndfc, pmdb, etc.

# Check NDFC main DB size
kubectl exec -n ndfc deployment/ndfc-server -- \
  psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('ndfc'));"

# Find large tables
kubectl exec -n ndfc deployment/ndfc-server -- \
  psql -U postgres ndfc -c "
SELECT relname, pg_size_pretty(pg_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_relation_size(relid) DESC
LIMIT 10;"
```

---

## NDI Diagnostics

### Telemetry Collection

```bash
# Check NDI flow collector pod
kubectl get pods -n ndi | grep collector
kubectl logs -n ndi deployment/ndi-flow-collector --tail=200 | grep -i "error\|drop"

# Check Elasticsearch health (NDI primary storage)
kubectl exec -n ndi deployment/ndi-elasticsearch -- \
  curl -sk http://localhost:9200/_cluster/health?pretty
# Expected: status "green"; if "red": shards are unassigned (disk or node issue)

# Check Elasticsearch disk usage
kubectl exec -n ndi deployment/ndi-elasticsearch -- \
  curl -sk http://localhost:9200/_cat/allocation?v
# If disk.percent > 85%: Elasticsearch watermark triggered, stops accepting writes
```

### NDI Anomaly Engine

```bash
# Check anomaly engine logs
kubectl logs -n ndi deployment/ndi-anomaly-engine --tail=200 | grep -i "error\|fail"

# Verify NDI license is valid
kubectl exec -n ndi deployment/ndi-anomaly-engine -- \
  curl -sk http://nd-license-service/api/v1/licenses | python3 -m json.tool | grep -i "ndi\|insights"
```

---

## Network Diagnostics

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Test connectivity to all managed switch IPs
acs network test --host <switch-ip> --port 22     # SSH
acs network test --host <switch-ip> --port 161    # SNMP
acs network test --host ldap.corp.example.com --port 636  # LDAPS

# Capture traffic on the data interface (requires tcpdump)
kubectl exec -n ndfc deployment/ndfc-discovery-manager -- \
  timeout 30 tcpdump -i eth0 -n host <switch-ip> -c 50

# Check SNMP trap reception
kubectl exec -n ndfc deployment/ndfc-server -- \
  timeout 30 tcpdump -i eth0 -n udp port 162 -c 10
```

---

## Performance Diagnostics

```bash
# ND cluster resource snapshot
acs system resources

# Kubernetes resource usage per namespace
kubectl top pods --all-namespaces --sort-by=cpu | head -20

# Measure REST API response time
time curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"svc-monitor","userPasswd":"<pass>","domain":"local"}'
# Expected: < 2 seconds; > 5 seconds indicates platform performance issue

# Check NDFC API response time
TOKEN=$(... obtain token ...)
time curl -sk \
  "https://nd-dc1.corp.example.com/appcenter/cisco/ndfc/api/v1/inventory/switches" \
  -H "Authorization: Bearer ${TOKEN}" > /dev/null
# Expected: < 5 seconds for < 200 switches
```

---

## Increasing Log Verbosity (Temporary)

For active troubleshooting, temporarily increase log verbosity on NDFC:

```bash
# Patch NDFC server log level to DEBUG
kubectl set env deployment/ndfc-server -n ndfc LOG_LEVEL=DEBUG

# Reproduce the issue and collect logs
kubectl logs -n ndfc deployment/ndfc-server --tail=500 | grep -i "debug\|error" > /tmp/ndfc-debug.log

# Return to INFO level after troubleshooting
kubectl set env deployment/ndfc-server -n ndfc LOG_LEVEL=INFO
kubectl rollout restart deployment/ndfc-server -n ndfc
kubectl rollout status deployment/ndfc-server -n ndfc
```

DEBUG logging generates large volumes and may impact performance. Revert to INFO as soon as the issue is reproduced and logs collected.
