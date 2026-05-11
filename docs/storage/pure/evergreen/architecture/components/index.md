# Evergreen — Components

> Part of the [Evergreen Architecture](../) reference.

---

## Controller Pair (CT0 / CT1)

FlashArray runs dual active-active controllers. Both controllers handle read and write I/O simultaneously. On single-controller failure, all I/O shifts to the surviving controller within milliseconds.

| Property | Detail |
|---|---|
| Controller designation | CT0 (primary) / CT1 (secondary) — symmetric; neither is passive |
| I/O model | Active-active — both process host I/O simultaneously |
| Failover time | < 30 ms for host-transparent failover (with multipathing) |
| Controller interconnect | NVLink or PCIe fabric (internal) for cache coherency and NVRAM mirroring |
| Management interface | Eth0 on each CT — distinct management IPs; VIP used for shared management access |

```bash
# Check controller status from FlashArray CLI
ssh pureuser@<flasharray-ip>
purehw list --type ct

# Example output:
# Name  Status    Model         Temperature  Voltage
# CT0   Healthy   FA-X70R4      38°C         OK
# CT1   Healthy   FA-X70R4      37°C         OK
```

## DirectFlash Modules (DFM)

DirectFlash Modules are Pure Storage's proprietary NVMe flash storage units. Unlike commodity SSDs, they expose raw NAND flash directly to the Purity OS, allowing Pure's software to manage wear levelling, garbage collection, and data placement at the array level.

| Property | Detail |
|---|---|
| Interface | NVMe (PCIe Gen 4 or Gen 5 depending on platform generation) |
| Form factor | 2.5" U.2 or E3 enterprise form factor |
| Capacity tiers | 4 TB, 12 TB, 24 TB, 48 TB (varies by FlashArray model) |
| RAID equivalent | Purity RAID-3D (triple parity) — tolerates concurrent multi-DFM failures |
| Controller awareness | DFMs are owned by the array, not individual controllers — both CTs access all DFMs |
| Hot-swap | Yes — non-disruptive replacement under Evergreen support coverage |

```bash
# Check DFM status
purehw list --type drive

# Show only non-healthy drives
purehw list --type drive | grep -v Healthy

# Check drive space usage
purearray list --space
```

## NVMe Shelves (Expansion Shelves)

Expansion shelves add raw DFM capacity without adding controllers. Shelves attach via SAS or NVMe-oF to the primary controller chassis.

| Model | Max shelves | Drive slots | Notes |
|---|---|---|---|
| //X | Up to 3 shelves | 24 per shelf | SAS-attached DFM expansion |
| //XL | Up to 9 shelves | 24 per shelf | Higher capacity ceiling |
| //C | Up to 3 shelves | Cold-tier DFMs | QLC flash for cost-optimised workloads |

```bash
# List all chassis and shelves
purehw list --type shelf

# List drives by location (chassis:slot)
purehw list --type drive | sort -k1
```

## Purity//FA Operating System

Purity//FA is the operating system running on both controllers. It provides the data management, replication, and protocol services.

| Component | Description |
|---|---|
| **Volume management** | Thin provisioning, snapshots, volume groups |
| **Data reduction** | Inline deduplication + compression (always-on, no configuration needed) |
| **Replication** | Async and sync (ActiveCluster) replication to remote arrays |
| **Protocol services** | FC, iSCSI, NVMe/FC, NVMe/RoCE, NVMe/TCP |
| **APIs** | REST API v1/v2; Pure1 cloud telemetry |
| **RBAC** | Local users, AD/LDAP integration, role-based access |

```bash
# Check Purity version
purearray list

# Check all running services
pureservice list

# Check replication connections
purearray list --connect
```

## Host Connectivity Ports

Each controller has a set of front-end host connectivity ports and back-end storage ports.

```bash
# List all ports and their status
pureport list

# Filter by protocol
pureport list | grep -i "FC\|iSCSI\|NVMe"

# Show port performance
pureport list --performance
```

| Port type | Protocol | Count (typical X70R4) |
|---|---|---|
| FC | 16/32 Gbps Fibre Channel | 4 per controller (8 total) |
| iSCSI / NVMe/TCP | 10/25 GbE | 4 per controller (8 total) |
| NVMe/RoCE | 25/100 GbE | Optional — addon card |
| Management | 1 GbE | 2 per controller (dedicated management) |

## NVRAM / Write Cache

Each controller contains NVRAM (non-volatile RAM), used as a write cache to acknowledge writes immediately while flushing to flash asynchronously.

| Property | Detail |
|---|---|
| NVRAM mirroring | Write acknowledged to NVRAM on CT0 AND CT1 before host ACK — write is safe even if one controller fails |
| Flush to DFM | NVRAM drained to DFM within seconds under normal operation |
| Battery / capacitor | Supercapacitor backed — maintains NVRAM contents through short power loss |
| Monitoring | Included in `purehw list` hardware health output |

```bash
# Check NVRAM component health
purehw list | grep -i nvram
```

## Component Health Summary

```bash
# Full hardware inventory and health
purehw list

# Summary of non-healthy components (should return nothing in a healthy array)
purehw list | grep -v "Healthy\|Name\|---"

# Alert-level view — any open hardware alerts
purealert list --flagged
```
