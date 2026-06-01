# PowerScale — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Procedure.
</div>
```text
┌──────────────────────────────────── Dell PowerScale — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     PowerScale escalation: severity triage, vendor support contact, and required artifacts    │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │              OS             │  │            OneFS            │  │        Distributed FS       │   │
│   │           Tiering           │  │          SmartPools         │  │        Auto data move       │   │
│   │         Replication         │  │            SyncIQ           │  │        Async DR copy        │   │
│   │          Snapshots          │  │          SnapshotIQ         │  │       Space-efficient       │   │
│   │         Load balance        │  │         SmartConnect        │  │       DNS client dist.      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerScale nodes (All-Flash/Hybrid) · InfiniBand backend · 25/100 GbE frontend           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OneFS              = Dell PowerScale distributed filesystem OS; all nodes share a single namespace │
│    SmartPools         = tiering engine; moves files between All-Flash, Hybrid, and Archive tiers      │
│    SyncIQ             = async replication to DR cluster; RPO-based schedule; failover in minutes      │
│    SnapshotIQ         = space-efficient snapshots; accessed via .snapshot directory in each share     │
│    SmartConnect       = DNS-based load balancing; distributes NFS/SMB client connections across nodes │
│    Access zone        = logical container with separate authentication and export namespace per tenant│
│    Quota              = directory or user quota; hard/soft/advisory limits enforced by OneFS QuotaIQ  │
│    CloudPools         = tiering to cloud object storage (S3/Blob); data remains accessible locally    │
│    isi CLI            = OneFS command-line interface; all management operations available via isi c...│
│    Node pool          = group of same-model nodes sharing protection domain for data distribution     │
│    Protection level   = N+2:1, N+3:1 etc.; defines how many node or drive failures are tolerated      │
│    File pool policy   = rule-based policy assigning files to specific node pools or storage tiers     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Support Portal

Open and manage cases at [https://www.dell.com/support](https://www.dell.com/support). Log in with your Dell account and navigate to **My Cases** to track open cases.

SupportAssist for PowerScale (embedded in OneFS) can automatically open cases for hardware faults — confirm it is configured and calling home by running:

```bash
isi phone_home settings view
isi phone_home send --type test
```

Verify SupportAssist connectivity to Dell's SRS gateway before relying on auto-case creation.

## Opening a Case

Required information before calling or opening an online case:

| Field | How to Obtain |
|---|---|
| Cluster serial number | `isi license list` or the chassis label on each node |
| Node serial numbers | `isi status -n` or the node chassis label |
| OneFS version | `isi version` |
| Symptom description | Clear statement of what failed, when it started, and frequency |
| Affected nodes | `isi status` output showing node state |
| Client impact | Number of clients affected, protocols, affected paths under `/ifs` |

For SMARTFAIL, drive, or node hardware faults, the severity should be set to **P1** (production down) or **P2** (degraded) depending on whether I/O has been interrupted.

## Information to Collect

Collect the full cluster diagnostic bundle using `isi_gather_info` before opening or escalating a case:

```bash
# Collect full cluster diagnostic bundle (runs on any node, gathers all nodes)
isi_gather_info

# Show overall cluster node and drive health
isi status

# List all storage pool tiers and their capacity usage
isi storagepool list

# Show per-drive statistics including I/O errors and firmware
isi statistics drive

# Show recent alerts (last 50)
isi alerts list --limit 50

# Show all active and recent cluster background jobs
isi job list

# Show installed OneFS version
isi version
```

The `isi_gather_info` output is written to `/ifs/data/Isilon_Support/` by default. Upload this file to the Dell support case using the **Secure Upload** link in the case portal.

## SLA Tiers

| Tier | Priority | Response Time | Coverage |
|---|---|---|---|
| ProSupport Plus | P1 — Production Down | 2 hours | 24x7x365 |
| ProSupport Plus | P2 — Degraded Performance | 4 hours | 24x7x365 |
| ProSupport Plus | P3 — Non-critical issue | Next business day | Business hours |
| ProSupport Plus | P4 — General question | Next business day | Business hours |
| ProSupport | P1 | 4 hours | 24x7x365 |
| ProSupport | P2—P4 | Next business day | Business hours |

Confirm your cluster's support contract level in the Dell support portal under **My Products and Services**.

## Escalation Procedure

If a P1 case is not progressing within the response SLA or a critical outage requires urgent escalation:

1. Call the Dell support line and request **escalation to a senior engineer** for your open case number.
2. Contact your **Dell account team Technical Account Manager (TAM)** — TAMs have direct lines into the engineering team for critical production issues.
3. For prolonged or complex outages, request engagement with **Dell Global Priority Services (GPS)** — GPS provides on-site or remote senior engineering support beyond standard TAM involvement.
4. Reference the case number, cluster serial, and business impact statement (number of users/petabytes affected) in all escalation communications.
