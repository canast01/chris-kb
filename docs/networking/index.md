# Networking

<div class="kb-summary">
Networking knowledge base covering switching, routing, security, and network services. Includes design references, configuration procedures, connectivity troubleshooting, and validation guides for enterprise network environments.
</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Network Layers Overview                         │
│                                                                      │
│  Layer 1 — Physical                                                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Cables · SFP+ · DAC · Patch panels · Switch ports           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  Layer 2 — Logical (VLANs / Switching)                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  VLANs · Trunks · LACP · vPC/MLAG · STP · MAC tables         │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  Layer 3 — Routing                                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  OSPF (intra-DC) · BGP (WAN/cloud) · ECMP · ACLs             │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  Layer 4 — Overlay (NSX-T / VXLAN)                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  NSX-T segments · DFW micro-segmentation · VXLAN tunnels     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  Cloud                                                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  AWS Direct Connect · Azure ExpressRoute · IPSec VPN         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
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
