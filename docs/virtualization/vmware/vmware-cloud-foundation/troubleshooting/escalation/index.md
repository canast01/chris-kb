---
tags:
  - troubleshooting
  - vcf
  - vmware
---
# VCF Troubleshooting — Escalation


<div class="kb-summary">
Escalation reference covering Information to Collect Before Opening an SR, Support Tiers.

*Applies to: VCF 4.x / 5.x*
</div>

```text
┌──────────────────────────────── VMware Cloud Foundation — Escalation ─────────────────────────────────┐
│                                                                                                       │
│  Escalate VCF issues to VMware GSS when upgrade is stuck, data is at risk,                            │
│  or SDDC Manager is inaccessible; attach SOS bundle and timeline.                                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │             Pre-Escalation Steps            │   │
│   │            SDDC Mgr inaccessible             │  │               Run SOS utility               │   │
│   │              Upgrade stuck >4h               │  │          Collect component bundles          │   │
│   │         Data at risk: vSAN degraded          │  │           Document failed task ID           │   │
│   │           All self-steps exhausted           │  │             Timeline of changes             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SOS bundle and task IDs allow GSS to quickly triage the failure point.                               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                GSS Engagement                │  │               Escalation Path               │   │
│   │         Open SR at support.broadcom          │  │               T1: triage + SOS              │   │
│   │           Severity P1: full outage           │  │             T2: VCF SE assigned             │   │
│   │         Include VCF version + build          │  │            T3: engineering review           │   │
│   │                Attach SOS ZIP                │  │        CritSit: 24/7 if data at risk        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GSS may request live SSH session to SDDC Manager and component appliances;                           │
│  prepare access for remote engineers before the call.                                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SOS utility   = VCF support bundle; /opt/vmware/sddc-support/sos                                     │
│  SR            = Service Request; raise at support.broadcom.com                                       │
│  Task ID       = SDDC Mgr async operation ID; include in SR                                           │
│  P1 severity   = highest priority; production outage; 24/7 SLA                                        │
│  CritSit       = Critical Situation; exec escalation + war room                                       │
│  VCF version   = e.g., VCF 5.2.0.0 build 12345678                                                     │
│  T2 VCF SE     = VMware senior engineer specialising in VCF                                           │
│  Timeline      = chronological list of changes before issue                                           │
│  Broadcom      = VMware support portal post-acquisition                                               │
│  Live SSH      = GSS remote debug via Bomgar or WebEx                                                 │
│  Do not remediate= stop retrying stuck upgrades; wait for GSS guidance                                │
│  Component bundle= per-product logs (VC/NSX/ESXi) for targeted debug                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

VCF support is managed through the [Broadcom Support Portal](https://support.broadcom.com) under the VMware Cloud Foundation product line. When opening an SR, the SoS health check bundle and the SDDC Manager support bundle are the two most important artefacts — Broadcom support will almost always request these as the first action, so collecting them before opening the ticket saves significant time. The VCF Support Matrix (available on the Broadcom compatibility guide) must be referenced to confirm that the versions of vCenter, ESXi, NSX, and vSAN in your environment are a supported combination before filing lifecycle-related SRs.

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Information to Collect Before Opening an SR

- SDDC Manager version: Administration > About
- Affected component name and version
- SoS health check output: `python3 /opt/vmware/sddc-support/sos --health-summary`
- SDDC Manager support bundle: `vcf-support-bundle --type sddc`
- Component-specific support bundle if issue is isolated (e.g. NSX, vCenter)
- Timeline of events — last known good state, first observed failure, changes made
- Screenshot of SDDC Manager task failure or error message

## Support Tiers

| Severity | Description | Response SLA (Production) |
|---|---|---|
| S1 | Production down, no workaround | 30 minutes |
| S2 | Major feature unavailable | 4 hours |
| S3 | Partial degradation, workaround available | Next business day |
| S4 | General question or enhancement | Next business day |

---

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
