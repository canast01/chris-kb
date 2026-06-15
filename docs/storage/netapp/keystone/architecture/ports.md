---
tags:
  - keystone
  - netapp
  - networking
  - firewall
  - ports
  - storage-as-a-service
---
# NetApp Keystone — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for NetApp Keystone (Storage as a Service). Keystone deploys NetApp hardware on-premises managed by NetApp. The Keystone Collector appliance handles metering and telemetry upload. Data access protocols are the same as the underlying ONTAP or StorageGRID system.

*Applies to: NetApp Keystone STaaS*
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
│    AFF                = All Flash FAS; ONTAP-based NVMe/SSD array used for Extreme and Performance t  │
│    FAS                = Fabric Attached Storage; ONTAP hybrid HDD/SSD for Standard service level      │
│    StorageGRID        = NetApp S3 object storage; Object service level in Keystone subscriptions      │
│    AutoSupport        = ONTAP telemetry relay; sends call-home data and log bundles to NetApp         │
│    Service request    = NetApp SR; support ticket opened via mysupport.netapp.com portal              │
│    SKU                = Keystone service SKU identifies the service level and raw or usable capacity  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## How It Works

Keystone is a NetApp-managed STaaS offering using the same ONTAP / StorageGRID hardware as standard NetApp deployments. On-premises components include a **Keystone Collector** VM that measures consumed capacity and uploads usage data to NetApp.

## Keystone Collector (Outbound — Required)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Keystone Collector appliance | keystone.netapp.com, aiqum.netapp.com | Capacity metering, usage reporting, and entitlement validation |
| 443 | TCP | Keystone Collector appliance | ONTAP cluster management LIF | Collector → ONTAP API (capacity collection via AIQUM / Active IQ Unified Manager) |

## Admin Access (Keystone Portal — SaaS)

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | keystone.netapp.com | Admin browser — Keystone service dashboard, capacity reports, SLA tracking |

## Data Access Protocols (Same as Underlying Storage)

Keystone uses ONTAP or StorageGRID hardware with identical data protocols:

| Underlying System | Relevant Ports Page |
|---|---|
| ONTAP (NAS/SAN/NVMe) | [NetApp ONTAP — Ports](../../ontap/architecture/ports/) |
| StorageGRID (Object) | S3 443 / 9000 inbound from clients |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Keystone Collector | keystone.netapp.com | 443 | Metering upload — required for STaaS billing |
| Keystone Collector | ONTAP mgmt LIF | 443 | Capacity data collection |
| Admin browsers | keystone.netapp.com | 443 | SaaS portal |
| Client hosts | ONTAP data LIFs | Per protocol | Same as ONTAP standard ports |

## Verify

```bash
# From Keystone Collector VM — test NetApp portal connectivity
curl -sk -o /dev/null -w "%{http_code}" https://keystone.netapp.com/

# From Keystone Collector — test ONTAP management API
curl -sk -o /dev/null -w "%{http_code}" https://<ontap-mgmt-lif>/api/cluster

# Check Keystone Collector service status
systemctl status keystone-collector
```

## See also

- [NetApp Keystone — Architecture](how-it-works/)
- [NetApp ONTAP — Ports](../../ontap/architecture/ports/)
- [NetApp SnapCenter — Ports](../../snapcenter/architecture/ports/)
