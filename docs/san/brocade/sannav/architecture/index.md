# SANnav — Overview

> Part of the [SANnav](../../) reference.

---

## What Is SANnav

Brocade SANnav is a SAN management platform delivered in two product variants:

- **SANnav Management Portal** — single-fabric or multi-fabric management for day-to-day operations: zoning, firmware management, MAPS policies, performance dashboards, inventory, and event management. Deployed as a standalone virtual appliance (OVA/ISO).
- **SANnav Global View** — a higher-level aggregation layer for large environments with multiple SANnav Management Portal instances. Provides a consolidated dashboard, cross-fabric health summary, and centralised alert aggregation without replacing per-fabric portal instances.

Both products run as Linux-based virtual appliances and communicate with managed switches via HTTPS and SNMP. Switch-side prerequisites are minimal: the switch must have an IP address reachable from SANnav and must have HTTPS enabled.

---

## Deployment Topology

```
┌──────────────────────────────────────────────────────┐
│                  SANnav Global View                  │
│         (single VM, aggregates portal data)          │
└───────────────┬──────────────────┬───────────────────┘
                │                  │
    ┌───────────▼──────┐  ┌────────▼──────────┐
    │ SANnav Portal A  │  │  SANnav Portal B  │
    │  (Fabric A – DC1)│  │  (Fabric B – DC2) │
    └────────┬─────────┘  └────────┬──────────┘
             │                     │
    ┌────────▼──────────────────────▼───────┐
    │     Managed Brocade FC Switches        │
    │  (Gen 6 / Gen 7 directors and edge)    │
    └────────────────────────────────────────┘
```

Each Management Portal instance manages one or more fabrics. A single portal can scale to hundreds of switches; Global View federates across portals with no direct switch communication of its own.

---

## Supported Hardware

SANnav Management Portal and Global View support the following Brocade / Broadcom FC platforms:

| Platform | Gen | Max Ports | Notes |
|---|---|---|---|
| G730 Director | Gen 7 | 384 | 64G FC, NVMe-oF |
| G720 Director | Gen 7 | 192 | 32/64G FC |
| G630 Director | Gen 6 | 384 | 32G FC |
| G620 Director | Gen 6 | 128 | 32G FC |
| G610 Edge Switch | Gen 6 | 24 | 32G FC |
| G720 Edge Switch | Gen 7 | 24 | 64G FC |
| X7-8 Director | Gen 7 | 512 | 64G FC, high density |
| X6-8 Director | Gen 6 | 512 | 32G FC |

Legacy Gen 5 hardware (6510, 6520, DCX 8510) is supported in monitoring mode with reduced feature availability.

---

## Network Requirements

| Communication | Protocol | Port | Direction |
|---|---|---|---|
| SANnav → switch | HTTPS | 443 | Outbound from SANnav |
| SANnav → switch | SNMP v3 | 161/UDP | Outbound from SANnav |
| Switch → SANnav | SNMP trap | 162/UDP | Inbound to SANnav |
| Browser → SANnav | HTTPS | 443 | Inbound to SANnav |
| SANnav → LDAP | LDAPS | 636 | Outbound from SANnav |
| SANnav → SMTP | SMTP | 25 or 587 | Outbound from SANnav |
| Portal → Global View | HTTPS | 443 | Outbound from Portal |
| SANnav → NTP | NTP | 123/UDP | Outbound from SANnav |

SANnav uses the switch's management IP (mgmt VRF). Switches must not be behind NAT from the SANnav perspective, as SNMP trap source IPs are used for switch identification.

---

## VM Sizing

### SANnav Management Portal

| Environment | vCPU | RAM | Storage | Max Switches |
|---|---|---|---|---|
| Small (≤ 50 switches) | 8 | 32 GB | 300 GB | 50 |
| Medium (≤ 150 switches) | 16 | 64 GB | 500 GB | 150 |
| Large (≤ 300 switches) | 24 | 96 GB | 1 TB | 300 |

### SANnav Global View

| Environment | vCPU | RAM | Storage | Max Portals |
|---|---|---|---|---|
| Standard | 8 | 32 GB | 500 GB | 10 |

- OS: CentOS / RHEL 8-based embedded Linux
- Hypervisors supported: VMware ESXi 6.7+, 7.x; KVM (QCOW2 image)
- Storage: thin provisioning is supported; thick provisioning preferred for production

---

## Functional Architecture

SANnav Management Portal is composed of the following internal services:

| Service | Role |
|---|---|
| Web UI (Angular) | Browser-based management console |
| REST API gateway | External API and internal service bus |
| Discovery engine | Continuous fabric topology polling via HTTPS/SNMP |
| Event engine | SNMP trap processing, alert evaluation, email/SNMP forward |
| MAPS analytics | MAPS policy violation monitoring and trending |
| SAN analytics | I/O performance data ingestion and visualization |
| Image management | Firmware repository, staged upgrades |
| Zone manager | Zoning configuration push, alias management |
| Report scheduler | Scheduled report generation and delivery |
| Time-series DB | Performance metric retention (internal InfluxDB) |
| PostgreSQL | Configuration, inventory, user, and event data |

---

## Integration with the Management Stack

In a typical Broadcom SAN environment, SANnav sits alongside:

- **Brocade Network Advisor (BNA)** — legacy predecessor; SANnav replaces BNA and provides migration tooling
- **VMware vCenter** — SANnav can pull host WWN data from vCenter for end-to-end path visibility
- **ServiceNow / ticketing** — alert forwarding via email or webhook (HTTPS POST to webhook endpoints)
- **SIEM** — syslog forwarding from SANnav appliance; SNMP trap forwarding to SIEM/NMS
- **Active Directory / LDAP** — user authentication and group-based role assignment

---

## Upgrade Path

SANnav follows a major.minor.patch version scheme (e.g. 2.4.0). Upgrade is performed via the SANnav Management Portal UI or CLI. In-place upgrades are supported; there is no requirement to re-deploy the appliance for minor or patch releases.

Always review the SANnav Release Notes for the target version before upgrading; some releases require an intermediate hop version rather than a direct upgrade.

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
