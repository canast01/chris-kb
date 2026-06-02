# Nexus Dashboard

<div class="kb-summary">
Cisco Nexus Dashboard knowledge base covering fabric health, flow telemetry, policy compliance, integrations, and multi-site management for Cisco data centre environments.
</div>

```
┌────────────────────── Cisco Nexus Dashboard — Multi-Domain Management Platform ───────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Nexus Dashboard: multi-domain management platform hosting Insights, NDFC, and Orchestrator  │   │
│   │       Replaces DCNM; 3-node or 5-node cluster; form factors: virtual, physical, or cloud      │   │
│   │       NDFC (Nexus Dashboard Fabric Controller) replaces DCNM for LAN and SAN management       │   │
│   │         NDI: assurance and troubleshooting; NDO: multi-site policy push for ACI/NX-OS         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Cluster deployment → app install → site onboarding → fabric management and assurance               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Hosted Apps         │  │           Cluster           │  │         Connectivity        │   │
│   │        NDFC (fabric)        │  │        3-node HA min        │  │        OOB mgmt VLAN        │   │
│   │        NDI (insights)       │  │       5-node for scale      │  │          Data VLAN          │   │
│   │       NDO (orchestr.)       │  │        Master/Worker        │  │         Ext. svc IPs        │   │
│   │       AppStore install      │  │         Standby node        │  │        In-band option       │   │
│   │        App lifecycle        │  │       Quorum (2 of 3)       │  │        Fabric data NW       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Virtual node: 16 vCPU / 64 GB RAM / 550 GB disk; physical: Cisco UCS C220 or ND appliance          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       App        │     Function     │      Replaces     │   Key feature    │     Licence      │   │
│   │       NDFC       │   Fabric mgmt    │        DCNM       │    Zone/VSAN     │    Essentials    │   │
│   │       NDI        │    Assurance     │     None (new)    │  Flow analysis   │     Premier      │   │
│   │       NDO        │    Multi-site    │      MSO/mso      │   Policy sync    │     Advanced     │   │
│   │    ND cluster    │   App platform   │      DCNM VM      │    HA + scale    │     Bundled      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ND virtual nodes on vSphere/KVM · OOB management switch · Data fabric switches           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Nexus Dashboard = Cisco platform hosting fabric management and assurance apps as pods              │
│    NDFC          = Nexus Dashboard Fabric Controller; replaces standalone DCNM                        │
│    NDI           = Nexus Dashboard Insights; flow-level assurance, anomaly detection                  │
│    NDO           = Nexus Dashboard Orchestrator; multi-site ACI/NX-OS policy management               │
│    Master node   = Runs Kubernetes control plane and ND system services; always 3 masters             │
│    Worker node   = Optional; adds compute for app pods; increases app hosting capacity                │
│    Standby node  = Hot spare; automatically promotes if a master fails                                │
│    Quorum        = ND requires 2 of 3 master nodes healthy for full read-write operation              │
│    OOB network   = Management network for ND admin access and switch credential SSH                   │
│    Data network  = Fabric-facing network; ND apps use this to poll switch telemetry                   │
│    Ext. svc IP   = External service IPs pool; allocated for app ingress endpoints                     │
│    AppStore      = ND built-in app catalogue; install and upgrade apps from Cisco hosted repo         │
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
