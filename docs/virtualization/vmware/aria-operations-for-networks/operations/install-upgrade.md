---
tags:
  - aria-networks
  - operations
  - vmware
---
# vRNI Install & Upgrade
![vRNI Install & Upgrade](../../../../assets/virtualization-vmware-aria-operations-for-networks-operation.svg)


```bash
# Check HTTPS is reachable
curl -sk https://aon-platform.example.local -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200 (redirect to login page)

# SSH to platform to verify services
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra
```

```bash
# 1. Take config backup
TOKEN=$(curl -sk -X POST "https://aon.example.local/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk "https://aon.example.local/api/ni/settings/backup" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  --output "aon-backup-pre-upgrade-$(date +%Y%m%d).tar.gz"

# 2. Take vSphere snapshot of Platform VM (via PowerCLI or vCenter UI)
# PowerCLI:
Get-VM "aon-platform-01" | New-Snapshot -Name "Pre-Upgrade-6.14.0" -Description "Before AON upgrade to 6.14.0"

# 3. Note current version
curl -sk "https://aon.example.local/api/ni/system/version" \
  -H "Authorization: NetworkInsight ${TOKEN}" | python3 -m json.tool
```
```bash
ssh ubuntu@aon-platform.example.local

# Upload the upgrade bundle to the platform
scp VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak ubuntu@aon-platform.example.local:/tmp/

# On Platform VM
sudo /opt/vmware/bin/upgrade.sh /tmp/VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak

# Monitor upgrade progress
sudo tail -f /var/log/vrni-platform/upgrade.log
```
```bash
# Check version
curl -sk "https://aon.example.local/api/ni/system/version" \
  -H "Authorization: NetworkInsight ${TOKEN}" | python3 -m json.tool

# Check all services are running
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres

# Check Collectors re-connected (they should reconnect automatically)
curl -sk "https://aon.example.local/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys,json
for c in json.load(sys.stdin).get('results',[]):
    print(c.get('nickname',''), c.get('status',''))
"
```
```bash
# Revert Platform VM snapshot (this is a destructive operation — confirm before proceeding)
Get-VM "aon-platform-01" | Get-Snapshot -Name "Pre-Upgrade-6.14.0" | Set-VM -SnapShot $_ -Confirm:$false

# After revert, Collectors should auto-reconnect to the older Platform
# If not, re-pair manually:
ssh ubuntu@aon-collector-dc1.example.local
sudo /home/ubuntu/support/pairing.sh
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

!!! warning "Host enters maintenance mode"
    ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. Confirm DRS is Fully Automated and HA admission control is satisfied before starting.

---

## See also

- [vRNI Health Checks](health-checks/)
- [vRNI Common Issues](../troubleshooting/common-issues/)
- [AON Operational Procedures](procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
