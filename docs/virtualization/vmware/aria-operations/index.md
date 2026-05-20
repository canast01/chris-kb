# Aria Operations

<div class="kb-summary">
Technical and operational reference for VMware Aria Operations. Covers performance monitoring, capacity management, compliance, alerting, dashboards, and troubleshooting across vSphere, vSAN, NSX, and Aria-managed infrastructure.
</div>

```
┌──────────────────────────────────── Aria Operations (vROps) Stack ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           VMware Aria Operations — Performance, Capacity, and Compliance Management           │   │
│   │       Analytics cluster: master + replica + data nodes collect and correlate all metrics      │   │
│   │        Adapters: vSphere, vSAN, NSX, AWS, Azure, storage — each adds metric collection        │   │
│   │      Policies: alert thresholds, capacity model, workload placement, compliance benchmark     │   │
│   │          Rightsizing: reclaim wasted CPU/RAM; workload heatmaps; capacity forecasting         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Adapters collect metrics · analytics engine correlates · policies alert and guide optimisation     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │    Analytics: master+data   │  │   Alert: configure+action   │  │    RBAC: user + role mgmt   │   │
│   │   Adapters: vSphere/NSX/S3  │  │     Rightsizing: reclaim    │  │    SSO: AD/vCenter login    │   │
│   │   Management packs: extend  │  │  Capacity: forecast+what-if │  │    Compliance: benchmark    │   │
│   │  Policies: alert + capacity │  │    Dashboard: build+share   │  │     TLS: cert management    │   │
│   │   Remote collector: scale   │  │   Report: schedule+export   │  │   Audit log: user actions   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture scales collection · Operations optimise the environment · Security controls access    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │Adapter not coll. │vrops-support bund│ Analytics: online?│   GSS + bundle   │vrops-cli cluster │   │
│   │Alert storm: noise│adapter-log review│  Adapter: green?  │  TAM escalation  │ vrops-cli alerts │   │
│   │ Disk filling up  │ vsan/disk usage  │    Disk: >70%?    │ Collect app logs │vrops-cli capacity│   │
│   │ No capacity data │Analytics node log│ Data age: <15 min?│P1: analytics fail│vrops-cli objects │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Aria Operations VMs (master/replica/data/RC) · vSphere cluster · shared datastore · 443 network acces│
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Analytics node= Aria Operations cluster member that stores and processes collected metric data       │
│  Adapter       = Plugin collecting metrics from a source (vSphere, NSX, vSAN, AWS, storage)           │
│  Management Pack= Bundle of adapters, dashboards, alerts, and policies for a specific product         │
│  Policy        = Configuration for alert thresholds, capacity model, and compliance benchmark         │
│  Rightsizing   = Recommendations to reclaim oversized vCPU/vRAM allocations from idle VMs             │
│  Remote Collector= Aria Operations node deployed close to data source; forwards to analytics cluster  │
│  Compliance    = Benchmark checks (CIS, DISA STIG, PCI-DSS) against collected configuration data      │
│  Heatmap       = Visual grid showing resource utilisation across VMs, hosts, or clusters              │
│  What-if       = Capacity scenario modelling; simulates adding VMs or hosts to forecast headroom      │
│  Alert         = Symptom-driven notification when metric breaches threshold defined in policy         │
│  Workload      = Aria Operations concept; resource utilisation relative to demand and capacity        │
│  Report        = Scheduled or on-demand export of capacity, alerts, or compliance data as PDF/CSV     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
