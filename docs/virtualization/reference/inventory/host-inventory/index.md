# Host Inventory


<div class="kb-summary">
Host Inventory reference covering Overview, Host Inventory Table, Fields Reference, Host Lifecycle Events, Adding a Host.
</div>

```
┌────────────────────────────────────── vSphere — Host Inventory ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Per-ESXi-host record for lifecycle, capacity, and support — updated after each LCM cycle   │   │
│   │        Fields: hostname, cluster, hardware model, CPU (sockets/cores), RAM, ESXi build        │   │
│   │      Network: NIC count, VDS uplinks, NIC model; Storage: HBA count, HBA model, iDRAC IP      │   │
│   │      State: lockdown mode, maintenance mode, vSAN participation, host profile compliance      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hardware identity drives upgrade eligibility · ESXi build drives HCL compliance state              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Identity          │  │           Hardware          │  │            State            │   │
│   │       Hostname (FQDN)       │  │      Model (PowerEdge)      │  │          ESXi build         │   │
│   │        Cluster member       │  │      CPU sockets/cores      │  │        Lockdown mode        │   │
│   │       vCenter managed       │  │        RAM (GB total)       │  │         Maint. mode         │   │
│   │        iDRAC IP addr        │  │       NIC count/model       │  │         vSAN member         │   │
│   │          Site/rack          │  │       HBA count/model       │  │          Profile OK         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Hardware + state fields determine maintenance eligibility and capacity contribution                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Host       │      Model       │     CPU / RAM     │    ESXi build    │      State       │   │
│   │   esx-prod-01    │      R750xa      │    2x18c/1.5TB    │      8.0 U3      │      Active      │   │
│   │   esx-prod-02    │      R750xa      │    2x18c/1.5TB    │      8.0 U3      │      Active      │   │
│   │   esx-prod-03    │      R750xa      │    2x18c/1.5TB    │      8.0 U2      │   Needs patch    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell PowerEdge servers · iDRAC OOB · NIC/HBA PCIe cards · vSAN NVMe disks                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ESXi build    = Specific patch level (e.g. 8.0 U3 build 24022510); matches HCL entry               │
│    Lockdown mode = ESXi blocks direct SSH/shell; all management via vCenter API only                  │
│    Host profile  = vCenter config template enforcing NTP, syslog, lockdown, NIC teaming               │
│    HBA           = Host Bus Adapter; FC card connecting ESXi host to SAN fabric                       │
│    iDRAC         = Dell out-of-band management; independent of ESXi state for hardware ops            │
│    vSAN member   = Host contributing local NVMe/SSD disks to the vSAN datastore pool                  │
│    Maint. mode   = ESXi state where VMs are evacuated prior to host maintenance work                  │
│    HCL           = Hardware Compatibility List; ESXi build + model + driver must be listed            │
│    NIC teaming   = Multiple physical NICs bonded for redundancy and throughput on VDS                 │
│    Profile OK    = Host configuration matches host profile; non-compliant hosts flagged               │
│    Site/rack     = Physical location tag used for anti-affinity and failure domain config             │
│    CPU sockets   = Physical CPU count; drives vCPU overcommit capacity for the cluster                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Inventory](../index.md) reference.

---

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
