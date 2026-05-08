# vSAN — Escalation

Guidance on when to escalate vSAN incidents to VMware (Broadcom) support, what to collect before opening a case, and how to manage escalation effectively.

---

## When to Escalate

### Escalate Immediately (P1 — Data Risk)

Open a support case and mark it Priority 1 if any of the following conditions exist:

| Condition | Why It Is P1 |
|---|---|
| VM objects in "Inaccessible" state and cannot be recovered after network and host checks | Production VMs are completely unavailable |
| More host or disk failures than FTT policy can tolerate | Risk of data loss — cluster is below minimum fault protection |
| vSAN datastore disappears from vCenter | Complete management plane or data plane failure |
| Object resync has shown zero progress for > 4 hours with confirmed network and capacity health | Blocked rebuild — increasing data loss risk with each passing hour |
| Disk group failure on a host that is already the sole survivor of a previous failure | One more disk failure = permanent data loss |

Contact VMware Support: [support.broadcom.com](https://support.broadcom.com) — use the phone option for P1 cases.

### Escalate Same Day (P2 — Degraded Cluster)

Open a support case and mark it Priority 2 if:

| Condition |
|---|
| One or more objects degraded for > 24 hours with no hardware failure identified |
| Resync has been running for > 48 hours on a single host or disk replacement |
| Skyline Health shows RED for Data Integrity or Object Health after the expected recovery window |
| A disk group repeatedly goes offline and comes back without an identified cause |
| vSAN network health test consistently reports packet loss and network teams cannot find the cause |
| Cluster encryption key management errors that cannot be resolved through KMS configuration |

### Escalate Within the Week (P3 — Warning State)

| Condition |
|---|
| Skyline Health has persistent YELLOW tests that are not resolved by documented remediation steps |
| Capacity is consistently above 70% and expansion is not yet approved |
| Performance degradation that cannot be attributed to known workload changes |
| HCL check fails for hardware that you believe is certified (possible HCL database issue) |
| Questions about ESA migration planning or stretched cluster design validation |

---

## Pre-Escalation Checklist

Collect all of the following before opening a case. A complete first submission significantly reduces time to resolution — VMware support will request this data regardless.

### State Capture

```bash
# On each affected ESXi host — capture cluster and object state
esxcli vsan cluster get > /tmp/vsan_cluster_state.txt
esxcli vsan health cluster list >> /tmp/vsan_cluster_state.txt
esxcli vsan debug object list >> /tmp/vsan_cluster_state.txt
esxcli vsan debug resync summary get >> /tmp/vsan_cluster_state.txt
esxcli vsan storage list >> /tmp/vsan_cluster_state.txt
esxcli vsan network list >> /tmp/vsan_cluster_state.txt
esxcli vsan debug network test >> /tmp/vsan_cluster_state.txt

# Save to a time-stamped file
cp /tmp/vsan_cluster_state.txt \
    /tmp/vsan_state_$(date +%Y%m%d_%H%M%S).txt
```

### Information Template

Prepare the following information before submitting the case:

```
Environment:
  vSphere version:         e.g. 8.0 U2
  vSAN version / mode:     e.g. 8.0 U2 ESA / OSA
  Cluster host count:      e.g. 6 nodes
  vSAN storage policy:     e.g. FTT=2, RAID-6
  Stretched cluster:       Yes / No
  Encryption:              Yes (KMS type) / No

Incident timeline:
  When problem first detected:    YYYY-MM-DD HH:MM UTC
  What changed before the issue:  e.g. ESXi patch applied, disk replaced
  Current cluster health state:   e.g. 2 hosts degraded, 14 objects absent

Current health:
  esxcli vsan cluster get output: <paste>
  esxcli vsan debug object list non-healthy output: <paste>
  esxcli vsan debug resync summary get output: <paste>

Error messages:
  Skyline Health alerts: <paste>
  vmkernel.log errors: <paste relevant lines>
  vsanmgmt.log errors: <paste relevant lines>
```

### Support Bundle

Generate a full support bundle before opening the case (see Diagnostics → Support Bundle Collection):

```bash
# VCSA shell — generate support bundle
vc-support -l /tmp/vc-support-$(date +%Y%m%d).tgz

# ESXi host shell — per-host bundle for each affected host
vm-support --log-level 6 --vsan
```

Upload the bundle to the case when prompted. Bundles can be uploaded via the Broadcom support portal or via the `sftp` transfer instructions provided in the case.

---

## Opening the Case

### Broadcom Support Portal

URL: [https://support.broadcom.com](https://support.broadcom.com)

1. Log in with your Broadcom account (linked to your support entitlement).
2. Navigate to **Support** → **Open a Support Request**.
3. Select product: **VMware vSAN** or **VMware vSphere**.
4. Enter severity and summary.
5. Paste the environment information and state capture output.
6. Attach the support bundle.

### Phone Escalation (P1)

For P1 cases, do not rely on portal submission alone. Call the VMware support line:
- North America: +1 (877) 486-9273
- EMEA: +44 (0)3453 700 100
- Full list: [https://www.broadcom.com/support/vmware/contact-support](https://www.broadcom.com/support/vmware/contact-support)

State "Priority 1 — production down" clearly at the start of the call. Request direct assignment to a vSAN support engineer.

---

## Working the Case

### What to Expect from VMware Support

| Stage | Typical Timeline | What Happens |
|---|---|---|
| Initial response | P1: < 30 min; P2: < 2 hours; P3: < 8 hours | Engineer assigned; initial data request |
| Data analysis | 1–4 hours after data receipt | Engineer reviews bundle, logs, state capture |
| Root cause | P1: same day; P2: 1–3 days | Identified or escalated to engineering |
| Resolution | Varies | Workaround or patch provided |

### Maintain a Case Log

Keep a running log of:
- Case number and assigned engineer name.
- All data submitted and when.
- Each action taken and its result.
- Timestamps of all communications.

This is especially important for P1 cases where multiple engineers may be involved across shifts.

### Escalate Within Support (if Needed)

If progress stalls:

1. Request escalation to a senior vSAN engineer or vSAN team lead.
2. If case severity is not being treated appropriately, contact your account team or TAM (Technical Account Manager).
3. For critical data loss scenarios, request a Conference Bridge call with the vSAN engineering team.

---

## Internal Escalation Path

Define your internal escalation path before an incident occurs:

```mermaid
graph TD
    incident(["vSAN incident detected"])
    l1["L1 — On-call storage engineer\nInitial investigation\n(first 30 minutes)"]
    l1check{"Resolved\nwithin 1 hour?"}
    l2["L2 — Storage team lead\nSenior engineer\nDeeper diagnosis"]
    l2check{"Inaccessible objects\nor P1 confirmed?"}
    l3["L3 — Platform / Infra Manager\nBusiness impact confirmed\nStakeholders notified"]
    vendor["VMware Support\n(Broadcom)\nP1: < 4 hours\nP2: < 24 hours"]
    resolved(["Incident resolved"])

    incident --> l1
    l1 --> l1check
    l1check -->|"Yes"| resolved
    l1check -->|"No"| l2
    l2 --> l2check
    l2check -->|"Yes"| l3 --> vendor
    l2check -->|"No — P2/P3"| vendor
    vendor --> resolved

    classDef level fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    classDef vendor fill:#dc2626,stroke:#b91c1c,color:#fff

    class l1,l2,l3 level
    class l1check,l2check decision
    class incident,resolved terminal
    class vendor vendor
```

| Level | Role | When |
|---|---|---|
| L1 | On-call storage engineer | Initial investigation — first 30 minutes |
| L2 | Storage team lead / senior engineer | L1 cannot resolve within 1 hour, or any inaccessible objects |
| L3 | Platform or infrastructure manager | P1 incident declared, business impact confirmed |
| Vendor | VMware Support | L2 cannot identify root cause within 4 hours (P1) or 24 hours (P2) |

Document the escalation path in your runbook and ensure on-call contacts are current and tested.

---

## Post-Incident Actions

After a vSAN incident is resolved, complete the following:

### Root Cause Analysis (RCA)

| Section | Contents |
|---|---|
| Incident summary | What failed, when, what was impacted |
| Timeline | Chronological list of events, detections, and actions |
| Root cause | Hardware failure, software bug, misconfiguration, operator error |
| Contributing factors | Capacity headroom, FTT policy, monitoring gaps |
| Resolution | Steps taken to resolve |
| Preventive actions | What changes will prevent recurrence |

### Preventive Actions Checklist

After any disk or disk group failure:

- [ ] Verify FTT policy is appropriate for the cluster size and risk tolerance.
- [ ] Confirm disk replacement SLA with hardware vendor — how quickly can a replacement arrive?
- [ ] Review capacity headroom — was the cluster above 70% before the failure?
- [ ] Confirm resync throttle policy — is it set too low, slowing recovery?
- [ ] Review monitoring — was the disk failure detected before it caused an outage?
- [ ] Check HCL compliance — was the failed disk on the vSAN HCL?
- [ ] Verify NTP configuration — time drift can mask or complicate disk group failures.

After any network-related vSAN issue:

- [ ] Document the vSAN network topology (switch, port, VLAN, MTU) for all hosts.
- [ ] Confirm MTU is 9000 end-to-end and tested with `vmkping -d -s 8972`.
- [ ] Review NIOC configuration — is vSAN traffic getting adequate bandwidth share?
- [ ] Confirm redundancy — are vSAN vmkernels teamed across two physical NICs?

### VMware Knowledge Base

Search the VMware Knowledge Base before and after incidents:
[https://knowledge.broadcom.com](https://knowledge.broadcom.com)

Search by: error message, health check name, symptom description. Many vSAN issues have published KB articles with specific resolution steps.
