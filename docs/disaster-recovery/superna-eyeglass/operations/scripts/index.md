# Superna Eyeglass — Scripts

```
┌───────────────────────────────────── Superna Eyeglass — Scripts ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Superna Eyeglass — Automation Scripts                             │   │
│   │          Scripts automate routine Superna Eyeglass operations — run via cron or CI/CD         │   │
│   │               Always store credentials in vault (not in script); log all output               │   │
│   │                 Test scripts in non-production before scheduling in production                │   │
│   │                        Scope scripts to least-privilege service account                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Status / Reporting Scripts          │  │              Automation Scripts             │   │
│   │           Job success rate report            │  │            Auto-expire old points           │   │
│   │              Capacity trending               │  │          Auto-add new VMs to policy         │   │
│   │            SLA compliance report             │  │          Nightly DR test validation         │   │
│   │             RPO / RTO dashboard              │  │             Alert on job failure            │   │
│   │               igls sync status               │  │               igls rapa status              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link   │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection            │
│  RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats       │
│  SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies         │
│  DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS        │
│  Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster              │
│  Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product       │
│  Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits            │
│  Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site            │
│  Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team                  │
│  Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha       │
│  Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation      │
│  igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations                         │
│  SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation         │
│  Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Automation scripts for Eyeglass cover SyncIQ health checking, RPO compliance reporting, automated pre-failover validation, and post-failover validation using the Eyeglass REST API. Scripts are typically written in Python or Bash and executed from a management jump host with network access to both the Eyeglass appliance and the PowerScale clusters.

| Script | Language | Purpose |
|---|---|---|
| `synciq-health-check.py` | Python | Query Eyeglass REST API for all policy states; alert on failures |
| `rpo-compliance-report.py` | Python | Export RPO compliance per SyncIQ policy with lag metrics |
| `pre-failover-validation.sh` | Bash | Run automated pre-failover checks: DR readiness score, DNS, quotas |
| `post-failover-validation.py` | Python | Validate shares accessible, quotas applied, DNS resolved at DR site |

**Example: pre-failover validation (Bash)**

```bash
#!/bin/bash
EYEGLASS_HOST="eyeglass-dr.example.com"
API_TOKEN="$EYEGLASS_API_TOKEN"

# Check DR readiness score
score=$(curl -sk -H "Authorization: Bearer $API_TOKEN" \
  "https://$EYEGLASS_HOST/api/v1/dr/readiness" | jq '.score')

if [ "$score" -lt 100 ]; then
  echo "ERROR: DR readiness score is $score — failover blocked."
  exit 1
fi
echo "DR readiness score: $score — proceeding."
```
