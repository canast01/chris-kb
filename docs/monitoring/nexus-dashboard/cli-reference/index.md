# Nexus Dashboard CLI Reference

Nexus Dashboard is managed via its REST API and the `nd` CLI available on the appliance via SSH. The REST API base URL is `https://<nd_fqdn>/login`. SSH as `rescue-user` for appliance-level operations.

---

## Appliance Access

```bash
# SSH to Nexus Dashboard
ssh rescue-user@<nd_fqdn>

# Check ND services status
acs health

# Check cluster node status
acs cluster info

# Show ND version
cat /var/lib/nd/version.txt

# View logs
kubectl logs -n nd-base <pod_name>
```

---

## REST API — Authentication

```bash
# Authenticate and get token
curl -k -X POST https://<nd_fqdn>/login   -H "Content-Type: application/json"   -d '{"userName":"admin","userPasswd":"<pass>","domain":"DefaultAuth"}'

# The response contains a token field — use as Authorization header
```

---

## Fabric Health

```bash
# List all fabrics (sites) managed by ND
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/sites   -H "Authorization: <token>"

# Get health for all sites
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/sites/health   -H "Authorization: <token>"

# Get detail for a specific site
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/sites/<site_id>   -H "Authorization: <token>"
```

---

## Insights & Alerts

```bash
# List all active alerts
curl -k -X GET "https://<nd_fqdn>/nexus/infra/api/api/v1/faults?severity=critical"   -H "Authorization: <token>"

# List anomalies
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/events/anomalies   -H "Authorization: <token>"

# List advisories
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/advisories   -H "Authorization: <token>"
```

---

## Nodes & Inventory

```bash
# List all nodes across managed fabrics
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/nodes   -H "Authorization: <token>"

# Get node detail
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/nodes/<node_id>   -H "Authorization: <token>"

# Check software versions
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/software-upgrades/compatibility   -H "Authorization: <token>"
```

---

## Services (Insights / Orchestrator)

```bash
# List installed ND services
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/services   -H "Authorization: <token>"

# Get status of a specific service
curl -k -X GET https://<nd_fqdn>/nexus/infra/api/api/v1/services/<service_id>   -H "Authorization: <token>"
```
