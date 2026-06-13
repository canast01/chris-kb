---
tags:
  - troubleshooting
  - vmware
  - vsphere-replication
---
# vSphere Replication — Escalation


<div class="kb-summary">
Escalation reference covering Before Opening a Support Case, Severity Definitions, If SRM is Also Involved, VMware Support Portal, Escalation Path and 1 more sections.

*Applies to: vSphere Replication 8.x*
</div>

  VR Escalation Path
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Step 1: Collect (both sites)                                                                         │
│  ┌─────────────────────────────────────────────────────────┐                                          │
│  │ VRA support bundle (VAMI) │ ESXi hbr.log / hostd.log    │                                          │
│  │ vCenter system logs       │ Replication status capture  │                                          │
│  │ VR / vSphere / SRM version│ Symptom timeline + errors   │                                          │
│  └─────────────────────────────────────────────────────────┘                                          │
│                  │                                                                                    │
│                  ▼                                                                                    │
│  Step 2: Severity Assessment                                                                          │
│  ┌──────────────────────────────────────────────────────┐                                             │
│  │ Sev 1: active recovery failing  → open SR + call NOW │                                             │
│  │ Sev 2: all replications down    → open SR (urgent)   │                                             │
│  │ Sev 3: subset RPO violation     → open SR (normal)   │                                             │
│  └──────────────────────────────────────────────────────┘                                             │
│                  │                                                                                    │
│                  ▼                                                                                    │
│  Step 3: Escalation Triggers                                                                          │
│  ┌──────────────────────────────────────────────────────┐                                             │
│  │ Sev 1 unresolved >2h → Critical Escalation Team      │                                             │
│  │ Recurring / SLA breach → TAM engagement              │                                             │
│  │ Suspected defect      → VR Engineering via SR        │                                             │
│  └──────────────────────────────────────────────────────┘                                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Before Opening a Support Case

Collect from both protected and recovery sites:

| Item | How to Collect |
|---|---|
| VRA support bundle (both sites) | VRA VAMI → Support → Generate Support Bundle |
| ESXi hostd log (source host) | SSH to ESXi → `/var/log/hostd.log` |
| ESXi hbr log | SSH to ESXi → `/var/log/hbr.log` |
| vCenter logs | vCenter → Administration → Export System Logs |
| Replication status screenshot | vCenter → Site Recovery → Replications (capture status at time of issue) |
| VR version | VRA VAMI → Summary → Version |
| vSphere version | vCenter → About |
| SRM version (if paired with SRM) | SRM admin UI → About |
| Symptom timeline | When issue started, what action preceded it, expected behavior |
| Error messages | Exact text from vCenter Tasks/Events or VRA VAMI |

---

## Severity Definitions

| Severity | Condition |
|---|---|
| Sev 1 | Active DR recovery operation failing; VMs cannot be recovered |
| Sev 2 | All replications failing; DR capability degraded but no active recovery |
| Sev 3 | Subset of VMs in RPO violation or single VR configuration issue |
| Sev 4 | General how-to question, minor issue |

For Sev 1 (active recovery operation blocked): create case AND call VMware Support immediately.

---

## If SRM is Also Involved

If using SRM to manage VR-based protection groups:
1. Open a single VMware Support case — SRM and VR teams collaborate internally
2. Include: SRM support bundle (from both sites) in addition to VRA bundles
3. Specify: the issue is in the "vSphere Replication" layer vs "SRM orchestration" layer if known

---

## VMware Support Portal

1. **Portal:** support.broadcom.com → Log Case
   - Product: VMware vSphere Replication
   - Version: [VR version]
   - Attach: VRA support bundles from both sites, ESXi logs, symptom description

2. For Sev 1: after creating case, call VMware Support and reference case number

---

## Escalation Path

| Escalation | Trigger |
|---|---|
| Technical Account Manager | Recurring issue, SLA breach |
| Critical Escalation Team | Sev 1 unresolved within 2 hours |
| VR Engineering | Suspected defect — escalate via support case |

---

## Useful Resources

- vSphere Replication Documentation: docs.vmware.com/vsphere-replication
- Interoperability Matrix: interopmatrix.vmware.com (VR ↔ vSphere ↔ SRM)
- VMware KB: kb.vmware.com (search "vSphere Replication")
- vSphere Replication Community: communities.vmware.com/community/vmtn/vsphere/vspherereplication
