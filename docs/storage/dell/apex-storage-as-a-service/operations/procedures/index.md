# APEX Storage as a Service — Procedures

```
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
> Part of the [APEX Storage as a Service](../../index.md) reference.

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
