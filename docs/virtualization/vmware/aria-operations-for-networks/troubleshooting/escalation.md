---
tags:
  - aria-networks
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Operations for Networks — Escalation

<div class="kb-summary">
How to escalate VMware Aria Operations for Networks (vRNI) issues to Broadcom support: what data to collect, how to generate the support bundle, step-by-step case creation on support.broadcom.com, and the escalation path when progress stalls.

*Applies to: Aria Operations for Networks (vRealize Network Insight) 6.x*
</div>
![Aria Operations for Networks — Escalation](../../../../assets/virtualization-vmware-aria-operations-for-networks-troublesh.svg)




---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
preescalation_selfcheck: "Pre-Escalation Self-Check" {shape: rectangle}
stepbystep_data_collection: "Step-by-Step Data Collection" {shape: rectangle}
how_to_open_the_sr_on_supportbroadco: "How to Open the SR on support.broadcom.com" {shape: rectangle}
escalation_path: "Escalation Path" {shape: rectangle}
what_not_to_do: "What NOT to Do" {shape: rectangle}
useful_commands_for_case_updates: "Useful Commands for Case Updates" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> preescalation_selfcheck: investigate
symptom -> stepbystep_data_collection: investigate
symptom -> how_to_open_the_sr_on_supportbroadco: investigate
symptom -> escalation_path: investigate
symptom -> what_not_to_do: investigate
symptom -> useful_commands_for_case_updates: investigate
preescalation_selfcheck -> resolution
stepbystep_data_collection -> resolution
how_to_open_the_sr_on_supportbroadco -> resolution
escalation_path -> resolution
what_not_to_do -> resolution
useful_commands_for_case_updates -> resolution
```

## Before you begin

- **Access required:** SSH ubuntu@ access to the Platform VM; vRNI UI admin access; Broadcom support account at support.broadcom.com with active Aria Ops for Networks entitlement
- **Note:** The Platform VM SSH user is `ubuntu`, not `root` — run `sudo` for privileged commands
- **Do NOT power off the Platform VM** during an active incident without GSS direction — the in-memory flow database may not survive an unclean shutdown
- **Do NOT run a PAK upgrade** if the platform is already degraded — the upgrade process may fail and leave the platform in an unrecoverable state
- **Do NOT remove or reconfigure Proxy VMs** during the investigation — the flow collection topology is what GSS uses to trace where data is being lost

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command / Location | Expected result |
|---|---|---|
| vRNI version | vRNI UI → Settings → Overview → Version | Note full version (e.g. 6.12.0) |
| Platform VM status | vSphere Client: check power state of vRNI Platform VM | Powered on, VMware Tools running |
| Proxy VM status | vSphere Client: check power state of all vRNI Proxy VMs | All powered on |
| UI accessibility | Browse to `https://<vrni-fqdn>/` | Login page loads |
| VAMI accessibility | Browse to `https://<vrni-fqdn>:5480` | VAMI login page loads |
| Data source status | vRNI UI → Settings → Data Sources | All sources show Connected |
| Flow data in UI | vRNI UI → Dashboard → Traffic Overview | Recent flows visible (within 15 min) |
| Platform disk space | SSH: `df -h` | All partitions below 85% used |

---

## Step-by-Step Data Collection

### 1. Get the vRNI version and platform VM health

In the vRNI UI: click **Settings** (top right) → **Overview** → note the platform version and build number.

```bash
# SSH to the Platform VM as ubuntu
ssh ubuntu@<vrni-fqdn>

# Check platform service status
sudo systemctl status vrni

# Disk space (flow database fills the /var/log or /data partition)
df -h

# Memory and CPU
free -h
top -bn1 | head -20
```

### 2. Generate the support bundle

**Method 1 — Via SSH (recommended for any severity):**

