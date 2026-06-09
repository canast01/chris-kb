# Networking

<div class="kb-summary">
Networking knowledge base covering switching, routing, security, and network services. Includes design references, configuration procedures, connectivity troubleshooting, and validation guides for enterprise network environments.
</div>

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
  <strong>Load Balancer & Services</strong>
  <span>Load balancer VIP management, pool health monitoring, and IPAM. DNS and DHCP covered under Protocols.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Connectivity testing, packet loss, path tracing, and reachability validation.</span>
</a>

<a class="kb-card" href="external-connectivity/">
  <strong>External Connectivity</strong>
  <span>Internet egress, WAN/MPLS, cloud direct connections, and partner API connectivity paths.</span>
</a>

<a class="kb-card" href="network-design/">
  <strong>Network Design</strong>
  <span>Enterprise network design — topology, redundancy, trust zones, and observability references.</span>
</a>

<a class="kb-card" href="protocols/">
  <strong>Protocols</strong>
  <span>Protocol reference — FC, iSCSI, NFS, SMB, DNS, DHCP, NTP, LDAP, SNMP, TLS, Syslog, and SMTP.</span>
</a>

</div>
