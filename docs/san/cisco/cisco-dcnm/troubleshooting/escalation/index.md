# Cisco DCNM — Escalation


<div class="kb-summary">
> Part of the [Cisco DCNM](../../index.md) reference.
</div>

---

## Overview

This page covers when and how to escalate Cisco DCNM issues to Cisco TAC, what information to collect before opening a case, and how to engage effectively given DCNM's approaching end-of-life status.

---

## Escalation Decision Matrix

| Condition | Internal Action First | Escalate to Cisco TAC |
|---|---|---|
| Switch shows Unmanageable — network cause confirmed | Fix SSH/SNMP connectivity | No |
| Switch shows Unmanageable — credentials verified, network OK | Collect discovery log | Yes |
| Zone activation fails — merge conflict | Resolve on switch NX-OS CLI | No |
| Zone activation fails — DCNM API error, no clear cause | Collect logs | Yes |
| PM not collecting data after restart | Check SNMP, disk, DB | Yes if restart does not resolve |
| DCNM GUI not loading after restart | Check Java heap, disk, DB | Yes if no resolution |
| Upgrade fails mid-way | Revert to VM snapshot | Yes with install log |
| HA failover not working | Check HA log, VIP, replication | Yes |
| Database corruption — restore fails | Restore from backup | Yes if backup restore fails |
| Security incident (unauthorized access) | Follow security IR process | Yes + internal security team |

---

## End-of-Life Notice

**DCNM 11.x is in its final maintenance phase.** Cisco has announced EoL for standalone DCNM in favour of NDFC on Nexus Dashboard. Before opening a TAC case, confirm:

- The issue is reproducible on DCNM 11.x
- The DCNM version is within the support window (check `cisco.com/go/eol` for DCNM EoL milestones)
- TAC may recommend migrating to NDFC as the resolution for some bugs that will not receive backported fixes

---

## Cisco TAC Access

Open a support case at the Cisco Support Portal:

- URL: `https://mycase.cisco.com` or `https://tools.cisco.com/ServiceRequestTool/`
- Product: **Cisco Data Center Network Manager (DCNM)**
- Navigate to: **Open New Case > Software**

Requirements:
- A valid Cisco support contract (SNTC or equivalent)
- DCNM license serial number or contract number
- DCNM version string (from `/var/dcnm/version` or **Administration > System > About**)

---

## Severity Levels

| Severity | Definition | Cisco Response SLA |
|---|---|---|
| S1 — Critical | Production fabric management completely unavailable; active impact to business operations | 2 hours (24x7) |
| S2 — Severe | Major functionality broken; workaround exists but operations are significantly impaired | 4 hours (24x7) |
| S3 — Moderate | Partial functionality impaired; workaround available | Next business day |
| S4 — Minor | Cosmetic, documentation, or general question | 3–5 business days |

For S1/S2, call Cisco TAC immediately after opening the case:
- Cisco TAC global phone numbers: `https://www.cisco.com/c/en/us/support/web/tsd-cisco-worldwide-contacts.html`

---

## Information to Collect Before Escalating

### Always Include

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

### For Performance / DB Issues

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

### For Upgrade Failures

```bash
# Upgrade log
cp /var/log/dcnm/install.log /tmp/

# Current and previous DCNM version
cat /var/dcnm/version
# Include in case: source version, target version, and exact error message
```

---

## Support Case Description Template

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

---

## Escalation Path Within Cisco TAC

1. Open the case online with full details and the support bundle attached upfront.
2. If the assigned TAC engineer is unresponsive within the SLA window, request escalation to the **TAC Duty Manager** — state this directly on the case notes or via phone.
3. If the issue is a suspected software bug, ask the TAC engineer to open a **Bug report (CSCxxxxxx)** and confirm whether a fix is planned or if a workaround exists.
4. For DCNM-specific EoL bugs: Cisco may advise migrating to NDFC. If this is not immediately feasible, document the business justification and ask TAC to investigate whether a patch can be backported.
5. Your Cisco Account Manager or Partner can escalate to Cisco engineering for high-impact situations — engage them for S1/S2 cases that are not resolving quickly.

---

## Common Cisco DCNM Bug References

Keep a local record of any active CSCxxxxxx bug IDs affecting your environment. When opening a new case for a known issue, reference the existing bug ID to accelerate TAC routing.

Useful search:
- Cisco Bug Search Tool: `https://bst.cisco.com/bugsearch/`
- Search by product: DCNM; filter by version and status (Open / Fixed in version)
