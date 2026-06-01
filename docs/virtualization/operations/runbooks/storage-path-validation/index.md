# Virtualization Storage Path Validation


<div class="kb-summary">
Virtualization Storage Path Validation reference covering Overview, Pre-Checks, Steps, Validation, Rollback and 1 more sections.
</div>

```
┌─────────────────────────────────── Storage Path Validation Runbook ───────────────────────────────────┐
│                                                                                                       │
│    Use after SAN changes, storage maintenance, host work, or datastore alerts                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Check Sequence                │  │                 Common Fixes                │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │           1. Datastore visibility            │  │             Rescan HBA adapters             │   │
│   │           2. Host storage adapters           │  │             Check HBA driver/FW             │   │
│   │           3. Path count and state            │  │           Fix zoning on SAN switch          │   │
│   │            4. Multipathing policy            │  │            Set RR per array guide           │   │
│   │          5. Array masking / zoning           │  │             Add host to zone set            │   │
│   │            6. Datastore I/O test             │  │            Run iometer / dd test            │   │
│   │            7. App I/O validation             │  │              App owner confirms             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    HBA      = Host Bus Adapter; FC or iSCSI NIC on ESXi connecting to SAN fabric                      │
│    Zoning   = SAN switch config allowing specific HBAs to see specific storage ports                  │
│    Masking  = Array-side config allowing specific initiators to access specific LUNs                  │
│    RR       = Round Robin multipathing policy; distributes I/O across all active paths                │
│    Dead path = Path in dead/error state; verify SAN port, cable, and zone config                      │
│    Rescan   = ESXi re-discovers storage; run after SAN changes to pick up new LUNs                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

Use this after SAN changes, storage maintenance, host work, or datastore alerts.

## Pre-Checks

- Confirm affected hosts and datastores.
- Confirm storage array status.
- Confirm SAN zoning or masking changes.
- Confirm no active datastore outage.
- Confirm maintenance window if changes are planned.

## Steps

1. Check datastore visibility.
2. Check host storage adapters.
3. Check path count and path state.
4. Check multipathing policy.
5. Review storage latency.
6. Confirm VMs can access datastores.
7. Compare against expected path design.

## Validation

- Expected paths are visible.
- No dead paths remain unless expected.
- Datastores are mounted.
- Latency is normal.
- No new storage alarms.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
