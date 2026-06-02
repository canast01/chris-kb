# NetApp Keystone

<div class="kb-summary">
NetApp Keystone STaaS knowledge base — architecture, operations, security, and troubleshooting for on-premises consumption-based storage subscriptions.
</div>

```text
┌─────────────────────────────────────────── NetApp Keystone ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         NetApp Keystone: Storage-as-a-Service; on-prem hardware; subscription billing         │   │
│   │         Service tiers: Extreme, Premium, Standard, Value — mapped to performance SLOs         │   │
│   │        Managed by NetApp Keystone Success Manager; hardware installed at customer site        │   │
│   │      Billing: committed capacity + burst; monthly invoicing via Active IQ Digital Advisor     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Customer orders -> NetApp installs ONTAP hardware -> consume file/block/object storage             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Service Levels       │  │          Management         │  │          Protocols          │   │
│   │        Extreme (NVMe)       │  │         Active IQ DA        │  │          NFS v3/v4          │   │
│   │        Premium (SSD)        │  │       Keystone Portal       │  │           SMB 2/3           │   │
│   │        Standard (SSD)       │  │         Success Mgr         │  │            iSCSI            │   │
│   │         Value (HDD)         │  │           REST API          │  │              FC             │   │
│   │        Burst headroom       │  │         AutoSupport         │  │          S3 object          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    NetApp owns hardware; customer owns data and workloads                                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Function     │       Owner       │       Tool       │      Notes       │   │
│   │     Hardware     │   ONTAP arrays   │       NetApp      │    Field svc.    │     On-prem      │   │
│   │    Management    │    Portal/API    │      Customer     │   Active IQ DA   │    Cloud SaaS    │   │
│   │    Monitoring    │   Health/perf    │       Shared      │   AutoSupport    │     Via KSM      │   │
│   │     Billing      │   Usage report   │       NetApp      │   Keystone UI    │     Monthly      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NetApp AFF/FAS nodes on-premises · customer network switches · 10/25 GbE or FC           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Keystone STaaS    = Storage as a Service from NetApp; on-prem hardware, cloud billing              │
│    Active IQ DA      = Digital Advisor; portal for capacity, usage, billing, and health               │
│    KSM               = Keystone Success Manager; NetApp point of contact for the service              │
│    Service level     = Predefined performance tier: Extreme/Premium/Standard/Value                    │
│    Committed cap.    = Minimum capacity contracted; billed monthly regardless of use                  │
│    Burst capacity    = Excess above committed; billed at burst rate per TB per month                  │
│    AFF               = All Flash FAS; NetApp all-NVMe or all-SSD ONTAP storage arrays                 │
│    FAS               = Fabric-Attached Storage; hybrid HDD/SSD ONTAP arrays                           │
│    AutoSupport       = Telemetry agent; sends diagnostics from ONTAP to NetApp support                │
│    SVM               = Storage Virtual Machine; ONTAP multi-tenancy namespace unit                    │
│    Aggregate         = RAID group of disks in ONTAP; FlexVols and FlexGroups reside here              │
│    FlexVol           = Traditional ONTAP volume; thin-provisioned within an aggregate                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="design-standards/"><strong>Standards</strong><span>Service level selection, naming conventions, and capacity management thresholds.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, incident triage, and validation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>BlueXP, ONTAP, monitoring, and third-party integrations.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
<a class="kb-card" href="service-levels/"><strong>Service Levels</strong><span>Service level definitions, IOPS targets, and SLA compliance monitoring.</span></a>
<a class="kb-card" href="usage-reporting/"><strong>Usage Reporting</strong><span>Consumption reporting, BlueXP digital wallet, and billing reconciliation.</span></a>
</div>
