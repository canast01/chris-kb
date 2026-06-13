---
tags:
  - servicenow
---
# System Inventory Management


<div class="kb-summary">
System Inventory Management reference covering Overview, Required Fields, Daily Checks, Workflow.

*Applies to: ServiceNow*
</div>

```text
┌──────────────────────────────────── Inventory — System Inventory ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Server, VM, and appliance inventory: hostname, IP, OS version, owner, function        │   │
│   │        Use for: change impact scoping, patching campaigns, DR planning, capacity review       │   │
│   │     Keep current: discovery scan monthly; audit reconcile quarterly; decommission promptly    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Inventory Fields               │  │                 Maintenance                 │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │               Hostname (FQDN)                │  │            Discovery scan monthly           │   │
│   │              IP address (v4/v6)              │  │              Reconcile vs CMDB              │   │
│   │             OS / version / patch             │  │             Update on OS change             │   │
│   │               Function / role                │  │            Archive decommissioned           │   │
│   │             Environment + owner              │  │            Flag unpatched systems           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FQDN         = Fully Qualified Domain Name; hostname + domain; needed for cert and DNS             │
│    Discovery    = Automated scan (Nmap, SCCM, vCenter) to find all active systems                     │
│    Ghost system = System in inventory that no longer exists; remove after confirmation                │
│    Patch level  = OS patch currency; inventory identifies systems behind patch baseline               │
│    Role tag     = System function label (web, db, backup, infra); used for change scoping             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

System inventory management tracks servers, storage, network devices, and infrastructure components across environments.

## Required Fields

- Hostname
- IP address
- Operating system
- Environment
- Owner
- Location
- Support team

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Verify inventory records updated |  |  |
| Confirm new systems added |  |  |
| Validate decommissioned systems removed |  |  |

## Workflow

1. Identify new system
2. Record system details
3. Assign ownership
4. Update inventory database
