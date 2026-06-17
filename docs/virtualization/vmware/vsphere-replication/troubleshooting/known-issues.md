---
tags:
  - troubleshooting
  - vsphere-replication
  - vmware
  - known-issues
---
# VMware vSphere Replication — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known vSphere Replication bugs, error codes, and workarounds covering replication configuration, RPO violations, and appliance issues.

*Applies to: vSphere Replication 8.x*
</div>

```text
┌───────────────────────────────────── VMware vSphere Replication ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           VM-level async replication — hypervisor-based disk replication to DR site           │   │
│   │                 Protocols: HTTPS (VRMS) · hbr (TCP 31031/44046) · vCenter API                 │   │
│   │                 Management: vSphere Client plugin · VRMS appliance · REST API                 │   │
│   │             VR agent in VMkernel -> delta capture -> hbr -> target VRMS -> DR disk            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Agent            │  │     VR agent (VMkernel)     │  │     Tracks disk changes     │   │
│   │            Server           │  │        VRMS appliance       │  │       1 per site (OVA)      │   │
│   │           Channel           │  │        hbr connection       │  │       TCP 31031 delta       │   │
│   │            Target           │  │         DR site VRMS        │  │       Receives replica      │   │
│   │        Orchestration        │  │        SRM (optional)       │  │     Failover automation     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       VRMS       │Replication server│     HTTPS 8043    │  vCenter trust   │   OVA per site   │   │
│   │     VR agent     │ VMkernel tracker │   hbr TCP 31031   │       N/A        │ Built into ESXi  │   │
│   │    hbr server    │  Transfer relay  │     TCP 44046     │       N/A        │ On VRMS or ESXi  │   │
│   │       SRM        │ DR orchestration │       HTTPS       │       SSO        │Consumes VR groups│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: source ESXi (VR agent) -> hbr TCP -> DR site VRMS -> DR datastore                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VRMS         = vSphere Replication Management Server; central replication appliance                  │
│  VR agent     = VMkernel module tracking dirty blocks for replication                                 │
│  hbr          = host-based replication; proprietary protocol for delta transfer                       │
│  RPO          = Recovery Point Objective; minimum 5 minutes for vSphere Replication                   │
│  Delta        = set of changed disk blocks transferred each replication cycle                         │
│  Replication group = set of VMs replicated and recovered together                                     │
│  Recovery point = point-in-time copy at DR site; configurable retention count                         │
│  Multiple point recovery = VR keeps N recovery points; recover to any one                             │
│  Test recovery = recovers VM in isolated network at DR site; non-destructive                          │
│  Failover     = activates DR copy; source replication stops                                           │
│  Reprotect    = starts replication back from DR to original site after failover                       │
│  Lag          = time behind RPO target; alert when lag > RPO                                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- vSphere Replication errors appear in the vSphere Client under `vSphere Replication → VMs` — expand the replication entry for status.
- Collect logs from the VRMS (vSphere Replication Management Server) appliance at `/opt/vmware/hms/logs/`.

## Replication Configuration

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot configure replication — target datastore full` | VR 8.x | Insufficient space on target for seed/full sync | Free space or select different target datastore; enable thin provisioning | N/A |
| `Replication seed failed` for large VMs (>2 TB) | VR 8.x | Seed copy times out during low-bandwidth window | Use offline seed (export/import VMDK manually); configure replication after seed in place | N/A |
| `Replication paused — quiesce failed` on Windows VM | VR 8.x | VSS quiesce failing due to VSS writer error in guest | Disable application quiescing in replication settings; investigate VSS error in guest Windows Event Log | N/A |

## RPO and Sync

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| RPO alarm despite recent successful sync | VR 8.x | RPO calculation includes quiesce time; large VMs exceed window | Increase RPO target; reduce VM change rate or quiesce timeout | N/A |
| Replication stalled at 0% delta | VR 8.x | ESXi changed block tracking (CBT) reset | Reset CBT: power off VM, disable CBT, re-enable CBT, power on; replication resumes | N/A |

## Appliance

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VRMS UI unavailable — `Connection Refused` on port 8043 | VR 8.x | `hms` service crashed (OOM or cert issue) | SSH to VRMS; restart: `service hms restart` | N/A |
| VRMS registration lost after VCSA certificate replacement | VR 8.x | VRMS extension certificate trust invalidated | Re-register VRMS extension in vCenter via VRMS VAMI → Configuration | N/A |

## See also

- [VMware vSphere Replication — Common Issues](common-issues.md)
- [VMware SRM — Known Issues](../../srm/troubleshooting/known-issues/)
- [VMware vCenter — Known Issues](../../vcenter/troubleshooting/known-issues/)
