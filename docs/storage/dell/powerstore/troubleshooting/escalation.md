---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# PowerStore — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Support Case, Required Information for a Case, Case Priority Levels, Escalation Path and 4 more sections.

*Applies to: PowerStore 3.x*
</div>
```text
┌──────────────────────────────────── Dell PowerStore — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     PowerStore escalation: severity triage, vendor support contact, and required artifacts    │   │
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
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
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
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
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

## Support Portal

Dell PowerStore support cases are logged through the Dell support portal at [https://www.dell.com/support](https://www.dell.com/support). PowerStore is covered under the ProSupport or ProSupport Plus contract associated with the system's service tag.

Access the portal with a Dell account that is associated with your company's service contracts. If you do not have a Dell account, your account team can provision access.

## Opening a Support Case

### Via PowerStore Manager (Recommended)

The fastest method for opening a case is directly from PowerStore Manager, which pre-populates the case with the system serial number, software version, and relevant logs:

1. PowerStore Manager → **Help → Contact Support → Open Service Request**
2. Describe the symptom and impact
3. Attach additional diagnostics if available (support package, log dumps)

Dell SupportAssist (if enabled and connected) may already have automatically created a case for qualifying hardware faults — check **PowerStore Manager → Help → My Cases** before opening a duplicate.

### Via Dell Support Portal

If PowerStore Manager is inaccessible:

1. Navigate to [https://www.dell.com/support](https://www.dell.com/support)
2. Sign in and go to **My Products and Services → Service Requests → Create New**
3. Select **PowerStore** as the product type
4. Enter the system service tag (serial number)

### Via Phone

| Region | Phone Number |
|---|---|
| Global (main) | +1 800 945 3355 |
| UK | +44 0800 028 2847 |
| Germany | +49 0800 000 3672 |
| Australia | +61 1800 812 393 |

For P1 (critical production-down) issues, always call after opening the portal case — phone escalation is faster than portal-only for urgent issues.

## Required Information for a Case

Always collect this data before or immediately after opening the case:

| Field | How to Obtain |
|---|---|
| System service tag / serial number | PowerStore Manager → Hardware → Appliance |
| PowerStoreOS version | `GET /api/rest/software_installed` |
| Appliance model | PowerStore Manager → Dashboard or `GET /api/rest/appliance` |
| Active alerts at time of incident | `GET /api/rest/alert?state=active` |
| Event log (last 24 hours) | `GET /api/rest/event?order=created_timestamp desc` |
| Support package | PowerStore Manager → Help → Collect Support Materials |
| Affected workloads | List volumes, hosts, and applications affected |
| Timeline | When the issue started; what changed before it occurred |
| Error message | Exact text from alerts or REST API responses |
| Impact statement | Production down / degraded / single host / DR site |

## Case Priority Levels

| Priority | Condition | Dell Response Time | Coverage |
|---|---|---|---|
| P1 — Critical | Production system down; all hosts have lost storage access | 2 hours initial response; continuous engagement | 24×7×365 |
| P2 — High | Production system degraded; significant performance impact; DR capability lost | 4 hours initial response | 24×7×365 |
| P3 — Medium | Degraded functionality; workaround available; non-production impacted | Next business day | Business hours |
| P4 — Low | General question; documentation request; minor issue with workaround | Next business day | Business hours |

ProSupport Plus subscribers receive enhanced SLAs including proactive mission-critical support and next-business-day onsite hardware replacement.

## Escalation Path

### Level 1 — Open a P1/P2 Case

For any production-impacting issue, open the case at P1 or P2 priority immediately. Include the impact statement in the case description — this determines initial routing.

### Level 2 — Request Technical Account Manager (TAM) Escalation

If you have a ProSupport Plus contract with a TAM assigned, contact your TAM directly for critical escalations:

- TAMs can escalate to engineering and expedite hardware dispatch
- TAM contact details are in your Dell account profile under **My Team**

### Level 3 — Executive Escalation

For prolonged P1 incidents (P1 open for more than 4 hours without satisfactory progress):

1. Call Dell support and request escalation to the **Duty Manager** or **Global Escalation Team**
2. Contact your **Dell account executive** and request formal executive escalation
3. Dell's escalation process triggers a bridge call with engineering involvement and executive sponsorship

## SupportAssist — Automated Case Creation

With SupportAssist enabled and connected, PowerStore automatically creates service requests for qualifying hardware faults (drive failures, power supply faults, node hardware alerts). These cases are pre-populated with diagnostic data and sent directly to Dell's proactive monitoring team.

Verify SupportAssist is connected: **PowerStore Manager → Settings → Support → SupportAssist → Status: Connected**.

If SupportAssist shows disconnected:

```bash
# Test outbound connectivity to Dell SRS
curl -k https://esrs3.emc.com   # Should return a 200 or redirect

# Check proxy configuration if behind a proxy
# PowerStore Manager → Settings → Support → SupportAssist → Proxy Settings

# Verify DNS resolution
nslookup esrs3.emc.com   # From the management network
```

## Remote Support Sessions

Dell Support engineers can initiate remote sessions through SupportAssist. These sessions are:

- Initiated by Dell from the SRS cloud — Dell engineers cannot initiate sessions without your consent
- Routed through the SRS gateway (not directly to your management IP)
- Audited — all session activity is logged

To permit a remote session:

1. The Dell support engineer will provide a session ID
2. In PowerStore Manager → **Help → Remote Support Sessions → Approve Session** — enter the session ID
3. The session is active for the duration specified; it terminates automatically at expiry

You can monitor active remote sessions and revoke them at any time from the same Remote Support Sessions view.

## Diagnostic Resources

| Resource | URL | Use |
|---|---|---|
| Dell Support Portal | [https://www.dell.com/support](https://www.dell.com/support) | Case management, downloads, knowledge base |
| Dell PowerStore Documentation | [https://www.dell.com/support/home/en-us/product-support/product/powerstore/docs](https://www.dell.com/support/home/en-us/product-support/product/powerstore/docs) | Official product documentation |
| Dell Security Advisories | [https://www.dell.com/support/security](https://www.dell.com/support/security) | CVEs and security patches for PowerStoreOS |
| Dell PowerStore Interoperability Matrix | [https://elabnavigator.dell.com](https://elabnavigator.dell.com) | Host OS, HBA, switch, and software compatibility |
| Dell Community Forums | [https://www.dell.com/community](https://www.dell.com/community) | Peer knowledge base; useful for non-critical questions |

## Escalation Checklist (P1 Incident)

Use this checklist when a P1 incident is declared:

- [ ] Support case opened at P1 priority with impact statement (production down)
- [ ] Dell support engineer on the bridge call or acknowledged via portal
- [ ] Support package attached to the case or upload in progress
- [ ] System serial number, software version, and hardware model confirmed with support
- [ ] Timeline documented: when the issue started; what changed; which hosts are affected
- [ ] SupportAssist confirmed — check if Dell has an existing automated case for this incident
- [ ] Internal incident declared; application owners and management notified
- [ ] TAM contacted if ProSupport Plus (can expedite engineering engagement)
- [ ] Change freeze enacted — no additional changes until the P1 is resolved
- [ ] If hardware fault: confirm Dell has dispatched the replacement component (check case notes)
- [ ] DR failover readiness assessed — if site is at risk, evaluate failing over to DR

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
