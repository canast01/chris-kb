# Aria Operations for Logs — Learning Path

<div class="kb-summary">
Recommended reading order for Aria Operations for Logs (vRLI). Follow these stages in order to build a complete mental model before working with it in production.
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture
**Goal**: Understand how log data flows from sources through ingestion, field extraction, and into queryable retention tiers.
**Read in this order**:
- [How It Works](../architecture/how-it-works/) — syslog ingest (UDP/TCP 514, SSL 1514), content pack pipeline, and Elasticsearch-backed storage tiers
- [Design Standards](../architecture/design-standards/) — cluster sizing rules, node count vs. ingestion rate, and retention volume planning
- [Integrations](../architecture/integrations/) — vCenter, NSX, ESXi syslog forwarding, SIEM integration via syslog re-forward, and Aria Operations alert linking

**Why first**: Log volume and retention requirements determine cluster size before deployment; understanding content pack field extraction prevents confusion when building alerts and dashboards.

---

## Stage 2 — Deployment
**Goal**: Deploy a clustered vRLI environment with HA, syslog sources configured, and content packs installed.
**Read**:
- [Deploy](../deploy/) — OVA deployment, master + worker node join sequence, and VIP/load balancer configuration
- [Install & Upgrade](../operations/install-upgrade/) — rolling upgrade procedure, pre-upgrade log drain, and Integrated Load Balancer (ILB) behaviour during upgrades

**Why second**: HA clustering and VIP assignment must be planned before any sources send logs; retrofitting a VIP after sources are live causes a brief ingestion gap.

---

## Stage 3 — Operations
**Goal**: Maintain ingestion health, manage retention and archival, and keep alert forwarding current.
**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift
- [CLI Reference](../operations/cli-reference/) — vRLI API and admin CLI for node status, retention partition management, and content pack installation
- [Procedures](../operations/procedures/) — content pack deployment, extracted field creation, alert definition and forwarding rules, and archive bucket configuration
- [Backup & Restore](../operations/backup-restore/) — configuration export, NFS archive setup, and restore sequence for master node failure
- [Scripts](../operations/scripts/) — API-based query automation, log export scripts, and bulk alert suppression during maintenance windows

**Why third**: Operational tasks depend on a stable cluster with known ingestion rates and content packs already deployed.

---

## Stage 4 — Security
**Goal**: Restrict dashboard and alert access by role, encrypt log transport, and satisfy audit log retention requirements.
**Read**:
- [Access Control](../security/access-control/) — user roles, dataset-scoped access, and shared dashboard permissions
- [Authentication](../security/authentication/) — Active Directory integration, SSO via vIDM, and local admin account controls
- [Encryption](../security/encryption/) — TLS on syslog port 1514, HTTPS-only admin UI enforcement, and certificate rotation
- [Hardening](../security/hardening/) — disabling plaintext port 514, restricting admin UI access by IP, and audit log forwarding to SIEM

**Why fourth**: Encryption and port hardening affect source configuration; changing syslog transport from UDP 514 to SSL 1514 requires coordinated updates on all sending hosts.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose ingestion gaps, missing fields, and alert forwarding failures with minimal log loss.
**Read**:
- [Common Issues](../troubleshooting/common-issues/) — dropped events, content pack field extraction failures, alert storm suppression, and cluster split-brain recovery
- [Diagnostics](../troubleshooting/diagnostics/) — support bundle collection, ingestion pipeline log locations, and Elasticsearch shard health queries
- [Escalation](../troubleshooting/escalation/) — GSS data requirements, cluster diagnostic export, and SR classification for data-loss scenarios

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
