# Evergreen — Overview

> Part of the [Evergreen Architecture](../) reference.

---

## Overview

Evergreen is Pure Storage's hardware subscription model for the FlashArray platform (//X, //C, and //E series). Rather than purchasing hardware outright, customers subscribe to a capacity and performance tier, with controller hardware refreshes, Purity software upgrades, and support included in the subscription cost. The defining principle is no forklift upgrades: when controllers reach end of generation, Pure replaces them non-disruptively while data remains on the existing NVMe drive shelf — hosts stay connected and I/O continues during the swap.

Evergreen spans two primary tiers:

- **Evergreen//Forever** — base subscription; includes non-disruptive controller refresh (Ever Modern) every three years, all Purity software upgrades, and support
- **Evergreen//Flex** — adds non-disruptive capacity and blade swap flexibility for FlashBlade; allows adding, removing, or swapping storage media without disruption

Evergreen//One (STaaS consumption model) is covered in a separate section of this KB.

## Controller Refresh Model

```mermaid
graph LR
  A["FlashArray Gen N\n(current)"] -->|"Non-disruptive\nhardware swap"| B["FlashArray Gen N+1\n(upgraded blades/controllers)"]
  B -->|"Evergreen//Forever"| C["FlashArray Gen N+2"]
  A & B & C --> DATA[("Data — always online\nno migration required")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  class A,B,C ctrl
  class DATA store
```

## HA Topology

FlashArray under Evergreen runs active-active dual controllers. Both controllers handle read and write I/O simultaneously; on controller failure, all I/O shifts to the surviving controller within milliseconds with no host-visible interruption (assuming redundant host paths).

**Non-Disruptive Controller Refresh (NDCR)** — the Ever Modern process — allows Pure to replace one controller at a time while the other continues serving I/O. The process is:

1. Failover all I/O to controller 1
2. Remove controller 0, install new-generation controller 0
3. Resync controller 0, failover I/O to controller 0
4. Remove controller 1, install new-generation controller 1
5. Resync controller 1, restore active-active operation

The entire process is non-disruptive to hosts provided multipathing is correctly configured on all connected hosts.

## Connectivity

FlashArray supports multiple host connectivity protocols:

| Protocol | Use Case |
|---|---|
| Fibre Channel (FC) | Block storage for VMware, bare-metal, and mission-critical applications requiring dedicated SAN fabric |
| iSCSI | Block storage over IP networks; lower cost than FC with good performance at 10/25GbE |
| NVMe/FC | NVMe over Fibre Channel for lowest latency block workloads; requires NVMe-capable HBAs |
| NVMe/RoCE | NVMe over RDMA Converged Ethernet; high-throughput, low-latency block over 25/100GbE |
| NVMe/TCP | NVMe over standard TCP/IP; broadest compatibility without requiring specialised NICs or fabric |

**Replication**

- **ActiveCluster** — synchronous replication between two FlashArray systems; RPO=0, host-transparent failover via a mediator quorum service; requires stretched fabric or IP connectivity between sites
- **Async replication** — snapshot-based asynchronous replication to a remote FlashArray with configurable RPO intervals

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
