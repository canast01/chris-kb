# Cisco DCNM — Escalation

> Part of the [Cisco DCNM](../../index.md) reference.

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

- URL: `https://mycase.cloudapps.cisco.com` or `https://tools.cisco.com/ServiceRequestTool/`
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

### For Discovery or Connectivity Issues

```bash
# Discovery log for the affected switch
grep "<switch-ip>" /var/log/dcnm/discovery.log > /tmp/discovery-issue.log

# SSH test result
ssh -v -o ConnectTimeout=10 dcnm_mgmt@<switch-ip> 'show version' 2>&1 > /tmp/ssh-test.txt

# SNMP test result
snmpget -v3 -u dcnm_poll -l authPriv -a SHA -A <auth-pass> \
  -x AES -X <priv-pass> <switch-ip> sysDescr.0 > /tmp/snmp-test.txt 2>&1
```

### For Zone Activation Issues

```bash
# Export the zone database for the affected fabric (GUI or API)
# Include in case: fabric name, VSAN ID, error message shown in DCNM

# On the principal MDS switch:
show zone status vsan <vsan-id>
show zone merge-failure vsan <vsan-id>
# Include this output in the case
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
- Cisco Bug Search Tool: `https://bst.cloudapps.cisco.com/bugsearch/`
- Search by product: DCNM; filter by version and status (Open / Fixed in version)
