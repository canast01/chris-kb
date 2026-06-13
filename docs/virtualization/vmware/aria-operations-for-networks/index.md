---
tags:
  - aria-networks
  - vmware
---
# Aria Operations for Networks

<div class="kb-summary">
Technical and operational reference for VMware Aria Operations for Networks. Covers network visibility, flow analytics, topology mapping, path analysis, and security exposure analysis.

*Applies to: Aria Operations for Networks 6.x*
</div>

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

```text
┌──────────────────────── Aria Operations for Networks — Installation Sequence ─────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Deploy Checks                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  DNS A-records for platform node and data node FQDNs  ·  PTR records created                          │
│  NTP confirmed  ·  vCenter + NSX Manager service accounts prepared                                    │
│  Physical switch SNMP community or SNMPv3 credentials available                                       │
│  IPFIX: physical switches and NSX VDS support flow export                                             │
│  Datastore: ≥200 GB for platform node  ·  ≥200 GB per data node                                       │
│                                                                                                       │
│                                        │  deploy platform node OVA                                    │
│                                        ▼                                                              │
│  Step 2 · Platform Node Deployment                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Aria Ops for Networks OVA  ·  Role: Platform                                                  │
│  Set FQDN, management IP, gateway, DNS, NTP  ·  Set admin password                                    │
│  Power on  ·  Access UI at https://vrni-fqdn  ·  Initial setup wizard                                 │
│  Accept EULA  ·  Enter licence  ·  Platform node initialises                                          │
│  Confirm platform Running state before deploying proxy/data nodes                                     │
│                                                                                                       │
│                                        │  deploy proxy/data nodes                                     │
│                                        ▼                                                              │
│  Step 3 · Proxy Node Deployment                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Proxy OVA  ·  Role: Proxy (also called data source node)                                      │
│  During deploy, enter platform node FQDN and shared secret pairing key                                │
│  Proxy joins platform cluster  ·  Appears in Admin → Infrastructure                                   │
│  Deploy additional proxies for scale or geographic separation if needed                               │
│  Verify all proxies connected and showing green health in platform UI                                 │
│                                                                                                       │
│                                        │  add data sources                                            │
│                                        ▼                                                              │
│  Step 4 · Data Source Configuration                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add vCenter: Infrastructure → Data Sources → Add vCenter  ·  Creds + thumbprint                      │
│  Add NSX Manager: enter NSX FQDN + credentials  ·  Topology sync begins                               │
│  Physical network: add switches via SNMP  ·  Read community / v3 credentials                          │
│  Verify data collection: Infrastructure → Data Sources  ·  All sources green                          │
│  Network topology auto-builds: VMs → logical → physical overlay visible                               │
│                                                                                                       │
│                                        │  configure flow collection                                   │
│                                        ▼                                                              │
│  Step 5 · Flow Collection (IPFIX)                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  NSX: enable IPFIX in NSX Manager  ·  Collector IP = proxy node management IP                         │
│  VDS: configure IPFIX export on distributed switch  ·  Collector IP + port 2055                       │
│  Physical switches: configure NetFlow/IPFIX export toward proxy node                                  │
│  Verify flows arrive: Network Map → select entity → view flows                                        │
│  Flow data enables application discovery, security group recommendations                              │
│                                                                                                       │
│                                        │  configure dashboards and security groups                    │
│                                        ▼                                                              │
│  Step 6 · Dashboards & Security Planning                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Topology maps: browse VM-to-VM paths  ·  Identify unplanned traffic flows                            │
│  Application discovery: AI groups related VMs into application constructs                             │
│  Security groups: recommended NSX micro-segmentation rules from observed flows                        │
│  Alerts: configure for new open ports, policy violations, topology changes                            │
│  Reports: schedule weekly traffic analysis and security posture reports                               │
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
  <span>Step-by-step initial deployment: platform OVA, collector nodes, data sources, and IPFIX flow collection.</span>
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
