---
tags:
  - pure
  - troubleshooting
search:
  boost: 1.5
---
# FlashBlade — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Path.

*Applies to: FlashBlade Purity//FB 4.x*
</div>
```text
┌──────────────────────────────────── Pure FlashBlade — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     FlashBlade escalation: severity triage, vendor support contact, and required artifacts    │   │
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
│   │            Blades           │  │           NVMe+CPU          │  │         Parallel I/O        │   │
│   │             File            │  │           NFS/SMB           │  │        Scale-out NAS        │   │
│   │            Object           │  │           S3/Swift          │  │         Bucket store        │   │
│   │         Replication         │  │            Async            │  │          DR/backup          │   │
│   │           SafeMode          │  │         Locked snaps        │  │      Ransomware resist      │   │
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
│    Physical: FlashBlade//S or //E chassis · storage blades · 100 GbE network · Pure1 SaaS             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashBlade         = Pure massively parallel all-flash NAS and object platform; single namespace   │
│    Blade              = individual storage module in FlashBlade chassis; NVMe and CPU per blade       │
│    File system        = FlashBlade NFS/SMB export namespace; up to 4 PiB per file system              │
│    Object store       = S3-compatible bucket store on FlashBlade; versioning and lifecycle rules      │
│    purefb CLI         = REST CLI client for FlashBlade: purefb fs list, purefb array show commands    │
│    Replication        = async file or object replication between FlashBlade systems for DR            │
│    SafeMode           = admin-locked snapshots; protected from deletion even by local array admin     │
│    S3 multitenancy    = per-bucket policy and IAM-style access control for object storage             │
│    NFS Kerberos       = FlashBlade NFS supports krb5, krb5i, and krb5p security flavours              │
│    SMB multichannel   = FlashBlade uses SMB multichannel for improved Windows client performance      │
│    Inline compression = always-on data reduction; typically 2-10x for unstructured data               │
│    ActiveScale        = enterprise geo-distribution and erasure coding for large object workloads     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
Pure Support Escalation Path — FlashBlade
  Blade failure / incident
          │
          ▼
  Pure1 portal ──► fault auto-detected by phone-home?
          │ Yes ──► Pure may auto-open case + dispatch blade
          │ No  ──► Open case at support.purestorage.com
          │
          ▼
  Case opened ──► Support engineer reviews Pure1 telemetry
          │
          ▼
  Provide: purefb array list, purefb blade list, alert list
          │
          ▼
  Pure TAC ──► Remote session / field engineer / blade dispatch
```

> Part of the [FlashBlade Troubleshooting](index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Support Portal

Pure Storage support is accessed through the support portal at **https://support.purestorage.com**.

All FlashBlade arrays with an active subscription have automatic case creation capability through Pure1. Pure1 (https://pure1.purestorage.com) provides a unified view of array health, active alerts, and open support cases. Phonehome telemetry is transmitted from the array to Pure1 over port 443; when a hardware fault is detected, Pure1 can automatically open a support case and dispatch a replacement part without customer action.

Ensure phonehome is active at all times. To verify from the array:

```bash
purearray phonehome --status
```

## Opening a Case

When opening a case manually, provide the following information to reduce time to resolution:

| Field | How to Obtain |
|---|---|
| Array serial number | Purity GUI > System > Array, or `purearray list` |
| Purity//FB version | `purensshow --version` or `purearray list` |
| Symptom description | Clear description of what is wrong, when it started, and what changed |
| Impact severity | Number of affected users/services, whether production is down or degraded |
| Steps already taken | Commands run, reboots attempted, any changes made before opening the case |

Severity classification at case open determines SLA response time — set severity accurately to receive appropriate response.

## Information to Collect

Run the following commands and attach output to the support case before or immediately after opening:

```bash
# Array identity and software version
purearray list

# All active alerts with severity and description
purealert list

# Full diagnostic bundle (generates a support file on the array)
purediag

# Drive health and status
puredrive list

# Capacity usage across filesystems and object store
purearray list --space

# Recent system message log
puremsg list

# Filesystem list with provisioned and used capacity
purefb filesystem list

# Blade health and status
purefb blade list

# Replication link health and lag
purefb replication list
```

The `purediag` command generates a diagnostic bundle that Pure Support can pull directly via phonehome if the support tunnel is active. If phonehome is offline, download the diagnostic output and attach it to the case via the support portal.

## SLA Tiers

| Priority | Response Time | Description |
|---|---|---|
| P1 | 1 hour, 24x7 | Production system down or critically impaired; no workaround available |
| P2 | 4 hours, 24x7 | Production system degraded; workaround in place but operation is impacted |
| P3 | Next business day | Non-critical issue or question; system is operational with minor impact |
| P4 | Best effort | General enquiry, feature request, or documentation question |

P1 and P2 cases should be followed up with a phone call to the Pure Support line to ensure immediate engagement. Case severity can be escalated at any time if business impact increases.

## Escalation Path

If a case is not progressing at the expected pace or the business impact increases:

1. **Request a duty manager** — use the escalation option in the support portal or ask the support engineer to escalate to a duty manager for senior engagement
2. **Pure TAM contact** — for customers with a Technical Account Manager (TAM), contact the TAM directly for major incidents; the TAM can coordinate resources across support, engineering, and account management
3. **Account team escalation** — for contractual or SLA compliance issues, contact the Pure account executive or customer success manager
4. **Executive escalation** — in cases of sustained outage or repeated resolution failures, request executive-level escalation through your TAM or account executive

For P1 incidents involving data loss risk, request immediate engineering involvement alongside standard support engagement.

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
