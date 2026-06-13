---
tags:
  - operations
---
# Virtualization Network Validation


<div class="kb-summary">
Virtualization Network Validation reference covering Overview, Pre-Checks, Steps, Validation, Rollback and 1 more sections.
</div>

```text
┌────────────────────────────── Virtualization Network Validation Runbook ──────────────────────────────┐
│                                                                                                       │
│    Use after network changes, VLAN changes, host work, NSX changes, or VM connectivity issues         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Check Sequence                │  │                 Common Fixes                │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │           1. VM network assignment           │  │             Reassign port group             │   │
│   │          2. Port group VLAN config           │  │             Fix VLAN ID mismatch            │   │
│   │            3. Host uplink status             │  │              Check NIC / cable              │   │
│   │           4. VLAN / overlay config           │  │            Fix switch VLAN trunk            │   │
│   │         5. NSX segment (if overlay)          │  │             Re-deploy NSX config            │   │
│   │               6. Ping from VM                │  │             Check firewall rule             │   │
│   │           7. DNS resolution in VM            │  │             Check DNS server IP             │   │
│   │           8. App connectivity test           │  │              App owner confirms             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Port group    = Named network on a vSwitch or dvSwitch; VMs connect to port groups                 │
│    dvSwitch      = Distributed virtual switch; managed centrally from vCenter                         │
│    VLAN trunk    = Physical switch port allowing multiple VLANs; must match port group                │
│    NSX segment   = Overlay network (GENEVE); not tied to physical VLANs                               │
│    Uplink        = Physical NIC on ESXi connected to physical switch; check link state                │
│    Teaming       = NIC bonding policy on vSwitch; active/standby or load balance                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

Use this after network changes, VLAN changes, host work, NSX changes, or VM connectivity issues.

## Pre-Checks

- Confirm affected VLANs or segments.
- Confirm port groups or NSX segments.
- Confirm uplink status.
- Confirm recent switch or firewall changes.
- Confirm affected VM scope.

## Steps

1. Check VM network assignment.
2. Check port group or segment configuration.
3. Check host uplinks.
4. Check VLAN or overlay configuration.
5. Check gateway reachability.
6. Check NSX edge and routing if used.
7. Test from affected and unaffected VMs.

## Validation

- VM connectivity works.
- Uplinks are healthy.
- VLAN or segment config is correct.
- Routing is working.
- No new network alarms.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
