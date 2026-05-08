# Keystone — Components

> Part of the [Keystone Architecture](../) reference.

---

## Components

- **NetApp-managed storage controllers** — AFF/FAS/StorageGRID hardware; NetApp owns, installs, and manages; customer does not purchase or depreciate the hardware
- **Keystone Collector** — VM agent deployed on the customer's infrastructure; collects consumption data from ONTAP and StorageGRID; forwards telemetry to NetApp for billing
- **BlueXP / ActiveIQ Digital Advisor** — web portal at https://activeiq.netapp.com; Keystone dashboard shows committed vs. consumed capacity, burst status, and SLA compliance per tier
- **Keystone Success Manager (KSM)** — dedicated NetApp contact for the subscription; handles capacity planning, billing queries, escalations, and renewal

---

## Service Levels

NetApp Keystone offers tiered service levels based on performance characteristics. Each service level is defined by IOPS and latency targets per TB.

| Service Level | Workload Type | IOPS/TB | Latency Target |
|---|---|---|---|
| Extreme | Latency-sensitive (databases, VDI) | Up to 12,000 | < 1 ms |
| Premium | High-performance mixed workloads | Up to 4,000 | < 1 ms |
| Performance | General purpose mixed I/O | Up to 2,000 | < 2 ms |
| Value | Archival, backup, infrequent access | Up to 64 | < 17 ms |

> Exact service level names and IOPS targets vary by region and contract version — always refer to your subscription order form.

### Viewing Assigned Service Levels

From **BlueXP → Keystone → Dashboard**:
- **Subscriptions** tab — shows each subscription with committed and burst capacity per service level
- **Digital Wallet** — monthly consumption per service level

### Burst Capacity

- Each service level allows burst consumption above committed capacity
- Burst is charged at a higher per-TB rate
- Burst limits are defined in the subscription agreement
- Monitor burst usage via BlueXP Digital Wallet before month-end

### QoS Policy Mapping (ONTAP CLI)

Keystone service levels map to ONTAP QoS adaptive policies:

```bash
qos adaptive-policy-group show
```

Each Keystone service level corresponds to a named adaptive QoS policy group applied to the volumes.
