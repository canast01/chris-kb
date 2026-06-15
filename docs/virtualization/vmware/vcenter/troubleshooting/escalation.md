---
tags:
  - troubleshooting
  - vcenter
  - vmware
  - vsphere-8
search:
  boost: 1.5
---
# vCenter — Escalation

<div class="kb-summary">
How to escalate vCenter Server issues to Broadcom support: what data to collect, how to generate the VCSA support bundle, step-by-step SR submission on the Broadcom portal, and the escalation path when progress stalls.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌───────────────────────────────────── vCenter Server — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│  Escalate vCenter issues to Broadcom GSS when the VCSA is inaccessible or repeatedly                  │
│  crashing, vMotion/DRS is broken cluster-wide, or data loss is suspected.                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 1 — Collect Data               │  │          Step 2 — Open the SR               │   │
│   │  VCSA shell: run vc-support script           │  │  Go to support.broadcom.com → sign in       │   │
│   │  Collect vcenter.log + vpxd.log              │  │  Product: VMware vCenter Server             │   │
│   │  Note exact vCenter version + build          │  │  Type: Technical → pick sub-category        │   │
│   │  Screenshot of error from vSphere Client     │  │  Severity: S1 down / S2 major / S3 minor    │   │
│   │  Write timeline: last good → first failure   │  │  Attach VCSA bundle + vpxd.log              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  For S1: open portal case AND call the phone number on the case confirmation page.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 3 — Escalation Path            │  │         What NOT to Do                      │   │
│   │  T1: triage + confirm bundle received        │  │  Do not reboot VCSA mid-incident            │   │
│   │  T2: vCenter SE assigned; provides guidance  │  │  Do not modify VCSA DB without GSS          │   │
│   │  T3: engineering review if SE cannot fix     │  │  Do not snapshot VCSA mid-upgrade           │   │
│   │  CritSit: request if data at risk or 24h+    │  │  Do not apply patches mid-incident          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCSA          = vCenter Server Appliance; Photon OS Linux appliance running vCenter                  │
│  vpxd.log      = primary vCenter daemon log; first file Broadcom requests                             │
│  vc-support    = VCSA support bundle script; generates /var/core/vc-support-*.tgz                     │
│  SR            = Service Request; support case number assigned by Broadcom                            │
│  GSS           = Global Support Services; Broadcom's technical support team                           │
│  S1 severity   = highest; vCenter inaccessible; no workaround; 30-min SLA                             │
│  CritSit       = Critical Situation; executive escalation + dedicated war room                        │
│  vCSHA         = vCenter Server High Availability; two-node active/passive setup                      │
│  SSO           = Single Sign-On; vCenter identity provider; login failures start here                 │
│  vPostgres     = embedded PostgreSQL database used by VCSA                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access required:** SSH to VCSA (root credentials); vSphere Client access; Broadcom support account with entitlement to vSphere
- **Do this first:** collect all data below before touching the VCSA. Broadcom will ask for the bundle and logs in their first response
- **Do NOT reboot** the VCSA mid-incident unless explicitly instructed. A reboot may rotate logs and lose the state captured at the time of failure
- **Do NOT snapshot** the VCSA appliance during an active upgrade — this is unsupported and blocks the upgrade from completing

---

## Pre-Escalation Self-Check

Run these before opening the SR. Many vCenter issues are resolvable without Broadcom.

| Check | Command / location | Expected result |
|---|---|---|
| vCenter UI accessible | Browse to `https://<vcenter-fqdn>/ui/` | Login page loads |
| VCSA services status | SSH → `service-control --status` | All services show `Running` |
| vpxd service | SSH → `service-control --status vmware-vpxd` | `Running` |
| SSO service | SSH → `service-control --status vmware-sso` | `Running` |
| Embedded DB space | SSH → `df -h /storage/db` | Under 70% used |
| Disk space overall | SSH → `df -h` | No partition at 100% |
| vCSHA status (if configured) | vSphere Client → vCenter HA | Active node healthy |
| Recent vpxd errors | SSH → `grep ERROR /var/log/vmware/vpxd/vpxd.log | tail -20` | Review for known error strings |
| NTP sync | SSH → `timedatectl status` | `System clock synchronized: yes` |

---

## Step-by-Step Data Collection

Run all of these before opening the SR. SSH to the VCSA as root.

