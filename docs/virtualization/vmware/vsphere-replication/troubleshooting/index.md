# vSphere Replication — Troubleshooting

<div class="kb-summary">
vSphere Replication — Troubleshooting reference.
</div>

```text
┌──────────────────────────────── vSphere Replication — Troubleshooting ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Replication failing: verify firewall rules on ports 443, 8043, 31031; check site pairing cert │   │
│   │     RPO violations: check available WAN bandwidth; review missed sync count in VR monitor     │   │
│   │     VR appliance unreachable: verify VRMS/VRS VM is powered on; check VAMI service status     │   │
│   │     CBT issues: reset CBT on VM via snapshot cycle; required after hardware change events     │   │
│   │       Collect support bundle from VRMS VAMI; attach to VMware GSS case with vCenter logs      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues triage network and appliance faults · diagnostics use logs and VAMI                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │       Replication fail      │  │        vCenter events       │  │         VRMS bundle         │   │
│   │        RPO violation        │  │         VAMI health         │  │        GSS case open        │   │
│   │       VRMS unreachable      │  │        VR monitor UI        │  │       vCenter log bndl      │   │
│   │        CBT corruption       │  │      /var/log/vmware/vr     │  │        TAM escalation       │   │
│   │        Site pair fail       │  │        Firewall test        │  │        Skyline health       │   │
│   │      Disk space target      │  │        Cert validity        │  │        Version compat       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues triage replication faults · diagnostics use VAMI and VR monitor                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │   Rep failing    │  vCenter events  │ /var/log/vmware/vr│   VRMS bundle    │   Re-configure   │   │
│   │   RPO violated   │  VAMI health pg  │    /var/log/hms   │   GSS P1 case    │    Reduce RPO    │   │
│   │    VRMS down     │  VR monitor UI   │  /var/log/vmware  │   TAM escalate   │   Restart VRMS   │   │
│   │    CBT issue     │  Firewall test   │    VRMS syslog    │  Skyline health  │    Reset CBT     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (VRMS + VRS) · RAM DIMMs · WAN link · Firewall between sites · Target datastore              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Replication failure = VR sync cycle did not complete; check vCenter events for error code and source │
│  RPO violation      = Missed sync count > 0 in VR monitor; investigate bandwidth or appliance health  │
│  CBT               = Changed Block Tracking; bitmap tracking VMDK changes; corruption causes resync   │
│  CBT reset          = Snapshot + delete cycle on a VM to force CBT bitmap rebuild; triggers full      │
│  VAMI               = Virtual Appliance Management Interface; check service status and disk usage here│
│  VR Monitor UI      = vCenter plugin tab showing per-VM replication status, RPO, and last sync time   │
│  Site pairing failure = Lost trust between source/target vCenter; re-pair after certificate change    │
│  Firewall ports     = 443 (vCenter), 8043 (VRMS mgmt), 31031 (VRS data); all required between sites   │
│  VRMS support bundle = Diagnostic archive from VAMI including VR logs; attach to GSS case             │
│  Disk space target  = Insufficient space on target datastore; VR pauses replication until resolved    │
│  Skyline Health     = VMware proactive tool validating VR configuration against known best practices  │
│  Log path           = Primary VR logs at /var/log/vmware/vr/; HMS service logs at /var/log/hms        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
