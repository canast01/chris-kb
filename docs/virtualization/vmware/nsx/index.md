# NSX

<div class="kb-summary">
Technical and operational reference for VMware NSX. Covers segments, gateways, distributed firewall, routing, edge nodes, and overlay networking for software-defined network and security across vSphere environments.
</div>

```
NSX — Software-Defined Networking Overview
┌──────────────────────────────────────────────────────────┐
│  Management Plane                                        │
│  NSX Manager Cluster (3 nodes, active-active, VIP)      │
│  UI / API / Policy → pushes config to all nodes         │
└─────────────────────────┬────────────────────────────────┘
                          │ config distribution
      ┌───────────────────┼──────────────────────┐
      ▼                   ▼                       ▼
┌─────────────┐   ┌───────────────┐   ┌──────────────────┐
│  ESXi Host  │   │  ESXi Host    │   │  Edge Node VM    │
│  (Transport │   │  (Transport   │   │  T0 Gateway      │
│   Node)     │   │   Node)       │   │  BGP peer        │
│  ├─ DFW     │   │  ├─ DFW       │   │  NAT / LB / VPN  │
│  ├─ T1 GW   │   │  ├─ T1 GW     │   │                  │
│  └─ TEP vmk │   │  └─ TEP vmk   │   │  fp-eth0/fp-eth1 │
│  Geneve 6081│   │  Geneve 6081  │   │  → Physical Router│
└──────┬──────┘   └───────┬───────┘   └────────┬─────────┘
       └──────────────────┘                     │
              Geneve overlay                    │ BGP / static
              (TEP ↔ TEP, VNI-based)            │
                                       ┌────────▼─────────┐
                                       │  Physical Network │
                                       │  (underlay)       │
                                       └──────────────────┘
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
