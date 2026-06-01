# SANnav — Escalation

> Part of the [SANnav](../../index.md) reference.

---

## Overview

This page covers when and how to escalate SANnav issues to Broadcom support, what information to collect before opening a case, and how to engage effectively.

---

## Escalation Decision Matrix

| Condition | Internal Action | Escalate to Broadcom |
|---|---|---|
| Switch unreachable — network issue | Fix routing/firewall | No |
| Switch unreachable — SANnav bug (connectivity looks fine) | Collect logs | Yes |
| Zone activation fails — merge conflict | Resolve conflict on switch | No |
| Zone activation fails — SANnav API error with no clear cause | Collect logs | Yes |
| Firmware upgrade stuck > 45 min | Check switch state | Yes if switch healthy and SANnav is stuck |
| SANnav GUI not loading | Restart services, check disk/RAM | Yes if restart does not fix |
| Database corruption or restore failure | Restore from backup | Yes if backup restore fails |
| SANnav upgrade fails partway through | Revert to snapshot | Yes with upgrade log |
| Performance severely degraded after upgrade | Collect support bundle | Yes |
| Security incident (unauthorized access) | Follow security incident response | Yes + internal security team |

---

## Support Portal Access

Broadcom support is accessed via the Broadcom Support Portal:

- URL: `https://support.broadcom.com`
- Product: **Brocade SANnav Management Portal** or **SANnav Global View**
- Navigate to: **My Cases > Open a New Case**

You will need:
- A valid Broadcom support entitlement (linked to your maintenance contract)
- The SANnav appliance serial number or license key
- The SANnav version (from `sannav version` or **Administration > System > About**)

---

## Severity Levels

| Severity | Definition | Broadcom Response SLA |
|---|---|---|
| S1 — Critical | Production fabric management completely unavailable; active fabric outage | 1 hour (24x7) |
| S2 — High | Major functionality broken; workaround exists but significantly impacts operations | 4 hours (24x7) |
| S3 — Medium | Non-critical functionality impaired; workaround available | Next business day |
| S4 — Low | Cosmetic issue, documentation request, general question | 3–5 business days |

For S1/S2 cases, call Broadcom support directly after opening the case online to ensure immediate engagement:
- Broadcom support phone: available at `https://support.broadcom.com` under **Contact Support**

---

## Information to Collect Before Escalating

### Always Include

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

### For Upgrade Issues

```bash
# Upgrade log
cp /opt/sannav/logs/upgrade.log /tmp/
# Include the previous version and target version in the case description
```

### For Performance Issues

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

---

## Engaging Broadcom TAC Effectively

1. **Open the case online first** — include as much detail as possible in the initial case description. TAC engineers spend less time on cases where the problem is clearly described.
2. **Attach the support bundle and relevant logs** — do not wait to be asked; attaching upfront reduces back-and-forth.
3. **State the business impact** — clearly indicate whether the issue is blocking fabric management or is a degraded-but-functional situation. This affects prioritisation.
4. **Include a timeline** — when did the issue start? What changed before it started? What has been tried?
5. **Stay available** — S1/S2 cases require someone with system access to be available for collaborative troubleshooting.

---

## Escalation Path Within Broadcom

If a case is not making progress:

1. Ask the case owner (TAC engineer) for a status update and ETA.
2. If the TAC engineer is not responsive within the SLA window, ask to escalate to the TAC duty manager — you can request this directly on the case or via phone.
3. If your account team (Broadcom account manager or partner) is engaged, they can escalate to Broadcom engineering for development-level issues (bugs).
4. For critical production impact, Broadcom offers 24x7 critical situation support — request this through the support portal or your account team.

---

## Common Support Case Information Template

Use the following template as the case description when opening a new SANnav support case:

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
