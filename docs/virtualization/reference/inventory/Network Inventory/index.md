# VMware Network Inventory

```
┌───────────────────────────────────── vSphere — Network Inventory ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Per-VDS record tracking port groups, VLAN assignments, uplinks, and NSX overlay config    │   │
│   │     VDS is the standard for production clusters; one VDS per cluster with defined uplinks     │   │
│   │       Port groups: Management, vMotion, vSAN, iSCSI/NFS, NSX TEP — each on distinct VLAN      │   │
│   │     NSX overlay: GENEVE-encapsulated traffic over TEP VLAN; logical segments over physical    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical NIC uplinks → VDS → port groups → VMs and VMkernel adapters                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         VDS Identity        │  │         Port Groups         │  │         NSX Overlay         │   │
│   │           VDS name          │  │       PG-Mgmt VLAN 10       │  │         TEP VLAN ID         │   │
│   │         VDS version         │  │      PG-vMotion VLAN 20     │  │        Segment count        │   │
│   │         MTU setting         │  │       PG-vSAN VLAN 30       │  │          Gateway IP         │   │
│   │         Uplink count        │  │       PG-iSCSI VLAN 40      │  │         Tier-0 name         │   │
│   │          LB policy          │  │         PG-VM trunk         │  │         Edge cluster        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    VDS config + NSX overlay define all VM and VMkernel reachability across the cluster                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     VDS name     │     Version      │        MTU        │     Uplinks      │    LB policy     │   │
│   │   vds-prod-01    │       8.0        │        9000       │     2x 25GbE     │  Route by port   │   │
│   │   vds-mgmt-01    │       8.0        │        1500       │     2x 10GbE     │  Active/standby  │   │
│   │   vds-edge-01    │       8.0        │        9000       │     2x 25GbE     │  Route by port   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: 25/100GbE NICs · top-of-rack switches · physical VLAN trunks to hosts                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VDS           = vSphere Distributed Switch; centrally managed in vCenter across hosts              │
│    Port group    = Named VLAN policy container on VDS; VMkernel or VM adapters attach here            │
│    VMkernel      = ESXi virtual NIC for Management, vMotion, vSAN, iSCSI, NFS traffic                 │
│    VLAN          = 802.1Q tag isolating traffic at Layer 2 across the physical switch fabric          │
│    MTU 9000      = Jumbo frames required for vSAN and NSX TEP traffic (GENEVE overhead)               │
│    TEP           = Tunnel Endpoint; NSX GENEVE encapsulation source/dest per ESXi host                │
│    GENEVE        = NSX overlay protocol; carries logical segment traffic over underlay IP             │
│    Tier-0 GW     = NSX logical router peering with physical switches; handles N/S routing             │
│    Tier-1 GW     = NSX tenant router for workload E/W routing; connected to Tier-0                    │
│    LB policy     = VDS uplink selection: route by port ID, IP hash, active/standby, LACP              │
│    Edge cluster  = NSX Edge transport nodes hosting Tier-0/1 gateways and load balancers              │
│    Segment       = NSX logical network; GENEVE-backed overlay equivalent of a VLAN port group         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
| Field | Example |
|---|---|
| vSwitch or DVS Name | vDS-prod-01 |
| Port Group Name | pg-prod-app-vlan100 |
| VLAN ID | 100 |
| MTU | 1500 or 9000 |
| Uplink Mapping | vmnic0, vmnic1 |
| VMkernel Adapters | vmk0 (mgmt), vmk1 (vMotion), vmk2 (vSAN) |
| vMotion Network | VLAN 200, vmk1 |
| Management Network | VLAN 10, vmk0 |
| vSAN Network | VLAN 300, vmk2 |
| NSX Segment Mapping | seg-prod-app-01 maps to VLAN 100 |
| NIC Teaming Policy | Load-based or Active/Standby |
| Notes | Any exceptions or non-standard config |
