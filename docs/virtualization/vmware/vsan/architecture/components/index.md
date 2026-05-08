# vSAN — Components

## Core Components

| Component | Description |
|---|---|
| **Disk Group** | Unit of storage on each host: one cache device + one or more capacity devices (OSA). ESA uses NVMe only with no separate cache tier. |
| **CLOM** | Cluster Level Object Manager — policy compliance, placement decisions, and triggering resyncs when policy is violated. |
| **DOM** | Distributed Object Manager — handles I/O for each vSAN object; coordinates reads and writes across hosts. |
| **LSOM** | Local Log-Structured Object Manager — manages on-disk layout within disk groups. |
| **CMMDS** | Cluster Monitoring Membership Directory Service — tracks cluster membership and health metadata. |
| **vSAN Datastore** | The logical datastore namespace visible to vCenter and all cluster hosts. |
| **vSAN Witness** | Lightweight host or appliance holding only metadata for 2-node clusters — tiebreaker arbitration. |

## Disk Group Design

**Original Storage Architecture (OSA) — vSAN 6.x / 7.x:**
- 1 cache SSD + up to 7 capacity drives per disk group
- Up to 5 disk groups per host
- All-Flash: cache tier used for write buffering only
- Hybrid: cache tier used for both read caching and write buffering

**Express Storage Architecture (ESA) — vSAN 8.0+:**
- NVMe-only; no separate cache tier
- Each NVMe contributes directly to capacity with inline compression
- Minimum 4 hosts required; higher throughput and lower latency than OSA

## FTT and RAID Policies

| FTT | RAID Method | Minimum Hosts | Space Overhead |
|---|---|---|---|
| 1 | RAID-1 (Mirroring) | 3 | 2x |
| 1 | RAID-5 (Erasure Coding) | 4 | 1.33x |
| 2 | RAID-6 (Erasure Coding) | 6 | 1.5x |
| 2 | RAID-1 (Mirroring) | 5 | 3x |
| 3 | RAID-1 (Mirroring) | 7 | 4x |

Erasure Coding (RAID-5/6) is supported on All-Flash and ESA only.

## Stretched Cluster

A vSAN Stretched Cluster spans two active data sites with a third witness site:

- **Site A and Site B:** Both active, hold RAID-1 mirrors of each VM object
- **Witness Site:** Holds only metadata; acts as tiebreaker for split-brain prevention

Network requirements:

| Link | Maximum Latency |
|---|---|
| Site A to Site B | < 5 ms RTT |
| Data sites to Witness | < 200 ms RTT |
