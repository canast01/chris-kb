# Aria Operations for Networks — Design Standards


<div class="kb-summary">
Design Standards reference covering Sizing, Collector Placement Guidelines, Network Requirements, High Availability, Certificate Requirements and 3 more sections.
</div>

```text
┌──────────────────────────────────────── vRNI Design Standards ────────────────────────────────────────┐
│                                                                                                       │
│  Sizing, collector placement, and data source standards for Aria Operations for Networks.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Platform Appliance Sizing           │  │             Collector Placement             │   │
│   │        Small: up to 1000 VMs, 4 vCPU         │  │       1 collector per network segment       │   │
│   │        Medium: up to 3000 VMs, 8 vCPU        │  │       Collector close to data sources       │   │
│   │       Large: up to 10000 VMs, 16 vCPU        │  │        Max 10 collectors per platform       │   │
│   │         RAM scales with flow volume          │  │        Collector: 4 vCPU / 12 GB RAM        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Platform appliance receives flows; collectors aggregate from remote segments.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Data Source Standards             │  │             Network Requirements            │   │
│   │          NSX-T: primary flow source          │  │          UDP 2055 for NetFlow/IPFIX         │   │
│   │        vCenter: inventory + topology         │  │          TCP 443 to vCenter/NSX API         │   │
│   │        Physical switches: SNMP/IPFIX         │  │        Collector to platform: TCP 443       │   │
│   │           Cloud: AWS VPC Flow Logs           │  │           DNS resolution required           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM on vSphere; collector VMs per segment; NTP sync required                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Platform Appliance  = Central vRNI VM; stores flow data, runs analytics, hosts UI                    │
│  Collector           = Lightweight VM that receives IPFIX/NetFlow and forwards to platform            │
│  IPFIX               = IP Flow Information Export; standard protocol for flow telemetry               │
│  NetFlow             = Cisco flow export protocol; v5/v9 supported by vRNI collectors                 │
│  Data Source         = Any device or system providing flows or inventory to vRNI                      │
│  NSX-T               = Primary flow source; exposes distributed firewall and overlay flows            │
│  vCenter             = Inventory source; maps VM names, hosts, clusters to flow IPs                   │
│  SNMP                = Used to poll physical switch interface counters and topology                   │
│  VPC Flow Logs       = AWS/Azure cloud flow records ingested via cloud data source                    │
│  Flow Map            = vRNI visual topology showing traffic paths between entities                    │
│  Retention           = Default 13 months for flows; configurable per deployment size                  │
│  PAK File            = Upgrade bundle for vRNI; applied via VAMI or update manager                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Sizing

### Platform VM Sizing

| Deployment Size | Use Case | vCPU | RAM | OS Disk | Data Disk | Flows/sec |
|---|---|---|---|---|---|---|
| **Small (Brick)** | Lab / PoC, up to 1,000 VMs | 4 | 16 GB | 75 GB | 200 GB | up to 2,000 |
| **Medium** | Mid-size environments, up to 3,000 VMs | 8 | 32 GB | 75 GB | 500 GB | up to 10,000 |
| **Large** | Production, up to 10,000 VMs | 16 | 64 GB | 75 GB | 1 TB | up to 30,000 |
| **Extra-Large** | Telco/ISP, unlimited VMs | 32 | 128 GB | 75 GB | 2 TB | up to 100,000 |

The "Small (Brick)" form factor deploys Platform and Collector functionality in a single VM — intended for lab use only. All other deployments use separate Platform and Collector VMs.

### Collector VM Sizing

| Deployment Size | vCPU | RAM | Disk | Flows/sec per Collector |
|---|---|---|---|---|
| **Standard** (default) | 4 | 12 GB | 100 GB | up to 15,000 |
| **Large** | 8 | 24 GB | 150 GB | up to 30,000 |

Collector VM sizing is selected at OVA deployment time via OVF properties. You cannot resize a Collector post-deployment without redeployment.

## Collector Placement Guidelines

- Deploy **one Collector per NSX-T Manager cluster**. A single NSX-T Manager (or manager cluster) should be paired to exactly one Collector. Splitting NSX-T polling across multiple Collectors causes topology correlation errors.
- For **multi-site** deployments: deploy a Collector at each data center or availability zone where NSX-T/vCenter instances are running.
- Collectors must have **L3 reachability** to:
  - vCenter Server (TCP 443)
  - NSX-T Manager VIP (TCP 443)
  - Physical switch management interfaces (SNMP, SSH if applicable)
  - Platform VM (TCP 443 outbound)
- Physical switches and ESXi vDS send NetFlow/IPFIX to the **Collector**, not to the Platform. The Collector IP must be reachable from the switch management plane on **UDP 2055**.
- Collector VMs do **not** require a routable IP from the physical fabric data plane — only UDP 2055 from switch management interfaces.

## Network Requirements

### Ports and Protocols

| Source | Destination | Port | Protocol | Purpose |
|---|---|---|---|---|
| Collector VM | vCenter Server | 443 | TCP | vCenter API polling |
| Collector VM | NSX-T Manager VIP | 443 | TCP | NSX-T API polling |
| Collector VM | NSX-V Manager | 443 | TCP | NSX-V API polling |
| Collector VM | Platform VM | 443 | TCP | Data upload, control channel |
| Collector VM | Physical switch mgmt | 22 | TCP | SSH (optional, for config collection) |
| Collector VM | Physical switch mgmt | 161 | UDP | SNMP (interface stats, optional) |
| Platform VM | Collector VM | 443 | TCP | Health checks, config push |
| Physical switches | Collector VM | 2055 | UDP | NetFlow v5/v9 / IPFIX |
| ESXi vDS | Collector VM | 2055 | UDP | IPFIX from distributed switch |
| NSX-T transport nodes | Collector VM | 2055 | UDP | NSX-T built-in IPFIX |
| Palo Alto firewalls | Collector VM | 514 | UDP/TCP | Syslog traffic logs |
| Admin workstations | Platform VM | 443 | TCP | UI and REST API access |
| Platform VM | LDAP/AD server | 389/636 | TCP | LDAP authentication |
| Platform VM | NTP server | 123 | UDP | Time synchronization |
| Platform VM | SMTP server | 25/587 | TCP | Email alert notifications |
| Platform VM | Syslog/SIEM | 514/6514 | UDP/TCP | Outbound event forwarding |

### DNS Requirements

All VM FQDNs must resolve forward and reverse:
- Platform VM FQDN → A record → Platform VM IP
- Platform VM IP → PTR record → Platform VM FQDN
- Same for each Collector VM

NTP synchronization is mandatory. Platform and Collector VMs must be within ±1 second of each other. Time drift causes flow correlation failures and UI errors.

## High Availability

### Platform VM HA

AON provides **no native HA** for the Platform VM. Protect it with:

- **vSphere HA**: VM restart policy set to highest priority. RTO is typically 5–10 minutes (VM restart + service startup).
- **vSphere FT** is not supported for Platform VM (multi-vCPU).
- Regular config backups (see Backup and Restore page).

The Platform VM holds all persistent data. Loss of the Platform VM without a backup means redeployment from scratch with loss of all historical flow data, applications, and alerts.

### Collector VM HA

Collectors are **stateless** — all persistent state is on the Platform VM. If a Collector VM fails:
- Flow ingestion stops for that Collector's data sources
- Topology polling stops
- Historical data is preserved on the Platform

Recovery: deploy a new Collector OVA → pair using the existing pairing key (same key as the failed Collector, regenerated from UI). Data sources (vCenter, NSX-T) re-associate automatically.

vSphere HA can restart Collector VMs, which is sufficient for most environments.

## Certificate Requirements

| Component | Default | Recommendation |
|---|---|---|
| Platform VM HTTPS | Self-signed (auto-generated at first boot) | Replace with CA-signed cert before production |
| Collector-to-Platform TLS | Auto-generated, pinned during pairing | Not user-replaceable; managed internally |
| NSX-T API trust | Configurable (accept all / validate CA) | Validate CA cert in production |
| vCenter API trust | Configurable | Validate CA cert in production |

Certificate replacement for Platform VM HTTPS:

1. Obtain a certificate with the Platform FQDN in the SAN.
2. UI: Settings → SSL Certificate → Replace Certificate
3. Upload PEM-formatted certificate and private key.
4. The UI will restart (NGINX reload); expect ~30 seconds of downtime.

## LDAP / AD Integration for RBAC

AON supports LDAP and AD for user authentication and group-to-role mapping.

**Configuration:** Settings → Users and Groups → Authentication → LDAP

| Field | Example |
|---|---|
| Server | `ldap://ad.example.local` or `ldaps://ad.example.local:636` |
| Bind DN | `CN=svc-aon,OU=Service Accounts,DC=corp,DC=local` |
| Bind Password | — |
| Search Base | `OU=Users,DC=corp,DC=local` |
| Username Attribute | `sAMAccountName` (AD) or `uid` (OpenLDAP) |
| Group Search Base | `OU=Groups,DC=corp,DC=local` |
| Group Member Attribute | `member` |

