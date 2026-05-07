# Aria Suite Lifecycle — Troubleshooting

## Installation Failures

Installation failures during initial LCM deploy or product install are usually caused by DNS resolution issues, insufficient resources, or OVA validation errors.

```bash
# Check LCM installer log
tail -200 /var/log/vmware/vrlcm/lcm-install.log

# Verify DNS resolution for all product FQDNs from LCM node
for fqdn in vrops.example.com vra.example.com wsa.example.com; do
  echo -n "$fqdn: "; nslookup $fqdn | grep "Address" | tail -1
done

# Check disk space before install
df -h /data /var/log /tmp

# Verify NTP sync (required for certificate operations)
chronyc tracking | grep "System time"
```

Common installation error codes:

| Error Code | Meaning | Resolution |
|---|---|---|
| `VRLCM_ERR_001` | DNS resolution failure | Fix DNS records; verify from LCM node |
| `VRLCM_ERR_012` | Insufficient disk space | Free space on `/data`; min 50 GB free |
| `VRLCM_ERR_023` | OVA checksum mismatch | Re-download bundle; verify SHA256 |
| `VRLCM_ERR_031` | vCenter connectivity failure | Check credentials and firewall to port 443 |
| `VRLCM_ERR_045` | Certificate pre-check failure | Verify cert CN/SAN matches product FQDN |

## Upgrade Stuck or Hung

If an upgrade operation stays in `RUNNING` state for more than 2 hours with no progress in the logs, use the following checks:

```bash
# Check current running operations
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/operations?status=RUNNING" \
  | python3 -m json.tool

# Check the specific request details
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/requests/<request-id> \
  | python3 -m json.tool

# Tail the LCM upgrade log
tail -f /var/log/vmware/vrlcm/lcm-upgrade.log

# Check if the Ansible runner is still active
ps aux | grep ansible

# Check for locked database operations
journalctl -u vmware-vrlcm-db -n 100 --no-pager | grep -i "lock\|block"
```

To safely retry a stuck upgrade:

```bash
# Cancel the stuck request (use with caution — verify state first)
curl -sk -X DELETE -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/requests/<request-id>

# Restart LCM service
systemctl restart vmware-vrlcm

# Re-trigger the upgrade after service recovers (allow 5 minutes)
curl -sk -u admin:<password> https://<lcm-fqdn>/lcm/api/v1/health
```

## Service Not Starting

```bash
# Check service status and recent errors
systemctl status vmware-vrlcm -l

# Check for port conflicts
ss -tlnp | grep -E "8080|443|5432"

# Check Java heap errors in service log
journalctl -u vmware-vrlcm --since "1 hour ago" | grep -i "OutOfMemory\|heap"

# Verify Postgres is up before starting LCM
systemctl start vmware-vrlcm-db
sleep 10
systemctl start vmware-vrlcm

# Check LCM database connectivity
psql -U vrlcm -h localhost -p 5432 -c "\l" 2>&1
```

Service startup failure causes:

| Symptom | Likely Cause | Action |
|---|---|---|
| Immediate exit after start | DB not ready | Start DB first; wait 30 seconds |
| Port 443 bind failure | nginx conflict or prior instance | `killall nginx`; restart nginx |
| `OutOfMemoryError` in log | JVM heap too small | Increase heap in `/etc/vmware/vrlcm/jvm.properties` |
| `Connection refused` on API | Service starting slowly | Wait 3–5 minutes; check log for ready message |

## Log Locations

All LCM logs are under `/var/log/vmware/vrlcm/`:

| Log File | Purpose |
|---|---|
| `lcm-app.log` | Main application log |
| `lcm-upgrade.log` | Upgrade operation detail |
| `lcm-install.log` | Product installation steps |
| `lcm-certmanager.log` | Certificate operations |
| `lcm-db.log` | Database queries and errors |
| `lcm-health-check.log` | Health check run output |

```bash
# Search all LCM logs for a specific error keyword
grep -r "ERROR\|FATAL" /var/log/vmware/vrlcm/ | tail -100

# Watch all logs live
tail -f /var/log/vmware/vrlcm/*.log

# Collect a support bundle
/usr/lib/vmware-vrlcm/scripts/lcm-support-bundle.sh --output /tmp/
ls -lh /tmp/lcm-support-*.zip
```

## Password and Credential Issues

```bash
# Reset LCM admin password via CLI
/usr/lib/vmware-vrlcm/bin/vrlcm-passwd-reset.sh --user admin

# Update stored product credentials (e.g. vCenter password changed)
curl -sk -X PUT -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/credentials/<credential-id> \
  -H "Content-Type: application/json" \
  -d '{"password": "<new-password>"}'

# Test connectivity with updated credentials
curl -sk -X POST -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/credentials/<credential-id>/test
```
