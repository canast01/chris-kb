# Aria Ops for Logs — Escalation

```
┌──────────────────────────────── Aria Operations for Logs — Escalation ────────────────────────────────┐
│                                                                                                       │
│  Escalate vRLI issues when log ingestion loss or corruption impacts operations and compliance.        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │           Pre-Escalation Checklist          │   │
│   │        Log ingestion stopped > 1 hour        │  │           Support bundle from VAMI          │   │
│   │      Cluster node down, cannot recover       │  │         vRLI version and patch level        │   │
│   │        Disk corruption / index error         │  │       Timeline: when ingestion stopped      │   │
│   │        Compliance data loss suspected        │  │          System monitor screenshot          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Open VMware SR with support bundle; engage TAM for compliance-critical data loss.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             VMware Support Path              │  │               Internal Actions              │   │
│   │         SR: my.vmware.com or portal          │  │       Notify security/compliance team       │   │
│   │      P2: node down; P1: full data loss       │  │       Redirect sources to SIEM direct       │   │
│   │         TAM: compliance data loss P1         │  │      Change freeze during investigation     │   │
│   │         KB: search before opening SR         │  │       RCA: document and present in 48h      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI appliance · /storage disk · VAMI · VMware SR portal · SIEM fallback target                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Support bundle    = VAMI-generated archive; mandatory before opening VMware SR                       │
│  P1 SR             = Critical: full log ingestion loss; compliance risk; live call                    │
│  P2 SR             = Major: single node down but cluster partial; business hours                      │
│  TAM               = Technical Account Manager; escalation path for premium accounts                  │
│  SIEM fallback     = Direct syslog to Splunk/SIEM while vRLI is being recovered                       │
│  Compliance notify = Inform security/compliance team if regulated log data lost                       │
│  Change freeze     = Halt all changes during active incident to preserve evidence                     │
│  RCA               = Root Cause Analysis; required after P1 by most compliance frameworks             │
│  Index error       = vRLI log data index corruption; may require rebuild with data loss               │
│  Disk corruption   = /storage filesystem error; requires vRLI restore from backup                     │
│  Cluster node down = Worker or master unavailable; check NTP + network + disk                         │
│  kb.vmware.com     = Search VMware KB before opening SR; known fixes often available                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## When to Escalate

Escalate to Broadcom support when:

- All cluster nodes are unreachable and a restore from VM backup is not available
- Log ingestion has stopped on all nodes and internal troubleshooting (disk, service restarts, firewall) has not resolved the issue
- Cassandra storage corruption is suspected (persistent errors in `cassandra/system.log` referencing corruption or unrecoverable states)
- Cluster split-brain: nodes disagree about cluster membership and will not re-join
- Post-upgrade: the cluster is in a degraded state and a rollback via snapshot has failed
- The support bundle cannot be generated and critical log data is at risk of being overwritten

---

## Opening a Broadcom Support Request

Support portal: [https://support.broadcom.com](https://support.broadcom.com)

**Product to select:** VMware Aria Operations for Logs (formerly vRealize Log Insight), under VMware Cloud Foundation portfolio.

| Severity | Condition | Response Target |
|---|---|---|
| S1 | All nodes down; log ingestion completely stopped; production impact | 30 minutes (24x7) |
| S2 | Cluster degraded; significant data loss risk | 4 hours (24x7) |
| S3 | Partial issues; alerts not firing; ingestion reduced but not stopped | Next business day |
| S4 | General questions, configuration advice | Next business day |

---

## Data to Collect Before Opening an SR

**Support bundle (required for all SRs):**

```bash
# Generate via API
curl -sk -u 'admin:<password>' -X POST \
  "https://vrli-prod-01.example.local/api/v2/support/bundle"

# Wait for completion, then download
curl -sk -u 'admin:<password>' -o vrli-support-bundle.zip \
  "https://vrli-prod-01.example.local/api/v2/support/bundle/download"
```

Via UI: **Administration → Cluster → Support Bundle → Generate and Download**.

**Additional data to capture:**

| Issue Type | Additional Collection |
|---|---|
| Ingestion failure | `ss -tulnp` output; `tail -200 /var/log/loginsight/ingestion.log` |
| Query failure | `tail -100 /var/log/loginsight/query.log`; Cassandra `nodetool status` output |
| Cluster split-brain | `curl .../api/v2/cluster/nodes` from each node; `/var/log/loginsight/runtime.log` |
| Post-upgrade failure | Upgrade log: `/var/log/loginsight/upgrade.log`; version before and after |
| Certificate failure | `openssl s_client` output; certificate expiry dates |
| Agent connectivity | Agent log from the failing host; `nc -zv` connectivity test output |

---

## SR Handoff Checklist

Before handing the SR to the next shift or specialist:

- [ ] SR number in the incident ticket
- [ ] Support bundle uploaded to SR (confirm upload completed)
- [ ] Aria Ops for Logs version (master and worker): `curl .../api/v2/version`
- [ ] Number of cluster nodes and their current states
- [ ] Estimated log data at risk (approximate retention period and ingestion rate)
- [ ] Timeline: last known good state → first failure → all actions taken
- [ ] Current state of all VM snapshots (present/absent, age)
- [ ] Broadcom case manager name and contact recorded

---

## VMware Knowledge Base

Before opening an SR, check:

- Broadcom KB: `site:kb.vmware.com "vRealize Log Insight" <error term>`
- Release notes for the installed version — known issues listed per release
- VMware Communities: `communities.vmware.com` — search for the specific error message

Common KB categories for Aria Ops for Logs:
- Cluster node not joining: search `Log Insight worker node join failed`
- Ingestion stopped: search `Log Insight ingestion stopped disk full`
- Cassandra errors: search `Log Insight Cassandra compaction`
- Certificate errors: search `Log Insight SSL certificate replace`
