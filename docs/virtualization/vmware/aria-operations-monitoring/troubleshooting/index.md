# Aria Operations — Troubleshooting (Monitoring)

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
```text
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
```bash
# Check Aria Ops cluster node resource usage
ssh admin@aria-ops.example.com
# Check CPU and memory
top -b -n 1 | head -20

# Check disk usage on key partitions
df -h /storage/db /storage/log /storage/core
```
