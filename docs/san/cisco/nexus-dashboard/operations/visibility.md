---
tags:
  - operations
  - san
---
# Nexus Dashboard: Endpoint Tracking, Flow Visibility, and Topology View


<div class="kb-summary">
Nexus Dashboard: Endpoint Tracking, Flow Visibility, and Topology View reference covering Flow Visibility, Topology View, Path Trace for Troubleshooting, Common Visibility Issues.

*Applies to: Cisco MDS · Nexus*
</div>

```text
┌──────────────────────────────────── Nexus Dashboard — Visibility ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        NDI Visibility: comprehensive view of fabric state — topology, endpoints, flows        │   │
│   │             Topology view: interactive map of spine/leaf/border-leaf interconnects            │   │
│   │           Endpoint tracking: VM/container moves, dual-home detection, stale entries           │   │
│   │              Flow analytics: per-flow visibility with source/dest/protocol/bytes              │   │
│   │              Audit trail: who changed what and when across ACI and NX-OS fabrics              │   │
│   │               Multi-site: unified view across multiple ACI domains in single UI               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Visibility data from APIC REST + MDT streaming · stored in NDI DB · rendered in ND UI                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Topology view = Interactive fabric map showing switch interconnects and health                       │
│  Endpoint = VM, container, or bare-metal IP/MAC connected to fabric leaf                              │
│  Dual-home = Endpoint connected to two leaf switches for redundancy                                   │
│  Stale endpoint = Endpoint record remaining after VM is deleted; detected by NDI                      │
│  Flow analytics = NDI tracking actual traffic flows through fabric for visibility                     │
│  Audit trail = NDI logging all APIC configuration changes with user and timestamp                     │
│  Multi-site view = Single ND UI showing health and state for all registered ACI sites                 │
│  EPG = Endpoint Group; ACI policy construct; endpoints grouped by EPG                                 │
│  Contract = ACI inter-EPG connectivity policy; NDI verifies enforcement                               │
│  BD = Bridge Domain; ACI Layer-2 forwarding domain containing EPGs                                    │
│  Border leaf = Leaf switch connecting ACI fabric to external L3 networks                              │
│  Delta analysis = NDI showing configuration changes between two epochs                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Common Visibility Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Endpoint not found | Not yet learned or aged out | Check on leaf: `show endpoint ip <ip>` |
| Flow data missing | Telemetry not enabled on leaf | Verify ERSPAN/sFlow config on fabric switches |
| Path trace shows "No path" | Policy contract missing | Check ACI contracts between source and destination EPGs |
| Topology not loading | NDI not connected to APIC | Re-check fabric connection in NDI settings |
| Latency values all zero | Latency telemetry requires specific hardware | Verify leaf hardware supports latency reporting |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
