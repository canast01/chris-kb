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
┌────────────────────────────────── Aria Operations — Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Adapter Not Collecting            │  │               UI / API Issues               │   │
│   │               Check credential               │  │             Restart web service             │   │
│   │             Verify network reach             │  │             Check master status             │   │
│   │              Review adapter log              │  │             vracli cluster list             │   │
│   │             Re-test in Solutions             │  │             Clear browser cache             │   │
│   │             Check firewall rules             │  │             Check cert validity             │   │
│   │                Reinstall PAK                 │  │            Collect support bundle           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Support bundle via vrops-support-get command; logs in /var/log/vmware/vcops on each node           │
│                                                                                                       │
│                                                  ▼                                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Performance Issues              │  │            Alert / Policy Issues            │   │
│   │              Check node CPU/mem              │  │             Check symptom state             │   │
│   │             Review object count              │  │              Policy inheritance             │   │
│   │            Reduce collection int             │  │              Alert dedup check              │   │
│   │                Add data nodes                │  │             Outbound plugin test            │   │
│   │               Archive old data               │  │             Notification history            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Logs: /var/log/vmware/vcops · support bundle: vrops-support-get from master node SSH                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Support bundle = Compressed archive of logs and config; used by VMware GSS for diagnosis             │
│  vrops-support-get = CLI command on Aria Ops appliance to collect support bundle                      │
│  Solutions UI = Administration > Solutions; shows adapter status and allows credential test           │
│  Cluster list = vracli cluster list shows node health: ONLINE/OFFLINE/INITIALIZING                    │
│  PAK reinstall = Remove and re-add adapter package; resets adapter state without data loss            │
│  Collection interval = How often adapter polls source; reduce if master is overloaded                 │
│  Symptom state = True/False evaluation of a threshold condition for an object                         │
│  Policy inheritance = Child policy inheriting settings from parent; override at child level           │
│  Alert dedup = Aria Ops suppressing repeat alerts for same symptom within cool-down window            │
│  Notification history = Log of outbound alert notifications sent; in Administration > Outbound        │
│  Object count = Number of monitored objects; growth reduces collection capacity per node              │
│  Data node = Worker node; adding nodes scales collection capacity linearly                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
