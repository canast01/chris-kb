# APEX Storage as a Service

<div class="kb-summary">
Dell APEX Storage as a Service — consumption-based on-premises storage managed by Dell. Covers architecture, operations, security, and troubleshooting for PowerStore, PowerScale, and PowerFlex deployed under the APEX STaaS model.
</div>

```
┌─────────────────────────────────── Dell Apex Storage as a Service ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Apex STaaS: Dell-owned hardware on customer premises; consumed as a cloud service       │   │
│   │       Block: NVMe-based tiers (Performance/Capacity); File: NFS/SMB via PowerScale nodes      │   │
│   │            Managed via Apex Console (cloud portal); Dell handles hardware lifecycle           │   │
│   │              Billing: committed base + consumed burst; monthly subscription model             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Apex Console order → Dell installs hardware → customer connects hosts → consume storage            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Storage Tiers        │  │          Management         │  │         Connectivity        │   │
│   │         Perf (NVMe)         │  │         Apex Console        │  │            iSCSI            │   │
│   │        Capacity (SAS)       │  │       CloudIQ monitor       │  │              FC             │   │
│   │        File (NFS/SMB)       │  │        SCG telemetry        │  │           NFS/SMB           │   │
│   │        Committed base       │  │           REST API          │  │          iSCSI CHAP         │   │
│   │        Burst capacity       │  │        Billing portal       │  │         FC port sec.        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Dell retains ownership of hardware; customer manages workloads and data                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Function     │       Owner       │       Tool       │      Notes       │   │
│   │     Hardware     │   Arrays/nodes   │        Dell       │    Field svc.    │     On-prem      │   │
│   │    Management    │    Portal/API    │      Customer     │   Apex Console   │    Cloud SaaS    │   │
│   │    Monitoring    │   Health/perf    │       Shared      │     CloudIQ      │     Via SCG      │   │
│   │       Data       │    Workloads     │      Customer     │    Host tools    │  Customer owns   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell array hardware on-premises · customer network (iSCSI VLAN / FC fabric)              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Apex STaaS     = Storage as a Service; consumption-based billing for on-prem Dell storage          │
│    Apex Console   = Cloud portal at apex.dell.com; provision volumes, view usage, raise SRs           │
│    Committed base = Minimum contracted storage tier; always billed regardless of use                  │
│    Burst capacity = Pre-installed but unbilled storage; consumed when above committed level           │
│    SCG            = Secure Connect Gateway; transmits telemetry from arrays to CloudIQ                │
│    CloudIQ        = Dell cloud-based analytics; health scores, predictive alerts, capacity            │
│    NVMe tier      = Performance storage tier; all-flash NVMe drives; lowest latency                   │
│    Capacity tier  = Lower-cost SAS/NL-SAS tier; higher latency; suited to cold workloads              │
│    iSCSI CHAP     = Challenge Handshake Auth Protocol; authenticates iSCSI initiators                 │
│    FC port sec.   = FC fabric binding + port security; restricts which HBAs can login                 │
│    vVols          = Virtual Volumes; per-VM storage objects; VASA provider exposes to vCenter         │
│    REST API       = Apex Console REST API; automate volume creation, mapping, and reporting           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Authentication, access control, encryption, and hardening.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostics, and escalation.</span></a>
</div>
