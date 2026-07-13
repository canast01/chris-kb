---
tags:
  - linux
  - compute
  - networking
  - firewall
  - ports
description: "Firewall port reference for Linux servers in a managed enterprise environment. Covers management access, monitoring, and the outbound ports required to..."
---
# Linux — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Linux servers in a managed enterprise environment. Covers management access, monitoring, and the outbound ports required to keep Linux hosts updated and managed.

*Applies to: RHEL 8+ / Ubuntu 22.04+ and derivatives*
</div>
![Linux — Ports and Network Requirements](../../../assets/compute-linux-architecture-ports.svg)

## Before you begin

- SSH (22) is the primary management channel — restrict to jump host source IPs in firewall rules and `/etc/ssh/sshd_config`
- Monitoring agents (Prometheus node_exporter, Zabbix agent) listen locally and are scraped or polled from the monitoring server
- Linux hosts need outbound access to package repositories for patching — restrict to approved mirror IPs in locked-down environments

---

## Inbound — Management Access

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 22 | TCP | Jump hosts, Ansible control node, management systems | SSH — primary management channel; restrict source IPs |

---

## Inbound — Monitoring Agents

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 9100 | TCP | Prometheus scraper | node_exporter — OS metrics (CPU, memory, disk, network) |
| 9090 | TCP | Prometheus scraper | Prometheus (if node acts as Prometheus server) |
| 10050 | TCP | Zabbix Server / Proxy | Zabbix agent (passive mode — Zabbix polls the agent) |

---

## Outbound — Monitoring and Event Reporting

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 10051 | TCP | Zabbix Server / Proxy | Zabbix agent active mode — agent pushes data to Zabbix |
| 162 | UDP | SNMP trap receiver | SNMP traps (if SNMP agent configured with trap destination) |
| 514 | UDP/TCP | Syslog server | rsyslog/syslog-ng forwarding |

---

## Outbound — Time, DNS, and Updates

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 123 | UDP | NTP server | chronyd/ntpd time synchronisation |
| 53 | TCP/UDP | DNS server | Name resolution |
| 443 | TCP | Package repos (RHEL satellite, Ubuntu mirror, EPEL) | OS and package updates (dnf/apt) |
| 443 | TCP | Red Hat CDN / RHSM server | Red Hat subscription registration (RHEL) |

---

## Application Ports

Application services (web servers, databases, etc.) expose their own ports on top of the base OS. See:
- [MySQL — Ports](../../mysql/architecture/ports/)
- [PostgreSQL — Ports](../../postgresql/architecture/ports/)

---

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Jump hosts | Linux host | 22 | SSH — restrict to jump host IPs only |
| Ansible / automation | Linux host | 22 | Same SSH channel |
| Prometheus | Linux host | 9100 | node_exporter scrape |
| Zabbix Server | Linux host | 10050 | Zabbix passive agent poll |
| Linux host | Syslog server | 514 UDP | Event log forwarding |
| Linux host | NTP server | 123 UDP | Time sync |
| Linux host | Package repo | 443 | OS patching |

---

## Verify

```bash
# From jump host — test SSH
ssh -o ConnectTimeout=5 user@<linux-host> uptime

# From Prometheus server — test node_exporter
curl -s http://<linux-host>:9100/metrics | head -5

# From Linux host — test NTP sync
chronyc tracking | grep "System time"

# From Linux host — test outbound DNS
dig @<dns-server> corp.local

# From Linux host — test package repo connectivity
curl -sk -o /dev/null -w "%{http_code}" https://<satellite-or-repo-host>/
```


```text title="Expected output"
13:47:22 up 42 days, 3:15, 1 user, load average: 0.12, 0.08, 0.05
# HELP node_cpu_seconds_total Seconds the cpus spent in each mode.
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="user"} 8847.23
node_cpu_seconds_total{cpu="0",mode="system"} 1203.45
System time offset      : 0.000012345 seconds slow of NTP time
; <<>> DiG 9.16.23-RH <<>> @10.20.30.40 corp.local
; (1 server found)
;; Query time: 12 msec
;; SERVER: 10.20.30.40#53(10.20.30.40)
;; WHEN: Wed Jan 15 13:47:35 UTC 2025
;; MSG SIZE  rcvd: 87
200
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ssh: connect to host <linux-host> port 22: Connection timed out` | Verify the host is reachable with `ping <linux-host>` and check firewall rules allow SSH from the jump host. |
    | `curl: (7) Failed to connect to <linux-host> port 9100: Connection refused` | Confirm node_exporter is running with `systemctl status node_exporter` and listening on port 9100. |
    | `dig: couldn't get address for '<dns-server>': not known` | Replace `<dns-server>` with a valid IP address (e.g., `8.8.8.8`) or verify DNS server hostname resolves. |
---

## See also

- [Linux — Architecture](../how-it-works/)
- [Linux — Operations](../../operations/)
- [MySQL — Ports](../mysql/architecture/ports.md)
- [PostgreSQL — Ports](../postgresql/architecture/ports.md)
- [Ansible — Ports](../../../automation/ansible/architecture/ports.md)
