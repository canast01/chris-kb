# PowerScale — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Procedure.
</div>

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
