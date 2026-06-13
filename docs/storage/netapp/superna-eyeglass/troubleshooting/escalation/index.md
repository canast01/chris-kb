---
tags:
  - netapp
  - troubleshooting
---
# Superna Eyeglass — Escalation


<div class="kb-summary">
Escalation reference covering Opening a Support Request, Required Information for SR, Severity Levels, License Issues, Escalation Path.
</div>

```text
┌──────────────────────────────────── Superna Eyeglass — Escalation ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Superna Eyeglass — Escalation Path                              │   │
│   │              L1 Triage: review logs, match to known issues in runbook (0–30 min)              │   │
│   │         L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)         │   │
│   │             Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)             │   │
│   │            Sev1 (data loss / production impact): page on-call + open critical case            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Information to Collect Before Escalating                           │   │
│   │          Product version: Superna Eyeglass version string from About / version command        │   │
│   │                                Full log bundle: igls sync status                              │   │
│   │                     Symptom timeline: when first occurred; any changes made                   │   │
│   │                Scope: single job / all jobs / all components — narrows root cause             │   │
│   │                    Error codes: exact error messages and exit codes from logs                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
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
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Opening a Support Request

Raise support cases at: [https://support.superna.net](https://support.superna.net)

**Before opening an SR**, collect a support bundle — this dramatically reduces time to resolution:

1. Log in to Eyeglass Admin UI
2. Navigate to: Admin → Support Bundle
3. Click "Download Support Bundle" — this captures logs, configuration, and system state in a single archive
4. Upload the bundle to the SR when creating it

## Required Information for SR

| Field | Detail |
|---|---|
| Eyeglass version | Admin UI → About → version string |
| OneFS version | Both primary and DR clusters |
| SyncIQ policy count | DR → Replication Policies → total count |
| Error description | Exact error text from UI or logs |
| Timestamps | When the issue first occurred (with timezone) |
| DR readiness score | Current score and what changed |
| Recent changes | Any OneFS upgrades, Eyeglass upgrades, or network changes prior to issue |

## Severity Levels

| Severity | Criteria | Response SLA |
|---|---|---|
| S1 (Critical) | Production failover blocked; DR completely inoperative | 1–2 hours |
| S2 (High) | DR readiness score degraded; failover at risk | Same business day |
| S3 (Medium) | Non-critical feature broken; workaround available | 2 business days |
| S4 (Low) | Cosmetic issue, documentation, enhancement request | Best effort |

## License Issues

Licensing issues (appliance reporting "Unlicensed") are handled via the Superna licensing portal:

1. Go to [https://superna.net/support/](https://superna.net/support/)
2. Locate license by serial number
3. Confirm that the license UUID matches the UUID shown in Admin UI → License
4. If UUID mismatch (after OVA redeployment), request license re-issue via the portal

Do not open a general support SR for licensing — use the licensing portal directly.

## Escalation Path

1. Initial SR — assigned to Tier 1 support
2. If no resolution within SLA: comment in SR "Request escalation to Tier 2"
3. For critical issues, call Superna's emergency support line (listed on the support portal)
4. For account-level escalation: contact Superna account manager


