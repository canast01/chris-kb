---
tags:
  - netapp
---
# Keystone Service Levels

<div class="kb-summary">
NetApp Keystone offers tiered service levels based on performance characteristics. Each service level is defined by IOPS and latency targets per TB.

*Applies to: Keystone STaaS*
</div>

## Standard Service Levels

| Service Level | Workload Type | IOPS/TB | Latency Target |
|---|---|---|---|
| Extreme | Latency-sensitive (databases, VDI) | Up to 12,000 | < 1 ms |
| Premium | High-performance mixed workloads | Up to 4,000 | < 1 ms |
| Performance | General purpose mixed I/O | Up to 2,000 | < 2 ms |
| Value | Archival, backup, infrequent access | Up to 64 | < 17 ms |

> Exact service level names and IOPS targets vary by region and contract version — always refer to your subscription order form.

## Viewing Assigned Service Levels

From **BlueXP → Keystone → Dashboard**:
- **Subscriptions** tab — shows each subscription with committed and burst capacity per service level
- **Digital Wallet** — monthly consumption per service level

## Burst Capacity

- Each service level allows burst consumption above committed capacity
- Burst is charged at a higher per-TB rate
- Burst limits are defined in the subscription agreement
- Monitor burst usage via BlueXP Digital Wallet before month-end

## Changing Service Levels

To change a volume's service level (move data between tiers):
- Raise a request with the Keystone Success Manager
- NetApp performs the tiering via QoS policy changes at the ONTAP level
- Service level changes may take time depending on data volume

## QoS Policy Mapping (ONTAP CLI)

Keystone service levels map to ONTAP QoS adaptive policies. To see:

```bash
qos adaptive-policy-group show
```

Each Keystone service level corresponds to a named adaptive QoS policy group applied to the volumes.

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Unexpected burst charges | Burst usage in BlueXP | Identify volumes exceeding tier |
| Workload latency above target | QoS policy applied | Verify correct service level |
| Service level not matching SLA | Subscription order form | Engage Keystone Success Manager |
