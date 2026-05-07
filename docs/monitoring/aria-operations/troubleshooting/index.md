# Aria Operations: Troubleshooting Common Issues

This page covers frequent operational issues in VMware Aria Operations: adapter collection failures, login problems, data gaps, and performance degradation. Use these checks before raising a support case.

## Checking Adapter and Collector Status

Most data problems originate from an adapter instance that has stopped collecting.

Navigation: **Administration > Solutions > Cloud Accounts / Adapter Instances**

```bash
# Check adapter instance status via API
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/adapterinstances" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" | jq '.adapterInstanceList[] | {name, status: .statusMessage}'

# View recent collection log for a specific adapter instance
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/adapterinstances/<adapterId>/monitoringstate" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json"
```

Adapter status meanings:

| Status | Meaning | Action |
|---|---|---|
| COLLECTING | Normal operation | None |
| STOPPED | Adapter manually stopped | Start adapter instance |
| FAILED | Authentication or network error | Check credentials, test connection |
| NO_DATA | Connected but no metrics | Verify permissions on monitored system |
| WAITING | Queued for collection | Wait one cycle; restart if persistent |

## Log Files and Diagnostic Collection

```bash
# SSH to Aria Ops node (default admin user)
ssh admin@aria-ops.example.com

# View collector service log
tail -f /storage/log/vcops/collector.log

# View web service log
tail -f /storage/log/vcops/web.log

# Collect a support bundle from CLI
/usr/lib/vmware-vcops/tools/support/vcopsSupport.sh

# Check service health
/etc/init.d/vmware-vcops-watchdog status
```

## Login and Authentication Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| "Invalid credentials" on login | Password expired or LDAP failure | Reset local admin password via vApp console |
| SSO login loop | vCenter SSO misconfigured | Reconfigure SSO under Administration > Authentication |
| Session expires too quickly | Default session timeout | Change in Administration > Global Settings > Session Timeout |
| API token rejected | Token expired (24-hour TTL) | Re-authenticate to get a new token |

```bash
# Obtain a new API auth token
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "authSource": "LOCAL", "password": "yourpassword"}' \
  | jq '.token'
```

## Collection Failures and Data Gaps

If objects show stale or missing data:

1. Check adapter status (see above).
2. Verify network connectivity from collector to monitored system.
3. Confirm credentials have not expired.
4. Check for certificate errors (common after vCenter recertification).

```bash
# Test connectivity from Aria Ops node to vCenter
ssh admin@aria-ops.example.com
curl -sk https://vcenter.example.com/sdk/vimService.wsdl | head -5

# Force a collection cycle for an adapter instance
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/adapterinstances/<adapterId>/testconnection" \
  -H "Authorization: vRealizeOpsToken <token>"
```

## Performance Degradation

| Symptom | Likely Cause | Fix |
|---|---|---|
| UI very slow | Cassandra or Postgres overloaded | Check disk I/O, expand datastore |
| Dashboards timeout | Too many widgets with long time ranges | Reduce widget count and range |
| Alert processing delayed | High workload on analytics node | Check analytics service, consider scaling cluster |
| High vApp CPU usage | Too many objects or metrics | Review object count; disable unused adapters |

```bash
# Check Aria Ops cluster node resource usage
ssh admin@aria-ops.example.com
# Check CPU and memory
top -b -n 1 | head -20

# Check disk usage on key partitions
df -h /storage/db /storage/log /storage/core
```

## Common Issues Reference

| Issue | First Check | Second Check |
|---|---|---|
| Objects missing from UI | Adapter instance status | Object collection group membership |
| Metrics not updating | Last collection timestamp | Adapter credentials |
| Alerts not firing | Alert definition policy assignment | Symptom threshold values |
| Report emails not sending | Outbound SMTP settings | Email recipients field |
| License warning banner | License key expiry date | Add new key in Administration > Licensing |
