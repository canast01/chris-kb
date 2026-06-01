# Aria Operations for Networks — How It Works

## Deployment Model

Aria Operations for Networks (AON, formerly vRealize Network Insight / VRNi) consists of two distinct VM roles deployed from separate OVAs:

| Component | Role | Count |
|---|---|---|
| **Platform VM** | UI, analytics engine, data store, API endpoint | 1 per deployment |
| **Collector VM** | Data collection agent — communicates with data sources | 1–N (one per NSX-T/vCenter site recommended) |

Collectors maintain a persistent TLS connection back to the Platform VM on TCP 443. All raw flow data, API-pulled topology, and parsed configs are shipped from Collector to Platform for indexing. The Platform VM is the sole persistent data store — Collectors hold no long-term state.

```text
[ESXi hosts / vDS]   ──IPFIX/NetFlow──►  [Collector VM]  ──TLS 443──►  [Platform VM]
[NSX-T Manager]      ──REST API──────►   [Collector VM]
[vCenter Server]     ──REST API──────►   [Collector VM]
[Physical switches]  ──NetFlow UDP 2055──► [Collector VM]
[Palo Alto firewall] ──Syslog/API──────►  [Collector VM]
```
┌─────────────────────────────────────────── How vRNI Works ────────────────────────────────────────────┐
│                                                                                                       │
│  Flow collection from NSX/switches/cloud, analytics processing, and flow map rendering.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Flow Collection Layer             │  │             Inventory Collection            │   │
│   │           NSX-T IPFIX to collector           │  │           vCenter API: VMs + hosts          │   │
│   │           Physical switch NetFlow            │  │          NSX API: segments + rules          │   │
│   │             Cloud VPC flow logs              │  │             DNS: name resolution            │   │
│   │        Collector forwards to platform        │  │           CMDB enrichment optional          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Collected flows and inventory feed the analytics engine for correlation and search.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Analytics Engine               │  │                Flow Map & UI                │   │
│   │          Correlates IPs to VM names          │  │        Flow Map: entity traffic view        │   │
│   │         Detects micro-seg violations         │  │        Search: natural language query       │   │
│   │          Anomaly detection on flows          │  │         Dashboards: predefined views        │   │
│   │           Path tracing end-to-end            │  │           Export: CSV / API query           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM + collector VMs on vSphere; NSX-T and physical switches as sources                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Flow Record         = 5-tuple (src IP, dst IP, src port, dst port, proto) + byte/packet count        │
│  IPFIX               = Standard flow export protocol; used by NSX-T and modern switches               │
│  Collector           = Lightweight VM that receives IPFIX/NetFlow from data sources                   │
│  Analytics Engine    = Platform component correlating flows with inventory for search                 │
│  Flow Map            = Visual graph of traffic between application tiers and VMs                      │
│  Path Tracing        = vRNI feature showing physical + logical path for a given flow                  │
│  Micro-seg Violation = Flow allowed/denied differently than NSX DFW rule intent                       │
│  Natural Language Search= vRNI query interface using plain English flow queries                       │
│  Anomaly Detection   = Automatic flagging of unusual flow volume or new connections                   │
│  Entity              = Any named object: VM, host, IP, application, security group                    │
│  Inventory Sync      = Periodic API poll of vCenter/NSX to refresh entity metadata                    │
│  VPC Flow Logs       = Cloud flow records from AWS/Azure ingested as a data source                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

### Stage 2: Map Application Dependencies

AON builds application tiers automatically by clustering VMs that communicate with each other. You can also define application boundaries manually:

**UI**: Plan & Assess → Applications → Add Application → Define membership by:
- NSX security group membership
- VM name regex (`web-.*`, `db-.*`)
- IP subnet
- NSX tag

### Stage 3: Generate Security Group Recommendations

Once an application is defined, AON analyzes all observed flows and recommends:
- Which VMs should be in which NSX security groups
- Which DFW rules to create (source group, destination group, port, action)
- Flows that will be **allowed** vs **blocked** by the recommended policy

**UI**: Plan & Assess → Micro-Segmentation → Recommended Rules tab

The recommendation output includes:
```yaml
Source Group: sg-web-tier
Destination Group: sg-db-tier
Port: TCP 3306
Action: Allow

Source Group: sg-web-tier
Destination Group: any
Port: TCP 443
Action: Allow
```

### Stage 4: Push to NSX

Recommendations can be exported or pushed directly:
- **Export**: Download as CSV or JSON for manual review before applying
- **Push to NSX**: AON calls the NSX-T API to create security groups and DFW rules directly (requires NSX-T integration with write permissions — separate from the read-only data source)

## Application Discovery Mechanism

AON's application discovery uses three methods:

1. **Flow-based clustering**: VMs that communicate with each other above a configurable threshold are grouped as candidate application tiers.
2. **DNS/hostname pattern matching**: VM names are parsed with configurable regex patterns to auto-label tiers (e.g., `web-`, `app-`, `db-`).
3. **NSX tag import**: Existing NSX tags on VMs are imported and mapped to application definitions.

Discovery results appear under: **Plan & Assess → Applications → Discovered Applications**

## Flow Data Retention Defaults

| Data Type | Default Retention | Configurable |
|---|---|---|
| Raw flow records (full detail) | 30 days | Yes (dependent on disk) |
| Aggregated flow summaries | 6 months | Yes |
| Topology snapshots | 30 days | No |
| Security recommendations | Until manually cleared | — |
| Problem/alert history | 90 days | No |
| Audit logs | 90 days | No |

Retention is disk-constrained. Platform VM disk usage is monitored and old data is purged when disk utilization exceeds 80% of the data partition.

To check current retention configuration:
**UI**: Settings → Infrastructure → Platform → Data Retention

## Internal Service Architecture

The Platform VM runs a set of internal services on Ubuntu:

| Service | Function |
|---|---|
| `vrni-platform` | Core application service (Spring Boot) |
| `cassandra` | Time-series flow data store |
| `kafka` | Internal message bus between collector and platform |
| `elasticsearch` | Search index for topology and flows |
| `nginx` | Reverse proxy for HTTPS UI and API |
| `postgres` | Configuration and metadata database |

Collectors run a lightweight agent that communicates only outbound to the Platform on TCP 443 — no listening ports are required on the Collector beyond those for flow ingestion (UDP 2055, UDP 6343).