After configuring LDAP, map AD groups to AON roles:

Settings → Users and Groups → Groups → Add Group

| AD Group | AON Role |
|---|---|
| `GRP-AON-Admins` | Super Admin |
| `GRP-AON-NetEng` | Network Engineer |
| `GRP-AON-SecEng` | Security Engineer |
| `GRP-AON-Readonly` | Auditor |

## Backup Considerations

- Flow data is **not** backed up — only configuration is exportable.
- The Platform VM holds Cassandra, Elasticsearch, and PostgreSQL data. These are **not** application-consistent with VM snapshots while services are running.
- Recommended backup approach: UI config export (Settings → Backup) + vSphere snapshot taken during a maintenance window with services quiesced.
- Retain at least 3 rolling config exports.
- Store config exports off-VM (download and archive externally).

## Version Compatibility

Always check the [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com/) before deployment. Key constraints:

| AON Version | NSX-T Supported | vCenter Supported | NSX-V Supported |
|---|---|---|---|
| 6.12.x | 3.1, 3.2, 4.0, 4.1 | 7.0, 8.0 | 6.4 (limited) |
| 6.13.x | 3.2, 4.0, 4.1, 4.2 | 7.0, 8.0, 8.0 U1 | Not supported |
| 6.14.x | 4.0, 4.1, 4.2, 4.2.1 | 7.0 U3, 8.0, 8.0 U2 | Not supported |

NSX-V compatibility was dropped in AON 6.13. If you have NSX-V data sources, pin AON to 6.12.x until migration is complete.
