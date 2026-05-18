# VxRail Hardware

VxRail hardware notes for nodes, disks, NICs, power, cooling, iDRAC, and firmware inventory.

```
┌─────────────────────────────────────────────────────┐
│                   VxRail Chassis                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Node 1  │  │  Node 2  │  │  Node N  │  ...     │
│  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │          │
│  │ │ CPU  │ │  │ │ CPU  │ │  │ │ CPU  │ │          │
│  │ │ MEM  │ │  │ │ MEM  │ │  │ │ MEM  │ │          │
│  │ └──────┘ │  │ └──────┘ │  │ └──────┘ │          │
│  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │          │
│  │ │Disks │ │  │ │Disks │ │  │ │Disks │ │          │
│  │ │(vSAN)│ │  │ │(vSAN)│ │  │ │(vSAN)│ │          │
│  │ └──────┘ │  │ └──────┘ │  │ └──────┘ │          │
│  │ NIC PSU  │  │ NIC PSU  │  │ NIC PSU  │          │
│  │ Fan iDRAC│  │ Fan iDRAC│  │ Fan iDRAC│          │
│  └──────────┘  └──────────┘  └──────────┘          │
│         │              │              │              │
│         └──────────────┴──────────────┘             │
│                  Management Network                  │
│           ┌─────────────────────────┐               │
│           │    VxRail Manager VM    │               │
│           │  iDRAC ◄──► REST API   │               │
│           └─────────────────────────┘               │
└─────────────────────────────────────────────────────┘
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
