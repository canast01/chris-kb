# Inventory

Asset and configuration management references.


```text
┌────────────────── Inventory — Asset Tracking, CMDB, Lifecycle & License Management ───────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Inventory: know what assets exist, their state, owners, location, and support status     │   │
│   │      CMDB: track CI relationships and change history; feeds incident and change processes     │   │
│   │      Lifecycle: EOL dates drive refresh planning; licence counts prevent compliance gaps      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Asset & Config       │  │          Lifecycle          │  │     Licenses & Contracts    │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      Hardware asset reg     │  │       EOL/EOS tracking      │  │      License inventory      │   │
│   │       CMDB CI records       │  │       Refresh planning      │  │       Compliance count      │   │
│   │     Environment mapping     │  │      Decommission proc      │  │       Renewal calendar      │   │
│   │       System inventory      │  │      Migration tracking     │  │       Vendor contacts       │   │
│   │      Rack/rack-unit map     │  │      HW lifecycle state     │  │        Support levels       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CMDB         = Configuration Management Database; stores CIs and their relationships               │
│    CI           = Configuration Item; any asset tracked in CMDB with attributes and relations         │
│    EOL          = End of Life; vendor no longer sells the product; EOS = end of support               │
│    Asset register= Authoritative list of all hardware: serial, location, owner, lifecycle state       │
│    Refresh plan = Scheduled replacement of assets approaching EOL; budgeted in advance                │
│    SAM          = Software Asset Management; tracks licence entitlements vs actual usage              │
│    Support contract= Vendor SLA for hardware; coverage level (NBD/4h/24x7); expiry date               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="asset-tracking/"><strong>Asset Tracking</strong><span>Hardware asset register — serial numbers, rack locations, owners, and lifecycle state.</span></a>
<a class="kb-card" href="configuration-management/"><strong>Configuration Management</strong><span>CMDB structure, CI relationships, configuration item lifecycle, and change linkage.</span></a>
<a class="kb-card" href="environment-mapping/"><strong>Environment Mapping</strong><span>Production, non-production, DR environment mapping — dependencies and data flow.</span></a>
<a class="kb-card" href="hardware-lifecycle/"><strong>Hardware Lifecycle</strong><span>EOL tracking, refresh planning, decommission procedures, and vendor support timelines.</span></a>
<a class="kb-card" href="license-management/"><strong>License Management</strong><span>Software license inventory, compliance tracking, renewal dates, and consumption monitoring.</span></a>
<a class="kb-card" href="support-contracts/"><strong>Support Contracts</strong><span>Vendor support contract register — coverage levels, expiry dates, and escalation contacts.</span></a>
<a class="kb-card" href="system-inventory/"><strong>System Inventory</strong><span>Server, VM, and appliance inventory — hostname, IP, OS version, and function.</span></a>
</div>
