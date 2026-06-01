# Nexus Dashboard — Escalation


<div class="kb-summary">
> Part of the [Nexus Dashboard](../../index.md) reference.
</div>

---

## Overview

This page covers when and how to escalate Nexus Dashboard issues to Cisco TAC, what information to collect before opening a case, and how to engage effectively across the ND platform, NDFC, and NDI application layers.

---

## Escalation Decision Matrix

| Condition | Internal Action First | Escalate to Cisco TAC |
|---|---|---|
| Node unhealthy — VM resource exhaustion | Increase VM RAM/CPU | No (unless ND cluster OOM with correct sizing) |
| Node unhealthy — all resources normal, cluster cannot form | Collect support bundle | Yes |
| NDFC switches unmanageable — SSH/SNMP confirmed broken | Fix switch credentials or ACL | No |
| NDFC switches unmanageable — connectivity fine, NDFC bug suspected | Collect NDFC logs | Yes |
| Zone activation fails — merge conflict | Resolve on switch CLI | No |
| Zone activation fails — NDFC API error, no clear cause | Collect logs | Yes |
| NDI not receiving telemetry — license invalid | Apply license | No |
| NDI not receiving telemetry — license valid, flows configured | Collect NDI logs | Yes |
| ND upgrade fails — cluster non-functional | Restore from snapshot | Yes with support bundle |
| etcd data corruption | Restore from backup | Yes before attempting restore |
| ND cluster cannot form quorum (2+ nodes down) | Restore missing nodes | Yes if nodes cannot be recovered |
| Security incident (unauthorized access) | Follow security IR process | Yes + internal security team |

---

## Cisco TAC Access

Open a support case at the Cisco Support Portal:

- Primary URL: `https://mycase.cisco.com`
- Product: **Cisco Nexus Dashboard** (platform) and/or **Nexus Dashboard Fabric Controller** (NDFC) or **Nexus Dashboard Insights** (NDI)
- Navigate to: **Open New Case > Software**

Requirements:
- Valid Cisco support contract (SNTC or equivalent)
- ND platform version and installed app versions
- Serial number of the ND physical appliance (if applicable) or VM UUIDs

---

## Severity Levels

| Severity | Definition | Cisco Response SLA |
|---|---|---|
| S1 — Critical | ND cluster is completely unavailable; active impact to DC operations | 2 hours (24x7) |
| S2 — Severe | Major functionality broken; fabric management or insights significantly impaired | 4 hours (24x7) |
| S3 — Moderate | Non-critical issue; workaround available | Next business day |
| S4 — Minor | Cosmetic, documentation, or how-to question | 3–5 business days |

For S1/S2, call Cisco TAC immediately after submitting the case online:
- Global phone numbers: `https://www.cisco.com/c/en/us/support/web/tsd-cisco-worldwide-contacts.html`

---

## Information to Collect Before Escalating

### Always Include

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# 1. Platform version
acs version

# 2. Installed app versions
acs apps status

# 3. Cluster health at time of issue
acs health
acs nodes list

# 4. Support bundle (primary artifact for TAC)
acs techsupport --output /tmp/nd-support-$(date +%Y%m%d).tar.gz
# Transfer to workstation:
scp ndadmin@nd-dc1-1.corp.example.com:/tmp/nd-support-$(date +%Y%m%d).tar.gz ./

# 5. Resource state
acs system resources

