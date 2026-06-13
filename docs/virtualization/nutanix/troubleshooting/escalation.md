---
tags:
  - nutanix
  - troubleshooting
  - escalation
  - support
  - gss
---
# Nutanix — Escalation

<div class="kb-summary">
When and how to escalate to Nutanix Global Support Services (GSS) — severity classification, support portal procedure, information to collect before calling, and critical situation handling.

*Applies to: AOS 6.x · AHV*
</div>

---

## Before you begin

- **Access:** Nutanix Portal account linked to your support contract (portal.nutanix.com); ensure your account has access to the affected cluster's serial numbers
- **Collect first:** NCC output and support bundle — GSS will request these immediately; having them ready cuts resolution time significantly

---

## When to Escalate Immediately

Escalate to Nutanix GSS **without delay** for:

- **Cluster cannot tolerate failure** — `CAN_TOLERATE_FAILURE_COUNT=0` and a node or disk is degraded
- **Production VMs are down** and you cannot restore them
- **Data loss suspected** — Stargate returning I/O errors to VMs
- **CVM unresponsive** and hardware-level access (IPMI/console) shows hardware faults
- **Multiple disks failed on same node**
- **Cluster will not accept writes** (storage full + no quick way to free space)

For all other issues, attempt NCC triage and log review first (see [Diagnostics](diagnostics/)), then open a lower-severity case.

---

## Severity Classification

| Severity | Definition | Nutanix SLA |
|---|---|---|
| S1 — Critical | Production cluster down / data loss | 30-minute response, 24×7 |
| S2 — Major | Significant degradation, partial outage | 4-hour response, 24×7 |
| S3 — Moderate | Non-critical cluster impact, workaround available | Next business day |
| S4 — Low | General questions, how-to, feature requests | Next business day |

Open all production-impacting issues as S1 or S2. You can always downgrade; it's harder to upgrade once the case is open.

---

## Before You Call / Open a Case

Collect the following before contacting GSS:

**Cluster info:**
```bash
ncli cluster info   # cluster name, AOS version, RF
ncli host list      # node serial numbers and IPs
ncli disk list | grep -v NORMAL   # any failed disks
```

**NCC results:**
```bash
ncc --health_checks run_all 2>&1 > /tmp/ncc-$(date +%Y%m%d).txt
# Attach the full output
```

**Support bundle:**
```text
Prism Element → Settings → Log Collector → Collect Logs (last 4 hours)
# Download and attach to the case
```

**Incident summary:**
- What changed before the issue started (upgrade, maintenance, config change)?
- Exact time the issue started
- Which VMs or services are impacted
- Steps already taken and their results

---

## Opening a Support Case (Nutanix Portal)

```text
1. Go to: https://portal.nutanix.com
2. Log in with your Nutanix Portal account
   (linked to your support contract — account setup done during purchase)
3. Support → Cases → Open New Case
4. Fill in:
   - Cluster: select from registered clusters (auto-populates serial numbers)
   - Severity: S1/S2/S3/S4
   - Summary: one-line description ("CVM on <ip> unreachable, Genesis not responding")
   - Description: symptom timeline, VMs affected, steps taken
5. Attach: NCC output, support bundle, relevant screenshots
6. Submit → you receive a case number immediately

For S1/S2 also call the phone support number on the portal to get immediate live response.
```

**Phone numbers** — visible after login at portal.nutanix.com/support/phone. Do not share here as they change.

---

## What Nutanix GSS Will Ask

Be ready to provide:

1. **Case number** (if calling in on an existing web case)
2. **Cluster UUID** — `ncli cluster info | grep UUID`
3. **AOS version** — `ncli cluster info | grep Version`
4. **Affected node serial numbers** — `ncli host list`
5. **NCC output** already attached to case
6. **Support bundle** — GSS will often request a fresh one
7. **Permission to access cluster remotely** — Nutanix uses Pulse for remote access (if Pulse is enabled)

---

## Enabling Remote Access for GSS

Nutanix support engineers access clusters via Nutanix Pulse (call-home tunnelling).

```text
Prism Element → Settings → Pulse
  Enable Pulse: Yes (required for remote access)
  Test Connection: Verify Pulse shows "Connected"
```

If Pulse is disabled (air-gapped environments):
- GSS will use WebEx/Teams screen share
- Or you provide Jump Host access under GSS supervision

---

## Nutanix Knowledge Base

Before or alongside a case, search the Nutanix Knowledge Base:

```text
portal.nutanix.com/page/documents/kbs
# Search by NCC check name, alert title, or error message
# KB articles often have exact KB-XXXXX identifiers — cite these in your case
```

Common resolution patterns come from KB articles. GSS will reference these directly.

---

## Post-Incident

After issue resolution:
- Request a Root Cause Analysis (RCA) from GSS if the issue caused production impact
- GSS provides RCA within 5 business days for S1 cases
- Update your internal incident record with the KB article reference and resolution steps
- Schedule NCC run 24 hours after resolution to confirm clean state

---

## See also

- [Nutanix — Diagnostics](diagnostics/)
- [Nutanix — Common Issues](common-issues/)
