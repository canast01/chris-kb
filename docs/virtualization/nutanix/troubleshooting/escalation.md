---
tags:
  - nutanix
  - troubleshooting
  - escalation
  - support
  - gss
search:
  boost: 1.5
---
# Nutanix — Escalation

<div class="kb-summary">
How to escalate Nutanix cluster issues to Nutanix Global Support Services (GSS): what data to collect, how to generate the NCC health report and support bundle, step-by-step case creation on portal.nutanix.com, and the escalation path when progress stalls.

*Applies to: AOS 6.x · AHV*
</div>
![Nutanix — Escalation](../../../assets/virtualization-nutanix-troubleshooting-escalation.svg)




---

## Before you begin

- **Access required:** Nutanix Portal account linked to your support contract (portal.nutanix.com); SSH access to any CVM in the cluster (default user: `nutanix`); Prism Element admin access
- **Do NOT restart multiple CVMs simultaneously** — each CVM is the storage controller for its node; taking multiple CVMs offline at once can reduce the cluster below RF threshold and cause data loss
- **NCC and support bundle first** — GSS will request these immediately; having them ready before calling significantly reduces time to resolution
- **Enable Pulse before calling** — Pulse (call-home) allows GSS engineers to remotely access the cluster via a secure tunnel, which accelerates diagnosis for complex issues

---

## When to Escalate Immediately

Escalate to Nutanix GSS without delay for any of these:

- **`CAN_TOLERATE_FAILURE_COUNT=0`** — the cluster cannot tolerate any further failure; one more disk or node failure = data loss
- **Production VMs are down** and cannot be restored by standard procedures
- **Data loss suspected** — Stargate returning I/O errors to VMs; VMs crashing on disk write
- **CVM unresponsive** — SSH to CVM fails; IPMI console shows hardware faults
- **Multiple disks failed on the same node** — beyond RF tolerance
- **Cluster will not accept writes** — storage full with no quick way to free space
- **Cluster upgrade failure** — AOS/AHV upgrade stuck or failed mid-way

For all other issues: attempt NCC triage and log review first (see [Diagnostics](diagnostics/)), then open a lower-severity case.

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| AOS version | `ncli cluster info \| grep -i version` | Note full version (e.g. 6.7.2) |
| Cluster UUID | `ncli cluster info \| grep -i uuid` | Note UUID for the case |
| RF and tolerance | `ncli cluster info \| grep -i "tolerate\|replication"` | CAN_TOLERATE_FAILURE_COUNT > 0 |
| Node health | `ncli host list` | All nodes show UP |
| Disk health | `ncli disk list \| grep -v NORMAL` | Empty output (all disks NORMAL) |
| CVM reachability | `ping <cvm-ip>` from another CVM | CVM responds |
| Genesis status | `genesis status` (on CVM) | All services Running |
| NCC quick check | `ncc --health_checks run_all 2>&1 \| tail -30` | PASS (or note which checks FAIL) |

---

## Step-by-Step Data Collection

### 1. Get the cluster info and version

```bash
# SSH to any CVM as nutanix
ssh nutanix@<cvm-ip>

# Cluster name, AOS version, RF, UUID
ncli cluster info

# Node serial numbers and IPs (required for case registration)
ncli host list

# Any disk not in NORMAL state
ncli disk list | grep -v NORMAL
```

### 2. Run NCC health checks

```bash
# Full NCC run — attach the full output to the case
ncc --health_checks run_all 2>&1 | tee /tmp/ncc-$(date +%Y%m%d%H%M).txt

# Quick check of critical checks only
ncc --health_checks run_all --ncc_critical_only=true 2>&1 | tail -100
```

GSS will ask for the full NCC output as the first diagnostic step. A fresh NCC run captures the current cluster health state.

### 3. Collect the support bundle

**Via Prism Element UI:**

1. Prism Element → click the **Settings** gear → **Log Collector**.
2. Set the time range to cover the failure period (minimum last 4 hours).
3. Click **Collect Logs**.
4. Wait for the bundle to be generated (5–20 minutes).
5. Download and attach to the case.

