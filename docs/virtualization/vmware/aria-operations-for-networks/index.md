# Aria Operations for Networks

<div class="kb-summary">
Aria Operations for Networks knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```
┌───────────────────────────────── Aria Operations for Networks Stack ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          VMware Aria Operations for Networks — Network Visibility and Troubleshooting         │   │
│   │        Path analysis: end-to-end network path between source and destination VMs or IPs       │   │
│   │        Flow analytics: IPFIX/NetFlow collection; application traffic maps; top talkers        │   │
│   │      Physical topology: autodiscovered switch/router map integrated with NSX overlay view     │   │
│   │        Security: network exposure analysis; identifies unintended external reachability       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Collectors gather flows · path analysis traces packets · topology maps the full network            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │    Platform + collectors    │  │    Path analysis: src→dst   │  │   Exposure: internet reach  │   │
│   │   NSX: overlay + DFW data   │  │    Flow: top talker + app   │  │    Security groups: view    │   │
│   │  IPFIX/NetFlow: from hosts  │  │    Physical topology: map   │  │   Alert: exposure + drift   │   │
│   │   Physical: SNMP discover   │  │      Alert: path change     │  │      RBAC: user + role      │   │
│   │    vCenter: VM + NIC data   │  │     Network intent: plan    │  │   Compliance: check rules   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture collects network data · Operations trace paths and flows · Security surfaces exposure │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │   No flow data   │  Collector logs  │ Collector: online?│   GSS + bundle   │ vrni-cli cluster │   │
│   │Path shows blocked│path analysis log │ Data source: sync?│  TAM escalation  │ vrni-cli sources │   │
│   │ Topology missing │ SNMP poll debug  │   Phys topo: OK?  │ Collect app logs │  vrni-cli flows  │   │
│   │NSX not integrated│NSX credential che│ NSX data: current?│P1: net blind spot│ vrni-cli alerts  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Aria Networks VMs (platform+collectors) · SNMP access to switches · IPFIX from ESXi hosts            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Path analysis = Traces every hop from source to destination; shows NSX DFW rules that allow/block    │
│  IPFIX         = IP Flow Information Export; flow telemetry from ESXi/NSX to collectors               │
│  Collector     = Aria Networks remote node that receives IPFIX/NetFlow and forwards to platform       │
│  Physical topology= Auto-discovered map of switches, routers, and links via SNMP and LLDP/CDP         │
│  Flow          = Recorded network conversation: src/dst IP, port, protocol, byte count, duration      │
│  Network intent= Policy that describes desired connectivity; Aria Networks validates compliance       │
│  Exposure      = VM or service reachable from internet/untrusted network; flagged as security risk    │
│  Application   = Auto-discovered group of VMs that communicate; basis for microsegmentation planning  │
│  Top talker    = VM or IP generating the highest volume of network flows in a time window             │
│  NSX integration= Aria Networks pulls DFW rule, segment, and group data directly from NSX Manager     │
│  SNMP          = Simple Network Management Protocol; used to poll physical switch for topology data   │
│  Data source   = vCenter, NSX, or physical device added to Aria Networks for data collection          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────── Aria Operations for Networks Stack ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          VMware Aria Operations for Networks — Network Visibility and Troubleshooting         │   │
│   │        Path analysis: end-to-end network path between source and destination VMs or IPs       │   │
│   │        Flow analytics: IPFIX/NetFlow collection; application traffic maps; top talkers        │   │
│   │      Physical topology: autodiscovered switch/router map integrated with NSX overlay view     │   │
│   │        Security: network exposure analysis; identifies unintended external reachability       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Collectors gather flows · path analysis traces packets · topology maps the full network            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │    Platform + collectors    │  │    Path analysis: src→dst   │  │   Exposure: internet reach  │   │
│   │   NSX: overlay + DFW data   │  │    Flow: top talker + app   │  │    Security groups: view    │   │
│   │  IPFIX/NetFlow: from hosts  │  │    Physical topology: map   │  │   Alert: exposure + drift   │   │
│   │   Physical: SNMP discover   │  │      Alert: path change     │  │      RBAC: user + role      │   │
│   │    vCenter: VM + NIC data   │  │     Network intent: plan    │  │   Compliance: check rules   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture collects network data · Operations trace paths and flows · Security surfaces exposure │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │   No flow data   │  Collector logs  │ Collector: online?│   GSS + bundle   │ vrni-cli cluster │   │
│   │Path shows blocked│path analysis log │ Data source: sync?│  TAM escalation  │ vrni-cli sources │   │
│   │ Topology missing │ SNMP poll debug  │   Phys topo: OK?  │ Collect app logs │  vrni-cli flows  │   │
│   │NSX not integrated│NSX credential che│ NSX data: current?│P1: net blind spot│ vrni-cli alerts  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Aria Networks VMs (platform+collectors) · SNMP access to switches · IPFIX from ESXi hosts            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Path analysis = Traces every hop from source to destination; shows NSX DFW rules that allow/block    │
│  IPFIX         = IP Flow Information Export; flow telemetry from ESXi/NSX to collectors               │
│  Collector     = Aria Networks remote node that receives IPFIX/NetFlow and forwards to platform       │
│  Physical topology= Auto-discovered map of switches, routers, and links via SNMP and LLDP/CDP         │
│  Flow          = Recorded network conversation: src/dst IP, port, protocol, byte count, duration      │
│  Network intent= Policy that describes desired connectivity; Aria Networks validates compliance       │
│  Exposure      = VM or service reachable from internet/untrusted network; flagged as security risk    │
│  Application   = Auto-discovered group of VMs that communicate; basis for microsegmentation planning  │
│  Top talker    = VM or IP generating the highest volume of network flows in a time window             │
│  NSX integration= Aria Networks pulls DFW rule, segment, and group data directly from NSX Manager     │
│  SNMP          = Simple Network Management Protocol; used to poll physical switch for topology data   │
│  Data source   = vCenter, NSX, or physical device added to Aria Networks for data collection          │
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
