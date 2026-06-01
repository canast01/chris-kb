# Nexus Dashboard — Design Standards

<div class="kb-summary">
Cluster sizing, form factor selection, IP addressing, naming conventions, and configuration baselines for Cisco Nexus Dashboard deployments.
</div>

```powershell
┌───────────────────────────────── Nexus Dashboard — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Cluster Standards               │  │            Operational Standards            │   │
│   │             3 physical nodes min             │  │            All fabrics onboarded            │   │
│   │             SSD 500 GB+ per node             │  │             MDT on all switches             │   │
│   │            Separate mgmt+data net            │  │                Alerts to ITSM               │   │
│   │            Backup config nightly             │  │             Weekly health review            │   │
│   │              NTP and DNS config              │  │           Dedicated read-only acct          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  3 physical x86 or VM nodes · SSD storage · dual-homed to mgmt and data networks                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Physical nodes minimum = Bare metal preferred for production; 3 for quorum                           │
│  SSD 500 GB = Flash required for streaming telemetry time-series write performance                    │
│  Separate networks = ND requires dedicated management and data network interfaces                     │
│  MDT on all switches = Model-Driven Telemetry enabled on every monitored switch                       │
│  All fabrics onboarded = Every ACI and NX-OS fabric registered in ND                                  │
│  ITSM alert = Every NDI event/anomaly routed to ServiceNow via webhook                                │
│  Read-only account = Dedicated APIC user with Observer role for NDI                                   │
│  NTP consistency = ND and all switches must use same NTP source for telemetry alignment               │
│  Weekly health review = Scheduled review of NDI health scores and open anomalies                      │
│  Backup = ND config backup nightly; stored externally on NFS or SCP target                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Cluster Sizing

| Cluster Size | When to Use | Notes |
|---|---|---|
| 3 nodes | Standard production (single service at scale) | NDFC **or** NDI — not both at maximum scale |
| 5 nodes | Multi-service or HA-critical deployments | Run NDFC + NDI at full scale simultaneously |
| 1 node | Lab only | Not supported for production; no quorum |

Use 5 nodes when:
- Both NDFC and NDI are deployed with > 100 switches
- SLA requires zero downtime during node failure (5-node cluster tolerates 2 failures vs 3-node tolerating 1)

## Form Factor

| Form Factor | Use Case | Notes |
|---|---|---|
| Physical appliance (UCS C220) | Production; performance-sensitive | Recommended for large fabrics |
| VMware virtual (OVA) | Smaller fabrics; lab | ≤ 50 switches per node recommended |
| AWS cloud | Remote site management | Limited to NDFC SAN mode |

## IP Addressing

Each Nexus Dashboard cluster requires:

| Interface | Count | Purpose |
|---|---|---|
| Management interface | 1 per node + 1 cluster VIP | Admin access and cluster API |
| Data interface | 1 per node | Fabric connectivity (NDFC, NDI telemetry) |

- Management and data interfaces must be in **different subnets**
- Cluster VIP must be in the same subnet as management interfaces
- Use `/24` or larger subnets; avoid `/30` or `/31`

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Cluster hostname | `nd-{site}-{seq}` | `nd-dc1-01` |
| Node name | `nd-{site}-node-{n}` | `nd-dc1-node-1` |
| Application display name | Match Cisco product name | `NDFC`, `NDI`, `NDO` |

## Configuration Checklist

- [ ] 3 or 5 nodes deployed and cluster formation complete
- [ ] Management VIP resolves in DNS
- [ ] NTP configured on all nodes (same source as managed switches)
- [ ] LDAP / TACACS+ authentication configured; local fallback account in CyberArk
- [ ] TLS certificate replaced (default self-signed → org PKI certificate)
- [ ] Backup job configured (daily config export via ND API or snapshot)
- [ ] NDFC / NDI licences applied and validated
- [ ] Fabric discovery completed and all switches reachable
