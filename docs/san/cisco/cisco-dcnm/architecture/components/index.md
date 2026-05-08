# Cisco DCNM — Components

> Part of the [Cisco DCNM](../../) reference.

---

## Overview

DCNM 11.x is a monolithic application (Java/Tomcat) running on a Linux-based virtual appliance. This page covers the internal components, discovery architecture, and the switch-side configuration DCNM requires.

---

## Core Services

| Service | Role |
|---|---|
| DCNM Server (Java/Tomcat) | Main application logic, REST API, GUI back-end |
| Web UI (DCNM SAN Client) | Browser-based (JavaFX) and web client for SAN management |
| PostgreSQL | Configuration, inventory, user, event, and topology data |
| SNMP Engine | SNMP v1/v2c/v3 polling, trap reception |
| Syslog Receiver | Syslog collection from managed switches |
| Discovery Manager | SSH-based device discovery, topology crawl |
| Performance Manager (PM) | SNMP MIB polling for interface and fabric statistics |
| Event Manager | Event processing, correlation, and forwarding |
| Image Management | Firmware repository for MDS NX-OS image staging |
| Report Engine | Scheduled report generation and delivery |
| License Manager | DCNM license enforcement and tracking |

---

## Discovery Architecture

DCNM discovers MDS switches using a seed-based approach:

1. Operator provides one or more seed switch IPs via **SAN > Fabrics > Discover**
2. DCNM connects to the seed switch via SSH using the provided credentials
3. DCNM runs `show cdp neighbors detail` and `show topology` to enumerate connected switches
4. DCNM recursively discovers all reachable switches in the fabric
5. SNMP is used for MIB-based inventory (port WWN, FC ID, etc.)

Discovery credentials must be an account with at least `network-operator` role on MDS switches. `network-admin` is required if DCNM will push configuration (zones, device aliases, VSAN config).

### Switch-Side Prerequisites

```bash
# On each MDS switch (NX-OS CLI)

# Enable SSH
feature ssh
ssh key rsa 2048

# Create DCNM service account
username dcnm_mgmt password <password> role network-admin

# Enable SNMPv3 for DCNM polling
snmp-server user dcnm_poll network-admin v3 auth sha <auth-pass> priv aes-128 <priv-pass>

# Configure DCNM as SNMP trap destination
snmp-server host <dcnm-ip> traps version 3 priv dcnm_poll

# Configure DCNM as syslog destination
logging server <dcnm-ip> 5 use-vrf management facility local7

# Verify
show snmp user
show logging server
```

---

## DCNM Internal Ports

| Port | Protocol | Service | Direction |
|---|---|---|---|
| 443 | HTTPS | Web UI (browser access) | Client → DCNM |
| 80 | HTTP | Redirect to HTTPS | Client → DCNM |
| 22 | SSH | DCNM SSH to switches | DCNM → switch |
| 161 | UDP | SNMP polling | DCNM → switch |
| 162 | UDP | SNMP trap receiver | Switch → DCNM |
| 514 | UDP | Syslog receiver | Switch → DCNM |
| 7543 | TCP | DCNM SAN Client (legacy thick client) | Client → DCNM |
| 2443 | TCP | gRPC (DCNM → Nexus Dashboard in hybrid deployments) | DCNM → ND |
| 5432 | TCP | PostgreSQL (HA sync) | DCNM nodes |
| 5000 | TCP | HA heartbeat | DCNM nodes |

---

## SAN Management Functional Areas

### VSAN Management

DCNM provides full VSAN lifecycle management:
- Create, modify, and delete VSANs
- Assign switch ports to VSANs
- Configure VSAN trunking on ISL ports

Navigate to **SAN > VSANs** to manage VSAN configurations. Changes are pushed to switches via SSH.

### Zone Management

DCNM provides a zone management workflow with:
- Zone creation by WWN or device alias
- Zone set management (create, activate, deactivate)
- Zone merge conflict detection across the fabric
- Zone set comparison (before/after diff)

Navigate to **SAN > Zoning** to access the zone editor.

### Device Alias Management

Device aliases are fabric-wide FC name assignments. DCNM manages device aliases using Cisco Fabric Services (CFS) for distribution:

Navigate to **SAN > Device Alias**:
- Create aliases: map WWN to a meaningful name (e.g., `esxi01-hba0`)
- Edit existing aliases
- Commit CFS distribution to push aliases to all switches

### ISL Monitoring

Navigate to **SAN > ISLs** for a per-fabric ISL view showing:
- ISL state (up/down)
- Utilization (Rx/Tx bps and %)
- CRC error counters
- ISL trunk VSAN membership

---

## Database

| Component | Database | Tables (key) |
|---|---|---|
| Inventory | PostgreSQL (sane) | switches, ports, hosts, enddevices |
| Zones | PostgreSQL (sane) | zonedb, zoneset, zonealiases |
| Events | PostgreSQL (sane) | events, traps, alarms |
| Performance | PostgreSQL (pmdb) | pmdata (interface counters) |
| Users | PostgreSQL (sane) | users, roles, groups |

Database size grows with the number of managed devices and event history retention. Monitor disk usage at `/var/lib/pgsql/` on the DCNM appliance.

---

## Image Management Component

DCNM's Image Management stores MDS NX-OS images and automates staged upgrades:

1. Navigate to **Administration > Image Management > Upload Image**
2. Upload the MDS NX-OS `.bin` image
3. Navigate to **Administration > Image Management > Upgrade**
4. Select target switches and firmware version
5. Schedule or execute immediately

MDS switches support In-Service Software Upgrade (ISSU) on dual-supervisor platforms (MDS 9706, 9710, 9718). ISSU allows firmware upgrades without disrupting active I/O.

---

## Performance Manager (PM)

PM polls SNMP interface counters from managed switches at a configurable interval (default: 5 minutes for most counters, 1 minute for critical ISLs).

Polled data includes:
- Port Rx/Tx throughput (bytes/sec)
- Port error counters (CRC, signal loss, encoding error)
- ISL utilization
- VSAN traffic breakdown (on supported MDS platforms)

PM data is stored in the PostgreSQL `pmdb` database. Default retention: 30 days. Increase disk allocation if longer retention is required.
