# ServiceNow — Asset Inventory

<div class="kb-summary">
Asset tracking, CMDB, environment mapping, lifecycle, and license management procedures within ServiceNow.
</div>

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
<!-- diagram:inventory -->

<div class="kb-grid">
  <a class="kb-card" href="asset-lifecycle/">
    <span class="kb-card-title">Asset Lifecycle</span>
    <span class="kb-card-desc">End-to-end lifecycle from procurement to decommission</span>
  </a>
  <a class="kb-card" href="asset-tracking/">
    <span class="kb-card-title">Asset Tracking</span>
    <span class="kb-card-desc">Track hardware and software assets in ServiceNow</span>
  </a>
  <a class="kb-card" href="cmdb/">
    <span class="kb-card-title">CMDB</span>
    <span class="kb-card-desc">Configuration item management and relationship mapping</span>
  </a>
  <a class="kb-card" href="environment-mapping/">
    <span class="kb-card-title">Environment Mapping</span>
    <span class="kb-card-desc">Document and map infrastructure environments</span>
  </a>
  <a class="kb-card" href="license-management/">
    <span class="kb-card-title">License Management</span>
    <span class="kb-card-desc">Software license tracking and compliance</span>
  </a>
  <a class="kb-card" href="support-contracts/">
    <span class="kb-card-title">Support Contracts</span>
    <span class="kb-card-desc">Vendor support contract tracking and renewal</span>
  </a>
<a class="kb-card" href="system-inventory/"><strong>System Inventory</strong><span>Physical and virtual server inventory — discovery, classification, and tracking.</span></a>
<a class="kb-card" href="configuration-management/"><strong>Configuration Management</strong><span>CMDB CI attributes, relationship mapping, and data quality management.</span></a>
<a class="kb-card" href="ownership/"><strong>Ownership</strong><span>Asset ownership assignment, accountability model, and transfer procedures.</span></a>
<a class="kb-card" href="cleanup/"><strong>Cleanup</strong><span>Stale CI remediation, duplicate removal, and CMDB hygiene procedures.</span></a>
<a class="kb-card" href="audit/"><strong>Audit</strong><span>Asset audit procedures, reconciliation with discovery data, and compliance reporting.</span></a>
<a class="kb-card" href="hardware-lifecycle/"><strong>Hardware Lifecycle</strong><span>Hardware asset lifecycle — procurement, tracking, refresh planning, and disposal.</span></a>
</div>
