---
tags:
  - aria-operations
  - vrops
  - networking
  - firewall
  - ports
  - monitoring
---
# Aria Operations — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for VMware Aria Operations (formerly vRealize Operations). Covers the analytics cluster UI/API, remote collectors, adapter connections to vCenter/NSX/ESXi, and outbound services.

*Applies to: Aria Operations 8.x / 2403+*
</div>

```text
┌─────────────────────── Aria Operations — Network Traffic Zones ───────────────────────────────────────┐
│                                                                                                       │
│  Consumer Zone          Analytics Cluster            Infrastructure Zone                              │
│  ──────────────         ──────────────────           ────────────────────                             │
│  Browsers  ──443──► Aria Operations     ──443──► vCenter (vSphere adapter)                            │
│  API clients──443──► (cluster VIP)      ──443──► NSX Manager (NSX adapter)                            │
│                                         ──443/5988──► ESXi hosts (host adapter)                       │
│                                         ──161 UDP──► SNMP devices                                     │
│                                         ──22──► Linux hosts (SSH adapter)                             │
│             Remote Collector ──3331──► Analytics Cluster (remote sites)                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- Aria Operations analytics cluster runs as 3 nodes (master, replica, data) — all nodes share a cluster VIP; open ports to the VIP and all node IPs
- Remote Collectors can be deployed in remote sites or DMZs to reduce the number of firewall holes — Remote Collector contacts the analytics cluster on 3331, and the analytics cluster does not need to reach back
- All adapters (vSphere, NSX, SNMP, SSH, etc.) are installed on the analytics cluster or remote collector — open the adapter's target ports from whichever node runs the adapter

---

## Inbound — Client to Aria Operations Cluster

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin browsers, REST API clients, Aria Automation (cost integration) | Aria Operations UI and REST API |
| 22 | TCP | Jump hosts | SSH — appliance and node management |
| 5480 | TCP | Admin workstations | VAMI appliance management |

---

## Remote Collector to Analytics Cluster

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 3331 | TCP | Remote Collector appliance | Analytics Cluster VIP / all nodes | Collector-to-cluster registration and data forwarding |
| 443 | TCP | Analytics Cluster | Remote Collector | Cluster management of remote collector (pushed config) |

---

## Aria Operations Analytics Cluster — Adapter Connections

### vSphere Adapter (vCenter)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Aria Operations / Remote Collector | vCenter Server | vSphere API — VM, host, cluster, datastore metrics |

### NSX Adapter

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Aria Operations / Remote Collector | NSX Manager | NSX REST API — transport nodes, logical components, DFW stats |

### ESXi Host Adapter

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Aria Operations / Remote Collector | ESXi host management IPs | ESXi HTTPS API (host-level hardware and performance) |
| 5988 | TCP | Aria Operations / Remote Collector | ESXi host management IPs | CIM/WBEM — hardware health monitoring |
| 5989 | TCP | Aria Operations / Remote Collector | ESXi host management IPs | CIM/WBEM over HTTPS |

### SNMP Adapter (Network Devices, Storage, UPS)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 161 | UDP | Aria Operations / Remote Collector | SNMP-managed devices | SNMP polling (GET) |
| 162 | UDP | SNMP-managed devices | Aria Operations | SNMP traps (inbound alerts) |

### SSH Adapter (Linux Hosts)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 22 | TCP | Aria Operations / Remote Collector | Linux hosts | SSH — OS-level metrics collection |

### Database Adapters (MySQL, PostgreSQL, MSSQL)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 3306 | TCP | Aria Operations / Remote Collector | MySQL servers | MySQL adapter metrics |
| 5432 | TCP | Aria Operations / Remote Collector | PostgreSQL servers | PostgreSQL adapter metrics |
| 1433 | TCP | Aria Operations / Remote Collector | SQL Server hosts | MSSQL adapter metrics |

---

## Aria Operations — Internal Cluster Ports

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 443 | TCP | Cluster nodes | Internal API and VIP routing |
| 5480 | TCP | Analytics Cluster | Remote Collectors | VAMI lifecycle operations |

---

## Outbound — External Services

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | *.vmware.com, *.broadcom.com | License check, content pack downloads |
| 123 | UDP | NTP server | Time synchronisation |
| 514 | UDP/TCP | Syslog server | Log forwarding |
| 25 | TCP | SMTP relay | Alert email delivery |
| 389/636 | TCP | Active Directory DCs | User authentication (LDAP/LDAPS) |
| 88 | TCP/UDP | Active Directory DCs | Kerberos |

---

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin browsers | Aria Operations VIP | 443 | UI and API |
| Remote Collector | Analytics Cluster | 3331 | Remote site data path |
| Aria Operations / RC | vCenter | 443 | vSphere adapter |
| Aria Operations / RC | NSX Manager | 443 | NSX adapter |
| Aria Operations / RC | ESXi hosts | 443, 5988 | Host adapter |
| Aria Operations / RC | SNMP devices | 161 UDP | SNMP polling |
| SNMP devices | Aria Operations | 162 UDP | SNMP traps (inbound) |
| Aria Operations / RC | Linux hosts | 22 | SSH adapter |

---

## Verify

```bash
# From admin workstation — test Aria Operations API
curl -sk -o /dev/null -w "%{http_code}" https://<aria-ops-fqdn>/suite-api/api/resources

# From Aria Operations SSH — test vCenter reachability
curl -sk -o /dev/null -w "%{http_code}" https://<vcenter-fqdn>/rest/com/vmware/cis/session

# From Aria Operations SSH — test NSX adapter connectivity
curl -sk -o /dev/null -w "%{http_code}" https://<nsx-manager-ip>/api/v1/cluster/status

# From Aria Operations SSH — test SNMP polling to a device
snmpget -v2c -c <community> <device-ip> 1.3.6.1.2.1.1.1.0

# From Remote Collector — test cluster connectivity
nc -zv <aria-ops-vip> 3331
```

---

## See also

- [Aria Operations — Architecture](how-it-works/)
- [Aria Operations — Deploy](../deploy/)
- [Aria Operations — Operations](../operations/)
- [Aria Automation — Ports](../../aria-automation/architecture/ports/)
- [vCenter — Ports](../../vcenter/architecture/ports/)
