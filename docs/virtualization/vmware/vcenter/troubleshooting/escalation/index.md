---
tags:
  - troubleshooting
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter — Escalation


<div class="kb-summary">
Escalation reference covering Severity Levels, SLA Tiers, Escalation Path, Useful Broadcom Resources, Information Broadcom Will Ask For.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌───────────────────────────────────── vCenter Server — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│  Escalate vCenter issues to VMware GSS when self-service troubleshooting exhausts                     │
│  available options; attach support bundle and document timeline.                                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │             Pre-Escalation Steps            │   │
│   │           VCSA crashes repeatedly            │  │            Collect support bundle           │   │
│   │             Data loss suspected              │  │           Snapshot VCSA if stable           │   │
│   │           All self-steps exhausted           │  │          Document exact error text          │   │
│   │          P1 outage: VC inaccessible          │  │            Timeline: when started           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  GSS requires SR number, support bundle, and change timeline to start root-cause.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                GSS Engagement                │  │               Escalation Path               │   │
│   │         Open SR at support.broadcom          │  │            T1: SR triage + bundle           │   │
│   │         Severity: P1 for full outage         │  │            T2: Senior SE assigned           │   │
│   │           Include vCenter version            │  │            T3: Engineering review           │   │
│   │          Attach support bundle ZIP           │  │            CritSit: 24/7 coverage           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GSS may request live session access via Bomgar/WebEx; prepare VCSA SSH access                        │
│  and vSphere Client access for remote support engineers.                                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GSS          = Global Support Services; VMware (Broadcom) official support                           │
│  SR           = Service Request; support ticket number; reference in all calls                        │
│  Support bundle= ZIP of all VCSA logs; generated via UI or vc-support.sh                              │
│  Severity P1  = critical; production outage; fastest SLA response                                     │
│  CritSit      = Critical Situation; escalation for P1 with exec involvement                           │
│  T1/T2/T3     = support tiers; T3 has access to engineering teams                                     │
│  Bomgar       = VMware remote access tool; screen share for live debug                                │
│  Timeline     = chronological list of changes/events before the issue                                 │
│  Snapshot     = pre-work safety net; capture VCSA state before GSS changes                            │
│  KB article   = VMware knowledge base; check before raising SR                                        │
│  vCenter version= full build number from Administration > About                                       │
│  Broadcom portal= support.broadcom.com replaced my.vmware.com for SRs                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
**From VCSA shell (`vm-support` bundle):**
```bash
/usr/bin/vm-support -n <vcenter-name>
# Output: /var/core/esx-<timestamp>.tgz
```

**ESXi Tech Support Mode logs** (from ESXi shell or DCUI → Troubleshooting Options):
```bash
vm-support
# Bundle created in /var/core/
```

**NSX Manager support bundle** (if NSX issue involved):
```text
NSX Manager UI → System → Support Bundle → Generate
```

## Severity Levels

| Severity | Definition | VMware Response Target |
|---|---|---|
| S1 (Critical) | Production down, no workaround | 30 min (Production), 15 min (Business Critical) |
| S2 (High) | Significant impact, partial workaround | 4 hours |
| S3 (Medium) | Minor impact, workaround available | 8 business hours |
| S4 (Low) | General question or enhancement | 12 business hours |

Request severity upgrade if business impact increases.

## SLA Tiers

| Support Tier | Description |
|---|---|
| Basic | Business hours only; S1 response: next business day |
| Production | 24×7 for S1/S2; standard response SLAs |
| Business Critical | 24×7 with faster SLAs; assigned Senior PSE |
| Enterprise / TAM | Dedicated Technical Account Manager; proactive support |

Verify your support tier in the Broadcom portal under **My Entitlements**.

## Escalation Path

1. **Open case** — provide full symptom description, logs, and build numbers
2. **Request escalation** — if no progress within SLA, ask for Senior PSE or escalation manager
3. **TAM engagement** — if you have a TAM, loop them into the case immediately for S1/S2
4. **Executive escalation** — through your Broadcom account team for prolonged P1 outages

## Useful Broadcom Resources

| Resource | URL |
|---|---|
| Security Advisories (VMSA) | https://support.broadcom.com/web/ecx/security-advisory |
| Product Lifecycle Matrix | https://support.broadcom.com/group/ecx/productlifecycle |
| Interoperability Matrix | https://interopmatrix.broadcom.com |
| VMware HCL | https://compatibilityguide.broadcom.com |
| Knowledge Base | https://knowledge.broadcom.com |
| vSphere Release Notes | Search by version in Knowledge Base |

## Information Broadcom Will Ask For

- **vCenter build number** (not just version — the 7-digit build number uniquely identifies the patch level)
- **ESXi build numbers** for affected hosts
- **`vm-support`** bundle from vCenter appliance
- **ESXi TSM log bundle** from affected host
- **Steps to reproduce** the issue
- **Frequency and scope** (one host, one cluster, all clusters)
- **Recent changes** (patches, firmware, network changes, vCenter upgrades)

Upload logs directly to the case via the Broadcom portal file upload — do not send via email due to size limits.
