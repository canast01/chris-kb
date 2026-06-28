---
tags:
  - operations
  - san
---
# Nexus Dashboard: Fabric Health Score, Endpoint Reachability, and Flow Telemetry

<div class="kb-summary">
Nexus Dashboard: Fabric Health Score, Endpoint Reachability, and Flow Telemetry reference covering Interpreting Health Score Changes, Endpoint Reachability, Flow Telemetry, Using Flow Data for Troubleshooting, Common Fabric Health Issues.

*Applies to: Cisco MDS · Nexus*
</div>

Flow telemetry fields:

| Field | Description |
|---|---|
| `src_ip` / `dst_ip` | Source and destination IP |
| `src_port` / `dst_port` | Transport layer ports |
| `protocol` | TCP, UDP, ICMP |
| `bytes` | Total bytes transferred |
| `latency_us` | Fabric latency in microseconds |
| `drop_count` | Packets dropped in fabric |

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Using Flow Data for Troubleshooting

```bash
# Identify dropped flows between two hosts
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/flows/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "src_ip": "10.0.10.100",
      "dst_ip": "10.0.20.50",
      "drop_count_gt": 0
    }
  }'
```

## Common Fabric Health Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Health score drops after upgrade | Post-upgrade anomalies detected | Review anomalies; acknowledge known post-upgrade events |
| Endpoint shown as unreachable | ARP entry expired or NIC offline | Check physical connectivity and ARP table on leaf |
| Flow telemetry missing | Telemetry not configured on switches | Enable NetFlow/ERSPAN on fabric switches |
| Health score not updating | NDI service connectivity issue | Check NDI cluster status in Nexus Dashboard services page |
| Endpoint shown in wrong EPG | VM migrated but policy not followed | Check VMM integration policy and port-group mapping |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Nexus Dashboard: Fabric Alerts, Severity, Acknowledgement, and Notification Policies](alerts.md)
- [Cisco Nexus Dashboard — Operations Backup & Restore](backup-restore.md)
- [Cisco Nexus Dashboard — Operations CLI Reference](cli-reference.md)
- [Nexus Dashboard — Operations](index.md)
- [Nexus Dashboard — Architecture](../architecture/)
- [Nexus Dashboard — Initial Deployment](../deploy/)
- [Nexus Dashboard — Security](../security/)
- [Cisco Nexus Dashboard — Troubleshooting](../troubleshooting/)