### 1. Get the vCenter version and build number

```bash
# SSH to vCenter Shell
ssh root@<vcenter-fqdn>

# Full vCenter version — include this in the SR description
cat /etc/applmgmt/appliance/update_status.json | python3 -m json.tool | grep -i version

# Or from VAMI (vCenter Appliance Management UI at port 5480):
# Login → Summary → Software Version — note the full build number (7 digits)

# Via vSphere Client: Administration → Deployment → System Configuration → Nodes → select vCenter → Summary
```

### 2. Collect the VCSA support bundle (takes 5–20 minutes)

```bash
# Generate support bundle — run from VCSA shell
vc-support

# The bundle is saved to /var/core/
ls -lh /var/core/
# Example: vc-support-vcenter01-2026-06-14--15.45.tgz

# If /var/core/ is full:
vc-support -w /tmp/
```

Upload this .tgz file to the Broadcom case. It contains all VCSA service logs, database state, and configuration.

### 3. Collect the vpxd log (the primary vCenter daemon log)

```bash
# The most recent vpxd.log is the first file Broadcom requests
ls -lh /var/log/vmware/vpxd/
cp /var/log/vmware/vpxd/vpxd.log /tmp/vpxd-$(date +%Y%m%d).log

# Also collect the SSO log if login is failing
cp /var/log/vmware/sso/vmware-sts-idmd.log /tmp/vmware-sts-idmd-$(date +%Y%m%d).log

# For upgrade failures, collect the installer log
ls -lh /var/log/vmware/install/
```

### 4. Check VCSA disk space (a common cause of VCSA service failures)

```bash
# Full disk space check — flag any partition at or near 100%
df -h

# If /storage/log is full, clear old log archives
ls -lh /var/log/vmware/*/

# For persistent disk-full issues, check database logs
du -sh /storage/db/
```

### 5. Check service status and recent errors

```bash
# List all VCSA services and their state
service-control --status

# Show recent errors in the primary service log
grep -i "ERROR\|FATAL\|Exception" /var/log/vmware/vpxd/vpxd.log | tail -50

# If SSO/login is failing
grep -i "ERROR\|FATAL" /var/log/vmware/sso/vmware-sts-idmd.log | tail -30

# Database health check
/usr/lib/vmware-vpostgres/bin/psql -U vc -d VCDB -c "SELECT count(*) FROM vpx_task WHERE state = 'running';"
```

### 6. Write the timeline

```text
vCenter version: 8.0 U2c build 23477823
VCSA hostname: vcenter-01.corp.local
Issue first observed: 2026-06-14 14:30 UTC
Last known good state: 2026-06-14 10:00 UTC
Changes in the 24h before the issue:
  - 09:30: vCenter 8.0 U2b → U2c upgrade initiated via VAMI
  - 14:25: VAMI showed upgrade progress stalled at 70%
  - 14:30: vpxd service stopped responding; vSphere Client shows "Connection refused"
Steps already taken:
  - Checked /var/log/vmware/vpxd/vpxd.log: shows "vc-health: VCDB disk full"
  - /storage/db is at 98% — cleared old task history
  - Services still not running
Blast radius: all ESXi hosts show "Disconnected" in vSphere Client; VMs continue running
```

---

## How to Open the SR on Broadcom Support Portal

1. Go to **support.broadcom.com** and sign in with your Broadcom account. If you do not have one: click **Register** and use your company email — entitlement is linked to your support contract.

2. Click **Open a New Case** in the top navigation.

3. Under **Select Product Family**, choose **VMware vSphere**.

4. Under **Product**, select **VMware vCenter Server** and pick your exact version from the drop-down.

5. Under **Request Type**, select **Technical**.

6. Under **Severity**, select:
   - **S1 — Critical**: vCenter is completely inaccessible; all hosts show Disconnected; you cannot manage any VMs; no workaround
   - **S2 — Major**: vCenter is partially accessible or repeatedly crashing; specific workflows (migration, provisioning) are broken but VMs are running
   - **S3 — Minor**: Non-critical vCenter feature is broken (alarms, performance charts); management is possible; cluster is healthy
   - **S4 — General**: How-to, pre-check, or non-urgent configuration question

7. In the **Summary** field, write one sentence: product + symptom + scope. Example: `vCenter 8.0 U2c upgrade stalled at 70% since 14:25 UTC — vpxd stopped, all ESXi hosts showing Disconnected`.

