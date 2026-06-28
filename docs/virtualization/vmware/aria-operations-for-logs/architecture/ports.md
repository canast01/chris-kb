---
tags:
  - aria-operations-for-logs
  - vrli
  - log-insight
  - networking
  - firewall
  - ports
  - logging
---
# Aria Operations for Logs — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for VMware Aria Operations for Logs (formerly vRealize Log Insight). Covers the cluster Integrated Load Balancer (ILB) for UI and syslog ingest, log forwarding, and outbound integration with Aria Operations.

*Applies to: Aria Operations for Logs 8.x / 2403+*
</div>
![Aria Operations for Logs — Ports and Network Requirements](../../../../assets/virtualization-vmware-aria-operations-for-logs-architecture-.svg)

## Before you begin

- Aria Operations for Logs uses an Integrated Load Balancer (ILB) with a virtual IP — open all inbound ports to the ILB VIP, not individual node IPs
- Syslog ingest accepts both UDP 514 and TCP 514 — use TCP for reliable delivery; UDP for high-volume, low-criticality sources
- The Aria Log agent (CFAPI) uses port 9543 (TLS) for agent-based ingest from Windows/Linux hosts
- Cluster-internal communication between the master and worker nodes uses 9000 TCP — this does not need to cross external firewalls if nodes are on the same L2

---

## Inbound — Client to Aria Operations for Logs Cluster

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin browsers, REST API clients | Aria Logs web UI and API |
| 22 | TCP | Jump hosts | SSH — appliance management |
| 5480 | TCP | Admin workstations | VAMI appliance management |

---

## Inbound — Log Sources to Cluster ILB

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 514 | UDP | ESXi hosts, vCenter, network devices, legacy syslog sources | Syslog ingest (UDP) |
| 514 | TCP | App servers, network devices (reliable syslog) | Syslog ingest (TCP / RFC 6587) |
| 1514 | TCP | Syslog sources (alternate port) | Syslog over TLS (SYSLOG-TLS, RFC 5425) |
| 9543 | TCP | Hosts running Aria Log Agent (Windows/Linux) | CFAPI — TLS-secured agent-based log collection |

---

## Cluster Internal — Master to Worker Nodes

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 9000 | TCP | Master node → Worker nodes | Internal log forwarding — event distribution across cluster |
| 443 | TCP | Cluster nodes | Internal API and ILB health checks |

---

## Outbound — Aria Logs Integration

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | Aria Operations (vROPS) | Alert and event forwarding to Aria Operations |
| 514 | UDP/TCP | Remote syslog server (if forwarding configured) | Log forwarding to external SIEM or syslog aggregator |
| 9000 | TCP | Remote Aria Logs cluster | Cross-cluster log forwarding |

---

## Outbound — External Services

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | *.vmware.com, *.broadcom.com | License check, content pack downloads |
| 123 | UDP | NTP servers | Time synchronisation — critical for log timestamp accuracy |
| 25 | TCP | SMTP relay | Alert email delivery |
| 389/636 | TCP | Active Directory DCs | Admin user authentication |
| 88 | TCP/UDP | Active Directory DCs | Kerberos |

---

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin browsers | Aria Logs ILB VIP | 443 | UI and REST API |
| ESXi / vCenter | Aria Logs ILB VIP | 514 UDP | vSphere syslog — configure in vCenter Advanced Settings |
| App servers | Aria Logs ILB VIP | 514 TCP | Reliable syslog |
| Aria Log Agents | Aria Logs ILB VIP | 9543 | Encrypted agent-based log ingest |
| Network devices | Aria Logs ILB VIP | 514 UDP | Network syslog |
| Aria Logs | Aria Operations | 443 | Alert/event integration |
| Aria Logs | SIEM / syslog | 514 | Forwarding to external log target |

---

## Verify

```bash
# From admin workstation — test Aria Logs UI
curl -sk -o /dev/null -w "%{http_code}" https://<aria-logs-vip>/

# From ESXi host — verify syslog is configured to send to Aria Logs
esxcli system syslog config get | grep -i remote

# From a Linux app server — test UDP syslog ingest
logger -n <aria-logs-vip> -P 514 -d -t test "port verify message"

# From a Linux host — test TCP syslog
nc -w 2 <aria-logs-vip> 514 < /dev/null && echo "TCP 514 open"

# From Aria Logs SSH — test NTP
ntpq -p

# From Aria Logs SSH — test Aria Operations integration
curl -sk -o /dev/null -w "%{http_code}" https://<aria-ops-fqdn>/suite-api/api/resources
```

---

## See also

- [Aria Operations for Logs — Architecture](../how-it-works/)
- [Aria Operations for Logs — Deploy](../../deploy/)
- [Aria Operations — Ports](../../aria-operations/architecture/ports.md)
- [vCenter — Ports](../../vcenter/architecture/ports.md)