```bash
# SSH to the Platform VM as ubuntu
ssh ubuntu@<vrni-fqdn>

# Generate the support bundle
sudo /etc/init.d/support-bundle.sh

# Bundle is written to /data/support-bundles/
ls -lh /data/support-bundles/

# Copy to a local machine for upload
scp ubuntu@<vrni-fqdn>:/data/support-bundles/<bundle-filename>.tar.gz /tmp/
```

**Method 2 — Via VAMI UI:**

1. Browse to `https://<vrni-fqdn>:5480` and log in.
2. Click **Support** → **Generate Support Bundle**.
3. Download the resulting archive.

### 3. Collect data source status and error details

In the vRNI UI:
1. Click **Settings** → **Data Sources**.
2. Note the status of each data source (Connected / Disconnected / Error).
3. For any source showing an error: click the source name and note the exact error message.
4. Export the data source list: Settings → Data Sources → Export (or screenshot the list).

```bash
# From the Platform VM — check network connectivity to data sources
# Replace <vcenter-ip> with an actual data source IP
ping -c 4 <vcenter-ip>
nc -zv <vcenter-ip> 443
```

### 4. Write the timeline

```text
vRNI version: 6.12.0 build XXXXXXXX
Platform VM: vrni-platform-01.corp.local
Proxy VMs: vrni-proxy-01 (vSphere), vrni-proxy-02 (NSX)
Data sources: 3 vCenter + 2 NSX + 4 physical switches
Issue first observed: 2026-06-14 09:00 UTC
Last confirmed flow data: 2026-06-14 08:30 UTC
Changes in 24h before the issue:
  - 08:00: vRNI PAK upgrade from 6.11 to 6.12.0 applied
  - 08:45: Upgrade completed; platform VM restarted
  - 09:00: UI accessible but all data sources show "Disconnected"
  - 09:10: Flow overview dashboard shows no data since 08:30 UTC
Steps already taken:
  - VAMI accessible; platform services appear running
  - Data source "Test Connection" fails for all 9 sources
  - Proxy VM ping to vCenter succeeds (network not the issue)
  - Did NOT delete data sources or run another PAK upgrade
Blast radius: All network flow analytics unavailable; 9 data sources disconnected
```

---

## How to Open the SR on support.broadcom.com

1. Go to **support.broadcom.com** and sign in with your Broadcom account.

2. Click **Open a Support Request**.

3. Under **Product Group**, select **VMware Cloud Foundation and Virtualization** → **VMware Aria Operations for Networks** (or search "vRealize Network Insight").

4. Under **Version**, select your vRNI version from Step 1.

5. Under **Severity**, select:
   - **Severity 1 — Critical**: Platform VM completely unreachable; all flow data missing for more than 2 hours; data integrity issue suspected; production network visibility is blind; no workaround
   - **Severity 2 — High**: All data sources disconnected but Platform VM is accessible; upgrade failed and platform is in an inconsistent state; Proxy VMs not collecting
   - **Severity 3 — Medium**: Single data source in error; specific flow type missing; UI accessible with some data visible; workaround exists
   - **Severity 4 — Low**: How-to question, pre-upgrade planning, data source configuration help

6. In the **Summary** field: product + symptom + scope. Example: `vRNI 6.12 — all 9 data sources disconnected after PAK upgrade 6.11→6.12, flow data collection stopped since 08:30 UTC`.

7. In the **Description** field, paste:
   - vRNI version from Step 1
   - Platform VM disk space and service status from Step 1
   - Data source error messages from Step 3
   - The timeline from Step 4

8. Under **Attachments**, upload the support bundle from Step 2.

9. Click **Submit**. You will receive a case number by email immediately.

10. **Severity 1 only:** call Broadcom/VMware support after submission:
    - North America: +1 877-486-9273 (24×7 for Severity 1)
    - EMEA: +44 (0)3453 700 100
    - State "Severity 1 — Aria Ops for Networks Platform VM down, all flow visibility lost" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at support.broadcom.com with support bundle and data source status attached
         ↓