8. In the **Description** field, paste:
   - The vCenter version and full build number from Step 1
   - The disk space output from Step 4
   - The last 20 ERROR lines from vpxd.log from Step 5
   - The timeline from Step 6
   - The current service-control --status output

9. Under **Attachments**, upload:
   - The VCSA support bundle tgz from Step 2
   - The vpxd.log copy from Step 3
   - The SSO log if login is failing

10. Click **Submit**. You will receive a case number by email immediately.

11. **S1 only:** the case confirmation page shows a regional phone number. Call it immediately:
    - State "Severity 1 — vCenter is completely down" at the start of the call.
    - Have SSH access to VCSA and the case number ready.

---

## Escalation Path

```text
Step 1 — Open case at support.broadcom.com with VCSA support bundle attached
         ↓
Step 2 — T1 support acknowledges and confirms bundle received (typically 30 min–4 hr)
         ↓
Step 3 — If no meaningful progress in 4 hours for S1 or 1 business day for S2:
         → Reply in the case: "Requesting T2 vCenter Senior Engineer assignment"
         → State: "Impact: [vCenter down / upgrade stalled / all hosts disconnected]"
         ↓
Step 4 — T2 vCenter SE is assigned; they will schedule a live Zoom/Webex session
         → Have SSH access to VCSA and VAMI (port 5480) ready for the call
         ↓
Step 5 — If T2 cannot resolve and issue requires appliance-level investigation:
         → T2 escalates to T3 (vCenter engineering) — you do not need to initiate this
         ↓
Step 6 — For vCenter data loss, SSO database corruption, or 24h+ with no resolution:
         → Request a Critical Situation (CritSit) engagement
         → Add to case: "Requesting CritSit — [reason: data loss / VCDB corrupted / 24h no progress]"
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Reboot VCSA mid-incident | Rotates logs; loses the service state at time of failure | Capture full logs first; only reboot if GSS says it is safe |
| Snapshot VCSA during an active upgrade | Explicitly unsupported; blocks upgrade completion | Snapshot before starting the upgrade, not during |
| Modify vPostgres database directly (SQL) | Can corrupt the vCenter database | Let GSS guide any DB-level intervention |
| Apply patches mid-incident | Adds variables to an already-broken environment | Freeze all changes until resolution |
| Delete and re-register hosts | Loses distributed switch state and VM-to-host mappings | Document the disconnected state and wait for GSS guidance |
| Open multiple SRs for the same issue | Splits diagnostic context across cases | Add information to the existing case; use one case per incident |

---

## Useful Commands for Case Updates

Paste these into case replies to show Broadcom the current state.

```bash
# VCSA service status — paste into every case update
service-control --status

# Most recent vpxd errors (last 50 lines of ERROR-level entries)
grep -i "ERROR\|FATAL" /var/log/vmware/vpxd/vpxd.log | tail -50

# Disk space (flag anything over 80%)
df -h

# NTP status
timedatectl status

# vCSHA status (if configured)
vcha-util status 2>/dev/null || echo "vCSHA not configured"

# Recent system logs
journalctl -n 100 --no-pager 2>/dev/null | tail -50
```

---

## Support Portal and SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| S1 — Critical | vCenter inaccessible; all hosts disconnected; data at risk | 30 minutes (24×7) |
| S2 — Major | Key workflow broken; upgrade stalled; partial access only | 4 hours |
| S3 — Minor | Non-critical feature broken; management still possible | 1 business day |
| S4 — General | How-to, pre-check, documentation question | 2 business days |

Your support tier (Production, Premier, Mission Critical) may reduce these SLAs. Check your contract under **My Entitlements** at support.broadcom.com.

---

## See also

- [vCenter — Diagnostics](diagnostics/)
- [vCenter — Common Issues](common-issues/)

---

## Verify resolution

- vSphere Client loads the login page and you can authenticate successfully
- All ESXi hosts show "Connected" in the vSphere Client
- Run `service-control --status` and confirm all services show `Running`
- Run `df -h` and confirm no partition is above 80%
- Perform the action that was failing (vMotion a test VM, add a host, provision a VM) and confirm it succeeds
- Monitor the vSphere Client Alarms view for 15 minutes and confirm no new vCenter-related alarms
