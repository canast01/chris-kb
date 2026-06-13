---
tags:
  - san
  - troubleshooting
---
# Brocade SANnav — Troubleshooting Escalation

```bash
# 1. SANnav version
sannav version

# 2. Support bundle
sannav support-bundle --output /tmp/sannav-diag-$(date +%Y%m%d).tar.gz

# 3. Affected switch firmware version (if switch-related issue)
# From SANnav UI: Inventory > Switches > [switch] > Details > Firmware Version
# From switch CLI:
firmwareshow

# 4. Appliance resource state at time of issue
free -h
df -h
uptime

# 5. Timeline of events
# Exact time the issue started
# Any changes made before the issue (upgrade, configuration change, network change)
# Steps already taken to troubleshoot
```
```text
┌───────────────────────────── Brocade SANnav — Troubleshooting Escalation ─────────────────────────────┐
│                                                                                                       │
│  SANnav escalation: internal L2/L3 → Broadcom TAC with log bundle, case, and access.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Internal Escalation Path           │  │           Broadcom TAC Escalation           │   │
│   │          L1 → L2: basic checks done          │  │         Open case: support.broadcom         │   │
│   │        L2 → L3: log bundle + timeline        │  │          Provide: SANnav + FOS vers         │   │
│   │         L3 → TAC: full data package          │  │          Sev-1: SANnav unreachable          │   │
│   │          Incident bridge for Sev-1           │  │          Remote: TAC SSH to SANnav          │   │
│   │          No changes during incident          │  │           RCA expected after close          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Collect SANnav logs and switch supportsave before contacting Broadcom TAC.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Escalation Data Package            │  │           Severity Classification           │   │
│   │         SANnav logs: journalctl dump         │  │          Sev-1: SANnav down; fabric         │   │
│   │         DB status: sannav-admin out          │  │           Sev-2: zone push failing          │   │
│   │            FOS version per switch            │  │          Sev-3: monitoring partial          │   │
│   │        supportsave from all switches         │  │         Sev-4: question/enhancement         │   │
│   │            Audit log export: CSV             │  │          CSAT survey after closure          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · management Ethernet · serial console access · Broadcom upload endpoint                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  journalctl dump = full SANnav service log export; share compressed to TAC                            │
│  sannav-admin    = SANnav VM CLI; db-status and status output needed for TAC                          │
│  supportsave     = FOS diagnostic bundle; one per switch in the affected fabric                       │
│  Audit log CSV   = SANnav action log export; shows what changed before incident                       │
│  Sev-1           = SANnav completely down; fabric management unavailable                              │
│  Sev-2           = SANnav partially working; zone changes or discovery failing                        │
│  TAC remote      = Broadcom engineer SSHs into SANnav VM with customer permission                     │
│  RCA             = Root Cause Analysis document; Broadcom provides after Sev-1 close                  │
│  CSAT            = Customer Satisfaction survey; sent by Broadcom after case closure                  │
│  FOS version     = Fabric OS version; compatibility matrix needed for SANnav match                    │
│  Incident bridge = conference call with all responders during active Sev-1 event                      │
│  No changes      = freeze all fabric and SANnav changes during active incident                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Collect resource stats over 10 minutes
for i in {1..10}; do
  echo "=== $(date) ==="
  free -h
  df -h /opt/sannav
  uptime
  sleep 60
done > /tmp/sannav-perf-$(date +%Y%m%d).txt
```
```yaml
Product: SANnav Management Portal
Version: 2.x.x (sannav version output)
Hypervisor: VMware ESXi 7.0 U3
Managed switches: [list models and FOS versions]

Problem description:
[Concise description of the symptom — what is broken, what error message is shown]

Business impact:
[e.g., "Unable to make any zone changes; fabric is operational but no zoning operations can be performed"]

When did the issue start:
[Date and time; what was happening at that time]

What changed before the issue:
[e.g., "SANnav was upgraded from 2.3.0 to 2.4.0 at 14:00 UTC on 2026-05-06"]

Steps taken:
1. [what was tried]
2. [what was tried]

Attachments:
- sannav-diag-20260507.tar.gz (support bundle)
- discovery-issue.log
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

