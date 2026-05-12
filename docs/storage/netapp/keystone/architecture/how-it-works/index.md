# Keystone — How It Works

## Overview

NetApp Keystone is a Storage as a Service (STaaS) subscription that delivers on-premises NetApp hardware — AFF/FAS for block and file, StorageGRID for object — on an OpEx consumption model. NetApp installs, owns, and manages the hardware at the customer's data center or colocation facility. The customer commits to a minimum capacity per service tier and pays for committed capacity plus burst usage above the commitment. A Keystone Collector agent reports consumption telemetry to NetApp for billing.

## STaaS Consumption Model

```mermaid
graph TB
  ONTAP["NetApp ONTAP\n(on-premises / colocation)"] -->|"telemetry"| KS["NetApp Keystone\n(STaaS portal)"]
  KS --> COMMIT["Committed Capacity Tier"]
  KS --> BURST["Burst Capacity\n(on-demand)"]
  KS --> BILL["Monthly Billing"]
  ADMIN(["Customer Admin"]) -->|"portal"| KS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ONTAP ctrl
  class KS,COMMIT,BURST,BILL cloud
  class ADMIN host
```

## Service Tiers

| Tier | Protocol / Platform | Use Case |
|---|---|---|
| Extreme | NVMe-AF (all-flash NVMe) | Latency-sensitive databases, high-IOPS transactional workloads |
| Premium | AFF (all-flash SAS/NVMe) | Mixed workloads, virtualization, general-purpose high-performance |
| Standard | FAS (hybrid or capacity flash) | File storage, backup targets, less latency-sensitive workloads |
| Object | StorageGRID | Unstructured data, backups, archives, S3-compatible object storage |

## Components

| Component | Description |
|---|---|
| NetApp-managed storage controllers | AFF/FAS/StorageGRID hardware; NetApp owns, installs, and manages; customer does not purchase or depreciate |
| Keystone Collector | VM agent on the customer's infrastructure; collects consumption data from ONTAP and StorageGRID; forwards telemetry to NetApp for billing |
| BlueXP / ActiveIQ Digital Advisor | Web portal at `activeiq.netapp.com`; Keystone dashboard shows committed vs. consumed capacity, burst status, and SLA compliance per tier |
| Keystone Success Manager (KSM) | Dedicated NetApp contact; handles capacity planning, billing queries, escalations, and renewal |

## Service Level Performance Targets

| Service Level | IOPS/TB | Latency Target | Workload Type |
|---|---|---|---|
| Extreme | Up to 12,000 | < 1 ms | Latency-sensitive (databases, VDI) |
| Premium | Up to 4,000 | < 1 ms | High-performance mixed workloads |
| Performance | Up to 2,000 | < 2 ms | General-purpose mixed I/O |
| Value | Up to 64 | < 17 ms | Archival, backup, infrequent access |

> Exact service level names and IOPS targets vary by region and contract version — always refer to your subscription order form.

## Connectivity

Storage protocols are identical to the underlying platform: NFS, SMB/CIFS, iSCSI, FC, and S3 (StorageGRID). The Keystone Collector VM requires outbound HTTPS (port 443) to `keystone.netapp.com` for telemetry reporting — no inbound ports are required.

## Capacity Model

- **Committed capacity** — minimum monthly capacity contracted per service tier; billed whether used or not
- **Burst capacity** — headroom above committed capacity up to a defined burst limit; billed at a higher per-TB rate when consumed
- **True-up cadence** — monthly; Collector consumption report is reconciled and the invoice reflects committed plus burst usage
- Committed capacity can be increased mid-term but cannot be decreased; plan initial sizing conservatively and use burst for growth headroom

## QoS Policy Mapping

Keystone service levels map to ONTAP QoS adaptive policies:

```bash
# View assigned adaptive QoS policy groups
qos adaptive-policy-group show
```

Each Keystone service level corresponds to a named adaptive QoS policy group applied to volumes — e.g., `extreme-ks`, `premium-ks`, `standard-ks`.

## Capacity Management Thresholds

| Threshold | Action |
|---|---|
| 70% of committed capacity | Internal review; forecast growth timeline |
| 80% of committed capacity | Alert triggered; begin capacity amendment process |
| 90% of committed capacity | Burst activates; escalate to Keystone Success Manager |
| Burst limit reached | Further provisioning blocked; emergency amendment required |

```bash
# Request committed capacity increase at least 60 days before anticipated growth
# Monitor burst usage via BlueXP Digital Wallet before month-end
```
