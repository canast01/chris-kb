# VxRail — Escalation

<div class="kb-summary">
Dell support escalation procedures for VxRail incidents: severity classification, required information checklist, case creation steps, SupportAssist automatic case handling, and TAM escalation path for critical issues.
</div>

```text
┌───────────────────────────────────────── VxRail — Escalation ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────┐       │
│   │  Escalation is required when internal troubleshooting does not resolve the issue          │       │
│   │  P1: production impact / node down / vSAN with no redundancy → call Dell immediately      │       │
│   │  P2: degraded but functional (reduced redundancy, LCM blocked) → open web case           │        │
│   │  P3: no immediate impact (informational alert, single event, planning question)           │       │
│   │  Always check for an existing SupportAssist automatic case before creating a duplicate    │       │
│   └───────────────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                                       │
│   Severity triage         Gather info             Open case              TAM escalation               │
│        │                       │                       │                       │                      │
│        ▼                       ▼                       ▼                       ▼                      │
│   P1/P2/P3?           Cluster serial            dell.com/support         Contact TAM                  │
│   Impact scope        Node service tags         Create Service Request   Provide case #               │
│   Redundancy state    VxRail version            Attach bundle            Request bridge call          │
│   Nodes affected      Symptom timeline          Set severity             Engineering bridge           │
│                       Support bundle            Check SupportAssist                                   │
│                       ESXi bundles                                                                    │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Dell GSS         = Global Support Services; handles all hardware and software support cases         │
│   ProSupport       = Dell premium support tier with defined SLAs per severity level                   │
│   SupportAssist    = Dell automated telemetry and case creation tool embedded in iDRAC                │
│   TAM              = Technical Account Manager; Dell named support contact for critical cases         │
│   Service tag      = Dell hardware serial number; required to open a case on any node                 │
│   P1 SLA           = Next business day or 4-hour on-site response depending on contract               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## When to Escalate

### Severity Classification

| Severity | Definition | Examples | Action |
|---|---|---|---|
| P1 | Production impact; data at risk; no redundancy | Node down + vSAN absent objects; entire cluster offline; vSAN capacity at 100% with VMs failing | Call Dell Enterprise Support immediately |
| P2 | Degraded but functional; redundancy reduced; upgrade blocked | Single node degraded; LCM pre-check failing after multiple fix attempts; vSAN degraded (still accessible) | Open web case; select High severity |
| P3 | No immediate impact; monitoring alert; planning question | Single informational iDRAC event; version question; firmware upgrade assistance | Open web case; standard severity |

### P1 Checklist — Before Calling

Before calling Dell on a P1, have the following ready:

- [ ] VxRail cluster serial number (VxRail Plugin → System → Cluster Info)
- [ ] VxRail software version (VxRail Plugin → System → Software Version)
- [ ] Service tags for all affected nodes
- [ ] Description of the symptom and exact time it started
- [ ] VxRail support bundle (if VxRail Manager is reachable)
- [ ] ESXi vm-support bundles from affected nodes (if reachable)
- [ ] iDRAC SEL export from affected nodes
- [ ] Current vSAN health status screenshot or text output

---

## Required Information Table

Collect all of this before opening any case — incomplete information delays triage.

| Item | How to Retrieve | Notes |
|---|---|---|
| VxRail cluster serial number | VxRail Plugin → System → Cluster Info | Uniquely identifies the cluster in Dell systems |
| VxRail software version | VxRail Plugin → System → Software Version | Include full version string (e.g. 8.0.210-27074590) |
| Node service tags (serial numbers) | VxRail Plugin → Hosts → select node → Details | Required for each affected node |
| ESXi version per node | vCenter → Hosts → Summary | Confirm all nodes are on same ESXi build |
| Symptom description and first occurrence | Timestamps from VxRail Manager logs and vCenter events | Be specific: "First error at 14:32 UTC on 2026-06-01" |
| Steps already taken | Your troubleshooting notes | Prevents Dell repeating steps you have already done |
| VxRail support bundle | VxRail Plugin → Support → Generate Support Bundle | Required for all cases; generate before calling |
| ESXi support bundles | `vm-support -n -w /tmp/` on affected hosts | Required for ESXi-level issues; one bundle per affected host |
| iDRAC SEL export | `racadm getsel` output saved to file | Required for hardware fault cases |
| vSAN health status | vCenter → Cluster → Monitor → vSAN → Health | Screenshot or text copy of all health check results |

---

## Opening a Dell Support Case

### Web Case — Standard Procedure

1. Go to **https://www.dell.com/support/home**
2. Sign in with your Dell account (linked to your organisation's support contract)
3. Navigate to: **My Support → Create Service Request**
4. Enter the service tag of an affected node — the case is associated with that hardware
5. Select the product category: **VxRail**
6. Describe the issue, paste the symptom timeline, and attach bundles
7. Set the severity level (P1 / P2 / P3) — P1 triggers an immediate callback from Dell GSS

### Telephone — P1 Only

For P1 cases (production down, data at risk), call Dell directly:

- **Enterprise Support (US):** 1-800-945-3355 — have the service tag ready when you call
- **International numbers:** Available at https://www.dell.com/support/home → Contact Technical Support → choose your country

When you call, state "P1 VxRail case" immediately so the call is routed to the VxRail-specialised team. VxRail issues escalate automatically to the VxRail engineering team if initial GSS triage cannot resolve within the SLA window.

### Attach Bundles to the Case

After creating the case, upload the following files to the case record on the support portal:

```text
  Required attachments:
  - vxrail-support-bundle-<date>.zip  (from VxRail Plugin → Support)
  - esx-<hostname>-<date>.tgz         (vm-support bundle, one per affected host)
  - idrac-sel-<node-service-tag>.txt  (racadm getsel output)
  - vsan-health-<date>.txt            (esxcli vsan debug health get output)
