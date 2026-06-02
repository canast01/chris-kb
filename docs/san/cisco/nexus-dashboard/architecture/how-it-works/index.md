# Nexus Dashboard — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Key Hosted Applications, Deployment Topology, Node Types, Network Interfaces Per Node and 3 more sections.
</div>

```text
┌──────────────────────────────── Cisco Nexus Dashboard — How It Works ─────────────────────────────────┐
│                                                                                                       │
│  ND cluster discovers fabric sites, streams telemetry, and orchestrates multi-site policy.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Site Onboarding                │  │              Telemetry Pipeline             │   │
│   │            Add APIC/NDFC/switches            │  │         gRPC streaming from switches        │   │
│   │          Credentials: REST API auth          │  │         NDI: flow, latency, anomaly         │   │
│   │         Site health: continuous poll         │  │           Kafka bus: event routing          │   │
│   │          Reachability: ICMP + REST           │  │          Elasticsearch: query store         │   │
│   │         Discovered: fabric topology          │  │         Retention: configurable days        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Sites added to ND; apps query ND APIs to retrieve topology and telemetry data                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Policy Orchestration (NDO)          │  │               App Interactions              │   │
│   │          Template: define EPGs/BDs           │  │         NDFC: SAN zone push via REST        │   │
│   │         Deploy: push to remote APIC          │  │         NDI: anomaly alert webhooks         │   │
│   │         Delta: only changed objects          │  │           NDO: ACI multi-site sync          │   │
│   │         Rollback: prior template ver         │  │          Shared services: SSO/RBAC          │   │
│   │          Audit: deploy history log           │  │         API gateway: single endpoint        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · fabric switches (Nexus/MDS) · APIC cluster · management network                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  gRPC           = Google Remote Procedure Call; used for high-speed telemetry streaming               │
│  Kafka          = Distributed event streaming platform; routes telemetry within ND                    │
│  Elasticsearch  = Search/analytics engine storing historical telemetry for NDI                        │
│  APIC           = Application Policy Infrastructure Controller; ACI fabric controller                 │
│  EPG            = Endpoint Group; ACI policy construct grouping VMs or physical hosts                 │
│  BD             = Bridge Domain; Layer 2 forwarding domain in ACI                                     │
│  NDO template   = Policy definition object deployed to one or more APIC sites                         │
│  Delta deploy   = Only objects that changed since last deploy are pushed to APIC                      │
│  Rollback       = Revert site config to a previous NDO template version                               │
│  SSO            = Single Sign-On; shared auth across NDFC, NDI, NDO apps                              │
│  REST API       = HTTP-based interface used by ND to communicate with fabric sites                    │
│  API gateway    = Single HTTPS endpoint routing requests to correct ND app                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Software Versioning

Nexus Dashboard uses independent version streams for the platform and hosted applications. Check the Cisco compatibility matrix before any upgrade to confirm ND platform version compatibility with each installed application version.

| Component | Example Version |
|---|---|
| Nexus Dashboard platform | 3.1.1 |
| NDFC application | 12.2.2 |
| NDI application | 6.3.1 |
