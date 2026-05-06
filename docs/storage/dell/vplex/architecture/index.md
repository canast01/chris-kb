# Dell VPLEX Architecture

## Overview

Dell VPLEX is a storage virtualisation and federation platform that presents unified virtual volumes to hosts from one or more heterogeneous backend storage arrays. VPLEX abstracts physical storage into virtual volumes, enabling live data mobility between arrays, active-active block storage access across sites, and non-disruptive migration without host changes. VPLEX is deployed as a set of director pairs, each running the GeoSynchrony software stack. Management is via the `vplexcli` command-line interface or Unisphere for VPLEX web GUI.

## Components

| Component | Description |
|---|---|
| VPLEX Director | The core processing unit; each director has front-end FC ports (to hosts), back-end FC ports (to storage arrays), and a write cache module |
| Director Pair | Two directors in a chassis share a common cache over a high-speed interconnect; a director pair is the minimum HA unit |
| Engine | A VPLEX chassis containing one or two director pairs |
| VPLEX VS2 | Single-cluster deployment (one or two engines at one site) for local virtualisation and data mobility |
| VPLEX Metro | Two-cluster deployment across two sites with synchronous cache mirroring (<5ms RTT); provides active-active access with zero RPO |
| VPLEX Geo | Two-cluster deployment for longer distances using asynchronous replication via RecoverPoint; for DR, not active-active |
| Witness | A lightweight VM deployed at a third site that acts as a tiebreaker for VPLEX Metro quorum decisions |
| VPLEX Management Server (VMS) | A VM that hosts the management console and `vplexcli`; does not participate in the data path |

## HA Topology

**Single site (VS2 / Local):**

- Director pairs provide N+1 redundancy within a site — one director can fail without interrupting I/O.
- Cache within a director pair is mirrored; losing one director does not lose write data.
- Backend arrays connect to both directors in a pair for multipath redundancy.

**Metro (active-active, two sites):**

- Distributed devices span both clusters; each site has a complete copy of the data (synchronous mirroring).
- Hosts at both sites access the same distributed device simultaneously with full read/write capability.
- If one cluster becomes unreachable, the Witness determines which cluster continues serving I/O (quorum). Without a Witness, a cluster partition causes both sites to suspend I/O.
- Inter-Cluster Link (ICL) carries write synchronisation traffic between sites; RTT must be ≤5ms for Metro.

**Geo (async, two sites):**

- Uses RecoverPoint for asynchronous replication; VPLEX Geo presents the volume on one site at a time.
- Not active-active; Geo is a DR configuration for sites beyond Metro RTT limits.

## Connectivity

| Layer | Protocol / Interface | Details |
|---|---|---|
| Host to VPLEX | Fibre Channel (8Gb/16Gb) | Hosts zone to VPLEX front-end FC ports; VPLEX presents virtual volumes to hosts |
| VPLEX to Backend Array | Fibre Channel (8Gb/16Gb) | VPLEX back-end FC ports zone to backend array ports; VPLEX discovers and claims storage volumes |
| Inter-Cluster Link (Metro) | 10GbE or 25GbE WAN / dark fibre | Carries synchronous write data between Metro clusters; requires ≤5ms RTT |
| Management | 1GbE management interface | VMS connects to directors for management; vplexcli connects to the VMS |

## Sizing Guidelines

| Parameter | Guidance |
|---|---|
| Virtual volume size | Maximum virtual volume size determined by GeoSynchrony version; check release notes |
| Write cache per director | Cache size is fixed per director model; do not exceed 70% cache utilisation under sustained write workloads |
| Backend IOPS budget | Sum of all virtual volume IOPS must not exceed the backend array's rated IOPS after accounting for RAID overhead |
| ICL bandwidth (Metro) | ICL bandwidth must exceed peak write throughput at either site; provision 2× expected write bandwidth for headroom |
| Director port count | Allocate front-end ports based on host count and bandwidth requirements; maintain port balance across directors within an engine |
| Consistency groups | One consistency group per multi-volume application; do not exceed documented CG limits per GeoSynchrony version |
