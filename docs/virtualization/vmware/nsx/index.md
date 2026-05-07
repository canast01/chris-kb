# NSX

Technical and operational KBs for NSX.

## NSX Overlay Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                          NSX-T Control Plane                            │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────┐        │
  │  │  NSX Manager (3-node cluster)  +  vCenter integration       │        │
  │  └─────────────────────────────────────────────────────────────┘        │
  │                          │ management API                               │
  └──────────────────────────┼───────────────────────────────────────────── ┘
                             │
  ┌──────────────────────────▼───────────────────────────────────────────────┐
  │                         Transport Layer (TEPs)                           │
  │                                                                          │
  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
  │  │   ESXi-01       │  │   ESXi-02       │  │   ESXi-03       │          │
  │  │  TEP: 192.0.2.1 │  │  TEP: 192.0.2.2 │  │  TEP: 192.0.2.3 │          │
  │  │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │          │
  │  │  │ Segment A │  │  │  │ Segment A │  │  │  │ Segment B │  │          │
  │  │  │ (VXLAN)   │  │  │  │ (VXLAN)   │  │  │  │ (VXLAN)   │  │          │
  │  │  └─────┬─────┘  │  │  └─────┬─────┘  │  │  └─────┬─────┘  │          │
  │  └────────┼────────┘  └────────┼────────┘  └────────┼────────┘          │
  │           └─────────────────── GENEVE tunnel ────────┘                   │
  └──────────────────────────────────────────────────────────────────────────┘
                             │
  ┌──────────────────────────▼───────────────────────────────────────────────┐
  │                    Gateway Layer                                         │
  │                                                                          │
  │  ┌───────────────────────────────────────┐                              │
  │  │  Tier-1 Gateway (per tenant / app)    │  ← distributed routing       │
  │  │  (runs on all ESXi hosts)             │                              │
  │  └────────────────────┬──────────────────┘                              │
  │                       │  uplink                                         │
  │  ┌────────────────────▼──────────────────┐                              │
  │  │  Tier-0 Gateway (north-south routing) │  ← runs on Edge Nodes        │
  │  │  ┌────────────┐  ┌────────────┐       │                              │
  │  │  │  Edge VM 1 │  │  Edge VM 2 │  HA   │                              │
  │  │  └─────┬──────┘  └─────┬──────┘       │                              │
  │  └────────┼───────────────┼──────────────┘                              │
  └───────────┼───────────────┼────────────────────────────────────────────┘
              │  BGP / static │
  ┌───────────▼───────────────▼────────────────────────────────────────────┐
  │                    Physical Network (underlay)                          │
  │                   (leaf-spine, no VLAN trunking per segment)            │
  └────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-9">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>NSX Manager and Edge CLI — gateways, routing, DFW, tunnels, and diagnostics.</span>
</a>

<a class="kb-card" href="technical-deep-dive/">
  <strong>Technical Deep Dive</strong>
  <span>Managers, edges, overlays, ports, commands, logs, and failure points.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Python NSX-T API health check, transport node monitor, DFW rule audit, and Ansible NSX-T playbook.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily checks, health check, change readiness, incident triage, maintenance window, and post-change validation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Edge health, transport node issues, DFW connectivity, and NSX recovery procedures.</span>
</a>


<a class="kb-card" href="distributed-firewall/">
  <strong>Distributed Firewall</strong>
  <span>Distributed Firewall notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="edge-nodes/">
  <strong>Edge Nodes</strong>
  <span>Edge Nodes notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="segments/">
  <strong>Segments</strong>
  <span>Segments notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="tier-gateways/">
  <strong>Tier Gateways</strong>
  <span>Tier Gateways notes, checks, commands, and references.</span>
</a>
</div>