**Via CLI:**

```bash
# SSH to any CVM as nutanix
# Generate support bundle (saves to /home/nutanix/support-bundle/)
logbay collect --case_id="<case-number>"

# Without case ID:
logbay collect --output_dir="/tmp/logbay-$(date +%Y%m%d)"

# List generated bundles
ls -lh ~/support-bundle/
```

### 4. Collect targeted logs for specific issues

| Issue Type | Additional Collection |
|---|---|
| CVM not responding | `ncli host list`; IPMI/iDRAC console; `genesis status` on affected CVM |
| Stargate I/O errors | `allssh grep -i "stargate\|iof\|I/O error" /home/nutanix/data/logs/stargate.INFO` |
| Genesis failure | `cat /home/nutanix/data/logs/genesis.out` on affected CVM |
| Disk failure | `ncli disk list`; `smartctl -a /dev/<disk>` on the AHV host |
| Upgrade failure | Upgrade log: `/home/nutanix/data/logs/upgrade.out` |
| Network issue | `ping <all cvm IPs>` from each CVM; `ncli network switch-interfaces list` |

### 5. Write the timeline

```text
AOS version: 6.7.2
Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Cluster: prod-nutanix-01 (4 nodes, RF2)
CAN_TOLERATE_FAILURE_COUNT: 0 (1 disk failed on node 3)
Issue first observed: 2026-06-14 10:00 UTC
Last NCC clean run: 2026-06-13 22:00 UTC
Changes in 24h before the issue:
  - 09:30: Node 3 NCC alert: "Disk [SSD-01] marked as to_remove"
  - 10:00: Stargate I/O errors observed on VMs hosted on node 3
  - 10:05: VM "db-prod-01" on node 3 shows kernel panic (disk I/O failure)
Steps already taken:
  - ncli disk list: 1 disk on node 3 shows state "DEAD"
  - ncc run: "disk_health_check" FAIL on node 3
  - Did NOT remove the disk or restart the CVM
  - Did NOT initiate disk repair
Blast radius: 1 production VM down (db-prod-01); cluster at RF minimum; 1 more failure = data loss
```

---

## How to Open the Case on portal.nutanix.com

1. Go to **portal.nutanix.com** and log in with your Nutanix Portal account (linked to your support contract).

2. Click **Support** → **Cases** → **Open New Case**.

3. Under **Cluster**, select the affected cluster from the registered clusters list. This auto-populates the cluster serial numbers and AOS version.

4. Under **Severity**, select:
   - **S1 — Critical**: Cluster down or cannot tolerate failure (CAN_TOLERATE_FAILURE_COUNT=0); production VMs down; data loss suspected; no workaround
   - **S2 — Major**: Significant degradation; partial outage; cluster is running but at elevated risk; workaround exists but incomplete
   - **S3 — Moderate**: Non-critical cluster impact; single non-critical VM affected; workaround available
   - **S4 — Low**: General questions, how-to, feature requests, pre-upgrade planning

5. In the **Summary** field: symptom + scope. Example: `Nutanix prod-01 — disk DEAD on node 3, CAN_TOLERATE_FAILURE=0, Stargate I/O errors on db-prod-01`.

6. In the **Description** field, paste:
   - AOS version and cluster UUID from Step 1
   - Failed disk state from Step 1
   - NCC check results summary from Step 2
   - The timeline from Step 5

7. Under **Attachments**, upload:
   - The NCC output from Step 2
   - The support bundle from Step 3

8. Click **Submit**. You receive a case number immediately.

9. **S1/S2 only:** also call the Nutanix phone support number:
   - The current phone numbers are listed at **portal.nutanix.com → Support → Phone Support** after login (numbers change; do not rely on hardcoded numbers)
   - State "Severity 1 — cluster cannot tolerate failure, production VM down, case number XXXXXXXX" at the start of the call

---

## Escalation Path

![Nutanix — Escalation — Diagram](../../../assets/virtualization-nutanix-troubleshooting-escalation-diagram.svg)

---

## Enabling Remote Access for GSS (Pulse)