Step 2 — T1 support engineer acknowledges (Sev1: < 30 min; Sev2: < 2 hr)
         ↓
Step 3 — If no meaningful progress in 30 minutes for Sev1 or 2 hours for Sev2:
         → Reply: "Requesting escalation to Aria Networks Senior Engineer"
         → State: "[platform down / all sources disconnected / flow data missing since X]"
         ↓
Step 4 — vRNI T2 Senior Engineer is assigned
         → They will request SSH access to the Platform VM for a live session
         → Have ubuntu@ SSH access and VAMI credentials ready
         ↓
Step 5 — If issue is a confirmed product bug (upgrade regression, flow DB corruption):
         → T2 escalates to Aria Networks Engineering
         → Engineering provides a targeted recovery procedure or hotfix
         ↓
Step 6 — For Sev1 with no resolution after 2 hours:
         → Request CritSit escalation; contact your Broadcom TAM
         → TAM convenes bridge call with GSS and Engineering
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Delete data sources during investigation | Data source config contains the connection history and last-good-state needed for GSS to trace the failure | Leave all data sources in place; only delete if GSS specifically instructs |
| Run a PAK upgrade on a degraded platform | Upgrade on an already-broken platform may fail mid-way and leave the system unrecoverable | Wait for GSS to stabilise the current state before any upgrade |
| Power off the Platform VM mid-incident | The in-memory flow database may not survive an unclean shutdown; adds data loss on top of the existing issue | Request a controlled shutdown from GSS; they will advise on safe power-cycle procedure |
| Remove a Proxy VM during diagnosis | Changes the collection topology GSS is using to trace where data is being lost | Leave all Proxy VMs running; GSS will direct any proxy-level action |
| Reconfigure or reset data source credentials | Changes the auth state GSS is examining; may trigger additional API errors on the data source side | Hold all credential changes until GSS confirms the issue is not auth-related |
| Re-run the PAK upgrade immediately after failure | A failed upgrade may have left configuration in a partial state; re-running may make it unrecoverable | Let GSS examine the failed upgrade log before any retry |

---

## Useful Commands for Case Updates

```bash
# SSH to Platform VM as ubuntu — paste these into every case update

# Platform service status
sudo systemctl status vrni

# Disk space (flow DB fills /data or /var/log)
df -h

# Memory and swap
free -h

# Check platform processes
ps aux | grep -E 'java|cassandra|nginx'

# Network connectivity to data sources
ping -c 4 <vcenter-ip>
nc -zv <vcenter-ip> 443

# Recent platform log entries
sudo tail -100 /var/log/vrni/platform.log | grep -i "error\|fail\|exception"
```

---

## Support SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| Sev 1 — Critical | Platform VM unreachable; all flow visibility lost; data integrity issue | < 30 min (24×7) |
| Sev 2 — High | All sources disconnected; platform accessible but flow collection stopped | < 2 hours (24×7) |
| Sev 3 — Medium | Single source failing; specific flow type missing; workaround exists | < 8 hours |
| Sev 4 — Low | How-to, pre-upgrade, data source config, non-urgent question | Next business day |

---

## See also

- [Aria Operations for Networks — Diagnostics](diagnostics/)
- [Aria Operations for Networks — Common Issues](common-issues/)

---

## Verify resolution

- Browse to the vRNI UI and confirm the login page loads
- Navigate to **Settings → Data Sources** and confirm all sources show **Connected**
- Check the **Traffic Overview** dashboard: recent flow data should appear within the last collection interval (typically 5–10 minutes)
- Run `df -h` on the Platform VM and confirm the flow data partition is not at or near 100%
- Confirm a Proxy VM can reach a data source: `nc -zv <vcenter-ip> 443` from the Platform VM
- Monitor for one full collection cycle (10–15 minutes) to confirm all data sources complete collection without errors