```

---

## SupportAssist — Automatic Case Creation

SupportAssist is embedded in iDRAC on all VxRail nodes. For critical hardware faults (disk failure, PSU failure, memory uncorrectable ECC), SupportAssist may automatically open a Dell support case and dispatch parts without manual action.

### Check for an Existing SupportAssist Case

Before opening a new case manually, verify a case does not already exist:

1. Log in to the iDRAC web interface of the affected node
2. Navigate to: **Overview → SupportAssist**
3. Review any open cases listed there
4. Alternatively check **https://www.dell.com/support/home → My Cases** — SupportAssist cases appear here

If an automatic case was created, add your notes and bundles to that existing case rather than creating a duplicate. Duplicate cases slow down the response process.

### SupportAssist Registration

For SupportAssist to function, it must be registered on each iDRAC:

```bash
# Check SupportAssist registration status
racadm supportassist view

# Check if SupportAssist is enabled
racadm get SupportAssist.General.Status
```

If SupportAssist is not registered, work with Dell account management to register it — this enables proactive case creation and reduces time to resolution for hardware faults.

---

## TAM Escalation Path

If you have a Technical Account Manager assigned (available under ProSupport Plus and certain enterprise contracts), use this path for critical issues.

### When to Involve the TAM

- P1 case open for more than 4 hours without a resolution path
- Recurring P1/P2 issues on the same cluster
- LCM upgrade has been blocked for more than 30 days
- VxRail engineering involvement needed (escalation beyond GSS)
- Critical business event (DR test, audit, migration) approaching while issue is unresolved

### TAM Escalation Steps

1. Call your TAM directly using their personal contact number (provided in your support contract)
2. Provide the case number for any existing Dell support case
3. State the business impact and timeline (e.g., "production down, 200 VMs offline since 06:00")
4. Request a technical bridge call with the VxRail engineering team if GSS has not resolved the issue

### Requesting an Engineering Bridge

If the issue is beyond GSS's ability to resolve, your TAM can arrange a bridge call with Dell VxRail engineering. Prepare:

- Case number
- VxRail support bundle uploaded to the case
- Timeline of all troubleshooting steps already taken
- Specific technical question or failure mode you need engineering to investigate

---

## Emergency Parts Dispatch

For a node with a failed disk where vSAN components are becoming absent, request an emergency parts dispatch when opening or updating the case:

- Specify your support contract level (Next Business Day / 4-Hour On-Site)
- Provide the physical location of the server (site address, rack, unit position)
- Confirm the part number from the iDRAC SEL or `racadm storage get pdisks` output

```bash
# Identify the failed disk part number and slot
racadm storage get pdisks -o -p State,ProductID,MediaType,FQDD

# Example output:
# FQDD = Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.1-1
# ProductID = SSDSCKKB480G8R
# State = Failed
```

Provide the FQDD and ProductID to Dell support to ensure the correct replacement part is dispatched.
