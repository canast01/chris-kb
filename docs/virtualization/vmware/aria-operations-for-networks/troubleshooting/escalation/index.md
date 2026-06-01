# Aria Operations for Networks — Escalation


<div class="kb-summary">
Escalation reference covering Before Opening a Support Case, Severity Definitions, Generate Support Bundle via CLI, Engage VMware Support, Escalation Path and 1 more sections.
</div>

---

## Before Opening a Support Case

Collect the following before contacting VMware Support:

| Item | How to Collect |
|---|---|
| Support bundle | Settings → Support → Download Support Bundle (Platform + all Collectors) |
| vRNI version | Settings → About → Version |
| Data source list | Settings → Data Sources → export or screenshot |
| Symptom timeline | When issue started, what changed before it started |
| Affected component | Collector, data source, UI, API, specific feature |
| Error messages | Screenshots or copy of exact error text |
| Network topology | Which sites, how many VMs, how many switches |

---

## Severity Definitions

| Severity | Condition | Response Target |
|---|---|---|
| Sev 1 | Complete loss of vRNI platform — no data, no UI | 30 minutes (with active collab) |
| Sev 2 | Major feature unavailable — e.g., all flows missing, NSX integration down | 4 business hours |
| Sev 3 | Specific data source failing, UI slow, one collector disconnected | Next business day |
| Sev 4 | General how-to, feature request, minor cosmetic issue | Standard queue |

---

## Generate Support Bundle via CLI

If the UI is unavailable:

```bash
ssh ubuntu@vrni.example.local

# Generate support bundle from CLI
sudo /etc/init.d/support-bundle.sh

# Bundle is placed in:
ls /data/support-bundles/
# Transfer via SCP:
scp ubuntu@vrni.example.local:/data/support-bundles/<bundle>.tar.gz /local/path/
```
```
┌─────────────────────────────────────────── vRNI Escalation ───────────────────────────────────────────┐
│                                                                                                       │
│  Escalation triggers, Support Request process, and TAM engagement for vRNI.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │              SR Severity Levels             │   │
│   │           Platform UI unreachable            │  │           P1: platform fully down           │   │
│   │          All flows missing >2 hours          │  │          P2: flows missing/degraded         │   │
│   │            Upgrade fails or loops            │  │             P3: feature/UI issue            │   │
│   │          Data corruption suspected           │  │            P4: how-to / question            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Triggers determine severity; SR opened with bundle; TAM engaged for P1/P2.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SR Process                  │  │                TAM Engagement               │   │
│   │          1. Generate support bundle          │  │             Notify TAM for P1/P2            │   │
│   │         2. Open GSS SR with severity         │  │           TAM escalates internally          │   │
│   │         3. Attach bundle + timeline          │  │           Provide change timeline           │   │
│   │            4. Follow GSS guidance            │  │              Bridge call for P1             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM; support bundle generated via SSH or VAMI; GSS portal for SR                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Support Bundle      = Compressed log archive; mandatory attachment for any SR                        │
│  GSS                 = Global Support Services; VMware/Broadcom support portal                        │
│  SR                  = Support Request; formal case opened with GSS                                   │
│  P1 Severity         = Production down; requires 24/7 response and bridge call                        │
│  P2 Severity         = Major degradation; business-hours priority response                            │
│  TAM                 = Technical Account Manager; escalation point for P1/P2                          │
│  Bridge Call         = Live conference with GSS, TAM, and customer for P1 issues                      │
│  Change Timeline     = Log of recent changes provided to GSS to narrow root cause                     │
│  Data Corruption     = Suspected invalid flow data; always P1 or P2 severity                          │
│  Upgrade Loop        = PAK upgrade repeatedly fails or rolls back; escalate to GSS                    │
│  Internal Escalation = TAM routes SR to engineering or BU team for complex issues                     │
│  RCA                 = Root Cause Analysis; provided by GSS after P1/P2 resolution                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

---

## Engage VMware Support

1. Go to **customerconnect.vmware.com** (or Broadcom Support Portal)
2. Select product: **VMware Aria Operations for Networks** (or **vRealize Network Insight**)
3. Attach: support bundle, version info, symptom description
4. If Sev 1: call support hotline directly after creating the case to request phone bridge

---

## Escalation Path

| Escalation Level | Trigger |
|---|---|
| Standard support | Initial case creation |
| Technical Account Manager | Recurring issue, contract SLA breach |
| Engineering escalation | Support cannot reproduce; feature defect suspected |
| Executive escalation | Business-critical outage, multi-day unresolved Sev 1 |

---

## Knowledge Base and Community

- VMware Aria Operations for Networks Documentation: docs.vmware.com/aria-networks
- VMware KB: kb.vmware.com (search "vRealize Network Insight" or "Aria Operations for Networks")
- VMware Community Forums: communities.vmware.com/community/vmtn/vrealize-network-insight
- Release Notes: check before upgrade for known issues and resolved bugs
