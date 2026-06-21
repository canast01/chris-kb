---
tags:
  - architecture
  - dell
---
# APEX Storage as a Service — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Use Cases, How It Works, Underlying Platforms, Best Practices.

*Applies to: APEX Storage-as-a-Service*
</div>
![APEX Storage as a Service — How It Works](../../../../assets/storage-dell-apex-storage-as-a-service-architecture-how-it-w.svg)




## Overview

Dell APEX Storage as a Service (STaaS) is a consumption-based storage model where Dell provisions, owns, and manages the physical infrastructure on-premises at the customer site. Capacity is metered monthly based on committed and burst usage, billed through the APEX Console. The underlying platforms are PowerStore, PowerScale, or PowerFlex, managed by Dell — the customer interacts primarily with the APEX Console or REST API for visibility, capacity requests, and billing reporting.

## Use Cases

| Use Case |
|---|
| Organisations that want on-premises storage economics without capital expenditure or operational management overhead |
| Environments requiring predictable $/TiB subscription pricing with burst capacity headroom |
| Multi-platform environments (block, file, object) under a single consumption agreement |
| IT teams that want to outsource hardware lifecycle management (firmware, hardware replace, capacity adds) to Dell |
| Capacity planning scenarios where future growth is uncertain and over-provisioning risk needs to be avoided |

## How It Works

Dell installs and owns the physical hardware. A Secure Connect Gateway (SCG) appliance at the customer site relays telemetry to Dell's cloud backend for metering and health monitoring. The APEX Console tracks consumed vs. committed capacity. Burst capacity above the committed tier is billed at an incremental per-TiB rate at the end of each billing period.

```mermaid
graph TB
  CUST["Customer\n(requests capacity\nvia APEX Console)"]
  CONSOLE["APEX Console\nOrder management\nSLA dashboard\nBilling portal"]
  DELL["Dell Operations\nProvisions hardware\non-site or Dell colo\n(FSE installs rack/cable)"]
  HW["Dell-managed Hardware\n(PowerStore / PowerScale\n/ PowerFlex)\nFirmware lifecycle managed\nby Dell"]
  SVC["APEX Storage Service\nBlock · File · Object\nmetered capacity"]
  WORK["Customer Workloads\n(VMs, containers,\ndatabases, files)"]
  BILL["Metered Billing\nCommitted fee\n+ burst overage\nmonthly invoice"]
  LIFECYCLE["Dell Proactive\nHardware Lifecycle\nfirmware updates\npart replacement\ncapacity expansion"]

  CUST -->|"capacity order\nvia web portal"| CONSOLE
  CONSOLE -->|"provision request\nto field services"| DELL
  DELL -->|"installs and initialises\nhardware on-site"| HW
  HW -->|"storage service\nexposed to customer"| SVC
  SVC -->|"volumes / shares\nmounted by hosts"| WORK
  WORK -->|"actual consumption\ntelemetry via SCG"| CONSOLE
  CONSOLE -->|"monthly invoice\ncommitted + burst"| BILL
  BILL -->|"billing data informs\ncapacity planning"| CUST
  HW -->|"SupportAssist telemetry\nproactive alerts"| LIFECYCLE
  LIFECYCLE -->|"hardware changes\ncoordinated with customer"| DELL

  classDef blue fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef green fill:#15803d,stroke:#166534,color:#fff
  classDef amber fill:#b45309,stroke:#92400e,color:#fff
  classDef purple fill:#7c3aed,stroke:#6d28d9,color:#fff

  class CUST,WORK blue
  class DELL,HW,LIFECYCLE green
  class CONSOLE,BILL amber
  class SVC purple
```

## Underlying Platforms

| Platform | Storage Type | Use Case |
|---|---|---|
| PowerStore | Block (NVMe) and file | General-purpose primary storage |
| PowerScale | NAS (scale-out NFS/SMB) | Unstructured data and file workloads |
| PowerFlex | Block (software-defined) | High-performance and Kubernetes workloads |

## Best Practices

| Recommendation | Detail |
|---|---|
| Keep Secure Connect Gateway appliances highly available | Deploy two SCG appliances for redundancy — loss of SCG connectivity causes telemetry gaps and may trigger alerts |
| Monitor committed vs. consumed capacity monthly | Request tier increases at least 30 days before hitting the committed threshold to avoid burst pricing |
| Use the APEX REST API to build automated capacity reports | Feed into internal capacity planning tools |
| Review APEX Console alerts daily | Infrastructure issues are Dell's responsibility to remediate but you need to confirm SLA compliance |
| Document subscription details in a runbook | Subscription ID, contract end date, committed tier, and burst thresholds for on-call staff |

---

## See also

- [Apex Storage As A Service — Design Standards](design-standards/)
- [Apex Storage As A Service — Integrations](integrations/)
