# Aria Suite Lifecycle — Health Checks

## Daily Health Checks

```bash
# LCM appliance disk usage — keep /data (NFS) and / below 80%
df -h

# LCM service status
systemctl status lcm

# Check recent log errors
grep -E "ERROR|WARN" /var/log/lcm/lcm-app.log | tail -50

# Verify NFS mount is healthy
mount | grep /data
ls /data/ | head
```

In the LCM UI:
- **Lifecycle Operations → Environments**: all environment cards should show green health indicators
- **Locker → Certificates**: check for certificates expiring within 30 days
- **Settings → My VMware**: verify bundle sync schedule last ran successfully
