---
tags:
  - aria-automation
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Automation — Escalation

<div class="kb-summary">
How to escalate VMware Aria Automation issues to Broadcom support: what data to collect, how to run vracli support-bundle, step-by-step case creation on support.broadcom.com, and the escalation path when progress stalls.

*Applies to: Aria Automation 8.x / 9.x*
</div>

```text
┌──────────────────────────────────── Aria Automation — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│  Escalate Aria Automation issues to VMware GSS when the vRA UI is completely                          │
│  unavailable, an upgrade has failed mid-run and services are in mixed state,                          │
│  or cloud account connections are globally broken with no deployment possible.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 1 — Collect Data               │  │          Step 2 — Open the SR               │   │
│   │  Run: vracli support-bundle on the appliance  │  │  Go to support.broadcom.com → sign in       │  │
│   │  Note vRA version + build (vracli version)   │  │  Product: VMware Aria Automation            │   │
│   │  Capture kubectl get pods -n prelude          │  │  Severity: P1 down / P2 degraded / P3 minor │  │
│   │  Check VAMI → Cluster Status and logs        │  │  Attach support bundle + pod state output   │   │
│   │  Write timeline: last good → first failure   │  │  Include vRA version and deployment type    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  For P1: open portal case AND call Broadcom support immediately.                                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 3 — Escalation Path            │  │         What NOT to Do                      │   │
│   │  T1: triage + confirm bundle received        │  │  Do not restart vRA services mid-upgrade    │   │
│   │  T2: vRA SE assigned; deep analysis          │  │  Do not delete failed deployments mid-case  │   │
│   │  T3: engineering review for code-level fix   │  │  Do not manually restart Postgres services  │   │
│   │  CritSit: P1 with upgrade stuck > 2 hours    │  │  Do not run vracli upgrade-apply mid-case   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vRA           = vRealize Automation; rebranded to Aria Automation in 2022                            │
│  vracli        = Aria Automation appliance CLI; generates support bundle and checks cluster state     │
│  prelude       = Kubernetes namespace in the vRA appliance where vRA microservices run                │
│  VAMI          = Virtual Appliance Management Interface; port 5480; cluster health and upgrade UI     │
│  vIDM          = VMware Identity Manager; auth backend for Aria Automation                            │
│  LCM           = Lifecycle Manager; used to deploy and upgrade Aria Automation in suites              │
│  Cloud account = vRA integration with vCenter, AWS, Azure, GCP, or NSX                                │
│  Deployment    = vRA provisioned workload; VM or cloud resource with blueprint/catalog item           │
│  GSS           = Global Support Services; Broadcom/VMware support team                                │
│  CritSit       = Critical Situation; Broadcom war room with engineering; 24×7 engagement              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access required:** SSH root access to the Aria Automation appliance; Broadcom support account at support.broadcom.com with active Aria Automation entitlement
- **Do NOT restart vRA services** during an upgrade failure — mixed-version service state is the most common cause of post-upgrade failures, and an unsupported restart may make it unrecoverable without a fresh deploy
- **Do NOT manually restart Postgres** (the embedded database) without GSS direction — an incorrect restart can corrupt the vRA database schema
- **Collect data BEFORE taking any recovery action** — GSS will need the support bundle from the exact failure state

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command / Location | Expected result |
|---|---|---|
| vRA version | SSH: `vracli version` | Note full version and build |
| VAMI accessibility | Browse to `https://<vra-fqdn>:5480` | VAMI login page loads |
| Cluster health | VAMI → Summary → Cluster Status | All services `Running` |
| Pod health | SSH: `kubectl get pods -n prelude` | No pods in `CrashLoopBackOff` or `Error` |
| vIDM connectivity | `vracli vIDM status` | Connection `OK` |
| Cloud account state | vRA UI → Infrastructure → Connections → Cloud Accounts | All accounts show Connected |
| Service logs | VAMI → Log Files | No recurring FATAL entries |
| vCenter connectivity | `curl -sk https://<vcenter-fqdn>/ui/` from vRA appliance | Returns HTML |
| Disk space | SSH: `df -h` | All partitions above 15% free |

