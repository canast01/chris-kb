---
tags:
  - san
  - troubleshooting
---
# Cisco DCNM — Troubleshooting Escalation

```bash
# 1. DCNM version
cat /var/dcnm/version

# 2. DCNM support bundle
/usr/local/cisco/dcm/dcnm/bin/collect-support-bundle.sh \
  --output /tmp/dcnm-support-$(date +%Y%m%d).tar.gz

# 3. Appliance resource state
free -h
df -h
uptime

# 4. Java heap state at time of issue
DCNM_PID=$(ps aux | grep "[d]cnm-server" | awk '{print $2}' | head -1)
jstat -gcutil ${DCNM_PID} 1s 5

# 5. OS-level resource snapshot
top -b -n 1 > /tmp/top-snapshot-$(date +%Y%m%d).txt
```
```text
┌─────────────────────────────── Cisco DCNM — Troubleshooting Escalation ───────────────────────────────┐
│                                                                                                       │
│  DCNM escalation: internal L2/L3 → Cisco TAC with log bundle, case severity, remote.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Internal Escalation Path           │  │             Cisco TAC Escalation            │   │
│   │         L1 → L2: basic checks + logs         │  │            Open case: TAC portal            │   │
│   │          L2 → L3: logs + show-tech           │  │           DCNM version + NX-OS ver          │   │
│   │         L3 → TAC: full data package          │  │           Sev-1: fabric management          │   │
│   │          Incident bridge for Sev-1           │  │           Remote: TAC SSH to DCNM           │   │
│   │        No config changes during inc.         │  │           RCA expected post-close           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Collect DCNM logs and MDS show tech-support before opening a Cisco TAC case.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Escalation Data Package            │  │           Severity Classification           │   │
│   │          DCNM logs: journalctl dump          │  │           Sev-1: DCNM down; fabric          │   │
│   │          appmgr status + db-status           │  │           Sev-2: zone push failing          │   │
│   │          show tech-support: per MDS          │  │          Sev-3: partial monitoring          │   │
│   │             Audit log CSV export             │  │           Sev-4: general question           │   │
│   │        Timeline: events before issue         │  │            CSAT after case close            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · management Ethernet · Cisco TAC upload portal · serial console access                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  journalctl dump = full DCNM service log; gzip and share to Cisco TAC                                 │
│  appmgr status   = DCNM VM CLI; service health output for TAC review                                  │
│  show tech-support= NX-OS MDS full diagnostic bundle; one per affected switch                         │
│  Audit log CSV   = DCNM action log export; shows what changed before incident                         │
│  Sev-1           = DCNM completely down; fabric management unavailable                                │
│  Sev-2           = DCNM partially working; zone changes or discovery failing                          │
│  Cisco TAC       = Technical Assistance Center; opened at tools.cisco.com                             │
│  TAC remote      = Cisco engineer SSHs into DCNM VM with customer permission                          │
│  RCA             = Root Cause Analysis; Cisco provides after Sev-1 case closure                       │
│  CSAT            = Customer Satisfaction survey; sent after TAC case closure                          │
│  Incident bridge = conference call coordinating all responders during Sev-1                           │
│  No config changes= freeze all DCNM and MDS changes during active incident                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Database diagnostics
psql -U postgres sane -c "
SELECT relname, pg_size_pretty(pg_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_relation_size(relid) DESC
LIMIT 20;" > /tmp/db-sizes-$(date +%Y%m%d).txt

psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('sane')), pg_size_pretty(pg_database_size('pmdb'));" >> /tmp/db-sizes-$(date +%Y%m%d).txt

# 10-minute resource collection
for i in {1..10}; do
  echo "=== $(date) ==="
  free -h; df -h /var/lib/pgsql; uptime
  sleep 60
done > /tmp/dcnm-perf-$(date +%Y%m%d).txt
```
```bash
# Upgrade log
cp /var/log/dcnm/install.log /tmp/

# Current and previous DCNM version
cat /var/dcnm/version
# Include in case: source version, target version, and exact error message
```
```yaml
Product: Cisco Data Center Network Manager (DCNM)
Version: 11.x.x (from /var/dcnm/version)
Deployment: Standalone / Native HA
Hypervisor: VMware ESXi 7.0 U3 (or KVM)
Managed switches: [MDS 9710 x2, MDS 9396T x4, NX-OS 8.4(2a)]

Problem description:
[Concise description of the symptom — what is broken or degraded]

Business impact:
[e.g., "Zone changes cannot be pushed to fabric; fabric is operational but no
 configuration changes can be made via DCNM"]

When did the issue start:
[Date and time — what was happening at that time]

What changed before the issue:
[e.g., "DCNM was upgraded from 11.4.1 to 11.5.4 on 2026-05-06 at 14:00 UTC"]

Steps taken to troubleshoot:
1. [what was checked]
2. [what was tried]
3. [result]

Attachments:
- dcnm-support-20260507.tar.gz (support bundle)
- discovery-issue.log
- ssh-test.txt / snmp-test.txt
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

