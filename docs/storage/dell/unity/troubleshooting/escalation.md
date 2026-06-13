---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# Unity — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Path.

*Applies to: Unity XT*
</div>
```text
┌───────────────────────────────────── Dell Unity XT — Escalation ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Unity XT escalation: severity triage, vendor support contact, and required artifacts     │   │
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
│   │             Ctrl            │  │         SP-A + SP-B         │  │        Cache mirrored       │   │
│   │             Pool            │  │       Dynamic FAST VP       │  │         Auto-tiering        │   │
│   │          NAS server         │  │        File protocols       │  │          Per-tenant         │   │
│   │           Snapshot          │  │        Writable snaps       │  │        Thin PiT copy        │   │
│   │         Replication         │  │         Async/Metro         │  │       Native or RP4VM       │   │
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
│    Physical: Unity XT 380F/480F/680F/880F · dual SPs · DPE/DAE expansion · 10/25 GbE                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Unity XT           = Dell unified mid-range array; block LUNs, file NAS, and VMware vVols          │
│    Unisphere          = HTML5 GUI and REST API for Unity XT management; SP-hosted management portal   │
│    UEMCLI             = CLI for Unity XT; uemcli -d <ip> -u admin -p <pw> /show commands              │
│    Storage pool       = collection of drives forming a usable pool; FAST VP tiers data automatically  │
│    FAST VP            = Fully Automated Storage Tiering VP; moves hot and cold data between tiers     │
│    NAS server         = virtual file server on Unity; each has its own IP, DNS, and CIFS/NFS shares   │
│    Data Mover         = older EMC term for NAS server; used in VNX and early Unity documentation      │
│    SP-A / SP-B        = storage processors; active-active HA pair with mirrored cache                 │
│    Snapshot           = space-efficient PiT copy of LUN or FS; writable snapshots supported           │
│    RecoverPoint       = RP4VM; journal-based continuous data protection for Unity volumes             │
│    Metro              = synchronous replication between two Unity XT sites; active-active zero RPO    │
│    vVols              = Virtual Volumes; VASA provider exposes per-VM storage objects to vCenter      │
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

Open and manage Unity support cases at [https://www.dell.com/support](https://www.dell.com/support). Log in with your Dell account and navigate to **My Cases** to create, update, and track cases.

SupportAssist (formerly ESRS/SRS) is embedded in Unity OE and automatically opens hardware fault cases when an SP, drive, or power module fails. Verify SupportAssist is enabled and calling home in Unisphere under **Settings > Support > SupportAssist**. Test connectivity using the **Send Test Alert** button.

## Opening a Case

Required information before opening a case:

| Field | How to Obtain |
|---|---|
| SP serial numbers | Chassis label on each SP; or Unisphere > **System > Hardware** |
| Unity OE version | `uemcli /sys/sw show`; or Unisphere > **System > Software** |
| Symptom description | Clear description of what failed, when it started, and frequency |
| Pool and LUN names affected | `uemcli /stor/pool show`, `uemcli /stor/prov/luns show` |
| Client impact | Hosts and applications affected; protocols (FC, iSCSI, NFS, SMB) |
| Recent changes | Any firmware, OE, or configuration changes made in the 48 hours before the fault |

For SP hardware failures or drive faults, Dell dispatches replacement parts automatically when SupportAssist is enabled. For P1 cases (production I/O interrupted), call the Dell support line directly rather than using only the portal.

## Information to Collect

```bash
# Show system general health and software version
uemcli -d <sp_ip> -u admin -p <password> /sys/general show

# Show all components not in OK health state
uemcli -d <sp_ip> -u admin -p <password> /env/health show -filter "health.value ne OK"

# Show all active alerts
uemcli -d <sp_ip> -u admin -p <password> /sys/alert show

# Show alert history
uemcli -d <sp_ip> -u admin -p <password> /sys/alert/hist show
```

**Collect the service support bundle** from Unisphere:

1. Navigate to **System > Support > Collect Service Information**.
2. Click **Collect** and wait for the bundle to complete (typically 5–15 minutes).
3. Download the bundle file and upload it to the Dell support case using the **Secure Upload** link in the case.

Alternatively, initiate via CLI: `uemcli /sys/serviceinfo collect`.

Include a **screenshot of the Unisphere health dashboard** showing the fault state to provide immediate context to the support engineer.

## SLA Tiers

| Tier | Priority | Response Time | Coverage | Parts Replacement |
|---|---|---|---|---|
| ProSupport Plus | P1 — Production Down | 2 hours | 24x7x365 | 4-hour on-site (where available) |
| ProSupport Plus | P2 — Degraded Performance | 4 hours | 24x7x365 | Next business day |
| ProSupport Plus | P3/P4 | Next business day | Business hours | Next business day |
| ProSupport | P1 | 4 hours | 24x7x365 | Next business day |
| ProSupport | P2–P4 | Next business day | Business hours | Next business day |

Verify your Unity system's support contract level in the Dell support portal under **My Products and Services**.

## Escalation Path

If a P1 case is not progressing within the response SLA or the fault is causing a prolonged production outage:

1. Call the Dell support line and request **escalation for an open case** — provide the case number and explain the business impact.
2. Contact your **Dell account team Technical Account Manager (TAM)** — TAMs have direct escalation paths into the Unity engineering and field services teams.
3. For multi-hour production outages with no resolution in sight, request engagement with **Dell Global Priority Services (GPS)** via your account team. GPS provides senior engineering support beyond standard case handling.
4. When escalating, always state: case number, SP serial numbers, current fault status, duration of impact, number of hosts/applications affected, and what has already been tried.

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
