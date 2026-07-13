---
tags:
  - reference
description: "Virtualization Glossary reference covering HA, DRS, vMotion, Storage vMotion, Snapshot and 5 more sections."
---
# Virtualization Glossary

<div class="kb-summary">
Virtualization Glossary reference covering HA, DRS, vMotion, Storage vMotion, Snapshot and 5 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

ha: "HA" {shape: rectangle}
drs: "DRS" {shape: rectangle}
vmotion: "vMotion" {shape: rectangle}
storage_vmotion: "Storage vMotion" {shape: rectangle}
snapshot: "Snapshot" {shape: rectangle}
datastore_latency: "Datastore Latency" {shape: rectangle}

ha -> drs: uses
drs -> vmotion: uses
vmotion -> storage_vmotion: uses
storage_vmotion -> snapshot: uses
snapshot -> datastore_latency: uses
```

## HA
High Availability. Automatically restarts VMs after host failure.

## DRS
Distributed Resource Scheduler. Balances workloads across hosts.

## vMotion
Moves a running VM between hosts.

## Storage vMotion
Moves VM storage between datastores.

## Snapshot
Point-in-time disk state used for backup or rollback.

## Datastore Latency
Time required to complete storage operations.

## CPU Ready
Time a VM waits for CPU scheduling.

## Ballooning
Memory reclamation mechanism used during memory pressure.

## Resync
Rebuild of storage components after failure or maintenance.

## Admission Control
Ensures enough capacity exists for failover.
