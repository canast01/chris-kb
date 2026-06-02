---
title: NSX
---

# NSX

<div class="kb-summary">
Technical and operational reference for VMware NSX. Covers segments, gateways, distributed firewall, routing, edge nodes, and overlay networking for software-defined network and security across vSphere environments.
</div>

```
┌──────────────────────────────── NSX Software-Defined Networking Stack ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     VMware NSX — Software-Defined Networking and Security                     │   │
│   │       Overlay networking: Geneve encapsulation over physical underlay; TEPs on each host      │   │
│   │    Routing: T0 Gateway (north-south, BGP to physical) · T1 Gateway (east-west, per tenant)    │   │
│   │ Security: Distributed Firewall (DFW) on every hypervisor kernel — zero-trust microsegmentation│   │
│   │     Edge: Edge Nodes run T0/T1 services; deployed as VM or bare-metal for high throughput     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    NSX Manager controls all SDN config · overlay transports workloads · DFW secures every VM          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │ NSX Manager: 3-node cluster │  │   Segment: create + attach  │  │   DFW: kernel-level rules   │   │
│   │  T0: BGP to physical fabric │  │    T0/T1: routing config    │  │    Gateway Firewall: N/S    │   │
│   │    T1: per-tenant routing   │  │   Edge node: health + BFD   │  │   IDS/IPS: signature-based  │   │
│   │   TEP: Geneve on VMk port   │  │   DFW: policy + group mgmt  │  │     Endpoint Protection     │   │
│   │   Transport zone: overlay   │  │    Alarms: BGP down, TEP    │  │    NSX Intelligence: flow   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines overlay and routing · Operations manage segments and DFW                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │ BGP session down │get logical-router│Manager: 3 nodes up│GSS: collect logs │ nsxcli get route │   │
│   │ TEP connectivity │ping ++netstack=vx│ Edge: HA state UP?│  TAM escalation  │ nsxcli get edge  │   │
│   │DFW rule blocking │get firewall stats│ TEP MTU: 1600 min │Collect tech-suppo│  nsxcli get fw   │   │
│   │Segment not visibl│get transport-node│ BGP neighbour up? │ P1: network down │  nsxcli get mgr  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts with TEP VMkernel NICs · physical ToR switches · BGP-capable fabric                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Geneve        = Generic Network Virtualisation Encapsulation; NSX overlay protocol (UDP 6081)        │
│  TEP           = Tunnel End Point; VMkernel port on each host used for Geneve overlay traffic         │
│  T0 Gateway    = Tier-0; connects NSX overlay to physical network via BGP or static routing           │
│  T1 Gateway    = Tier-1; per-tenant router; provides east-west routing between segments               │
│  DFW           = Distributed Firewall; stateful L4 firewall running in each ESXi kernel vNIC          │
│  Segment       = NSX logical network (replaces port group); backed by Geneve overlay or VLAN          │
│  Edge Node     = VM or bare-metal running T0/T1 data-plane services and gateway firewall              │
│  Transport Zone= Scope boundary for overlay or VLAN segments; spans hosts and edge nodes              │
│  BFD           = Bidirectional Forwarding Detection; fast failure detection for BGP peers             │
│  NSX Manager   = Control and management plane; 3-node cluster for HA; single pane of glass            │
│  IDS/IPS       = Intrusion Detection/Prevention System; signature-based; east-west traffic            │
│  Microsegment  = Zero-trust network policy per workload; DFW rules by VM tag or group                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```
┌──────────────────────────────────── NSX-T — Installation Sequence ────────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Deploy Checks                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  DNS/NTP confirmed on all hosts and vCenter  ·  vCenter trust established                             │
│  Management network: dedicated IPs for 3 NSX Manager nodes + 1 VIP reserved                           │
│  MTU 9000 on all physical switches for TEP (GENEVE encapsulation) traffic                             │
│  Host firmware and NIC drivers on NSX HCL  ·  vCenter version compatible                              │
│  Edge VM sizing: medium (4 vCPU/8 GB) minimum  ·  bare-metal for high throughput                      │
│                                                                                                       │
│                                        │  deploy NSX Manager cluster                                  │
│                                        ▼                                                              │
│  Step 2 · NSX Manager Deployment                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy NSX Manager OVA on first ESXi host  ·  Set size: medium or large                              │
│  Set management IP, gateway, DNS, NTP  ·  Set admin + audit passwords                                 │
│  Login to NSX Manager UI  ·  Accept EULA  ·  Enter licence key                                        │
│  Deploy second and third NSX Manager nodes  ·  Join to form 3-node cluster                            │
│  Configure VIP (virtual IP) for NSX Manager cluster  ·  Confirm all nodes UP                          │
│                                                                                                       │
│                                        │  register vCenter and configure transport                    │
│                                        ▼                                                              │
│  Step 3 · Transport Zones & Profiles                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add vCenter as compute manager  ·  Accept thumbprint  ·  Sync completes                              │
│  Create overlay transport zone  ·  Create VLAN transport zone                                         │
│  Create uplink profile: active/standby or LACP  ·  MTU 9000  ·  VLAN for TEP                          │
│  Create TEP IP pool: range of IPs on TEP subnet allocated per host/edge                               │
│  Host switch profile: maps physical NICs to logical uplinks                                           │
│                                                                                                       │
│                                        │  prepare hosts as transport nodes                            │
│                                        ▼                                                              │
│  Step 4 · Host Transport Node Preparation                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  System → Fabric → Hosts: select all cluster hosts  ·  Configure NSX                                  │
│  Select transport zone, uplink profile, TEP pool  ·  Apply to cluster                                 │
│  Monitor host prep status: each host transitions to Success state                                     │
│  Verify TEP IPs assigned  ·  TEP-to-TEP connectivity (ping from host)                                 │
│  NSX kernel modules loaded on all hosts  ·  No host in degraded state                                 │
│                                                                                                       │
│                                        │  deploy and configure Edge nodes                             │
│                                        ▼                                                              │
│  Step 5 · Edge Cluster Deployment                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Edge VM OVA on ESXi hosts (or bare-metal)  ·  Size: medium+                                   │
│  Edge transport node config: overlay TZ, VLAN TZ, uplink profile, TEP pool                            │
│  Create Edge cluster  ·  Add both Edge nodes  ·  BFD between edges enabled                            │
│  Tier-0 gateway: create, assign to Edge cluster  ·  Uplink port to physical router                    │
│  BGP or static routing: configure on Tier-0  ·  Confirm route advertisement                           │
│                                                                                                       │
│                                        │  configure logical networking                                │
│                                        ▼                                                              │
│  Step 6 · Logical Networking & Firewall                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Tier-1 gateway: linked to Tier-0  ·  Route advertisement for connected segments                      │
│  Segments: create logical segments  ·  Assign to Tier-1 or as standalone                              │
│  Distributed Firewall: review default allow rules  ·  Create baseline deny policy                     │
│  Micro-segmentation: tag VMs with NSX groups  ·  Apply workload-based policies                        │
│  Enable Gateway Firewall on Tier-0/Tier-1 for perimeter controls                                      │
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
