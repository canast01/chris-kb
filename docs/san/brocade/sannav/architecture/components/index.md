# SANnav — Components

> Part of the [SANnav](../../) reference.

---

## Overview

SANnav Management Portal is a monolithic virtual appliance containing all management services. This page documents the key internal components, their responsibilities, and the ports and dependencies that matter for infrastructure teams managing the appliance.

---

## Core Services

### Discovery Engine

The discovery engine is the component responsible for learning and maintaining the fabric topology. It operates in two modes:

- **Active polling** — SANnav initiates HTTPS REST API calls to each managed switch at a configurable interval (default: 30 seconds for health, 5 minutes for topology). Switch credentials are stored encrypted in the SANnav database.
- **Event-driven** — SNMP traps from switches trigger immediate re-polling of affected fabric segments. Trap-driven updates handle link events, zone changes, and port state transitions within seconds.

Discovery scope covers:
- Switch identity, model, firmware version, license state
- Port inventory: port number, type (E_Port, F_Port, N_Port), WWN, speed, operational state
- Attached device WWNs (host HBAs and storage array ports)
- ISL topology and path diversity
- Zone configuration (active and defined zone sets)

### Event Engine

The event engine receives and processes all SNMP traps from managed switches. It evaluates traps against configured alert policies and forwards matching events to:
- The SANnav event dashboard
- Email recipients
- Upstream SNMP trap receivers (NMS / SIEM)
- Webhook endpoints (configured under **Administration > Alert Policies > Forwarding**)

SNMP trap receipt requires switches to be configured with SANnav's management IP as a trap destination. Switches must also have SNMPv3 configured with credentials matching those entered in SANnav.

### MAPS Analytics Engine

The MAPS (Monitoring and Alerting Policy Suite) engine reads MAPS policy violation data from each switch. MAPS policies are configured on the switches themselves; SANnav does not push MAPS policies but collects violations and surfaces them in the dashboard.

SANnav aggregates MAPS violations across all managed switches, allowing fabric-wide views such as: "show all switches with CRC error violations in the last 24 hours."

### SAN Analytics

SAN Analytics is a separate licensed feature available on Gen 6 and Gen 7 switches. When enabled on the switch, the switch streams I/O performance telemetry (IOPS, throughput, exchange completion time) at per-port or per-flow granularity to SANnav.

SANnav stores this telemetry in its internal InfluxDB time-series database and renders it in the **SAN Analytics** dashboard. Retention period is configurable (default: 30 days).

Requirements:
- SAN Analytics license on each switch
- Sufficient SANnav storage (high-frequency per-flow data is large)
- NTP synchronization between switches and SANnav (timestamps must align)

### Zone Manager

The Zone Manager component provides the GUI-based zoning workflow. Zone changes made in the SANnav UI are compiled into FOS zoning commands and pushed to the switch via HTTPS. SANnav maintains a local copy of the zone database for offline viewing and comparison.

Supported operations:
- Create/edit/delete zones and zone aliases
- Activate zone sets
- Clone zone sets between VSANs or fabrics
- Import/export zone configurations

### Image Management

The Image Management component is a firmware repository and staged upgrade engine. It allows operators to:
- Upload FOS firmware images to SANnav
- Push firmware to individual switches or switch groups
- Schedule firmware activation (can be deferred to a maintenance window)
- Monitor upgrade progress and roll back if activation fails

Switches are upgraded non-disruptively using FOS hitless upgrade where supported. Dual-CP directors complete the upgrade with no I/O disruption.

---

## Internal Ports and Services

| Port | Protocol | Service | Direction |
|---|---|---|---|
| 443 | HTTPS | Web UI and REST API (inbound) | Client → SANnav |
| 443 | HTTPS | Switch management API calls | SANnav → switch |
| 161 | UDP/SNMP | SNMP polling | SANnav → switch |
| 162 | UDP/SNMP | SNMP trap receiver | Switch → SANnav |
| 636 | LDAPS | LDAP authentication | SANnav → AD/LDAP |
| 25/587 | SMTP | Email alert delivery | SANnav → mail relay |
| 123 | UDP/NTP | Time synchronization | SANnav → NTP |
| 22 | SSH | SANnav appliance CLI (admin access) | Admin → SANnav |
| 5432 | TCP | PostgreSQL (internal, localhost only) | Internal |
| 8086 | TCP | InfluxDB time-series DB (internal) | Internal |

External exposure: only ports 443, 162, and 22 need to be reachable from outside the SANnav appliance. PostgreSQL and InfluxDB are bound to localhost and not externally accessible.

---

## Database Components

| Database | Type | Purpose | Location |
|---|---|---|---|
| PostgreSQL | Relational | Config, inventory, users, events, jobs | `/opt/sannav/data/postgres` |
| InfluxDB | Time-series | SAN Analytics performance data | `/opt/sannav/data/influxdb` |

Both databases are embedded and managed by the SANnav appliance startup scripts. External database servers are not supported.

Backup of both databases is performed by the SANnav backup function (see [Backup & Restore](../backup-restore/)). Do not back up database directories directly while SANnav is running.

---

## Service Health Verification (Appliance CLI)

Access the appliance CLI via SSH (default user: `sannav` or `admin` depending on version):

```bash
# Check overall service status
sannav status

# Expected output shows services: running
# Services: sannav-ui, sannav-server, postgres, influxdb, nginx, rabbitmq

# Show current SANnav version
sannav version

# Check disk usage — alert if >80%
df -h /opt/sannav

# Review application logs
tail -f /opt/sannav/logs/server.log
tail -f /opt/sannav/logs/discovery.log

# Review event engine logs
tail -f /opt/sannav/logs/event-engine.log
```

---

## License Components

SANnav licensing is per managed switch port. Licenses are applied to the SANnav appliance, not to individual switches.

| License Type | Scope |
|---|---|
| Base license | Fabric discovery, inventory, zoning, MAPS monitoring, image management |
| SAN Analytics license | Per-port and per-flow I/O analytics (requires switch SAN Analytics license too) |
| Global View license | SANnav Global View appliance |

Licenses are applied via **Administration > License Management** in the GUI or via the REST API. Expired licenses revert to a read-only monitoring mode; no configuration changes can be pushed to switches.

Check license status:

```
GET /rest/license
Authorization: Bearer <token>
```

---

## Dependency Summary

| Dependency | Required | Notes |
|---|---|---|
| VMware ESXi or KVM | Yes | Hypervisor for appliance |
| NTP server | Yes | For telemetry timestamps and log correlation |
| DNS resolution | Recommended | For email, LDAP, and external integrations |
| SMTP relay | Recommended | For email alert delivery |
| LDAP / Active Directory | Optional | For SSO; local accounts work without LDAP |
| vCenter | Optional | For host-side WWN visibility |
| Syslog receiver | Optional | For SIEM integration |
