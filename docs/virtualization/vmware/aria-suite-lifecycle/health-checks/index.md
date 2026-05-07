# Aria Suite Lifecycle — Health Checks

## Overview

Run LCM health checks before any upgrade, after any certificate rotation, and as part of routine quarterly verification. Health checks surface service status, certificate expiry, disk pressure, and NTP drift.

```bash
# SSH into the LCM appliance
ssh root@<lcm-appliance-fqdn>

# Run the built-in health check script
/usr/lib/vmware-vrlcm/scripts/lcmHealthCheck.sh

# View last health check report
cat /var/log/vmware/vrlcm/lcm-health-check.log | tail -200
```

## Service Status Verification

```bash
# Check all LCM-related services
systemctl list-units --type=service | grep -i "vrlcm\|vmware"

# Check individual services
systemctl status vmware-vrlcm
systemctl status vmware-vrlcm-db
systemctl status nginx

# Restart a failed service
systemctl restart vmware-vrlcm

# View service logs via journald
journalctl -u vmware-vrlcm -n 200 --no-pager

# Check LCM API health endpoint
curl -sk https://localhost/lcm/api/v1/health | python3 -m json.tool
```

Key services and expected states:

| Service | Expected State | Notes |
|---|---|---|
| `vmware-vrlcm` | active (running) | Core LCM service |
| `vmware-vrlcm-db` | active (running) | Embedded Postgres |
| `nginx` | active (running) | Reverse proxy / UI |
| `vmware-vrlcm-certmanager` | active (running) | Certificate management |
| `sshd` | active (running) | Required for remote access |

## Certificate Expiry Checks

```bash
# Check LCM appliance certificate
openssl s_client -connect <lcm-fqdn>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates

# List all managed product certificates via LCM API
curl -sk -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/certificates \
  | python3 -m json.tool

# Check certificate expiry for a specific product
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/certificates?productId=<product-id>" \
  | python3 -m json.tool

# Trigger certificate rotation via LCM API
curl -sk -X POST -u admin:<password> \
  https://<lcm-fqdn>/lcm/api/v1/certificates/rotate \
  -H "Content-Type: application/json" \
  -d '{"productId": "<product-id>"}'
```

Certificate check thresholds:

| Days to Expiry | Status | Action |
|---|---|---|
| > 90 days | Healthy | No action required |
| 30–90 days | Warning | Plan rotation |
| 7–30 days | Critical | Rotate within a week |
| < 7 days | Emergency | Rotate immediately |

## Disk Space Verification

```bash
# Check all mount points
df -h

# Check LCM-specific data directories
du -sh /data/vmware/vrlcm/*
du -sh /var/log/vmware/vrlcm/

# Check Postgres database size
du -sh /data/vmware/vrlcm/db/

# Clean old LCM logs older than 30 days
find /var/log/vmware/vrlcm/ -name "*.log.*" -mtime +30 -delete

# Check available inodes (often missed)
df -i
```

Disk space thresholds:

| Mount | Warning | Critical | Action if Critical |
|---|---|---|---|
| `/` | 75% | 85% | Remove old bundles and logs |
| `/data` | 70% | 80% | Clean old content library cache |
| `/var/log` | 80% | 90% | Rotate and archive logs |

## NTP and Time Sync

```bash
# Check NTP sync status
timedatectl status

# Check chrony sources
chronyc sources -v

# Check time offset (must be < 5 seconds for SSO)
chronyc tracking | grep "System time"

# Force time sync
chronyc makestep

# Verify NTP config
cat /etc/chrony.conf
```

## Pre-Operation Health Summary

Before any LCM operation (upgrade, patch, certificate rotation), confirm all of the following pass:

```bash
# 1. All services running
systemctl is-active vmware-vrlcm vmware-vrlcm-db nginx

# 2. Disk space adequate
df -h | awk 'NR>1 && $5+0 > 70 {print "WARNING:", $0}'

# 3. No active LCM operations in progress
curl -sk -u admin:<password> \
  "https://<lcm-fqdn>/lcm/api/v1/operations?status=RUNNING" \
  | python3 -m json.tool

# 4. NTP in sync
chronyc tracking | grep "System time"

# 5. LCM API reachable and healthy
curl -sk -o /dev/null -w "%{http_code}" https://<lcm-fqdn>/lcm/api/v1/health
```
