---
tags:
  - aria-operations
  - vmware
---
# Aria Operations

<div class="kb-summary">
Technical and operational reference for VMware Aria Operations. Covers performance monitoring, capacity management, compliance, alerting, dashboards, and troubleshooting across vSphere, vSAN, NSX, and Aria-managed infrastructure.

*Applies to: Aria Operations 8.x*
</div>

```text
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
│  Aria Operations VMs (master/replica/data/RC) · vSphere cluster · shared datastore                    │
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

```text
┌─────────────────────────── Aria Operations (vROps) — Installation Sequence ───────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Deploy Checks                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  DNS A-record for master node FQDN + VIP  ·  PTR records created                                      │
│  NTP confirmed  ·  vCenter service account with read-only minimum rights                              │
│  Datastore sizing: master ≥500 GB, analytics node ≥200 GB per additional node                         │
│  Network: management port and NFS analytics store port reachable                                      │
│  Decide deployment size: standard (≤1500 objects) or large (≤3000+)                                   │
│                                                                                                       │
│                                        │  deploy master node OVA                                      │
│                                        ▼                                                              │
│  Step 2 · Master Node Deployment                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Aria Operations OVA on vCenter  ·  Select size: small/medium/large                            │
│  Set FQDN, management IP, gateway, DNS, NTP  ·  Set admin password                                    │
│  Power on  ·  Access admin UI at https://vrops-fqdn  ·  Initial setup wizard                          │
│  Accept EULA  ·  Enter licence  ·  Choose master or replica role: Master                              │
│  Wait for cluster to initialise  ·  Master node transitions to Running state                          │
│                                                                                                       │
│                                        │  add replica and collector nodes                             │
│                                        ▼                                                              │
│  Step 3 · Replica & Collector Nodes                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy additional OVAs for each data node  ·  Role: Data (replica)                                   │
│  Join each data node to master cluster using admin UI → Cluster Management                            │
│  Remote Collectors: deploy lightweight collector OVA for remote sites                                 │
│  Assign collector groups to define which adapters run on which collector                              │
│  Cluster health: all nodes green  ·  Online status confirmed before next step                         │
│                                                                                                       │
│                                        │  add vCenter cloud account                                   │
│                                        ▼                                                              │
│  Step 4 · vCenter Adapter & Cloud Account                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add vCenter cloud account: Data Sources → Add  ·  Enter vCenter FQDN + creds                         │
│  Accept vCenter thumbprint  ·  Collection cycle starts immediately                                    │
│  Verify objects discovered: hosts, clusters, VMs, datastores visible                                  │
│  Enable continuous discovery for new VM detection  ·  Collection interval: 5 min                      │
│  Check adapter health: green status in Data Sources panel                                             │
│                                                                                                       │
│                                        │  add additional adapters                                     │
│                                        ▼                                                              │
│  Step 5 · Additional Adapters & Management Packs                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  NSX Adapter: add NSX Manager  ·  Topology maps and flow data collected                               │
│  Storage adapters: Pure1, Dell CloudIQ, NetApp adapters from marketplace                              │
│  OS agents: deploy Aria Operations agent on Linux/Windows VMs for in-guest                            │
│  Third-party: SNMP adapter for physical network devices  ·  Custom metrics                            │
│  Management packs installed from VMware Marketplace  ·  Restart collector if needed                   │
│                                                                                                       │
│                                        │  configure dashboards and alerts                             │
│                                        ▼                                                              │
│  Step 6 · Dashboards, Alerts & Reports                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Import VMware default dashboards  ·  Assign to user groups                                           │
│  Configure alert definitions: capacity, performance, availability thresholds                          │
│  Notification plugins: email, Slack, ServiceNow webhook  ·  Route by severity                         │
│  Compliance: assign regulatory benchmarks (PCI, CIS) to objects                                       │
│  Reports: schedule weekly capacity and health reports  ·  Email distribution list                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>OVA deployment, cluster node expansion, vCenter adapter setup, and management pack configuration.</span>
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
