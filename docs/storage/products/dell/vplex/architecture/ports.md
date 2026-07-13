---
tags:
  - vplex
  - dell
  - networking
  - firewall
  - ports
  - storage
  - federation
description: "Firewall port reference for Dell VPLEX (storage federation / virtualization). Covers management, WAN COM link between VPLEX clusters (for VPLEX Metro)..."
---
# Dell VPLEX — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell VPLEX (storage federation / virtualization). Covers management, WAN COM link between VPLEX clusters (for VPLEX Metro), and host connectivity.

*Applies to: VPLEX GeoSynchrony 6.x*
</div>
![Dell VPLEX — Ports and Network Requirements](../../../../../assets/storage-dell-vplex-architecture-ports.svg)

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


```text title="Expected output"
200
Connection to 192.168.100.45 port 443 [tcp/https] succeeded!
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip certificate verification, or import the VPLEX management certificate into your system CA bundle. |
    | `nc: getaddrinfo: Name or service not known` | Verify the Site B VPLEX management IP address is correct and reachable from Site A; check DNS resolution or use the IP address directly instead of a hostname. |
## See also

- [Dell VPLEX — Architecture](../how-it-works/)
- [Dell VPLEX — Operations](../../operations/)
- [Dell RecoverPoint — Ports](../../recoverpoint/architecture/ports.md)
