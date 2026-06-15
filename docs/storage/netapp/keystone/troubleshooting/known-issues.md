---
tags:
  - troubleshooting
  - keystone
  - netapp
  - known-issues
---
# NetApp Keystone — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Keystone STaaS bugs, error codes, and workarounds. Most Keystone issues relate to the Keystone Collector appliance or portal connectivity — underlying ONTAP storage issues are tracked separately.

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


## Before you begin

- Keystone Collector logs: `journalctl -u keystone-collector` on the Collector VM.
- Portal access issues should be reported to NetApp Keystone support at `keystone.netapp.com`.
- ONTAP-layer issues (NFS, SMB, iSCSI, SnapMirror) are tracked in [ONTAP Known Issues](../../ontap/troubleshooting/known-issues/).

## Keystone Collector

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Collector not uploading metrics: `Connection refused to keystone.netapp.com` | Keystone | Port 443 blocked from Collector to keystone.netapp.com | Verify TCP 443 outbound from Collector VM; check proxy settings if applicable | N/A |
| `ONTAP API authentication failed` in Collector | Keystone | Collector service account credentials expired on ONTAP | Rotate password; update Collector config: `keystone-collector config update` | N/A |
| Capacity usage not matching Keystone portal values | Keystone | Collector polling lag (up to 24h for portal sync) | Wait 24 hours; if mismatch persists after 48h, raise support ticket | N/A |

## Keystone Portal

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Portal shows `No data` for recently onboarded cluster | Keystone | Initial baseline collection takes 24–48 hours | Wait 48 hours after Collector setup before raising issue | N/A |
| Burst billing alert unexpected | Keystone | Thin provisioning over-allocation exceeds committed capacity | Review actual consumed capacity; compare with committed Keystone tier in portal | N/A |

## See also

- [NetApp Keystone — Common Issues](common-issues.md)
- [NetApp ONTAP — Known Issues](../../ontap/troubleshooting/known-issues/)
