# Capacity on Demand — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Capacity Model, HA and Redundancy, Activation Flow, DR Site COD Architecture.
</div>

## Overview

Capacity on Demand (COD) is a software-defined capacity licensing model for Dell PowerMax and VMAX arrays. Physical drives are installed in the array chassis at the factory but the capacity is logically locked at the array controller level until a COD license is applied. No truck roll or hardware change is required — activation is entirely software-driven through SYMCLI or Unisphere.

## Capacity Model

```mermaid
graph LR
  ARRAY["Dell Array\nPowerStore / PowerMax\n(on-premises)"] <-->|"Dell APEX portal\ncapacity-on-demand"| APEX["Dell APEX\nCloud Console"]
  ADMIN(["Storage Admin"]) -->|"portal"| APEX
  APEX --> BILL["Usage-based Billing\n& Reporting"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAY ctrl
  class APEX,BILL cloud
  class ADMIN host
```
┌─────────────────────────────────────── Dell COD — How It Works ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Hardware ships with locked capacity; Dell licensing portal generates key for array serial   │   │
│   │      Apply license key via array management GUI or REST API; capacity available instantly     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Step 1 — Verify locked capacity visible in array: check available unlicensed drives/TB    │   │
│   │                  Step 2 — Log in to Dell Licensing Portal: licensing.dell.com                 │   │
│   │               Step 3 — Generate COD license key for specific array serial number              │   │
│   │            Step 4 — Apply key in array management UI: Settings > Licenses > Upload            │   │
│   │           Step 5 — Verify new capacity appears in available pool (no reboot needed)           │   │
│   │            Step 6 — Update CMDB: record activation date, TB unlocked, remaining COD           │   │
│   │               Step 7 — Close change ticket with before/after capacity screenshot              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  PowerStore REST activation:                                  │   │
│   │                   POST /api/rest/license  --data {"key": "<license_string>"}                  │   │
│   │                                                                                               │   │
│   │                                     Verify on PowerStore:                                     │   │
│   │                  GET /api/rest/capacity  → check used_gb and total_gb change                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Locked capacity  = Drives/nodes installed but not accessible; shown as "reserved" in array         │
│    Licensing portal = Dell web portal for generating COD/FOD keys per array serial number             │
│    Key binding      = COD key cryptographically tied to array serial; cannot be reused                │
│    Instant unlock   = Capacity joins pool within seconds; no volume migration or downtime             │
│    Before/after     = Screenshot capacity before and after activation; attach to change ticket        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
