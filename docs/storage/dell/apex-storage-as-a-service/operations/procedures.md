---
tags:
  - dell
  - operations
---
# APEX Storage as a Service — Procedures


<div class="kb-summary">
Procedures reference covering Incident Triage, Maintenance Window, Operational Tasks.

*Applies to: APEX Storage-as-a-Service*
</div>

```text
┌────────────────────────────── Dell Apex STaaS — Operational Procedures ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Apex procedures: create and map volumes, NFS exports, snapshots, capacity expansion      │   │
│   │          Volume create: Apex Console > Storage > Volumes > Create; set size and tier          │   │
│   │        NFS export: Apex Console > Storage > File > Create Share; set client access list       │   │
│   │      Capacity expand: raise SR in Apex Console; Dell processes and provisions within SLA      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Create volume → map host → host rescan → format/mount → monitor → snapshot schedule                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Block Volumes        │  │        File (NFS/SMB)       │  │        Data Services        │   │
│   │        Create volume        │  │         Create share        │  │         Create snap         │   │
│   │        Set size/tier        │  │        Set client ACL       │  │         Set schedule        │   │
│   │         Map to host         │  │        Mount on host        │  │          Clone snap         │   │
│   │         Host rescan         │  │          Test write         │  │        Restore clone        │   │
│   │         Format/mount        │  │         Expand share        │  │         Delete snap         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All capacity expansion requires a Dell SR; planned changes need lead time (days)                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Procedure     │   Portal path    │      Key step     │      Verify      │      Notes       │   │
│   │    Create vol    │   Storage>Vols   │    Size + tier    │   LUN visible    │   Thin default   │   │
│   │     Map host     │  Storage>Hosts   │      IQN/WWN      │     Host LUN     │    Rescan bus    │   │
│   │    NFS share     │   Storage>File   │    Client CIDR    │    Mount test    │    NFS v3/v4     │   │
│   │   Snap policy    │  Data Svc>Snap   │    Freq+retain    │   Snap listed    │     No quota     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: host HBA/NIC and OS multipath · NFS client on Linux/VMware · iSCSI initiator             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Host rescan      = OS command to detect new LUNs: iscsiadm rescan / hbacmd; or vCenter rescan      │
│    Client ACL       = NFS share access list; specify host IP or CIDR; rw or ro                        │
│    Thin default     = Apex volumes are thin-provisioned by default; physical use grows on write       │
│    LUN visible      = After mapping, host must see LUN via multipath; check multipathd/mpio           │
│    Snap policy      = Defines frequency (hourly/daily/weekly) and retention count                     │
│    Clone from snap  = Create writable volume from snapshot; mount as separate device                  │
│    Capacity expand  = Open SR specifying current committed + desired new committed size               │
│    NFS v4           = NFSv4 recommended for Kerberos security and improved locking                    │
│    IQN              = iSCSI Qualified Name; unique identifier for iSCSI initiator (host HBA)          │
│    WWN              = World Wide Name; unique FC port identifier; used in FC zoning and maps          │
│    Expand share     = Increase NFS share quota; non-disruptive in most cases                          │
│    iscsiadm         = Linux iSCSI management tool; discover, login, and rescan iSCSI targets          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [APEX Storage as a Service](../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Incident Triage

**On alert or issue:**
1. Log in to CloudIQ and check the health score and active alerts for the affected APEX system
2. Review the anomaly timeline in CloudIQ to identify when the degradation began and correlate with any change activity
3. Check the APEX console for any active Dell-managed maintenance or known service incidents
4. If performance degradation is confirmed and not tied to a Dell maintenance window, open a Dell support case directly from the CloudIQ alert — Dell is responsible for infrastructure remediation
5. If capacity is approaching the contracted limit, log in to the APEX console and initiate a capacity increase request

| Symptom | Likely Cause | Action |
|---|---|---|
| APEX system performance degradation | Infrastructure fault (Dell-managed) or workload surge | Check CloudIQ health score and anomaly timeline; open Dell support case if hardware/infra fault |
| Capacity alert: approaching contracted limit | Workload growth exceeding contracted amount | Log in to APEX console, review consumed capacity, contact Dell account team to amend contract |
| System shows offline or unreachable | Dell-managed infrastructure outage or network issue | Check APEX console for service status, open P1 support case with Dell if not a planned window |
| SLA breach concern (IOPS below SLA) | Workload exceeds SLA tier commitment | Collect CloudIQ performance data, open support case with Dell SLA breach evidence |
| CloudIQ showing "Not Reporting" for APEX system | SCG connectivity failure | Check SCG appliance: `dsagw status`, `dsagw list-devices`, `dsagw connectivity-check` |

## Maintenance Window

Dell is responsible for APEX infrastructure maintenance. Customer responsibilities during Dell-scheduled windows:

1. Confirm receipt of Dell's maintenance notification and acknowledge the scheduled window
2. Assess potential workload impact during the window — notify application owners if I/O disruption is possible
3. Confirm no customer-side changes (provisioning, workload migrations) are scheduled to overlap with the Dell window
4. Monitor the APEX system in CloudIQ and the APEX console during the window
5. After the window: confirm the system health score has returned to pre-maintenance baseline
6. If the system did not recover automatically after the Dell window, open a Dell support case immediately

## Operational Tasks

| Task | Notes |
|---|---|
| Raise a capacity increase request | APEX Console → Subscriptions → Request Capacity |
| Review monthly usage report | APEX Console → Billing & Usage; export for finance |
| Add or modify user access | Administration → Users & Roles in APEX Console |
| Open a support case | APEX Console → Support |
| Review underlying platform health | Check PowerStore/PowerScale/PowerFlex management UI directly if needed |

---

## Request Capacity Expansion

1. Log in to the APEX Console (console.dell.com/apex)
2. Navigate to **Services** and select the relevant APEX service
3. Click **Request Expansion** and specify the additional capacity required (in TB) and the desired tier
4. Submit the request — Dell will review and provision the additional capacity within the contracted SLA (typically measured in days)
5. Monitor the request status in **APEX Console → Support → Cases**
6. After provisioning is confirmed by Dell, verify the new capacity is visible in **Services → Capacity** and update the CMDB

## Open a Support Case from APEX Console

1. Log in to the APEX Console and navigate to **Support → New Case**
2. Select the affected service from the dropdown
3. Enter a clear description of the issue, including symptoms, start time, and any steps already taken
4. Attach relevant logs or screenshots to accelerate triage
5. Set the severity level appropriate to the business impact (P1 for outage, P2 for degraded, P3/P4 for non-urgent)
6. Submit — Dell support will acknowledge within the contracted response SLA and begin engagement

## Configure Data Protection Policy

1. Log in to the APEX Console and navigate to **Data Protection**
2. Select the service or volume group to protect
3. Click **Assign Snapshot Policy** and choose or create a policy specifying:
   - Snapshot frequency (hourly, daily, weekly)
   - Retention count or period
4. Apply the policy — snapshots begin on the next scheduled interval
5. Verify the policy is active in **Data Protection → Policies** and confirm the first snapshot completes successfully

## Review SLA Compliance Report

1. Log in to the APEX Console and navigate to **Reports → SLA Compliance**
2. Set the reporting period (typically the previous calendar month)
3. Review the report: available capacity, IOPS SLA met/missed, latency against SLA targets
4. Export the report (PDF or CSV) for management distribution or finance review
5. If any SLA breaches are identified, cross-reference with open support cases and request a Root Cause Analysis from Dell if applicable

## Initiate Service Migration (APEX Data Migration)

1. Contact the Dell account team to request a formal migration plan — migrations between APEX service tiers or infrastructure platforms are Dell-managed
2. Dell provides a migration assessment: data volume, estimated duration, and any downtime requirements
3. Within the approved change window, Dell uses the APEX migration tooling to copy data from the source service to the destination service tier
4. Monitor migration progress via the APEX Console and via the Dell support case
5. After migration completes, validate: mount points accessible, data integrity confirmed, performance metrics within expected range
6. Perform application-level validation with the application owners, then confirm cutover is complete
7. Decommission the old service after a post-migration soak period (typically 5–10 business days)

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
