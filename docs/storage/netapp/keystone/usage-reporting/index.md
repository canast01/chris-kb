---
tags:
  - netapp
---
# Keystone Usage Reporting

<div class="kb-summary">
Keystone Usage Reporting reference covering BlueXP Digital Wallet, Keystone Collector, Monthly Consumption Reports, Identifying High-Consuming Volumes (ONTAP CLI), Reporting Discrepancies and 1 more sections.
</div>
```text
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


## BlueXP Digital Wallet

Primary source for Keystone consumption reporting:

1. Log in to **BlueXP** (console.bluexp.netapp.com)
2. Navigate to **Digital Wallet → Keystone Subscriptions**
3. Select your subscription to view:
   - Committed capacity per service level
   - Consumed (logical) capacity per service level
   - Burst usage and burst limits
   - Month-to-date consumption trend

## Keystone Collector

The Keystone Collector is a virtual appliance deployed on-premises that collects and transmits consumption telemetry to NetApp:

```bash
# SSH to the Keystone Collector appliance
ssh admin@<collector_ip>

# Check collector service status
systemctl status keystone-collector

# View last collection run
journalctl -u keystone-collector --since "1 hour ago"
```

If the collector is offline, NetApp cannot generate accurate invoices — restore connectivity promptly.

## Monthly Consumption Reports

- Reports are generated monthly by NetApp
- Available in BlueXP Keystone dashboard before invoice generation
- Review consumption report against committed capacity before month-end
- If burst consumption is unexpected, identify the source before the invoice is finalized

## Identifying High-Consuming Volumes (ONTAP CLI)

```bash
# List volumes sorted by used capacity
volume show -vserver * -fields size,used,percent-used | sort -k4 -nr

# Identify volumes in burst service levels
qos statistics volume show
```

## Reporting Discrepancies

If the consumption report shows unexpected usage:

1. Compare ONTAP volume usage with Keystone report
2. Check for any large snapshots or recently provisioned volumes
3. Engage the Keystone Success Manager via the BlueXP support portal
4. Discrepancies must be raised before the invoice is finalized

## Key Metrics

| Metric | Where to Find | Normal |
|---|---|---|
| Committed capacity | BlueXP Digital Wallet | Contractual baseline |
| Burst usage | BlueXP Digital Wallet | 0 (or expected seasonal) |
| Collector health | Collector appliance status | Running, no errors |
| Telemetry latency | Last collection timestamp | Within last 24 hours |
