---
tags:
  - aria-logs
  - operations
  - vmware
---
# Aria Operations for Logs — Backup and Restore
![Aria Operations for Logs — Backup and Restore](../../../../assets/virtualization-vmware-aria-operations-for-logs-operations-ba.svg)


```bash
ssh admin@vrli-prod-01.example.local

# Confirm cluster health before backup window
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state}'
# All nodes should show state: "ACTIVE"

# Check disk usage — do not back up a node with >90% disk (indicates ingestion pressure)
df -h /var/log/loginsight
```

```bash
BASE="https://vrli-prod-01.example.local"
AUTH="admin:<password>"

# Export alert definitions
curl -sk -u "$AUTH" "$BASE/api/v2/alerts" | jq '.' > vrli-alerts-$(date +%Y%m%d).json

# Export notification channels
curl -sk -u "$AUTH" "$BASE/api/v2/notification" | jq '.' > vrli-notifications-$(date +%Y%m%d).json

# Export agents and agent groups
curl -sk -u "$AUTH" "$BASE/api/v2/agents/groups" | jq '.' > vrli-agent-groups-$(date +%Y%m%d).json

# Export archive configuration
curl -sk -u "$AUTH" "$BASE/api/v2/archiver" | jq '.' > vrli-archiver-$(date +%Y%m%d).json
```
```text
Administration → Archiving → Configure → enable NFS archive
```
```bash
# From master node SSH
showmount -e nas-01.example.local
mount -t nfs nas-01.example.local:/exports/vrli-archive /mnt/test-archive
touch /mnt/test-archive/.write-test && echo "OK" && rm /mnt/test-archive/.write-test
umount /mnt/test-archive
```
```bash
ssh admin@vrli-prod-01.example.local
curl -sk -u 'admin:<password>' \
  "https://localhost/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state}'
```
```text
Administration → Cluster → each node should show state Active and ingestion rate > 0 events/sec
```
```bash
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/alerts" | jq '. | length'
```

```d2
direction: right

hub: "Aria Operations for Logs\nOperations" {shape: hexagon}
verify: "Verify" {shape: rectangle}

hub -> verify
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## See also

- [Aria Ops for Logs — Procedures](procedures/)
- [Aria Operations for Logs — Common Issues](../troubleshooting/common-issues/)
- [Aria Operations for Logs — Health Checks](health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
