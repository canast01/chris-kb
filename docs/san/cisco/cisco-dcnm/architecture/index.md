# Cisco DCNM — Overview

> Part of the [Cisco DCNM](../../) reference.

---

## What Is Cisco DCNM

Cisco Data Center Network Manager (DCNM) is Cisco's SAN and LAN management platform for data center networks. For SAN environments, DCNM provides centralised management of Cisco MDS 9000 Fibre Channel switches and Cisco Nexus switches running FCoE.

**Important:** DCNM was officially renamed to **Nexus Dashboard Fabric Controller (NDFC)** starting with version 12.0 (released 2022). NDFC runs as an application on the Cisco Nexus Dashboard platform. Environments still running DCNM 11.x are using the standalone appliance form factor. This section covers DCNM 11.x. For NDFC 12.x, see the [Nexus Dashboard](../../nexus-dashboard/) section.

---

## DCNM Deployment Models

DCNM 11.x is deployed as a Linux-based virtual appliance (OVA for VMware, ISO for bare metal or KVM).

### Standalone Mode

Single DCNM server. Suitable for environments up to approximately 1,000 managed devices. No high availability.

### Native HA Mode

Two DCNM servers (active + standby) with shared external database (Oracle or PostgreSQL). Requires a Virtual IP (VIP) for client access. Recommended for production environments.

```
┌─────────────────┐         ┌─────────────────┐
│  DCNM Active    │◄──────►│  DCNM Standby   │
│  10.10.5.10     │  HA sync│  10.10.5.11     │
└────────┬────────┘         └─────────────────┘
         │ VIP: 10.10.5.15
         │
┌────────▼────────────────────────────────────┐
│         Managed MDS / Nexus Switches         │
└─────────────────────────────────────────────┘
```

### Federation Mode

Multiple DCNM instances managing separate fabrics, federated under a single login (available in 11.5+). Useful for large environments spanning multiple data centres.

---

## Supported Hardware

| Platform | Role | Notes |
|---|---|---|
| MDS 9132T | 32-port director | 32G FC |
| MDS 9148T | 48-port ToR | 32G FC |
| MDS 9396T | 96-port director | 32G FC |
| MDS 9706 | 6-slot director | 32G FC, modular |
| MDS 9710 | 10-slot director | 32G FC, high density |
| MDS 9718 | 18-slot director | 32G FC, very high density |
| Nexus 5672UP | FCoE/FC (N5K) | FCoE uplinks to MDS |
| Nexus 93180YC-FX | FCoE capable | NX-OS FCoE |

---

## Architecture Overview

DCNM management flow:

1. **Discovery** — DCNM discovers switches via SNMP and SSH/Telnet. SNMPv3 is preferred; SSH credentials are used for configuration push.
2. **Inventory** — Discovered devices are added to the DCNM inventory. Topology is built from CDP/LLDP and SNMP MIB data.
3. **Configuration push** — Zone changes, VSAN configuration, and device alias updates are pushed to switches via SSH (NX-OS CLI) or SNMP.
4. **Monitoring** — SNMP traps, syslog, and performance MIB polling provide real-time and historical monitoring data.
5. **Reporting** — Built-in reporting covers inventory, performance, events, and compliance.

---

## Network Requirements

| Communication | Protocol | Port | Direction |
|---|---|---|---|
| DCNM → switch | SSH | 22 | Outbound from DCNM |
| DCNM → switch | SNMP v3 | 161/UDP | Outbound from DCNM |
| Switch → DCNM | SNMP trap | 162/UDP | Inbound to DCNM |
| Switch → DCNM | Syslog | 514/UDP | Inbound to DCNM |
| Browser → DCNM | HTTPS | 443 | Inbound to DCNM |
| DCNM → LDAP | LDAPS | 636 | Outbound from DCNM |
| DCNM → SMTP | SMTP | 25 | Outbound from DCNM |
| DCNM → NTP | NTP | 123/UDP | Outbound from DCNM |
| DCNM HA sync | TCP | 5432, 5000 | Between DCNM nodes |

---

## VM Sizing (Standalone, 11.x)

| Environment | vCPU | RAM | Storage | Max Switches |
|---|---|---|---|---|
| Small | 8 | 32 GB | 500 GB | 50 |
| Medium | 16 | 64 GB | 1 TB | 200 |
| Large | 24 | 128 GB | 2 TB | 1000 |

Storage: thick provisioning recommended; thin provisioning acceptable with guaranteed reservation.

---

## Relationship to NDFC and Nexus Dashboard

DCNM 11.x is the last standalone appliance release. Cisco's direction is:

- **DCNM 12.x = NDFC** running on Nexus Dashboard
- New feature development is in NDFC only
- DCNM 11.x receives bug fixes and security patches (EoL announced for 2026)

Migration from DCNM 11.x to NDFC 12.x requires a fresh NDFC deployment and re-discovery of managed switches. Configuration migration tooling is provided by Cisco but zone databases and historical data do not migrate automatically.

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
