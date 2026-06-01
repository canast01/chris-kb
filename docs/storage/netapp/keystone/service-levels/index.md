# Keystone Service Levels


<div class="kb-summary">
NetApp Keystone offers tiered service levels based on performance characteristics. Each service level is defined by IOPS and latency targets per TB.
</div>
```
┌─────────────────────────────────────────── NetApp Keystone ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Keystone: Storage as a Service subscription for on-prem NetApp arrays             │   │
│   │                             Protocols: NFS · iSCSI · FC · S3 · SMB                            │   │
│   │                            Management: Keystone dashboard (BlueXP)                            │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Hardware          │  │       AFF/FAS on-prem       │  │         NetApp-owned        │   │
│   │        Service level        │  │       Extreme/Perf/Std      │  │         Latency SLA         │   │
│   │          Collector          │  │         Telemetry VM        │  │        ONTAP polling        │   │
│   │          Dashboard          │  │            BlueXP           │  │       Usage visibility      │   │
│   │           Billing           │  │       Committed+burst       │  │       Monthly invoice       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │Keystone Collecto │  Usage metering  │     ONTAP REST    │ Service account  │    On-prem VM    │   │
│   │      BlueXP      │   SaaS portal    │       HTTPS       │    OAuth2/SSO    │   NetApp SaaS    │   │
│   │   AFF Extreme    │  NVMe perf tier  │    FC/iSCSI/NFS   │  Kerberos/CHAP   │  Sub-ms latency  │   │
│   │   AutoSupport    │ Telemetry relay  │       HTTPS       │   Certificate    │    Call-home     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NetApp AFF/FAS arrays on-prem · Keystone Collector VM · BlueXP cloud portal              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Keystone           = NetApp STaaS; fixed-term subscription for ONTAP or StorageGRID capacity       │
│    Service level      = tiered SLA: Extreme (NVMe), Performance (SSD), Standard (HDD)                 │
│    Committed capacity = minimum contracted TiB; billed monthly even if below threshold                │
│    Burst capacity     = usage above committed; available without pre-ordering; billed monthly         │
│    Keystone Collector = on-prem VM that gathers usage metrics and sends to NetApp Keystone            │
│    BlueXP             = NetApp SaaS control plane; Keystone dashboard, DRaaS, and cloud integrations  │
│    AFF                = All Flash FAS; ONTAP-based NVMe/SSD array used for Extreme and Performance ...│
│    FAS                = Fabric Attached Storage; ONTAP hybrid HDD/SSD for Standard service level      │
│    StorageGRID        = NetApp S3 object storage; Object service level in Keystone subscriptions      │
│    AutoSupport        = ONTAP telemetry relay; sends call-home data and log bundles to NetApp         │
│    Service request    = NetApp SR; support ticket opened via mysupport.netapp.com portal              │
│    SKU                = Keystone service SKU identifies the service level and raw or usable capacity  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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