---

## Step-by-Step Data Collection

### 1. Get the Aria Automation version

```bash
# SSH to the Aria Automation appliance as root
ssh root@<vra-fqdn>

# Get full version information
vracli version

# Example output:
# Application Version:  8.16.1.21527
# Build Number: 23480234
```

### 2. Check pod health (all vRA microservices run as pods)

```bash
# Get pod state in the prelude namespace
kubectl get pods -n prelude

# Look for CrashLoopBackOff, Error, or pods with 0/1 containers ready
# Save full output to a file
kubectl get pods -n prelude > /tmp/pods-$(date +%Y%m%d).txt

# For any failing pods, get the recent logs
kubectl logs <pod-name> -n prelude --tail=200 > /tmp/pod-log-$(date +%Y%m%d).txt

# Check all namespaces (for upgrade issues with LCM components)
kubectl get pods -A | grep -v Running | grep -v Completed
```

### 3. Generate the vracli support bundle

```bash
# Generate the support bundle — takes 5–15 minutes
vracli support-bundle

# Bundle is saved to /tmp/
ls -lh /tmp/vracli-support-bundle*.tar.gz

# Copy to a local machine for upload to the case
# scp root@<vra-fqdn>:/tmp/vracli-support-bundle*.tar.gz /tmp/
```

This bundle contains pod logs, Postgres state, configuration, and the last 72h of service logs.

### 4. Collect VAMI cluster status (for upgrade failures)

1. Browse to `https://<vra-fqdn>:5480` and log in (root credentials).
2. Click **Summary** → note the cluster health and all service statuses.
3. Click **Upgrade** → note the current upgrade state if an upgrade is in progress.
4. Take a screenshot of the cluster status and attach to the case.

### 5. Write the timeline

```text
Aria Automation version: 8.16.1 build 23480234
Deployment: 3-node HA cluster (vra01, vra02, vra03)
vIDM: internal vIDM (same appliances)
Issue first observed: 2026-06-14 02:30 UTC
Last known good state: 2026-06-14 02:00 UTC
Changes in 24h before the issue:
  - 02:00: Aria Automation 8.16.0 → 8.16.1 upgrade initiated via VAMI
  - 02:25: VAMI upgrade showed "Upgrade failed" on node vra02
  - 02:30: vRA UI unresponsive; VAMI shows 3 services in Error state
Steps already taken:
  - kubectl get pods -n prelude: 4 pods in CrashLoopBackOff
  - Did NOT restart any services or attempt upgrade retry
  - VAMI shows upgrade status: FAILED at "Migrating database"
Blast radius: Aria Automation UI completely unavailable; no new deployments possible; 200 projects affected
```

---

## How to Open the SR on support.broadcom.com

1. Go to **support.broadcom.com** and sign in with your Broadcom account.

2. Click **Open a Support Request**.

3. Under **Product Group**, select **VMware Cloud Foundation and Virtualization** → **VMware Aria Automation**.

4. Under **Version**, select your Aria Automation version from Step 1.

5. Under **Severity**, select:
   - **Severity 1 — Critical**: Aria Automation UI completely down; no deployments are possible; an upgrade is stuck mid-run with services in mixed state; all cloud accounts disconnected; no workaround
   - **Severity 2 — High**: Specific service degraded; some cloud accounts disconnected; deployments partially failing; vRA UI accessible but specific operations fail
   - **Severity 3 — Medium**: Single catalog item or blueprint failing; specific cloud account in error; workaround exists
   - **Severity 4 — Low**: How-to question, pre-upgrade review, content design question, or non-urgent configuration review

6. In the **Summary** field: product + symptom + scope. Example: `Aria Automation 8.16.1 — upgrade from 8.16.0 failed at DB migration, 4 pods CrashLoopBackOff, UI unavailable, 200 projects affected`.

7. In the **Description** field, paste:
   - Aria Automation version from Step 1
   - The pod health summary from Step 2 (`kubectl get pods -n prelude`)
   - The VAMI upgrade status screenshot description from Step 4
   - The timeline from Step 5

