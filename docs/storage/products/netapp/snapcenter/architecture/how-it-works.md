---
tags:
  - architecture
  - netapp
---
# SnapCenter — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Topology, HA Options, Components, Connectivity and 2 more sections.

*Applies to: SnapCenter 5.x*
</div>
![SnapCenter — How It Works](../../../../../assets/storage-netapp-snapcenter-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Admin" as ADM
participant "SnapCenter Server\n(Windows)" as SC
participant "SnapCenter Plugin\n(host agent)" as PLG
participant "Application\n(SQL / Oracle / SAP)" as APP
participant "ONTAP\n(Snapshot engine)" as ONTAP
participant "SnapVault / SnapMirror" as REP

ADM -> SC: Schedule backup policy
SC -> PLG: Trigger pre-backup quiesce
PLG -> APP: Application-consistent quiesce
APP --> PLG: Quiesced
PLG -> ONTAP: Create Snapshot
ONTAP --> PLG: Snapshot created
PLG -> APP: Unquiesce
APP --> PLG: Running
ONTAP -> REP: Vault / mirror Snapshot to secondary
REP --> ONTAP: Replicated
SC --> ADM: Backup complete + catalog entry
@enduml
```

## Overview

SnapCenter is a Windows-based centralized data protection platform that orchestrates application-consistent ONTAP snapshots across a fleet of hosts and applications. It communicates with ONTAP storage systems via the ONTAP REST API or ZAPI, with application hosts via the SnapCenter Agent (TCP 8145), and exposes a web GUI on port 8146 and a REST API for automation. The architecture separates the control plane (SnapCenter Server), the data plane (ONTAP snapshots), and the agent layer (plugins on protected hosts).

## Topology

```d2
direction: right

SCW: "SnapCenter Server\n(Windows / Linux VM" {shape: rectangle}
PL1: "Plug-in for SQL Server" {shape: rectangle}
PL2: "Plug-in for Oracle" {shape: rectangle}
PL3: "Plug-in for VMware" {shape: rectangle}
ONTAP: "NetApp ONTAP\nSnapshot · SnapMirror · SnapVault" {shape: rectangle}
ADMIN: "DBA / Storage Admin" {shape: rectangle}

SCW -> PL1
SCW -> PL2
SCW -> PL3
PL1 -> PL2
PL2 -> PL3
PL3 -> ONTAP
ADMIN -> SCW
```

## HA Options

SnapCenter Server is not natively HA. Recommended approaches:

- **Windows Server Failover Cluster (WSFC)** — host the SnapCenter application on a WSFC for automatic failover
- **VM-based resilience** — run SnapCenter as a VM protected by VMware HA; RTO is VM restart time (~5 minutes)
- **MySQL HA** — run the repository on a highly available MySQL cluster to prevent data loss
- **SnapCenter Server backup** — use the built-in backup feature to snapshot the repository and application config daily; store on secondary ONTAP

## Components

| Component | Description |
|---|---|
| SnapCenter Server | Windows Server hosting the web application, scheduler, and REST API; accessible at `https://<server>:8146` |
| Repository Database | MySQL database storing all job history, policies, resource groups, and RBAC configuration |
| SnapCenter Agent | Lightweight Windows or Linux service (port 8145) on each protected host; runs pre/post quiesce scripts |
| Plug-in for Windows | VSS-based backup for SQL Server, Exchange, and Windows filesystems |
| Plug-in for UNIX | Agent extension for Linux/AIX; supports Oracle, SAP HANA, and UNIX filesystems |
| Plug-in for VMware vSphere | Separate OVA appliance registered with vCenter; VM-level and datastore-level backup without in-guest agents |
| ONTAP Storage Systems | Registered as storage connections; SnapCenter manages snapshots, SnapMirror updates, and SnapVault transfers via ONTAP APIs |
| SMTP / Email Relay | Optional; SnapCenter sends job notifications via SMTP |

## Connectivity

| Connection | Protocol / Port | Direction |
|---|---|---|
| Admin browser to SnapCenter GUI | HTTPS/8146 | Client → Server |
| SnapCenter Server to ONTAP | HTTPS/443 (REST) or ZAPI | Server → ONTAP cluster-mgmt LIF |
| SnapCenter Server to Agent | TCP/8145 | Server → Host agent |
| SnapCenter Agent to Server | TCP/8145 | Host → Server (callback) |
| SnapCenter to MySQL repository | TCP/3306 | Local (or network if remote DB) |
| SnapCenter to SMTP relay | TCP/25 or 587 | Server → Mail relay |
| Plug-in for VMware to vCenter | HTTPS/443 | Plugin OVA → vCenter |

## Sizing Guidelines

- **SnapCenter Server**: Minimum 4 vCPU / 8 GB RAM for up to 50 hosts; scale to 8 vCPU / 16 GB for 50–200 hosts; dedicated Windows Server 2019 or 2022
- **Repository database**: Allow ~500 MB per 1,000 backup jobs retained; 20 GB minimum partition
- **Concurrent jobs**: Default maximum is 5; increase to 10–20 in global settings for large environments
- **Plugin hosts per server**: Supports up to ~300–400 active hosts; beyond that, evaluate a secondary SnapCenter instance

## Plugins

| Plugin | Use Case |
|---|---|
| Plug-in for Windows | Windows filesystems, SQL Server |
| Plug-in for SQL Server | SQL Server databases (VSS-based) |
| Plug-in for Oracle | Oracle DB on Linux/Windows |
| Plug-in for SAP HANA | SAP HANA databases |
| Plug-in for VMware vSphere | VMware VMs and datastores |
| Plug-in for UNIX | Linux filesystems |

```bash
# Windows — restart plugin service
Restart-Service -Name "SnapCenter Plug-in for Windows"

# Linux — restart plugin service
/opt/NetApp/snapcenter/scc/bin/scc restart
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Service 'SnapCenter Plug-in for Windows' cannot be found on the computer.`** — Verify the exact service name with `Get-Service | grep SnapCenter` and use the correct display name.
    **`/opt/NetApp/snapcenter/scc/bin/scc: No such file or directory`** — Confirm SnapCenter plugin is installed at `/opt/NetApp/snapcenter/` and check the correct binary path with `find /opt/NetApp -name scc -type f`.
---

## See also

- [Snapcenter — Design Standards](../design-standards/)
- [Snapcenter — Integrations](../integrations/)
- [Snapcenter — Deploy](../../deploy/)