Nutanix support engineers access clusters via Pulse (call-home tunnelling).

```text
Prism Element → Settings gear → Pulse
  Enable Pulse: On
  Test Connection: confirm Pulse shows "Connected"
```

If Pulse is disabled (air-gapped environments):
- GSS will use WebEx/Teams screen share
- Or you provide Jump Host access under GSS supervision
- Let GSS know Pulse is disabled in the case description

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Restart multiple CVMs simultaneously | Each CVM is the storage controller for its node; restarting multiple at once reduces cluster RF below safe threshold and risks data loss | Only restart one CVM at a time, and only when GSS explicitly instructs |
| Remove a failed disk without GSS direction | A disk marked DEAD or FAILED may still hold component data that is part of an in-progress rebuild; removing it can cause permanent data loss | Let GSS confirm the rebuild state (ncli disk list + logbay) before any disk removal |
| Shut down a degraded cluster node | Takes node capacity and storage components offline; in a degraded cluster this may push below RF | Leave all nodes powered on; contact GSS before any node power operation |
| Run disk repair or scrub without GSS | Triggers background I/O that competes with recovery; changes the storage state GSS is analysing | Let GSS direct the exact repair procedure after reviewing the NCC and logbay data |
| Apply AOS or AHV upgrade during an active incident | Upgrades change the codebase and cluster state mid-incident; upgrade may fail on the degraded cluster | Freeze all upgrades until the incident is fully resolved and GSS clears it |
| Generate a fresh support bundle without noting the filename | Old bundles overwrite the incident state | Note the filename and timestamp before generating a new bundle; keep the incident-time bundle |

---

## Useful Commands for Case Updates

```bash
# SSH to any CVM as nutanix — paste these into every case update

# Cluster state
ncli cluster info

# Node health (looking for any DOWN nodes)
ncli host list

# Disk health (looking for non-NORMAL disks)
ncli disk list | grep -v NORMAL

# CVM service status on this node
genesis status

# Stargate I/O error check (last 100 lines)
tail -100 /home/nutanix/data/logs/stargate.INFO | grep -i "error\|FATAL\|I/O"

# Quick NCC summary
ncc --health_checks run_all --ncc_critical_only=true 2>&1 | tail -30

# Cluster storage usage
ncli cluster info | grep -i "storage\|usage\|capacity"
```

---

## Support SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| S1 — Critical | Cluster down; cannot tolerate failure; data loss; production VMs down | < 30 min (24×7) |
| S2 — Major | Significant degradation; partial outage; cluster running at risk | < 4 hours (24×7) |
| S3 — Moderate | Non-critical impact; single non-critical VM; workaround available | Next business day |
| S4 — Low | General questions, how-to, feature requests, planning | Next business day |

---

## Post-Incident

After issue resolution:

- Request a Root Cause Analysis (RCA) from GSS if the issue caused production impact (S1 cases: GSS provides RCA within 5 business days)
- Run NCC 24 hours after resolution to confirm clean state: `ncc --health_checks run_all 2>&1 | tail -30`
- Update your internal incident record with the KB article reference and resolution steps
- Verify cluster tolerance is restored: `ncli cluster info | grep -i tolerate` should show CAN_TOLERATE_FAILURE_COUNT > 0

---

## See also

- [Nutanix — Diagnostics](diagnostics/)
- [Nutanix — Common Issues](common-issues/)

---

## Verify resolution

- Run `ncli cluster info | grep -i tolerate` and confirm CAN_TOLERATE_FAILURE_COUNT > 0
- Run `ncli host list` and confirm all nodes are UP
- Run `ncli disk list | grep -v NORMAL` and confirm empty output (all disks NORMAL)
- Run `ncc --health_checks run_all 2>&1 | tail -50` and confirm no FAIL results
- Check that the previously affected VMs are running and serving I/O without errors
- Confirm Stargate I/O error log is no longer growing: `tail -f /home/nutanix/data/logs/stargate.INFO | grep -i "error\|FATAL"`
- Run NCC again at 24 hours post-resolution to confirm sustained clean state
