# Host Inventory

> Part of the [Inventory](../index.md) reference.

---

```text
┌─────────────────┬──────────────────────┬───────────────────┬──────────┬───────────┐
│   Hostname      │  Cluster             │  Hardware Model   │  ESXi    │  State    │
├─────────────────┼──────────────────────┼───────────────────┼──────────┼───────────┤
│ esx-prod-01     │ cl-prod-compute-01   │ Dell R750xa       │ 8.0 U3   │ Connected │
│  IP:10.10.10.11 │  2S×32C / 1024GB RAM │ FC HBA (QLogic)   │          │           │
├─────────────────┼──────────────────────┼───────────────────┼──────────┼───────────┤
│ esx-prod-02     │ cl-prod-compute-01   │ Dell R750xa       │ 8.0 U3   │ Connected │
│  IP:10.10.10.12 │  2S×32C / 1024GB RAM │ 4×25GbE NICs      │          │           │
├─────────────────┼──────────────────────┼───────────────────┼──────────┼───────────┤
│ esx-mgmt-01     │ cl-prod-mgmt-01      │ Dell R650         │ 8.0 U3   │ Connected │
│  IP:10.10.10.21 │  2S×16C /  256GB RAM │ 2×25GbE NICs      │          │ vSAN node │
└─────────────────┴──────────────────────┴───────────────────┴──────────┴───────────┘
  Each host: vmk0=mgmt │ vmk1=vMotion │ vmk2=vSAN │ vmk3=NSX-overlay
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
