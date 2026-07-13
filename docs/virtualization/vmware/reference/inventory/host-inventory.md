---
tags:
  - reference
description: "Host Inventory reference covering Overview, Host Inventory Table, Fields Reference, Host Lifecycle Events, Adding a Host."
---
# Host Inventory

<div class="kb-summary">
Host Inventory reference covering Overview, Host Inventory Table, Fields Reference, Host Lifecycle Events, Adding a Host.

*Applies to: vSphere 7.x / 8.x*
</div>

> Part of the [Inventory](index.md) reference.

---

```d2
direction: down

host_inventory_table: "Host Inventory Table" {shape: rectangle}
fields_reference: "Fields Reference" {shape: rectangle}
host_lifecycle_events: "Host Lifecycle Events" {shape: rectangle}
adding_a_host: "Adding a Host" {shape: rectangle}

host_inventory_table -> fields_reference: uses
fields_reference -> host_lifecycle_events: uses
host_lifecycle_events -> adding_a_host: uses
```

## Overview

Track every ESXi host in the environment using the table format below. One row per physical host. Update after hardware changes, firmware updates, or cluster moves.

## Host Inventory Table

| Hostname | Cluster | Model | CPU Sockets | Cores (per socket) | Total vCPUs | RAM (GB) | ESXi Version | HBA Type | NIC Count | Management IP | iDRAC/iLO | State | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| esx-prod-01 | cl-prod-compute-01 | Dell PowerEdge R750xa | 2 | 32 | 128 | 1024 | 8.0 U3 | FC (QLogic) | 4 x 25GbE | 10.10.10.11 | idrac-esx-prod-01 | Connected | |
| esx-prod-02 | cl-prod-compute-01 | Dell PowerEdge R750xa | 2 | 32 | 128 | 1024 | 8.0 U3 | FC (QLogic) | 4 x 25GbE | 10.10.10.12 | idrac-esx-prod-02 | Connected | |
| esx-prod-03 | cl-prod-compute-01 | Dell PowerEdge R750xa | 2 | 32 | 128 | 1024 | 8.0 U3 | FC (QLogic) | 4 x 25GbE | 10.10.10.13 | idrac-esx-prod-03 | Connected | |
| esx-mgmt-01 | cl-prod-mgmt-01 | Dell PowerEdge R650 | 2 | 16 | 64 | 256 | 8.0 U3 | — | 2 x 25GbE | 10.10.10.21 | idrac-esx-mgmt-01 | Connected | vSAN mgmt node |

## Fields Reference

| Field | Description |
|---|---|
| Hostname | Short hostname following naming standard `esx-<site>-<##>` |
| Cluster | vSphere cluster the host belongs to |
| Model | Vendor and model (e.g. Dell PowerEdge R750xa, HPE ProLiant DL380 Gen10) |
| CPU Sockets | Physical CPU socket count |
| Cores (per socket) | Core count per physical processor |
| Total vCPUs | Total logical CPUs visible to vSphere (sockets × cores × HT) |
| RAM (GB) | Physical memory installed |
| ESXi Version | Full ESXi build version (e.g. 8.0 U3b) |
| HBA Type | Fibre Channel card vendor/model; note if iSCSI or NVMe-oF |
| NIC Count | Number and speed of physical NICs used for vSphere networking |
| Management IP | IP address of the management VMkernel |
| iDRAC/iLO | Out-of-band management hostname or IP |
| State | Connected / Disconnected / Maintenance / Decommissioned |
| Notes | Any standing issues, upcoming replacements, or exceptions |

## Host Lifecycle Events

Track significant host events here for audit and troubleshooting context:

| Date | Hostname | Event | Performed By |
|---|---|---|---|
| 2026-03-10 | esx-prod-01 | ESXi upgraded to 8.0 U3 | C. Anastasiadis |
| 2026-04-02 | esx-prod-04 | Disk group replaced — vSAN rebuild complete | C. Anastasiadis |

## Adding a Host

When adding a new host to the inventory:

- [ ] Hostname assigned per naming standard
- [ ] iDRAC/iLO configured and reachable
- [ ] ESXi installed from approved baseline ISO
- [ ] Host added to vCenter and correct cluster
- [ ] NTP, DNS, syslog, and scratch partition configured
- [ ] Host firmware updated to approved baseline
- [ ] Host added to monitoring
- [ ] Inventory table updated
