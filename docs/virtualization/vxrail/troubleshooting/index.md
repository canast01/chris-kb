# VxRail Troubleshooting


<div class="kb-summary">
VxRail troubleshooting notes for lifecycle failures, manager issues, host alerts, vSAN alerts, bundles, and network alerts.
</div>

```
┌────────────────────────────────────── VxRail — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       LCM upgrade failures and rollback; VxRail Manager VM (Mystic service) unavailable       │   │
│   │        Host alerts from ESXi or hardware; vSAN alerts for degraded objects or capacity        │   │
│   │           Support bundle generation failures; network alerts for VLAN or link issues          │   │
│   │       iDRAC system event review; OMIVV alarm triage; VxRail API debug for service issues      │   │
│   │      Escalation: Dell GSS P1, TAM contact, ProSupport log archive for critical incidents      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    LCM/VxRail issues block upgrades · diagnostics isolate service failures                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      LCM/VxRail Issues      │  │         Diagnostics         │  │          Escalation         │   │
│   │       LCM fail triage       │  │       VxRail API debug      │  │        VxRail bundle        │   │
│   │       Mgr unavailable       │  │        LCM log files        │  │         Dell support        │   │
│   │         Host alerts         │  │          iDRAC SEL          │  │        GSS escalation       │   │
│   │         vSAN alerts         │  │        vSAN health UI       │  │         TAM contact         │   │
│   │         Bundle fail         │  │        Bundle gen log       │  │        P1 ProSupport        │   │
│   │          Net alerts         │  │         OMIVV alerts        │  │         Log archive         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    LCM issues block upgrades · diagnostics pinpoint service faults                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   LCM Failures   │   Mgr Unavail    │     Host/vSAN     │   Bundle Fail    │  Network Alerts  │   │
│   │   LCM pre-chk    │    VxRail svc    │    Host alerts    │  Bundle gen err  │  VLAN mismatch   │   │
│   │    LCM stall     │  Mystic server   │    vSAN degrade   │  Log collection  │  Link down NIC   │   │
│   │   LCM rollback   │    VxRail API    │   vSAN capacity   │   API timeout    │    MTU issue     │   │
│   │  Post-fail chk   │   Mgr restart    │    iDRAC alerts   │  Manual bundle   │    ToR config    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC · 25GbE NICs · ToR switches                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM failure       = Upgrade job failed mid-sequence; check LCM logs and pre-check output for root    │
│  VxRail Manager    = Embedded management VM running Mystic service; provides REST API and vCenter     │
│  Host alert        = ESXi or iDRAC hardware alarm (disk, NIC, PSU, CPU) surfaced in VxRail plugin     │
│  vSAN degraded     = vSAN object FTT violated; component on failed disk or host; rebuild in progress  │
│  Support bundle    = Compressed log archive from VxRail Manager and ESXi hosts for Dell GSS submission│
│  SupportAssist     = Dell proactive support; auto-opens cases on hardware fault; submits initial logs │
│  iDRAC SEL         = System Event Log; hardware events (disk, PSU, fan, NIC); first stop for HW triage│
│  OMIVV             = OpenManage Integration for VMware vCenter; surfaces Dell HW alarms in vCenter    │
│  TAM escalation    = Engaging named Dell Technical Account Manager for critical production incidents  │
│  Dell ProSupport P1 = Highest Dell support priority; production down; response in under 4 hours       │
│  LCM rollback      = Reverting a node to previous ESXi boot bank after a failed LCM upgrade attempt   │
│  Network alert     = VLAN mismatch, link down, or MTU issue detected by OMIVV or VxRail Manager       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── VxRail — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       LCM upgrade failures and rollback; VxRail Manager VM (Mystic service) unavailable       │   │
│   │        Host alerts from ESXi or hardware; vSAN alerts for degraded objects or capacity        │   │
│   │           Support bundle generation failures; network alerts for VLAN or link issues          │   │
│   │       iDRAC system event review; OMIVV alarm triage; VxRail API debug for service issues      │   │
│   │      Escalation: Dell GSS P1, TAM contact, ProSupport log archive for critical incidents      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    LCM/VxRail issues block upgrades · diagnostics isolate service failures                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      LCM/VxRail Issues      │  │         Diagnostics         │  │          Escalation         │   │
│   │       LCM fail triage       │  │       VxRail API debug      │  │        VxRail bundle        │   │
│   │       Mgr unavailable       │  │        LCM log files        │  │         Dell support        │   │
│   │         Host alerts         │  │          iDRAC SEL          │  │        GSS escalation       │   │
│   │         vSAN alerts         │  │        vSAN health UI       │  │         TAM contact         │   │
│   │         Bundle fail         │  │        Bundle gen log       │  │        P1 ProSupport        │   │
│   │          Net alerts         │  │         OMIVV alerts        │  │         Log archive         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    LCM issues block upgrades · diagnostics pinpoint service faults                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   LCM Failures   │   Mgr Unavail    │     Host/vSAN     │   Bundle Fail    │  Network Alerts  │   │
│   │   LCM pre-chk    │    VxRail svc    │    Host alerts    │  Bundle gen err  │  VLAN mismatch   │   │
│   │    LCM stall     │  Mystic server   │    vSAN degrade   │  Log collection  │  Link down NIC   │   │
│   │   LCM rollback   │    VxRail API    │   vSAN capacity   │   API timeout    │    MTU issue     │   │
│   │  Post-fail chk   │   Mgr restart    │    iDRAC alerts   │  Manual bundle   │    ToR config    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC · 25GbE NICs · ToR switches                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM failure       = Upgrade job failed mid-sequence; check LCM logs and pre-check output for root    │
│  VxRail Manager    = Embedded management VM running Mystic service; provides REST API and vCenter     │
│  Host alert        = ESXi or iDRAC hardware alarm (disk, NIC, PSU, CPU) surfaced in VxRail plugin     │
│  vSAN degraded     = vSAN object FTT violated; component on failed disk or host; rebuild in progress  │
│  Support bundle    = Compressed log archive from VxRail Manager and ESXi hosts for Dell GSS submission│
│  SupportAssist     = Dell proactive support; auto-opens cases on hardware fault; submits initial logs │
│  iDRAC SEL         = System Event Log; hardware events (disk, PSU, fan, NIC); first stop for HW triage│
│  OMIVV             = OpenManage Integration for VMware vCenter; surfaces Dell HW alarms in vCenter    │
│  TAM escalation    = Engaging named Dell Technical Account Manager for critical production incidents  │
│  Dell ProSupport P1 = Highest Dell support priority; production down; response in under 4 hours       │
│  LCM rollback      = Reverting a node to previous ESXi boot bank after a failed LCM upgrade attempt   │
│  Network alert     = VLAN mismatch, link down, or MTU issue detected by OMIVV or VxRail Manager       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="lcm-failures/">
  <strong>LCM Failures</strong>
  <span>Lifecycle Manager failures, pre-check errors, upgrade stops, and recovery workflow.</span>
</a>

<a class="kb-card" href="manager-unavailable/">
  <strong>Manager Unavailable</strong>
  <span>VxRail Manager UI or service availability issues.</span>
</a>

<a class="kb-card" href="host-alerts/">
  <strong>Host Alerts</strong>
  <span>ESXi host warnings, disconnected hosts, hardware alerts, and cluster impact.</span>
</a>

<a class="kb-card" href="vsan-alerts/">
  <strong>vSAN Alerts</strong>
  <span>vSAN health issues, object health, resync, capacity, and disk group problems.</span>
</a>

<a class="kb-card" href="support-bundle-failures/">
  <strong>Support Bundle Failures</strong>
  <span>Failed or incomplete support bundle collection troubleshooting.</span>
</a>

<a class="kb-card" href="network-alerts/">
  <strong>Network Alerts</strong>
  <span>VxRail networking symptoms, uplinks, VLANs, vmkernel checks, and connectivity validation.</span>
</a>

</div>
