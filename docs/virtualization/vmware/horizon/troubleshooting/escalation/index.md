# Horizon — Escalation

```text
  Escalation Path
┌──────────────────────────────────────────────────────────────┐
│  Internal Triage (L1/L2)                                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Collect: support bundle + UAG logs + agent logs +        │ │
│  │          affected VM name + session ID + Horizon version │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                             │                                │
│  ┌──────────────────────────▼──────────────────────────────┐ │
│  │ Sev Assessment                                           │ │
│  │  Sev 1 — full VDI outage ──► Open SR + call VMware now  │ │
│  │  Sev 2 — partial outage   ──► Open SR (24x7)            │ │
│  │  Sev 3 — single user/pool ──► Open SR (business hours)  │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                             │                                │
│  ┌──────────────────────────▼──────────────────────────────┐ │
│  │ VMware Support → TAM / Critical Escalation (if Sev 1    │ │
│  │  unresolved within SLA)  → Horizon Engineering          │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── VMware Horizon — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│  Escalate Horizon issues to VMware GSS when all users are impacted, agent fails                       │
│  on all desktops, or Connection Server is unresponsive.                                               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │             Pre-Escalation Steps            │   │
│   │           All users: cannot login            │  │          Collect CS support bundle          │   │
│   │         CS unresponsive: all failed          │  │              Collect agent logs             │   │
│   │        Pool provisioning: 100% error         │  │           Document error messages           │   │
│   │          Agent crash loop: all VMs           │  │             Timeline of changes             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  If all Connection Servers fail simultaneously, priority is restore from snapshot or backup.          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                GSS Engagement                │  │               Escalation Path               │   │
│   │         Open P1 SR: broadcom portal          │  │             T1: triage + bundles            │   │
│   │           Include Horizon version            │  │                T2: Horizon SE               │   │
│   │           Attach CS support bundle           │  │            T3: engineering review           │   │
│   │            Attach agent logs ZIP             │  │         CritSit: P1 with VIP impact         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GSS may request Bomgar remote access to Connection Server and desktop VMs;                           │
│  provide admin RDP to CS and vCenter access for remote engineers.                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SR            = Service Request; support ticket at support.broadcom.com                              │
│  P1 severity   = highest; production VDI outage; 24/7 response                                        │
│  CS support bundle= generated via Horizon Admin UI > Support                                          │
│  Agent logs    = C:\ProgramData\VMware\VDM\debug*.log on desktop                                      │
│  Timeline      = list of recent changes before failure                                                │
│  Horizon version= check Administration > Product Licensing                                            │
│  T2 Horizon SE = VMware senior Horizon specialist                                                     │
│  CritSit       = Critical Situation; exec escalation; 24/7 war room                                   │
│  Bomgar        = remote support tool; GSS engineer connect                                            │
│  Snapshot restore= fastest recovery for CS failure                                                    │
│  LDAP restore  = vdmimport from backup if CS config lost                                              │
│  KB article    = check VMware KB before raising SR                                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Engage VMware Support

1. **Portal:** customerconnect.vmware.com → Log Case
   - Product: VMware Horizon
   - Version: [current version]
   - Component: Connection Server / UAG / Agent / App Volumes (specify)
   - Problem: [describe symptom and impact]

2. **Attach:** support bundle, event exports, symptom description

3. **For Sev 1:** after creating case, call VMware Support and reference the case number for immediate phone assistance

---

## Escalation Within VMware

| Path | Trigger |
|---|---|
| Technical Account Manager | Contract with TAM — contact directly for priority handling |
| Critical Escalation Team | Sev 1 not resolved within SLA — request escalation via Support portal |
| Engineering escalation | Bug suspected — request escalation to Horizon engineering team |

---

## Useful Resources

- Horizon Documentation: docs.vmware.com/horizon
- Horizon Compatibility Matrix: interopmatrix.vmware.com
- VMware KB for Horizon: kb.vmware.com (search "VMware Horizon")
- Horizon Community Forum: communities.vmware.com/community/vmtn/horizon
- Horizon ADMX GPO templates: downloaded with Connection Server installer
