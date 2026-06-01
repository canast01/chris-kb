# InsightIQ

<div class="kb-summary">
Dell EMC InsightIQ performance analytics for PowerScale clusters — architecture, data collection, capacity trending, and operational runbooks.
</div>

```
┌──────────────────────────── InsightIQ — PowerScale Performance Reporting ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    InsightIQ: on-premises performance analytics appliance for Dell EMC PowerScale (Isilon)    │   │
│   │   Collects detailed performance data: IOPS, latency, throughput, protocol, and client stats   │   │
│   │    Stores multi-year historical data for trend analysis, capacity planning, and chargebacks   │   │
│   │            Deployed as VM (OVA) on vSphere; connects to PowerScale cluster via PAPI           │   │
│   │         Web UI with built-in dashboards and custom report builder; no agent on cluster        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    InsightIQ provides the long-term performance history that PowerScale built-in tools lack           │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Performance         │  │           Capacity          │  │          Workloads          │   │
│   │        IOPS per node        │  │         Space trends        │  │        Per-client IO        │   │
│   │      Latency per proto      │  │       Growth forecast       │  │       Per-share stats       │   │
│   │       Throughput MB/s       │  │        Quota tracking       │  │         Top talkers         │   │
│   │       CPU / disk util       │  │        Tier breakdown       │  │         Protocol mix        │   │
│   │        Cache hit rate       │  │        Dedup/compress       │  │       Chargeback data       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM: 4 vCPU/8 GB · local datastore for metrics DB · PAPI TCP 8080 to cluster                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  InsightIQ = Dell EMC performance analytics appliance for PowerScale clusters                         │
│  PAPI = PowerScale Platform API; REST interface used by InsightIQ to collect data                     │
│  OVA = Open Virtual Appliance; VM image for InsightIQ deployment on vSphere                           │
│  IOPS = Input/Output Operations per Second; primary performance metric                                │
│  Latency = Time from client request to response; measured per protocol (NFS, SMB, S3)                 │
│  Throughput = Data transfer rate in MB/s; saturates network before IOPS typically                     │
│  Top talkers = Clients or directories with highest IO activity                                        │
│  Protocol mix = Breakdown of IO by access protocol (NFS v3, NFS v4, SMB, S3, HDFS)                    │
│  Chargeback = Attributing storage consumption and IO cost to departments or projects                  │
│  Cache hit rate = Percentage of reads served from L1/L2 cache; high rate reduces latency              │
│  Quota tracking = Monitoring directory and user quota consumption over time                           │
│  Dedup/compress = Data reduction ratio metrics tracked for capacity planning                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────── InsightIQ — PowerScale Performance Reporting ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    InsightIQ: on-premises performance analytics appliance for Dell EMC PowerScale (Isilon)    │   │
│   │   Collects detailed performance data: IOPS, latency, throughput, protocol, and client stats   │   │
│   │    Stores multi-year historical data for trend analysis, capacity planning, and chargebacks   │   │
│   │            Deployed as VM (OVA) on vSphere; connects to PowerScale cluster via PAPI           │   │
│   │         Web UI with built-in dashboards and custom report builder; no agent on cluster        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    InsightIQ provides the long-term performance history that PowerScale built-in tools lack           │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Performance         │  │           Capacity          │  │          Workloads          │   │
│   │        IOPS per node        │  │         Space trends        │  │        Per-client IO        │   │
│   │      Latency per proto      │  │       Growth forecast       │  │       Per-share stats       │   │
│   │       Throughput MB/s       │  │        Quota tracking       │  │         Top talkers         │   │
│   │       CPU / disk util       │  │        Tier breakdown       │  │         Protocol mix        │   │
│   │        Cache hit rate       │  │        Dedup/compress       │  │       Chargeback data       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM: 4 vCPU/8 GB · local datastore for metrics DB · PAPI TCP 8080 to cluster                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  InsightIQ = Dell EMC performance analytics appliance for PowerScale clusters                         │
│  PAPI = PowerScale Platform API; REST interface used by InsightIQ to collect data                     │
│  OVA = Open Virtual Appliance; VM image for InsightIQ deployment on vSphere                           │
│  IOPS = Input/Output Operations per Second; primary performance metric                                │
│  Latency = Time from client request to response; measured per protocol (NFS, SMB, S3)                 │
│  Throughput = Data transfer rate in MB/s; saturates network before IOPS typically                     │
│  Top talkers = Clients or directories with highest IO activity                                        │
│  Protocol mix = Breakdown of IO by access protocol (NFS v3, NFS v4, SMB, S3, HDFS)                    │
│  Chargeback = Attributing storage consumption and IO cost to departments or projects                  │
│  Cache hit rate = Percentage of reads served from L1/L2 cache; high rate reduces latency              │
│  Quota tracking = Monitoring directory and user quota consumption over time                           │
│  Dedup/compress = Data reduction ratio metrics tracked for capacity planning                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>Deployment on vApp, PowerScale data collection intervals, and reporting database architecture.</span></a>
<a class="kb-card" href="design-standards/"><strong>Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>VMware, backup tools, monitoring, authentication, and API integration.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
<a class="kb-card" href="capacity/"><strong>Capacity</strong><span>Capacity planning, forecasting, and thresholds.</span></a>
<a class="kb-card" href="performance/"><strong>Performance</strong><span>Performance monitoring, tuning, and baselining.</span></a>
<a class="kb-card" href="reports/"><strong>Reports</strong><span>Reporting, dashboards, and data export.</span></a>
<a class="kb-card" href="workloads/"><strong>Workloads</strong><span>Protocol-level workload breakdown, per-client NFS/SMB throughput analysis, and hot-file reporting.</span></a>
</div>
