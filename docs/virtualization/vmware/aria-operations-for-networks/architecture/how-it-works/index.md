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

## Data Collection Flow

### Phase 1: Topology Ingestion

On first pairing and on a polling interval (default: 10 minutes for vCenter, 10 minutes for NSX-T), the Collector polls:

- **vCenter API** — VM inventory, NIC-to-portgroup mapping, host/cluster/datacenter hierarchy, vDS portgroup configs
- **NSX-T Manager API** — logical switches, segments, T0/T1 routers, router interfaces, DFW rules, security groups, NSX tags, NSX-T transport nodes
- **Physical switch APIs** (where applicable) — interface descriptions, VLAN assignments, routing table snapshots

### Phase 2: Flow Data Ingestion

Flow data arrives continuously on the Collector's UDP/TCP listeners:

| Protocol | Default Port | Sources |
|---|---|---|
| NetFlow v5/v9 | UDP 2055 | Cisco IOS/IOS-XE/NX-OS, Juniper |
| IPFIX | UDP 2055 | Arista EOS, VMware vDS, NSX-T, Fortinet |
| sFlow | UDP 6343 | Arista, Brocade (limited support) |

The Collector correlates each flow record with its topology context: VM name, host, cluster, NSX segment, security group. Enriched records are batched and pushed to the Platform for indexing.

### Phase 3: Analytics

The Platform stores enriched flows in an internal time-series store (Cassandra). The analytics engine:
1. Builds application dependency maps from observed flow patterns
2. Scores security group recommendations using observed traffic
3. Runs network assurance checks (MTU consistency, BGP session health, gateway reachability)
4. Detects anomalies (new flows, policy violations, topology changes)

## Data Plane vs Management Plane Visibility

| Layer | What AON Sees | How |
|---|---|---|
| Management plane | NSX-T DFW rules, security groups, tags, segments, T0/T1 config | NSX-T API polling |
| Management plane | VM inventory, portgroup membership, vDS config | vCenter API polling |
| Data plane | Actual traffic flows between workloads (src IP, dst IP, port, protocol, bytes, packets) | NetFlow/IPFIX from vDS or physical |
| Data plane | Micro-segmentation gap analysis (flows that cross DFW rules or would be blocked) | Correlation of flow data + DFW rule set |

AON does **not** sit inline — it is 100% passive for data plane traffic. Flow data is sampled or exported by the fabric, not mirrored packet-by-packet (with default NetFlow sampling on physical switches, typically 1:1000 or 1:512).

## Supported Data Sources

| Data Source | Integration Type | Data Collected |
|---|---|---|
| VMware NSX-T 3.x / 4.x | REST API (read-only) | Segments, DFW rules, groups, tags, T0/T1, transport nodes |
| VMware NSX-V 6.4 | REST API (read-only) | Logical switches, DFW, security groups, ESGs |
| VMware vCenter 7.0 / 8.0 | REST API (read-only) | VM inventory, NICs, hosts, clusters, vDS portgroups |
| VMware vDS (ESXi) | IPFIX | Flow records per vNIC, per host |
| NSX-T (built-in IPFIX) | IPFIX | East-west flows within NSX overlay |
| Cisco IOS-XE | NetFlow v9 export | Physical switch flows, interface stats |
| Cisco NX-OS | NetFlow v9 export | Data center fabric flows |
| Arista EOS | IPFIX export | Spine/leaf fabric flows |
| Juniper Junos | NetFlow v5/v9 | Physical flows |
| Palo Alto PAN-OS | Traffic log syslog / API | Firewall allow/deny logs |
| Checkpoint (limited) | Syslog | Firewall logs |
| AWS VPC | VPC Flow Logs (S3) | Cloud flow data |
| Azure (limited) | NSG Flow Logs | Cloud flow data |
| ServiceNow CMDB | REST API | CMDB asset correlation |

## Micro-Segmentation Workflow

AON's microsegmentation planning workflow follows four stages:

### Stage 1: Discover Flows

AON collects flow data from all configured sources for a recommended **30-day baseline period** before generating recommendations. The discovery period ensures seasonal and weekly traffic patterns are captured.

In the UI: **Plan & Assess → Micro-Segmentation → Applications → Select Application → Flows tab**

Alternatively, query flows directly:

```text
flows where destination port = 3306 and flow type = 'East-West'
```

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