# 6. Kubernetes event log
kubectl get events --all-namespaces --sort-by='.lastTimestamp' > /tmp/k8s-events-$(date +%Y%m%d).txt
```
```text
┌───────────────────────── Cisco Nexus Dashboard — Troubleshooting Escalation ──────────────────────────┐
│                                                                                                       │
│  Escalation path for ND: internal triage → Cisco TAC → cluster restore or rebuild.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Internal Triage (L1/L2)            │  │                Cisco TAC (L3)               │   │
│   │         Confirm impact: cluster/app          │  │            Open SR: severity 1-4            │   │
│   │           Collect: acs techsupport           │  │          Upload bundle to CX Cloud          │   │
│   │         Check: recent config changes         │  │          TAC WebEx: remote session          │   │
│   │        Check: Cisco PSIRT advisories         │  │         Patch or restore if directed        │   │
│   │         Try: acs restart failing app         │  │         Rebuild cluster: last resort        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Collect tech-support before any restart; TAC needs state data from failure moment                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Criteria              │  │               Recovery Actions              │   │
│   │         Sev 1: all apps unavailable          │  │           App restart: acs restart          │   │
│   │            Sev 2: one app failed             │  │         Backup restore: full cluster        │   │
│   │          Sev 3: degraded telemetry           │  │         Node replace: rejoin cluster        │   │
│   │            Sev 4: config question            │  │          Rebuild: deploy + restore          │   │
│   │           Always document timeline           │  │          Post-mortem: RCA document          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · backup storage · management network · spare node for rebuild                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SR             = Service Request; Cisco TAC case number                                              │
│  TAC            = Technical Assistance Center; Cisco L3 support                                       │
│  CX Cloud       = Cisco portal for SR management and tech-support file upload                         │
│  PSIRT          = Cisco security advisory team; check for relevant CVEs first                         │
│  acs restart    = Gracefully restarts a named ND app without rebooting the node                       │
│  Backup restore = Full cluster config recovery from most recent scheduled backup                      │
│  Node replace   = Remove failed node, add new node, rejoin cluster automatically                      │
│  Rebuild        = Deploy fresh cluster and restore from backup; last-resort recovery                  │
│  Severity 1     = Production down; Cisco SLA: 1-hour initial response                                 │
│  RCA            = Root Cause Analysis; post-incident document for future prevention                   │
│  Timeline       = Chronological log of symptoms, actions, and outcomes for TAC                        │
│  Tech-support   = Collected before any recovery action; preserves failure state                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

### For Cluster Formation or etcd Issues

```bash
# etcd health (collect from each node)
for node in nd-dc1-1 nd-dc1-2 nd-dc1-3; do
  ssh ndadmin@${node}.corp.example.com \
    "ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \
     --key=/etc/kubernetes/pki/etcd/server.key \
     endpoint status --write-out=table" > /tmp/etcd-${node}.txt 2>&1
done
```

### For Upgrade Failures

```bash
# Upgrade log
acs upgrade history > /tmp/upgrade-history.txt
acs system logs --component upgrade --tail 200 > /tmp/upgrade-log.txt

# Include: source ND version, target version, app versions pre-upgrade
# Include: exact error message shown during upgrade
```

---

## Support Case Description Template

```yaml
Product: Cisco Nexus Dashboard
Platform version: 3.x.x (acs version output)
NDFC version: 12.x.x (acs apps status output)
NDI version: 6.x.x (if installed)
Deployment type: 3-node VMware OVA / 3-node physical (UCS C220 M6)
Managed switches: [MDS 9710 x2, MDS 9396T x4, NX-OS 8.4(2a)]

Problem description:
[Concise description of the symptom — what is failing or degraded]

Business impact:
[e.g., "NDFC cannot push zone changes to any fabric; fabric is operational
 but all SAN management operations are blocked"]

When did the issue start:
[Date and time — timezone — what was happening at that time]

What changed before the issue:
[e.g., "ND platform upgraded from 3.0.1 to 3.1.1 at 14:00 UTC on 2026-05-07"]

Troubleshooting already performed:
1. [what was checked]
2. [what was tried]
3. [result]

Attachments:
- nd-support-20260508.tar.gz (ND support bundle)
- ndfc-support-20260508.tar.gz (NDFC support bundle)
- k8s-events-20260508.txt
- [any screenshots of error messages]
```

---

## Escalation Path Within Cisco TAC

1. **Open the case online** with full context and attach the support bundle before calling — TAC engineers spend less time when the problem is clearly described upfront.
2. If the assigned TAC engineer is not responding within the SLA window, request escalation to the **TAC Duty Manager** — state this on the case notes or via phone.
3. If the issue is a software bug, ask the engineer to file a **Bug report (CSCxxxxxx)**. Reference this bug ID in future cases about the same issue.
4. For production-critical situations (S1/S2) that are not resolving: engage your Cisco Account Manager or Cisco Partner — they can escalate to Cisco engineering.
5. Cisco offers 24x7 critical situation support for S1 cases — the TAC engineer managing your S1 case should proactively provide updates every 2-4 hours.

---

## Cisco Nexus Dashboard Bug Resources

- Cisco Bug Search Tool: `https://bst.cisco.com/bugsearch/`
  - Search by product: Nexus Dashboard, NDFC, or NDI
  - Filter by version and status (Open / Fixed)
- Cisco ND Release Notes: always review before upgrading for known issues and workarounds
- Cisco ND Compatibility Matrix: `https://www.cisco.com/c/en/us/support/cloud-systems-management/nexus-dashboard/series.html`
