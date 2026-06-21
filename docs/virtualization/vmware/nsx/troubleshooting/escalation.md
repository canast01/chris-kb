---
tags:
  - nsx
  - nsx-4
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# NSX — Escalation

<div class="kb-summary">
How to escalate NSX networking issues to Broadcom support: what data to collect, how to generate the NSX support bundle, step-by-step SR submission on the Broadcom portal, and the escalation path when progress stalls.

*Applies to: NSX 3.x / 4.x*
</div>
![NSX — Escalation](../../../../assets/virtualization-vmware-nsx-troubleshooting-escalation.svg)




---

## Before you begin

- **Access required:** SSH to each NSX Manager node; NSX Manager API access (admin credentials); Broadcom support account with entitlement to NSX
- **Do this first:** collect all data below before changing anything. Broadcom will ask for the support bundle in their first response
- **Do NOT change DFW rules** while the issue is open — adding or removing rules changes the enforcement state and makes diagnosis harder
- **Do NOT restart NSX Manager** unless Broadcom instructs you to. Restarting a Manager node in a DEGRADED cluster can cause split-brain

---

## Pre-Escalation Self-Check

Run these before opening the SR. Many NSX issues are resolvable without Broadcom.

| Check | What to do | Expected result |
|---|---|---|
| Manager cluster health | NSX Manager UI → System → Overview | All nodes show green |
| Manager cluster API | `curl -sk -u admin:<pw> https://<mgr>/api/v1/cluster/status` | `"control_cluster_status": "STABLE"` |
| Transport nodes | NSX Manager UI → Fabric → Nodes → Transport Nodes | All nodes Connected |
| TEP reachability | SSH to ESXi: `vmkping -I vmk10 <remote-tep-ip> -d -s 1500` | Replies received; increase to 8972 for jumbo |
| BGP sessions | SSH to Edge: `get bgp neighbor summary` | All peers in Established state |
| Alarms | NSX Manager UI → Alarms → Active | Note all CRITICAL alarms |
| NSX-vCenter sync | NSX Manager UI → System → vCenter → Registration status | Status: Connected |
| NSX version | `get version` from Manager CLI or API `/api/v1/node/version` | Matches your change record |

---

## Step-by-Step Data Collection

Run all of these before opening the SR.

### 1. Get the NSX version and build number

```bash
# SSH to any NSX Manager node
ssh admin@<nsx-manager>

# Get version via CLI
get version

# Or via API
curl -sk -u admin:<password> https://<nsx-manager>/api/v1/node/version
# Note: include build number in the SR, not just the release version
```

### 2. Capture the Manager cluster status

```bash
# Full cluster status — paste this into the SR description
curl -sk -u admin:<password> https://<nsx-manager>/api/v1/cluster/status | python3 -m json.tool

# Control and management cluster nodes
curl -sk -u admin:<password> https://<nsx-manager>/api/v1/cluster/nodes | python3 -m json.tool

# Transport node status — shows all hosts and edges
curl -sk -u admin:<password> "https://<nsx-manager>/api/v1/transport-nodes/status?status=DOWN" | python3 -m json.tool

# Active alarms
curl -sk -u admin:<password> "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL" | python3 -m json.tool
```

### 3. Generate the NSX support bundle (takes 10–30 minutes)

```bash
# Trigger support bundle generation via API
curl -sk -u admin:<password> \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"log_age": 48, "components": ["MANAGER", "CONTROLLER", "EDGE", "HOST"]}' \
  "https://<nsx-manager>/api/v1/node/support-bundles"
# Note the bundle ID returned in the response

# Poll for completion — repeat until status shows "SUCCESS"
curl -sk -u admin:<password> \
  "https://<nsx-manager>/api/v1/node/support-bundles/status"

# Download the bundle (URL provided in the status response)
curl -sk -u admin:<password> \
  -O "https://<nsx-manager>/api/v1/node/support-bundles/download/<bundle-id>"
```

### 4. Run Traceflow (for traffic drop or DFW issues)

In NSX Manager UI:

1. Go to **Plan & Troubleshoot** → **Traceflow**.
2. Fill in source VM, destination IP, protocol, and port.
3. Click **Trace**. Wait for results.
4. Click **Export** to download the trace as a JSON or PDF file. Attach this to the SR.

Include in the SR description: source VM, destination, the rule or component that dropped the packet, and what you expected to happen.

### 5. Write the timeline

```text
NSX version: 4.1.2 build 23182604
Manager nodes: nsx-mgr-01, nsx-mgr-02, nsx-mgr-03
vCenter: vcenter-01 (8.0 U2)
Issue first observed: 2026-06-14 14:30 UTC
Last known good state: 2026-06-14 09:00 UTC
Changes in the 24h before the issue:
  - 09:00: NSX 4.1.1 → 4.1.2 upgrade initiated via LCM
  - 14:25: Upgrade task showed FAILED on Edge cluster upgrade
  - 14:30: DFW drops reported on 3 workload VMs
Steps already taken:
  - Verified Manager cluster status: STABLE (Managers OK, Edges failed)
  - Ran Traceflow: packet dropped at DFW rule ID 1234 on host esxi-prod-02
  - Did NOT retry the upgrade or modify DFW rules
Blast radius: 3 VMs in tenant-A segment can no longer reach database segment
```

---

## How to Open the SR on Broadcom Support Portal

1. Go to **support.broadcom.com** and sign in. If you do not have an account: click **Register** and use your company email — entitlement is linked to your Broadcom contract.

2. Click **Open a New Case** in the top navigation.

3. Under **Select Product Family**, choose **VMware NSX**.