8. Under **Attachments**, upload:
   - The vracli support bundle from Step 3
   - The pod log files from Step 2 for each failing pod

9. Click **Submit**. You will receive a case number by email immediately.

10. **Severity 1 only:** call Broadcom/VMware support after submission:
    - North America: +1 877-486-9273 (24×7 for Severity 1)
    - EMEA: +44 (0)3453 700 100
    - State "Severity 1 — Aria Automation upgrade failed, UI down, 200 projects affected" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at support.broadcom.com with support bundle and pod state attached
         ↓
Step 2 — T1 support engineer acknowledges and reviews the bundle (Sev1: < 30 min)
         ↓
Step 3 — If no meaningful progress in 30 minutes for Sev1 or 2 hours for Sev2:
         → Reply: "Requesting escalation to Aria Automation Senior Engineer"
         → State: "[UI down / upgrade stuck / 200 projects affected]"
         ↓
Step 4 — Aria Automation T2 Senior Engineer assigned
         → They will request SSH access to the appliance for a live session
         → Have SSH and VAMI access ready; confirm the appliance is reachable
         ↓
Step 5 — If issue is a confirmed product bug (upgrade regression, Postgres schema issue):
         → T2 escalates to Aria Automation Engineering (T3)
         → Engineering provides a specific recovery procedure or hotfix
         ↓
Step 6 — For Sev1 unresolved after 2 hours:
         → Request CritSit escalation; contact your Broadcom TAM or Account Executive
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Restart all vRA services or the appliance VM during an upgrade | Mixed-version service state is unrecoverable without an expert; a blind restart may leave the database in a partially migrated state | Wait for GSS to review the VAMI logs and pod state; they will direct the exact restart sequence |
| Retry the upgrade from VAMI without GSS guidance | Retrying an upgrade that failed at DB migration may corrupt the vRA schema | Let GSS examine the failure point first |
| Manually restart the Postgres pod | Can corrupt the vRA database if a schema migration was in progress | Only restart with explicit GSS instruction and the exact command sequence |
| Delete failed deployment records from the vRA UI | Deployment records are used by GSS to trace the request chain through the microservices | Leave all deployment records intact; export them if needed |
| Apply vRA content changes (blueprints, catalog items) during investigation | Changes the content state GSS is analysing | Freeze all content changes until the case is resolved |
| Run LCM operations against the cluster mid-case | LCM may override the current VAMI state; may trigger another partial upgrade | Hold all LCM operations until GSS advises |

---

## Useful Commands for Case Updates

```bash
# Paste these into every case update (SSH to vRA appliance as root)

# Version confirmation
vracli version

# Pod health — the most important state indicator
kubectl get pods -n prelude

# Failing pod logs
kubectl logs <pod-name> -n prelude --tail=100

# Cluster overall health
vracli cluster status

# vIDM connectivity
vracli vIDM status

# Disk space (low disk space is a common upgrade failure cause)
df -h

# Database connectivity check (non-destructive)
vracli db status
```

---

## Support SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| Sev 1 — Critical | vRA UI down; upgrade stuck; no deployments possible | < 30 min (24×7) |
| Sev 2 — High | Service degraded; cloud accounts disconnected; deployments partially failing | < 2 hours (24×7) |
| Sev 3 — Medium | Single service or blueprint failing; workaround exists | < 8 hours |
| Sev 4 — Low | How-to, pre-upgrade, content design, non-urgent config review | Next business day |

---

## See also

- [Aria Automation — Diagnostics](diagnostics/)
- [Aria Automation — Common Issues](common-issues/)

---

## Verify resolution

- Run `kubectl get pods -n prelude` and confirm all pods show `Running` with containers ready (e.g. `1/1`)
- Browse to the Aria Automation UI and confirm the login page loads
- Log in as an administrator and confirm the Dashboard loads without errors
- Check **Infrastructure → Connections → Cloud Accounts** and confirm all cloud accounts show Connected
- Trigger a test deployment from a known working blueprint and confirm it provisions successfully
- Check VAMI → Summary and confirm all services show green
- Monitor for 30 minutes before closing the case
