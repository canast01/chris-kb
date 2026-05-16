# vSphere Replication — Escalation

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
