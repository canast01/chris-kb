# Evergreen — Components

> Part of the [Evergreen Architecture](../) reference.

---

> This page is a stub. Core components for the Evergreen FlashArray platform will be documented here, covering controller hardware, DirectFlash Modules, NVMe drive shelves, Purity//FA OS, and subscription tier comparison.

## Key Components

**Controllers**

Each FlashArray runs a pair of active-active controllers. The controller pair handles all I/O, runs the Purity//FA operating system, and manages the NVMe drive shelf. Controllers are replaced as part of the Ever Modern refresh cycle without data migration.

**DirectFlash Modules (DFMs)**

Pure's proprietary NVMe SSDs optimised for the Purity storage stack. DFMs remain in place during controller refreshes and across subscription generations — the subscription model is designed around the longevity of the drive shelf.

**NVMe Drive Shelves**

Expansion shelves attach to the primary controller pair to provide additional capacity. Shelves are supported across controller generations, enabling non-disruptive capacity growth throughout the subscription.

**Subscription Tiers**

| Tier | Description |
|---|---|
| Evergreen//Forever | Controller refresh included; upgrades to current-generation controllers at each refresh cycle |
| Evergreen//Flex | All Forever benefits plus non-disruptive media and capacity changes for FlashBlade deployments |

## Sizing Guidelines

Evergreen subscriptions are sized in TiB of usable capacity after data reduction. Pure provides a **data reduction guarantee**: if actual data reduction falls below the contracted ratio, Pure provides additional capacity at no charge.

| Series | Target Workload | Performance Profile |
|---|---|---|
| FlashArray//X | High-performance OLTP, VDI, databases | Highest IOPS and lowest latency; NVMe throughout |
| FlashArray//C | Capacity-optimised workloads, secondary storage, backups | Higher TiB per £ with QLC media; good for large sequential workloads |
| FlashArray//E | Archive and bulk cold storage at flash economics | Lowest cost per TiB; suitable for data that requires fast restore but low access frequency |

Sizing inputs: expected usable TiB (post-reduction), peak IOPS and bandwidth requirements, host protocol, and replication topology. Engage the Pure account team or use Pure1 capacity planning to model growth over the subscription term.
