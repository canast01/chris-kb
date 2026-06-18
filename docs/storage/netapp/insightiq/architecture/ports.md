---
tags:
  - insightiq
  - netapp
  - networking
  - firewall
  - ports
  - monitoring
---
# NetApp InsightIQ — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for NetApp InsightIQ. InsightIQ is a performance analytics tool that collects and displays performance data from PowerScale (Isilon) clusters. It runs as a virtual appliance and polls clusters over the management network.

*Applies to: NetApp InsightIQ 4.x (formerly Isilon InsightIQ)*
</div>

## Network Zones

```
┌──────────────────┐         ┌──────────────────────────────────────────────────────────────────────────┐
│  Admin Browsers  │──443───▶│  InsightIQ Virtual Appliance                                             │
└──────────────────┘         │  (Linux VM, runs PostgreSQL       │
                             │  + web service internally)        │
                             └──────────────┬───────────────────┘
                                            │
                                    8080 or 443 (outbound)
                                            │
                             ┌──────────────▼───────────────────┐
                             │  PowerScale / OneFS Cluster      │
                             │  (SmartConnect zone or           │
                             │   management IP)                 │
                             └──────────────────────────────────┘
```

## Inbound — Admin to InsightIQ

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin browsers | InsightIQ web UI (HTTPS) |
| 22 | TCP | Jump hosts | SSH — InsightIQ appliance OS access |

## InsightIQ to PowerScale (Outbound)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 8080 | TCP | InsightIQ appliance | PowerScale SmartConnect / mgmt IP | OneFS platform API — performance data collection |
| 443 | TCP | InsightIQ appliance | PowerScale mgmt IP | Newer InsightIQ versions use HTTPS for platform API |

## InsightIQ to Support / Updates (Outbound)

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | support.emc.com, netapp.com | Software updates and support registration |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin browsers | InsightIQ appliance | 443 | Web UI — management network |
| InsightIQ appliance | PowerScale mgmt/SmartConnect | 8080 or 443 | API polling — required for data collection |

## Verify

```bash
# From InsightIQ appliance — test PowerScale API reachability
curl -sk -o /dev/null -w "%{http_code}" https://<powerscale-mgmt>:8080/platform/latest/

# From admin workstation — test InsightIQ UI
curl -sk -o /dev/null -w "%{http_code}" https://<insightiq-ip>/

# From InsightIQ appliance — connectivity test to PowerScale
nc -zv <powerscale-mgmt-ip> 8080
```

## See also

- [NetApp InsightIQ — Architecture](how-it-works/)
- [Dell PowerScale — Ports](../../../dell/powerscale/architecture/ports.md)
- [NetApp ONTAP — Ports](../../ontap/architecture/ports.md)
