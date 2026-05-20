# VMware Management Tools Inventory

```
┌────────────────────────────────────── VMware — Management Tools ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Layered management toolstack for the VMware platform: compute, network, storage, lifecycle  │   │
│   │     Each tool manages a distinct layer; SDDC Manager orchestrates VCF lifecycle across all    │   │
│   │       Track: FQDN, version, admin URL, primary admin account, last upgrade date per tool      │   │
│   │    Access: all tools require LDAP/SSO + MFA; direct root is break-glass only, vault stored    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Compute/storage mgmt → network mgmt → operations and lifecycle management                          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Compute & Storage      │  │      Network & Security     │  │       Ops & Lifecycle       │   │
│   │        vCenter Server       │  │         NSX Manager         │  │       Aria Operations       │   │
│   │        vSphere Client       │  │         NSX UI / API        │  │          Aria Logs          │   │
│   │        VxRail Manager       │  │        Aria Networks        │  │       Aria Automation       │   │
│   │         vSAN Skyline        │  │       NSX Intelligence      │  │        Aria Suite LCM       │   │
│   │         SDDC Manager        │  │       Load Balancer UI      │  │       Skyline Advisor       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Hardware access: iDRAC / RACADM — independent of ESXi and vCenter for OOB management               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Tool       │       FQDN       │      Version      │    Admin URL     │   Last upgrade   │   │
│   │     vCenter      │   vcsa-prod-01   │       8.0 U3      │   https://vcsa   │     2025-03      │   │
│   │   NSX Manager    │    nsx-mgr-01    │       4.1.2       │   https://nsx    │     2025-03      │   │
│   │    VxRail Mgr    │    vxrail-mgr    │      8.0.300      │   https://vxrm   │     2025-04      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: management VMs on dedicated cluster · iDRAC on dedicated OOB network                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    vCenter Server  = Central management for ESXi clusters, VMs, storage, and networking               │
│    NSX Manager     = Control plane for NSX-T; manages segments, gateways, DFW policy                  │
│    VxRail Manager  = Dell VxRail appliance manager; Mystic service orchestrates LCM                   │
│    SDDC Manager    = VCF lifecycle orchestrator; manages domains, clusters, upgrades                  │
│    Aria Operations = vROps; monitors vSphere/vSAN/NSX with ML anomaly detection                       │
│    Aria Logs       = vRLI; log analytics for ESXi, vCenter, NSX, and infrastructure                   │
│    Aria Automation = vRA; IaC and self-service cloud automation; Terraform backed                     │
│    Aria Suite LCM  = Lifecycle Manager for Aria products; upgrades and cert rotation                  │
│    Skyline Advisor = Proactive support; flags known issues before they cause outages                  │
│    iDRAC           = Dell OOB management; hardware-level access independent of OS                     │
│    Aria Networks   = vRNI; network flow visibility and micro-segmentation planning                    │
│    Break-glass     = Emergency admin account in vault; used only when SSO/LDAP fails                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
| Tool | Version | URL | Integration | Service Account |
|---|---|---|---|---|
| vCenter | 8.x | vcenter.domain.local | ESXi, vSAN, NSX, Aria | svc-vcenter |
| Aria Operations | 8.x | aria-ops.domain.local | vCenter, NSX | svc-aria-ops |
| Aria Operations for Logs | 8.x | aria-logs.domain.local | vCenter, ESXi | svc-aria-logs |
| Aria Automation | 8.x | aria-auto.domain.local | vCenter, NSX, IPAM | svc-aria-auto |
| VxRail Manager | 8.x | vxrail-mgr.domain.local | vCenter, iDRAC | svc-vxrail |
| NSX Manager | 4.x | nsx-mgr.domain.local | vCenter, ESXi | svc-nsx |
| Backup Platform | — | backup.domain.local | vCenter API | svc-backup |
| Monitoring Platform | — | monitoring.domain.local | vCenter, ESXi | svc-monitoring |
| CMDB / Ticketing | — | — | Aria Automation | svc-cmdb |
