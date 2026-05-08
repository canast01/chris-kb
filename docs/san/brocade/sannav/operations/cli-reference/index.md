# SANnav — CLI Reference

> Part of the [SANnav](../../) reference.

---

## Overview

SANnav provides two CLI interfaces:
1. **SANnav appliance CLI** — accessed via SSH to the SANnav VM. Used for appliance administration, service management, backup, and upgrade.
2. **REST API** — the primary interface for automation and integration. Covers all operations available in the GUI.

This page documents the appliance CLI commands and the most commonly used REST API calls.

---

## Appliance CLI (SSH)

Connect via SSH: `ssh admin@sannav-dc1.corp.example.com`

### Service Management

```bash
# Show status of all SANnav services
sannav status

# Start all services
sannav start

# Stop all services (maintenance only)
sannav stop

# Restart all services
sannav restart

# Show current version
sannav version

# Show license summary
sannav license
```

### Backup and Restore

```bash
# Trigger a full backup to default local directory
sannav backup --type full

# Trigger a backup to a specific path
sannav backup --type full --destination /tmp/bkp/

# Check backup status
sannav backup --status

# List local backups
sannav backup --list

# Restore from a backup file
sannav restore /tmp/sannav-backup-20260506.tar.gz

# Monitor restore progress
sannav restore --status
```

### Upgrade

```bash
# Apply an upgrade package
sannav upgrade /tmp/sannav-upgrade-2.4.0.bin

# Check upgrade status (during upgrade)
sannav upgrade --status

# Show upgrade history
sannav upgrade --history
```

### Network Configuration

```bash
# Show current IP configuration
ip addr show eth0

# Show hostname
hostname

# Show DNS configuration
cat /etc/resolv.conf

# Test connectivity to a managed switch
curl -sk -o /dev/null -w "%{http_code}" https://<switch-ip>/rest/loginresult
# Expected: 200 or 401 (reachable); anything else = connectivity problem

# Test LDAP connectivity
ldapsearch -H ldaps://ldap.corp.example.com \
  -D "CN=sannav-svc,OU=Service Accounts,DC=corp,DC=example,DC=com" \
  -w <password> -b "DC=corp,DC=example,DC=com" "(sAMAccountName=testuser)"
```

### Log Access

```bash
# Main application log
tail -f /opt/sannav/logs/server.log

# Discovery engine log
tail -f /opt/sannav/logs/discovery.log

# Event processing log
tail -f /opt/sannav/logs/event-engine.log

# Upgrade log
cat /opt/sannav/logs/upgrade.log

# Search logs for errors in the last 100 lines
grep -i "ERROR\|FATAL\|Exception" /opt/sannav/logs/server.log | tail -100

# Show system journal (OS-level)
journalctl -u sannav -n 100 --no-pager
```

### Disk and System

```bash
# Disk usage
df -h

# Check SANnav data directory size
du -sh /opt/sannav/data/

# Check database sizes individually
du -sh /opt/sannav/data/postgres/
du -sh /opt/sannav/data/influxdb/

# Memory usage
free -h

# CPU load
uptime
```

---

## REST API Quick Reference

### Authentication

```bash
# Login — obtain token
TOKEN=$(curl -sk -X POST https://sannav-dc1.corp.example.com/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"svc-monitor","password":"<password>"}}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['authToken'])")

echo "Token: $TOKEN"

# Logout (always clean up sessions)
curl -sk -X DELETE https://sannav-dc1.corp.example.com/rest/logout \
  -H "Authorization: Bearer $TOKEN"
```

### Fabric and Switch Queries

```bash
# List all resource groups (fabrics)
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# List all switches
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Get a specific switch (replace <switchId>)
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches/<switchId>" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# List all ports (can be large — pipe through grep for filtering)
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/ports \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -m json.tool | grep -E '"portState"|"portType"|"portWwn"'
```

### Events and Alerts

```bash
# Get active alerts (last 100)
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/all/events?limit=100&filter=acknowledged:false" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Get events for a specific switch
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/all/events?switchId=<switchId>" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Zoning

```bash
# Get defined zone set for a fabric
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/<fabricId>/zonedb" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Get active zone set
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/<fabricId>/zones/active" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Inventory Export

```bash
# Export all switches to CSV (use Accept header for CSV format)
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: text/csv" -o switches-$(date +%Y%m%d).csv

echo "Exported to switches-$(date +%Y%m%d).csv"
```

### Firmware

```bash
# List available firmware images
curl -sk https://sannav-dc1.corp.example.com/rest/firmware/images \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Initiate firmware upgrade on a switch
curl -sk -X POST "https://sannav-dc1.corp.example.com/rest/firmware/upgrade" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "switchIds": ["<switchId>"],
    "firmwareVersion": "9.2.1a",
    "activationMode": "AUTO"
  }' | python3 -m json.tool
```

---

## Useful One-Liners

```bash
# Count managed switches by connectivity state
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/switches \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "
import sys, json, collections
data = json.load(sys.stdin)
states = collections.Counter(s.get('connectivityState') for s in data.get('switches', []))
print(dict(states))
"

# List all offline F_Ports (potential host/storage connectivity issues)
curl -sk https://sannav-dc1.corp.example.com/rest/resourcegroups/all/ports \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data.get('ports', []):
    if p.get('portType') == 'F_PORT' and p.get('portState') != 'ONLINE':
        print(p.get('switchName'), p.get('portIndex'), p.get('portState'))
"
```
