---
tags:
  - vplex
  - dell
  - networking
  - firewall
  - ports
  - storage
  - federation
---
# Dell VPLEX — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell VPLEX (storage federation / virtualization). Covers management, WAN COM link between VPLEX clusters (for VPLEX Metro), and host connectivity.

*Applies to: VPLEX GeoSynchrony 6.x*
</div>

```text
┌───────────────────────────────────────────── Dell VPLEX ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        VPLEX: federated storage virtualisation and active-active cross-site clustering        │   │
│   │                                     Protocols: FC · iSCSI                                     │   │
│   │                        Management: VPLEX Management Server / vplex CLI                        │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │        Virtualisation       │  │         Backend LUNs        │  │      Abstracted to VVs      │   │
│   │            Metro            │  │         Sync stretch        │  │        <5ms RTT sites       │   │
│   │             Geo             │  │      Async replication      │  │         Any distance        │   │
│   │          Clustering         │  │        Active-active        │  │       Shared namespace      │   │
│   │            Quorum           │  │          Witness VM         │  │      Split-brain guard      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  Virtual volume  │ Virtualised LUN  │      FC/iSCSI     │    FC zoning     │   Multi-vendor   │   │
│   │  Metro cluster   │   Sync stretch   │   Inter-cluster   │   Certificate    │    2-site max    │   │
│   │     Witness      │  Quorum arbiter  │       HTTPS       │   Certificate    │     3rd site     │   │
│   │     WAN-COM      │ Geo replication  │   Encrypted WAN   │   Certificate    │     Geo only     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: VPLEX VS2/VS6 appliance · FC fabric · backend arrays · WAN link (Metro/Geo)              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VPLEX              = Dell storage federation; aggregates arrays into virtual volumes across vendo  │
│    Virtual volume     = VPLEX-abstracted LUN presented to hosts; backend is array LUNs                │
│    VPLEX Metro        = synchronous active-active stretch cluster; same VV served from two sites      │
│    VPLEX Geo          = asynchronous active-active replication; higher RPO, no distance constraint    │
│    Distributed VV     = virtual volume spanning two sites for Metro active-active host access         │
│    Witness            = third-site quorum arbiter for Metro; prevents split-brain island scenarios    │
│    WAN-COM            = WAN communication module in VPLEX Geo; manages inter-site replication traffi  │
│    Management Server  = embedded Linux VM in VPLEX engine; serves web UI and vplex CLI                │
│    Consistency group  = set of virtual volumes that failover together maintaining write order         │
│    Backend volume     = LUN from underlying array presented to VPLEX engine for virtualisation        │
│    Local device       = RAID device or extent of backend volumes on a single VPLEX cluster            │
│    Cluster            = single VPLEX installation; Metro topology requires exactly two clusters       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Inbound — Management

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin workstations | Unisphere for VPLEX web UI and REST API |
| 22 | TCP | Jump hosts | SSH — VPLEX management server CLI |
| 443 | TCP | VMware vCenter, vRO | VPLEX vSphere plugin API |

## Outbound — Management Server to External

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 162 | UDP | SNMP receiver | SNMP traps |
| 514 | UDP | Syslog server | Syslog forwarding |
| 123 | UDP | NTP | Time sync |
| 443 | TCP | esrs.dell.com | ESRS support phone-home |

## VPLEX Metro — WAN COM Link (Between Sites)

For VPLEX Metro (active-active across sites), the VPLEX management servers communicate across the WAN:

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 443 | TCP | VPLEX Management Server (Site A) ↔ VPLEX Management Server (Site B) | VPLEX cluster management communication across WAN COM link |

The actual data path between VPLEX clusters uses fibre channel ISL or iSCSI — not IP-routed through a firewall in most deployments.

## Host Connectivity (iSCSI)

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 3260 | TCP | iSCSI initiator hosts | iSCSI front-end connections to VPLEX (if iSCSI front-end configured) |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin clients | VPLEX mgmt IP | 443, 22 | UI and CLI |
| VPLEX Site A mgmt | VPLEX Site B mgmt | 443 | Metro WAN COM link |
| iSCSI hosts | VPLEX iSCSI front-end | 3260 | Block (if iSCSI front-end) |
| VPLEX | ESRS | 443 | Support phone-home |

## Verify

```bash
# From admin workstation — test Unisphere for VPLEX
curl -sk -o /dev/null -w "%{http_code}" https://<vplex-mgmt-ip>/vplex/v2/version

# From Site A VPLEX mgmt — test Site B WAN COM reachability
nc -zv <site-b-vplex-mgmt-ip> 443
```

## See also

- [Dell VPLEX — Architecture](how-it-works/)
- [Dell VPLEX — Operations](../operations/)
- [Dell RecoverPoint — Ports](../../recoverpoint/architecture/ports/)
