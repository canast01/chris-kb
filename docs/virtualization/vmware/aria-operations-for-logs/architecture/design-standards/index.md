# Aria Ops for Logs — Standards


<div class="kb-summary">
Standards reference covering Naming Convention, Content Pack Standards, Alert Severity Standards, Cluster Sizing Rules.
</div>

## Naming Convention

Follow the same naming scheme as other LCM-managed appliances:

```text
vrli-<env>-<node#>.<domain>
```
```text
┌───────────────────────────── Aria Operations for Logs — Design Standards ─────────────────────────────┐
│                                                                                                       │
│  Standards for sizing, retention, clustering, and source onboarding in vRLI deployments.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Sizing Standards               │  │             Retention Standards             │   │
│   │      Master: 4 vCPU/16 GB/1 TB storage       │  │        Hot retention: 90 days on-disk       │   │
│   │     Workers: add for >500 GB/day ingest      │  │        Archive: 1 year NFS/S3 export        │   │
│   │     Cluster: master + 2 workers minimum      │  │     Security events: 1 year hot minimum     │   │
│   │       Network: 10 Gbps for high ingest       │  │     GDPR/compliance: region-local store     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Source onboarding and alert design standards ensure consistent and actionable logging.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Source Onboarding               │  │                 Alert Design                │   │
│   │     Install content pack before onboard      │  │      Alert on error patterns, not noise     │   │
│   │      Use TLS syslog (6514) for security      │  │    Threshold: count-based, not always-on    │   │
│   │      Tag sources: env/product/location       │  │       Route: critical → PagerDuty/SNow      │   │
│   │       ESXi: set syslog.global.logHost        │  │         Suppress: known noisy events        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI VMs (master + workers) · 10GbE NIC · NFS/S3 archive · vCenter · ESXi                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Hot retention     = On-disk log storage duration; older data rolled to archive or deleted            │
│  Archive           = Off-appliance export to NFS or S3; compressed, searchable via vRLI               │
│  Worker node       = Additional vRLI VM; master delegates ingestion and query to workers              │
│  Cluster           = Master + 2+ workers sharing index; required for HA and high ingest               │
│  syslog.global.logHost= ESXi advanced config key pointing ESXi syslog to vRLI IP:port                 │
│  TLS syslog        = Encrypted log transport on port 6514; prevents log tampering in transit          │
│  Source tag        = Custom field applied at ingest to identify source environment or product         │
│  Content pack      = Pre-built dashboards+alerts for a product; install before onboarding             │
│  Alert threshold   = Count or rate trigger; e.g. fire if >5 auth failures in 5 minutes                │
│  Suppress rule     = vRLI filter excluding known noisy or low-value events from alerting              │
│  GDPR retention    = Data residency requirement; logs stored in same region as source                 │
│  Ingest rate       = Measured in GB/day; determines sizing (master-only vs. cluster)                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
