# Aria Suite Lifecycle Operations
## Daily Health Checks

```bash
# 1. LCM appliance disk usage — keep /data (NFS) and / below 80%
df -h

# 2. LCM service status
systemctl status lcm

# 3. Check recent log errors
grep -E "ERROR|WARN" /var/log/lcm/lcm-app.log | tail -50

# 4. Verify NFS mount is healthy
mount | grep /data
ls /data/ | head
```

In the LCM UI:
- **Lifecycle Operations → Environments**: all environment cards should show green health indicators
- **Locker → Certificates**: check for certificates expiring within 30 days
- **Settings → My VMware**: verify bundle sync schedule last ran successfully

## Deploy a New Aria Product

1. LCM → Lifecycle Operations → Environments → select or create environment
2. Click "Add Product"
3. Select product (e.g., Aria Operations), version, and deployment size (Medium/Large)
4. Provide:
   - vCenter target: cluster, datastore, network
   - IP addresses / hostnames
   - Admin password (stored in LCM Locker)
5. LCM runs pre-checks (DNS, NTP, vCenter connectivity) — all must pass
6. Click Deploy — monitor via the workflow progress screen
7. Post-deployment: validate product UI is accessible and health shows green in LCM

## Trigger a Product Upgrade

1. LCM → Lifecycle Operations → Environments → click the product
2. Click "Upgrade" — LCM presents compatible target versions
3. Review pre-checks: all must pass before proceeding
4. Click "Start Upgrade" — LCM takes snapshots, performs upgrade, validates post-state
5. Monitor: Lifecycle Operations → Requests — expand the active upgrade task

If upgrade fails mid-way, LCM provides a "Rollback" option that reverts from snapshots.

## Check Upgrade Status

```bash
# Via LCM API
curl -k -u admin:password https://lcm.corp.local/lcm/lcops/api/v2/requests | python3 -m json.tool

# Via LCM appliance logs
tail -f /var/log/lcm/lcm-app.log | grep -E "upgrade|UPGRADE|task"
```

Via UI: Lifecycle Operations → Requests → filter by type "Upgrade" — shows step-by-step progress.

## Certificate Management via Locker

To replace a certificate on a managed product:

1. LCM → Locker → Certificates → Add Certificate (import PEM + private key)
2. LCM → Lifecycle Operations → Environments → select product → Replace Certificate
3. Select the new certificate from Locker → proceed through wizard
4. LCM restarts product services to apply the new certificate

**Never replace certificates directly on appliances** — LCM loses track of the certificate and future upgrades may fail.

## Storage Management

Monitor NFS binary repository usage:

```bash
# Available space per product
du -sh /data/wp-content/downloads/*

# Clean up old binaries no longer needed (after upgrade is validated)
# LCM UI → Settings → Binary Mapping → select old version → Delete
```

Keep at minimum: current version + one previous version of each managed product.

## Troubleshooting LCM Issues

```bash
# Restart LCM service (if UI unresponsive)
systemctl restart lcm
systemctl status lcm

# Check LCM API health
curl -k https://localhost/lcm/lcops/api/v2/ping

# Full log capture for support SR
tar -czf /tmp/lcm-logs-$(date +%Y%m%d).tar.gz /var/log/lcm/
```

Common issues:
| Symptom | Likely Cause | Fix |
|---|---|---|
| Product shows "Out of Sync" | LCM cannot reach product | Verify network connectivity and credentials |
| Upgrade pre-check fails — NTP | Time drift > 5 seconds | Fix NTP on target appliance |
| Upgrade fails at "Backup" step | vCenter connectivity lost | Verify vCenter credentials in LCM |
| Certificate shows expired in Locker | Not renewed before expiry | Import new certificate; replace on product |
