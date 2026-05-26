# InsightIQ CLI Reference

InsightIQ is the Dell EMC analytics platform for PowerScale (Isilon) performance monitoring. It exposes a REST API and SSH access to the InsightIQ appliance for direct management. The API base URL is `https://<insightiq_fqdn>/api/json/v2`.
---

## Appliance Access

```bash
# SSH to the InsightIQ appliance
ssh administrator@<insightiq_fqdn>

# Check InsightIQ service status
sudo service insightiq status

# Restart InsightIQ service
sudo service insightiq restart

# View logs
tail -f /var/log/insightiq/insightiq.log

# Check disk space (InsightIQ database can grow large)
df -h /home/insightiq
```
```

---

## Clusters

```bash
# List all monitored clusters
curl -k -u "admin:<pass>"   https://<insightiq_fqdn>/api/json/v2/clusters

# Get detail for a specific cluster
curl -k -u "admin:<pass>"   https://<insightiq_fqdn>/api/json/v2/clusters/<cluster_guid>

# List nodes in a cluster
curl -k -u "admin:<pass>"   https://<insightiq_fqdn>/api/json/v2/clusters/<cluster_guid>/nodes
```

---

## Performance Data

```bash
# List available performance breakouts
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/performance/breakouts"

# Query CPU utilisation for a cluster (last hour)
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/performance/breakouts/cluster.cpu.user?cluster=<guid>&begin=<epoch>&end=<epoch>"

# Query disk throughput
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/performance/breakouts/cluster.disk.bytes.in.rate?cluster=<guid>&begin=<epoch>&end=<epoch>"

# Query client protocol operations
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/performance/breakouts/cluster.protostats.nfs.ops.rate?cluster=<guid>&begin=<epoch>&end=<epoch>"
```

---

## Capacity

```bash
# Get capacity summary for a cluster
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/clusters/<guid>/capacity"

# Get per-node capacity
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/clusters/<guid>/nodes/<node_id>/capacity"
```

---

## Reports

```bash
# List available reports
curl -k -u "admin:<pass>"   https://<insightiq_fqdn>/api/json/v2/reports

# Download a report
curl -k -u "admin:<pass>"   "https://<insightiq_fqdn>/api/json/v2/reports/<report_id>/download"   -o report.csv
```
