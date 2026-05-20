# Cisco DCNM

<div class="kb-summary">
Cisco Data Center Network Manager knowledge base covering SAN fabric management, discovery, inventory, alerts, and monitoring for Cisco Fibre Channel environments.
</div>

```
┌────────────────────────────── Cisco DCNM — Data Center Network Manager ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        DCNM: centralised management for Cisco NX-OS — Nexus (LAN) and MDS (SAN) fabrics       │   │
│   │            Deployed as OVA (ESXi) or ISO (bare metal); modes: LAN, SAN, or Unified            │   │
│   │          SAN mode manages MDS 9000 VSANs, zones, ISLs, and SAN Analytics performance          │   │
│   │       Provides fabric discovery, template-based provisioning, compliance, and reporting       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Fabric discovery → zone management → performance monitoring → compliance reporting                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Fabric Management      │  │        SAN Analytics        │  │          Compliance         │   │
│   │       Switch discovery      │  │        Flow telemetry       │  │         Config check        │   │
│   │         Topology map        │  │         Port metrics        │  │         Policy audit        │   │
│   │        VSAN/zone mgmt       │  │         IOPS/latency        │  │       Change tracking       │   │
│   │        ISL management       │  │        Top-N reports        │  │        Diff baseline        │   │
│   │       Template deploy       │  │       Alert thresholds      │  │          Audit log          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    DCNM communicates with switches via SSH (config) and SNMP/Telemetry (monitoring)                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Function     │      Protocol     │      Output      │      Notes       │   │
│   │    Discovery     │  Topo/inventory  │      SSH/SNMP     │   Switch list    │   Credentials    │   │
│   │    Zone mgmt     │  VSAN/zone CRUD  │      SSH CLI      │   Zone config    │   Active zone    │   │
│   │    Analytics     │  Flow telemetry  │     Telemetry     │   IOPS/latency   │   Licence req.   │   │
│   │    Compliance    │   Policy check   │    Config diff    │   Report/alert   │  Baseline snap   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: DCNM OVA (8 vCPU/32 GB RAM) · OOB management VLAN · Cisco MDS 9000 switches              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DCNM          = Data Center Network Manager; Cisco centralised fabric management platform          │
│    NX-OS         = Cisco data centre OS running on Nexus and MDS switch platforms                     │
│    VSAN          = Virtual SAN; logical partition of the FC fabric; each VSAN is isolated             │
│    Zone          = FC zone: set of port WWNs allowed to communicate within a VSAN                     │
│    Active zone   = Zone configuration currently enforced on the fabric; push activates it             │
│    ISL           = Inter-Switch Link; FC trunk connecting two MDS switches in the fabric              │
│    SAN Analytics = DCNM module capturing frame-level telemetry; requires Analytics licence            │
│    Telemetry     = Streaming push from switch to DCNM collector; lower latency than polling           │
│    OVA           = Open Virtual Appliance; VMware VM image format used for DCNM deployment            │
│    Compliance    = DCNM feature comparing running config vs golden baseline; flags drifts             │
│    Template      = DCNM config template applied to switch interfaces, VSANs, or policies              │
│    SNMP          = Simple Network Management Protocol; used for fault and performance polling         │
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
