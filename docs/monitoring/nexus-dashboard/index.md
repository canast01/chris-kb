# Nexus Dashboard (Monitoring)

<div class="kb-summary">
Cisco Nexus Dashboard unified operations platform — architecture, NDFC/NDI services, fabric health, ACI integration, and operational runbooks.
</div>

```
┌───────────────────────── Nexus Dashboard — Fabric Monitoring and Operations ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Nexus Dashboard: Cisco management platform for ACI, DCNM/NDFC, and NX-OS fabric operations  │   │
│   │Hosts applications: Nexus Dashboard Insights (NDI), Fabric Controller (NDFC), Orchestrator (NDO│   │
│   │ NDI: real-time telemetry, anomaly detection, flow analytics, and infrastructure health scoring│   │
│   │ Deployed as cluster (3 master nodes) on physical servers or VMware; connects to APIC/switches │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Nexus Dashboard centralises Cisco fabric visibility into a single platform                         │
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Insights (NDI)       │  │      Fabric Controller      │  │         Orchestrator        │   │
│   │        Health scores        │  │        DCNM functions       │  │        Multi-site ACI       │   │
│   │        Anomaly detect       │  │       Switch inventory      │  │        Policy stretch       │   │
│   │        Flow analytics       │  │       Image management      │  │        Tenant deploy        │   │
│   │        Event analysis       │  │      Config compliance      │  │         Multi-fabric        │   │
│   │       Alerts/assurance      │  │       POAP zero-touch       │  │        BGP EVPN mgmt        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Nexus Dashboard: 3 physical/VM nodes · ACI: APIC cluster · NX-OS: switch management TCP 22/443       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Nexus Dashboard = Cisco management platform hosting fabric apps (NDI, NDFC, NDO)                     │
│  NDI = Nexus Dashboard Insights; real-time analytics and health scoring for Cisco fabrics             │
│  NDFC = Nexus Dashboard Fabric Controller; replaces DCNM for NX-OS and SAN fabric management          │
│  NDO = Nexus Dashboard Orchestrator; multi-site ACI policy management and tenant deployment           │
│  APIC = Application Policy Infrastructure Controller; ACI fabric controller                           │
│  Health score = NDI composite score per fabric/site from telemetry and event analysis                 │
│  Anomaly = NDI-detected deviation from learned baseline in fabric behaviour                           │
│  Flow analytics = NDI tracking IP flows through fabric for traffic analysis                           │
│  POAP = Power-On Auto Provisioning; zero-touch NX-OS switch bootstrap                                 │
│  BGP EVPN = Routing protocol for VXLAN fabric overlay managed by NDFC                                 │
│  Multi-site = NDO managing policy across multiple ACI sites or NDFC fabrics                           │
│  Assurance = NDI verifying fabric state matches intended policy configuration                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>Cluster topology, form factors (physical/virtual/cloud), service hosting, and upgrade co-residency.</span></a>
<a class="kb-card" href="design-standards/"><strong>Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>VMware, backup tools, monitoring, authentication, and API integration.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
<a class="kb-card" href="alerts/"><strong>Alerts</strong><span>Alert configuration, thresholds, and notification setup.</span></a>
<a class="kb-card" href="fabric-health/"><strong>Fabric Health</strong><span>Fabric-wide health scores, port flapping detection, BGP/OSPF adjacency alerts, and flow anomalies.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>NDFC, NDI, and Cisco Intersight service onboarding, configuration, and connectivity.</span></a>
<a class="kb-card" href="visibility/"><strong>Visibility</strong><span>End-to-end flow telemetry, micro-segmentation policy visibility, and network path tracing.</span></a>
</div>
