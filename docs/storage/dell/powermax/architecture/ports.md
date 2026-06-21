---
tags:
  - powermax
  - dell
  - vmax
  - networking
  - firewall
  - ports
  - storage
---
# Dell PowerMax — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell PowerMax (formerly VMAX). Covers Unisphere for PowerMax management, iSCSI data paths, and SRDF replication. FC fabric paths are not IP-based.

*Applies to: PowerMax 2500 / 8500 / PowerMaxOS 10.x*
</div>
![Dell PowerMax — Ports and Network Requirements](../../../../assets/storage-dell-powermax-architecture-ports.svg)





## Inbound — Management

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 8443 | TCP | Admin workstations | Unisphere for PowerMax web UI and REST API (primary) |
| 443 | TCP | Admin workstations | Unisphere alternate HTTPS port |
| 22 | TCP | Jump hosts | SSH — Solutions Enabler / symcli management |

## Outbound — Array to External

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 162 | UDP | SNMP receiver | SNMP traps |
| 514 | UDP | Syslog server | Syslog forwarding |
| 123 | UDP | NTP | Time sync |
| 443 | TCP | esrs.dell.com, cloudiq.dell.com | ESRS / CloudIQ support phone-home |

## iSCSI (SAN)

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 3260 | TCP | iSCSI initiator hosts | iSCSI block storage (PowerMax iSCSI ports) |

## SRDF Replication (if iSCSI-based SRDF)

For SRDF/Star, SRDF/Metro, or SRDF/A configured over IP links:

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 3260 | TCP | Source PowerMax iSCSI port → Target PowerMax | SRDF over iSCSI |

Fibre Channel SRDF uses FC fabric — no IP ports needed.

## Solutions Enabler (SYMCLI) Host-Based Management

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 2707 | TCP | SYMCLI host | SE server / GigE port on array | Solutions Enabler daemon (storEd) |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin clients | PowerMax | 8443 | Unisphere UI |
| SYMCLI hosts | PowerMax | 2707 | Solutions Enabler CLI |
| iSCSI hosts | PowerMax iSCSI ports | 3260 | Block access |
| Source PowerMax | Target PowerMax | 3260 | SRDF/A over IP (if iSCSI SRDF) |
| PowerMax | ESRS / CloudIQ | 443 | Support telemetry |

## Verify

```bash
# From admin workstation — test Unisphere API
curl -sk -o /dev/null -w "%{http_code}" https://<powermax-mgmt-ip>:8443/univmax/restapi/version

# From iSCSI host — discover targets
iscsiadm -m discovery -t sendtargets -p <powermax-iscsi-ip>:3260
```

## See also

- [Dell PowerMax — Architecture](how-it-works/)
- [Dell PowerMax — Operations](../operations/)
- [Dell SRDF-A — Ports](../../srdf-a/architecture/ports.md)
- [Dell SRDF-S — Ports](../../srdf-s/architecture/ports.md)
