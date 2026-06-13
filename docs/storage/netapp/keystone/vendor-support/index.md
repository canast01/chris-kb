---
tags:
  - netapp
---
# NetApp Keystone Vendor Support

<div class="kb-summary">
NetApp Keystone Vendor Support reference covering Keystone Success Manager, Support Portal, Opening a Case, Information to Collect, SLA Tiers and 1 more sections.

*Applies to: Keystone STaaS*
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


## Keystone Success Manager

Every Keystone subscription includes a dedicated Keystone Success Manager (KSM). The KSM is the primary NetApp contact for:

- Service issues and escalations beyond standard support case handling
- Capacity planning discussions and subscription amendment requests
- Monthly consumption review and billing query resolution
- Renewal planning and term negotiation
- Onboarding of new service tiers or StorageGRID object capacity

Contact the KSM directly for issues that require commercial or service-level attention, in addition to or instead of opening a technical support case.

## Support Portal

- **Technical support portal:** [https://support.netapp.com](https://support.netapp.com) — for infrastructure issues, Collector problems, and ONTAP/StorageGRID issues on Keystone-managed hardware
- **Keystone-specific issues:** raise via the KSM or open a Keystone ticket in the BlueXP portal
- Ensure your NetApp SSO account is linked to your company's support entitlement before opening cases

## Opening a Case

Required information when opening a Keystone support case:

- Keystone subscription ID (from BlueXP Keystone dashboard)
- Affected service tier (Extreme, Premium, Standard, Object)
- Keystone Collector version
- Clear description of the symptom and business impact
- Whether the issue is a billing discrepancy, a performance SLA breach, a Collector issue, or a platform infrastructure issue

## Information to Collect

Before contacting support, gather:

- Screenshot of the BlueXP Keystone dashboard showing the affected subscription and tier
- Keystone Collector VM status (`systemctl status keystone-collector`)
- Keystone Collector logs (`journalctl -u keystone-collector -n 200`)
- Consumption report for the affected billing period (download from BlueXP digital wallet)
- ONTAP EMS log extract if the issue is related to storage platform performance

## SLA Tiers

| Priority | Response Time | Scope |
|---|---|---|
| P1 | 4 hours | Service unavailable, data inaccessible, SLA guarantee breached |
| P2 | 8 hours | Degraded performance or partial service impact |
| P3 | Next business day | Non-critical issue, billing query, configuration change |

Keystone SLA guarantees 99.9999% (six nines) availability for the infrastructure service. SLA breaches are remediated by NetApp SRE, including hardware replacement if required. Infrastructure response and remediation are included in the subscription — no additional charges for hardware repair or replacement.

## Escalation

- Escalate persistent infrastructure or SLA issues to the KSM for routing to the Keystone Engineering team
- For billing or commercial disputes, escalate via the KSM to the NetApp account team
- Executive escalation for unresolved critical issues is available via the NetApp account executive
- Request TAM (Technical Account Manager) engagement for complex hybrid deployments combining Keystone STaaS, Cloud Volumes ONTAP, and BlueXP data services
