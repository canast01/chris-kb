# VxRail Hardware


<div class="kb-summary">
VxRail hardware notes for nodes, disks, NICs, power, cooling, iDRAC, and firmware inventory.
</div>

```
┌────────────────────────────────────────── VxRail — Hardware ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        VxRail hardware operations: node health monitoring via iDRAC and VxRail Manager        │   │
│   │      Disk replacement procedures using guided workflow; NIC health and link state checks      │   │
│   │           Power and cooling alarm management; iDRAC out-of-band access configuration          │   │
│   │         Firmware inventory and compliance tracking via OMIVV and LCM bundle validation        │   │
│   │       SupportAssist and CloudIQ for proactive hardware monitoring and capacity planning       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Node health monitors hardware state · hardware ops cover disk and NIC                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Node Health         │  │         Hardware Ops        │  │        HW Monitoring        │   │
│   │        VxRail plugin        │  │       Disk replacement      │  │         OMIVV alerts        │   │
│   │         iDRAC health        │  │        NIC link check       │  │        SupportAssist        │   │
│   │        ESXi connected       │  │        Power/cooling        │  │         CloudIQ view        │   │
│   │         vSAN node ok        │  │         iDRAC config        │  │        iDRAC SEL log        │   │
│   │        Hardware alarm       │  │         FW inventory        │  │         Temp/fan/PSU        │   │
│   │          Disk state         │  │        Guided removal       │  │         Drive SMART         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Node health surfaces hardware faults · ops guide replacement procedures                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Node Health    │   Disk Replace   │     NIC Health    │  Power/Cooling   │     iDRAC/FW     │   │
│   │  VxRail plugin   │ Guided workflow  │     Link state    │    PSU status    │   iDRAC config   │   │
│   │   iDRAC health   │ Pre-removal chk  │    NIC teaming    │   Temp alarms    │   FW inventory   │   │
│   │  ESXi connected  │   vSAN rebuild   │   Driver compat   │    Fan speed     │    iDRAC LDAP    │   │
│   │   vSAN node ok   │ Post-replace val │   OMIVV NIC chk   │  Cooling zones   │  FW compliance   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · NVMe/SSD/HDD drives · iDRAC OOB chip · PSUs · Cooling fans · NICs           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  iDRAC             = Integrated Dell Remote Access Controller; hardware health, OOB console, LDAP auth│
│  VxRail Manager    = Embedded management VM; aggregates node health from iDRAC and ESXi into plugin   │
│  OMIVV             = OpenManage Integration for VMware vCenter; surfaces Dell HW alarms in vCenter UI │
│  SupportAssist     = Dell proactive support service; auto-creates cases on hardware fault detection   │
│  CloudIQ           = Dell SaaS monitoring platform; capacity, health, and performance tracking        │
│  SEL               = System Event Log on iDRAC; records all hardware events (disk, PSU, fan, NIC)     │
│  SMART             = Self-Monitoring Analysis and Reporting Technology; drive health predictor        │
│  PSU               = Power Supply Unit; dual PSU in each VxRail node for redundancy                   │
│  NIC teaming       = Active/standby or LACP NIC bonding on VxRail nodes for network redundancy        │
│  Firmware inventory = LCM bundle tracks required FW versions for BIOS, iDRAC, NICs, and drives        │
│  vSAN disk group   = Cache + capacity disk grouping per node; disk failure triggers vSAN rebuild      │
│  Guided disk replacement = VxRail Manager workflow that puts node in maint mode before disk removal   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="node-health/">
  <strong>Node Health</strong>
  <span>Node hardware status, sensors, alerts, and serviceability checks.</span>
</a>

<a class="kb-card" href="disk-replacement/">
  <strong>Disk Replacement</strong>
  <span>Disk fault workflow, vSAN impact, replacement validation, and vendor handoff.</span>
</a>

<a class="kb-card" href="nic-health/">
  <strong>NIC Health</strong>
  <span>Physical NIC state, link status, uplinks, redundancy, and troubleshooting.</span>
</a>

<a class="kb-card" href="power-cooling/">
  <strong>Power and Cooling</strong>
  <span>Power supply, thermal, fan, and environmental alert review.</span>
</a>

<a class="kb-card" href="idrac/">
  <strong>iDRAC</strong>
  <span>iDRAC access, hardware inventory, logs, alerts, and support evidence.</span>
</a>

<a class="kb-card" href="firmware-inventory/">
  <strong>Firmware Inventory</strong>
  <span>Firmware versions, drift review, lifecycle alignment, and upgrade notes.</span>
</a>

</div>
