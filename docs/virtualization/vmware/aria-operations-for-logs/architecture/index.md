# Aria Operations for Logs — Architecture

## Overview

Aria Operations for Logs (formerly vRealize Log Insight) is a log analytics platform that collects, indexes, and correlates log data from VMware infrastructure and other sources. It is based on an Elasticsearch-backed storage and indexing engine.

---

## Cluster Topology

| Node Role | Description |
|---|---|
| **Master** | Primary node — handles ingestion, indexing, query coordination, and cluster management UI |
| **Worker** | Scale-out nodes — add workers to increase ingestion throughput and storage capacity |

A minimum of **3 nodes** (1 master + 2 workers) is recommended for production HA. Workers must be added through the master's Administration UI.

---

## Components

| Component | Description |
|---|---|
| **Log Insight Cluster** | Master + worker VMs |
| **Windows Agent** | Installed on Windows hosts to forward logs and Windows Event Log |
| **Linux Agent** | Installed on Linux hosts to forward syslog, log files, and journald |
| **Syslog Receiver** | Receives syslog over UDP/TCP on port 514, 1514; TLS on port 6514 |
| **Content Packs** | Pre-built dashboards, extracted fields, and alerts for specific products (vSphere, NSX, VCF, etc.) |
| **Cloud Proxy** | Lightweight forwarder deployed at remote sites to collect and forward logs to the central cluster |

---

## Network Ports

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| 514 | UDP/TCP | Inbound | Syslog (plaintext) |
| 1514 | UDP/TCP | Inbound | Syslog (plaintext, alternate) |
| 6514 | TCP | Inbound | Syslog over TLS |
| 9000 | TCP | Inbound | Log Insight agent ingestion |
| 443 | TCP | Inbound | Web UI (HTTPS) |
| 9543 | TCP | Inbound | Agent API (TLS) |

---

## Storage Architecture

- Based on **Elasticsearch** for indexing and querying.
- Storage is partitioned into **hot** (recent, fast SSD) and **cold** (older, capacity) tiers.
- Disk usage should not exceed **70%** of total capacity — Log Insight will throttle ingestion as it approaches capacity.
- Size storage for **30 days of hot retention** at the expected peak ingestion rate.
  - Rule of thumb: 100 GB/day ingestion requires approximately 3 TB raw for 30 days (with indexing overhead).

---

## Content Packs

Content packs provide pre-built dashboards, extracted fields, and alert definitions for specific products:

- VMware vSphere Content Pack
- VMware NSX Content Pack
- VMware VCF Content Pack
- Linux Content Pack
- Windows Content Pack

Install and update content packs from **Administration > Content Packs**. Content pack updates are independent of platform upgrades.

---

## Cloud Proxy for Remote Sites

For remote sites with latency or bandwidth constraints, deploy a **Cloud Proxy** appliance at the remote site. The proxy collects syslog and agent logs locally and forwards them to the central cluster, reducing direct log flow across WAN links.
