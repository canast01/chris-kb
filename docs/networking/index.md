# Networking

<div class="kb-summary">
Networking knowledge base covering switching, routing, security, and network services. Includes design references, configuration procedures, connectivity troubleshooting, and validation guides for enterprise network environments.
</div>

```
┌──────────────────────── Networking — Switching, Routing, Security & Services ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Networking KB: design references, configuration procedures, and troubleshooting guides    │   │
│   │     Covers: VLANs, BGP/OSPF, firewall validation, DNS, load balancing, connectivity tests     │   │
│   │        Foundation: segment by function, redundant paths, document every rule and change       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Switching & Routing     │  │           Security          │  │        Services & TS        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       VLANs / trunking      │  │        Firewall rules       │  │        DNS resolution       │   │
│   │      BGP / OSPF routing     │  │         VPN tunnels         │  │        Load balancer        │   │
│   │      Subnetting / CIDR      │  │        ACL validation       │  │      Connectivity tests     │   │
│   │          STP / LACP         │  │          NAT / PAT          │  │        Packet capture       │   │
│   │         QoS marking         │  │        IDS/IPS rules        │  │         Path tracing        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VLAN         = Virtual LAN; logical broadcast domain; isolates traffic by function or tenant       │
│    BGP          = Border Gateway Protocol; path-vector routing; used for WAN and DC fabric            │
│    OSPF         = Open Shortest Path First; link-state IGP; used within a campus or data centre       │
│    LACP         = Link Aggregation; bonds NICs for bandwidth + redundancy; IEEE 802.3ad               │
│    STP          = Spanning Tree Protocol; loop prevention; RSTP preferred; MSTP for VLANs             │
│    ECMP         = Equal-Cost Multi-Path; load-balance across redundant L3 paths                       │
│    NAT          = Network Address Translation; maps private IPs to public; hides topology             │
│    QoS          = Quality of Service; priority marking to protect latency-sensitive traffic           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────── Networking — Switching, Routing, Security & Services ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Networking KB: design references, configuration procedures, and troubleshooting guides    │   │
│   │     Covers: VLANs, BGP/OSPF, firewall validation, DNS, load balancing, connectivity tests     │   │
│   │        Foundation: segment by function, redundant paths, document every rule and change       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Switching & Routing     │  │           Security          │  │        Services & TS        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       VLANs / trunking      │  │        Firewall rules       │  │        DNS resolution       │   │
│   │      BGP / OSPF routing     │  │         VPN tunnels         │  │        Load balancer        │   │
│   │      Subnetting / CIDR      │  │        ACL validation       │  │      Connectivity tests     │   │
│   │          STP / LACP         │  │          NAT / PAT          │  │        Packet capture       │   │
│   │         QoS marking         │  │        IDS/IPS rules        │  │         Path tracing        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VLAN         = Virtual LAN; logical broadcast domain; isolates traffic by function or tenant       │
│    BGP          = Border Gateway Protocol; path-vector routing; used for WAN and DC fabric            │
│    OSPF         = Open Shortest Path First; link-state IGP; used within a campus or data centre       │
│    LACP         = Link Aggregation; bonds NICs for bandwidth + redundancy; IEEE 802.3ad               │
│    STP          = Spanning Tree Protocol; loop prevention; RSTP preferred; MSTP for VLANs             │
│    ECMP         = Equal-Cost Multi-Path; load-balance across redundant L3 paths                       │
│    NAT          = Network Address Translation; maps private IPs to public; hides topology             │
│    QoS          = Quality of Service; priority marking to protect latency-sensitive traffic           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="switching-routing/">
  <strong>Switching & Routing</strong>
  <span>VLANs, trunk ports, BGP, OSPF, route tables, subnetting, and TCP/IP.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Firewalls, VPN, rule validation, and network access control.</span>
</a>

<a class="kb-card" href="services/">
  <strong>Services</strong>
  <span>DNS, DHCP, load balancers, and network service management.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Connectivity testing, packet loss, path tracing, and reachability validation.</span>
</a>

</div>
