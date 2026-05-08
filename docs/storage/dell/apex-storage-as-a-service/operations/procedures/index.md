# APEX Storage as a Service — Procedures

> Part of the [APEX Storage as a Service](../../) reference.

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