4. Under **Product Version**, select your exact NSX version from the drop-down.

5. Under **Request Type**, select **Technical**.

6. Under **Severity**, select:
   - **S1 — Critical**: NSX Manager cluster DEGRADED and you cannot manage networking; DFW drops all production traffic; network is completely down with no workaround
   - **S2 — Major**: A key NSX workflow is failing (upgrade, Edge deployment) but existing VMs retain network connectivity; you have a partial workaround
   - **S3 — Minor**: Single tenant segment affected; non-critical feature degraded; network remains functional for most VMs
   - **S4 — General**: How-to, pre-check, or non-urgent configuration question

7. In the **Summary** field, write one sentence: product + symptom + scope. Example: `NSX 4.1.2 — Edge cluster upgrade failed at 14:25 UTC, DFW dropping traffic for 3 VMs in tenant-A segment`.

8. In the **Description** field, paste:
   - NSX version and build number
   - Manager cluster status API output
   - The timeline from Step 5
   - Traceflow export result (summarise what was dropped and where)
   - Active CRITICAL alarms list
   - What you have already tried

9. Under **Attachments**, upload:
   - The NSX support bundle from Step 3
   - The Traceflow export from Step 4
   - Any screenshots of NSX Manager alarms or cluster status

10. Click **Submit**. You will receive a case number by email immediately.

11. **S1 only:** the case confirmation page shows a regional phone number. Call it immediately and state "Severity 1 — NSX network is down" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at support.broadcom.com with NSX support bundle attached
         ↓
Step 2 — T1 support acknowledges and confirms bundle received (typically 30 min–4 hr)
         ↓
Step 3 — If no meaningful progress in 4 hours for S1 or 1 business day for S2:
         → Reply in the case: "Requesting T2 NSX Senior Engineer assignment"
         → State: "Impact: [X] VMs offline / Manager DEGRADED / upgrade failed"
         ↓
Step 4 — T2 NSX SE is assigned; they will schedule a live Zoom/Webex session
         → Have SSH access to NSX Manager and Edge nodes ready for the call
         → Have vSphere Client and NSX Manager UI open
         ↓
Step 5 — If T2 cannot resolve and issue requires code-level investigation:
         → T2 escalates to T3 (NSX engineering) — you do not need to initiate this
         ↓
Step 6 — For complete network outage, data loss risk, or 24h+ with no resolution:
         → Request a Critical Situation (CritSit) engagement
         → Add to case: "Requesting CritSit — [reason: network down / 24h no progress]"
         → CritSit brings dedicated team lead + exec visibility
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Restart NSX Manager service | Can cause split-brain in the Manager cluster if nodes are mid-sync | Only restart if explicitly instructed by Broadcom GSS |
| Reboot Edge nodes | Causes BGP session drops and traffic loss across all tenants using that Edge | Have GSS assess which Edge is safe to reboot first |
| Add or delete DFW rules mid-incident | Changes enforcement state; makes Traceflow results unreliable | Freeze all firewall policy changes until resolution |
| Retry a failed NSX upgrade | Can leave Managers and Edges at mixed versions; harder to recover | Wait for GSS to confirm the upgrade is safe to retry |
| Delete and re-add a Transport Node | Loses all TEP and host prep configuration | Document the node state and escalate |
| Resolve alarms manually without root cause | Masking the alarm does not fix the underlying issue | Leave alarms active for GSS to use in diagnosis |

---

## Useful Commands for Case Updates

Paste these into case replies to show Broadcom the current state.

```bash
# NSX Manager CLI (SSH to any Manager node: ssh admin@<mgr>)
nsxcli
get cluster status
get managers
get services
get corfu-cluster status

# Transport node and tunnel status
get transport-node-status
get tunnel status

# Edge node CLI (SSH to each Edge: ssh admin@<edge-ip>)
get version
get services
get bgp neighbor summary
get edge-cluster status
get interfaces

# From NSX Manager API (curl from management workstation)
# Manager cluster
curl -sk -u admin:<pw> https://<mgr>/api/v1/cluster/status | python3 -m json.tool

# Transport nodes in DOWN state
curl -sk -u admin:<pw> "https://<mgr>/api/v1/transport-nodes/status?status=DOWN" | python3 -m json.tool

# All active alarms
curl -sk -u admin:<pw> "https://<mgr>/api/v1/alarms?status=OPEN" | python3 -m json.tool

# Logical router status (for BGP/routing issues)
curl -sk -u admin:<pw> "https://<mgr>/api/v1/logical-routers" | python3 -m json.tool
```

---

## Support Portal and SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| S1 — Critical | Network down; Manager DEGRADED; data at risk; no workaround | 30 minutes (24×7) |
| S2 — Major | Upgrade failed; key feature broken; VMs still connected | 4 hours |
| S3 — Minor | Single segment issue; non-critical feature degraded | 1 business day |
| S4 — General | How-to, pre-check, documentation question | 2 business days |

---

## See also

- [NSX — Diagnostics](diagnostics/)
- [NSX — Common Issues](common-issues/)

---

## Verify resolution

- NSX Manager UI → System → Overview shows all Manager nodes green and cluster status STABLE
- All Transport Nodes show Connected in Fabric → Nodes
- Run Traceflow for the same source/destination that was failing — confirm packet reaches destination
- BGP sessions restored: SSH to Edge → `get bgp neighbor summary` → all peers Established
- Run `curl -sk -u admin:<pw> https://<mgr>/api/v1/alarms?status=OPEN&severity=CRITICAL` and confirm zero active critical alarms
- Monitor NSX Manager Alarms page for 15 minutes and confirm no new alerts
