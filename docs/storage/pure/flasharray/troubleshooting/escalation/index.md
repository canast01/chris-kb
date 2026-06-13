---
tags:
  - pure
  - troubleshooting
---
# FlashArray — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, Before Calling Support, SLA Tiers and 1 more sections.
</div>
```text
┌──────────────────────────────────── Pure FlashArray — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     FlashArray escalation: severity triage, vendor support contact, and required artifacts    │   │
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
│   │         Controllers         │  │        Active-active        │  │           No SPOF           │   │
│   │            Drives           │  │         DirectFlash         │  │         NVMe native         │   │
│   │           Volumes           │  │       Thin provisioned      │  │        Instant clone        │   │
│   │        ActiveCluster        │  │       Sync replication      │  │           Zero RPO          │   │
│   │           SafeMode          │  │       Immutable snaps       │  │      Ransomware resist      │   │
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
│    Physical: FlashArray//X or //C controllers · DirectFlash NVMe modules · 25/100 GbE / 32Gb FC       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashArray         = Pure all-NVMe block/file array; inline dedup and compression always enabled   │
│    DirectFlash        = Pure proprietary NVMe modules; direct flash access without SAS translation    │
│    ActiveCluster      = synchronous active-active stretch cluster; hosts see a single namespace       │
│    ActiveDR           = asynchronous replication to DR site; recovery point objective in seconds      │
│    SafeMode           = admin-locked immutable snapshots; cannot be deleted even by array administr...│
│    Protection group   = set of volumes and hosts sharing a snapshot and replication schedule          │
│    purefa CLI         = REST CLI tool for FlashArray; purefa CLI connects via REST API key            │
│    purearray          = purectl CLI command: purearray list and purearray show monitoring             │
│    Volume tag         = user-defined key-value label on volumes for policy and reporting purposes     │
│    Host group         = logical collection of hosts sharing volume access via a host group object     │
│    Inline dedup       = content-based deduplication performed inline before data is written to flash  │
│    Evergreen          = Pure architecture; controllers upgrade non-disruptively, shelves remain in ...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
Pure Support Escalation Path
  Array alert / incident
          │
          ▼
  Pure1 portal ──► Array auto-detected fault?
          │ Yes ──► Pure may auto-open case + dispatch parts
          │ No  ──► Open case manually at support.purestorage.com
          │
          ▼
  Case opened ──► Support engineer reviews Pure1 telemetry
          │
          ▼
  If needed: purediag --send ──► diagnostic bundle to case
          │
          ▼
  Pure TAC ──► Remote session / field engineer dispatch
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Support Portal

Pure Storage support is accessed at **[https://support.purestorage.com](https://support.purestorage.com)**.

**Account setup:**

1. Request an account from your Pure account team or register using your company email on the support portal
2. Your Pure1 login (pure1.purestorage.com) uses the same credentials — link your array serial number to your Pure1 organisation during onboarding
3. Once the array is registered in Pure1, it automatically appears in the support portal for case association
4. Add all relevant team members (storage admins, on-call engineers) as sub-users in the portal so they can open and track cases independently

**Pure1 integration with support:**

- Cases opened via the support portal are automatically linked to the array's Pure1 data
- Pure Support engineers can view array telemetry, alert history, and diagnostic data from Pure1 without requiring a manual diagnostic upload in most situations
- For critical issues, the support engineer may request you run `purediag --send` to push a fresh diagnostic bundle directly to the case

## Opening a Case

When opening a support case, provide the following minimum information to avoid delays:

| Field | Where to Find It |
|---|---|
| Array serial number | `purearray list` (Serial field) or Pure1 portal |
| Purity//FA version | `purearray list` (Version field) |
| Symptom description | Clear description of what is wrong, when it started, and what changed before the issue |
| Business impact | Number of affected hosts/VMs, applications impacted, whether the issue is production-down or degraded |
| Steps already taken | List of diagnostic commands run and their output |
| Severity / priority | P1 (production down) through P4 (general question) — see SLA tiers below |

Set the severity accurately — Pure uses it to determine response time and resource allocation.

## Information to Collect

Run and capture the following before or immediately after opening a case:

```bash
# Array identity and version
purearray list

# Controller health
purearray list --controller

# All active alerts
purealert list

# Drive health and status
puredrive list

# Array capacity and data reduction
purearray list --space

# Host connectivity
purehost list --connection

# Port status (FC/iSCSI/NVMe)
pureport list

# ActiveCluster pod status (if applicable)
purepod list

# Replication group status (if applicable)
purepgroup list

# Snapshot space usage (if capacity-related)
puresnap list --space

# Generate and save a full diagnostic bundle
purediag --output /tmp/diag_$(hostname)_$(date +%Y%m%d_%H%M).tgz
# Or send directly to Pure Support if phone-home is active:
purediag --send
```

## Before Calling Support

- [ ] Array name and serial number: `purearray list`
- [ ] Purity//FA version: `purearray list` (Version field)
- [ ] Active alerts: `purealert list` — copy full output
- [ ] Drive status: `puredrive list` — copy full output
- [ ] Controller status: `purearray list --controller`
- [ ] Relevant performance data: `purearray monitor` output at time of issue
- [ ] Host connection details if the issue is host-facing: `purehost list --connection`
- [ ] Pod status for ActiveCluster issues: `purepod list`
- [ ] Diagnostic bundle: `purediag --output /tmp/diag_<date>.tgz` and upload to case
- [ ] Symptom description: what changed before the issue, when it started, and business impact
- [ ] Change log: any changes made in the 24 hours before the issue (firmware, zoning, network, OS patching)

## SLA Tiers

| Severity | Response Time | Description |
|---|---|---|
| P1 — Critical | 1 hour | Production system down or data at risk; array inaccessible or both controllers failed |
| P2 — High | 4 hours | Production significantly degraded; single controller down, drive failures reducing redundancy, or replication broken |
| P3 — Medium | Next business day | Non-critical issue with a workaround in place; performance degradation, non-urgent configuration questions |
| P4 — Low | Best effort | General questions, documentation requests, feature enquiries, non-impacting observations |

> Response time = time from case submission to first contact from a Pure Support engineer. Resolution time varies by issue complexity.

Severity can be escalated after the case is opened if the situation worsens — call the Pure Support hotline directly for P1 issues rather than relying solely on the web portal.

**Support hotlines** (available 24x7 for P1/P2):

- Global: +1-650-729-4088
- EMEA: +44 808 189 0119
- Specific regional numbers available on the support portal after login

## Escalation Path

If a case is not progressing at the expected pace:

1. **Request escalation in the case** — add a case note requesting escalation to a senior support engineer or support manager
2. **Call the support hotline** — reference the existing case number; ask for a duty manager or case escalation
3. **Contact your Pure account team** — your Account Executive (AE) and Systems Engineer (SE) have escalation paths into the Pure Support management chain; use this channel for P1 situations where the standard process is not moving fast enough
4. **Pure executive escalation** — for sustained high-severity incidents, your AE can engage the VP of Customer Support directly
5. **Pure1 case tracking** — all cases are visible in Pure1 portal > Support > Cases; use this to track status and add attachments without calling

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
