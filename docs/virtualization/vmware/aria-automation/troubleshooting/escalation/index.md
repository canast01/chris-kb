# Aria Automation — Escalation

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Automation Escalation Path                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Internal (< 2 hours for P1/P2)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Collect: vracli version · vracli status             │  │
│  │  kubectl pod status · disk space · VIDM health       │  │
│  │  Deployment event logs · Kubernetes events           │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │  unresolved after 2h           │
│                           ▼                                │
│  Broadcom Support Portal  (support.broadcom.com)           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Attach: vracli support-bundle + pod status          │  │
│  │  P1: 30 min response · call support line immediately │  │
│  │  P2: 2h business hours · portal sufficient           │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │  SLA breached                  │
│                           ▼                                │
│  Portal Escalate button  ·  Broadcom TAM (if available)    │
└─────────────────────────────────────────────────────────────┘
```

## Support Portal

**Broadcom Support Portal:** [https://support.broadcom.com](https://support.broadcom.com)

Log in with your Broadcom Support account (formerly VMware Customer Connect). Aria Automation support cases are raised under the **VMware Cloud Foundation > Aria Automation** product.

---

## When to Escalate

Escalate to Broadcom support when internal troubleshooting has not resolved the issue within 2 hours for P1/P2, or when:

- Kubernetes pods are crash-looping and restarting the deployment does not resolve the issue
- PostgreSQL database is corrupted or not starting after a failed upgrade
- The cluster is split-brain: nodes disagree about cluster membership after a network event
- A deployment is stuck in `CREATE_INPROGRESS` for more than 2 hours with no log activity
- VIDM/SSO is inaccessible and all users (including admin) cannot log in
- The upgrade has partially applied and the cluster is in an inconsistent version state
- A rollback to snapshot has failed or the snapshot is no longer present

Do not power cycle Kubernetes pods manually if they are in an unknown state — this can corrupt the PostgreSQL write-ahead log and cause database inconsistency. Restart via `kubectl rollout restart` or `vracli cluster restart` and wait 5 minutes for self-healing.

---

## Generating a Support Bundle

The Aria Automation support bundle is required for all support cases.

**Via CLI (preferred — most comprehensive):**

```bash
# SSH to the Aria Automation appliance
ssh root@vra-prod-01.corp.local

# Generate the support bundle (this takes 5–15 minutes)
vracli support-bundle

# Bundle is saved to /tmp/ — check the filename
ls -lh /tmp/vracli-support-bundle*.tar.gz

# Copy to a local machine for upload
scp root@vra-prod-01.corp.local:/tmp/vracli-support-bundle*.tar.gz /tmp/
```

The bundle includes: service logs from all Kubernetes namespaces, cluster configuration, pod descriptions, database diagnostics (no data, structure only), networking information, and Kubernetes events.

**Targeted log collection** (when the full bundle cannot be generated):

```bash
# Collect logs from the prelude namespace (core Aria Automation services)
kubectl logs -n prelude -l app=assembler --tail=500 > /tmp/assembler.log
kubectl logs -n prelude -l app=iaas-gateway --tail=500 > /tmp/iaas-gateway.log
kubectl logs -n prelude -l app=catalog --tail=500 > /tmp/catalog.log
kubectl logs -n prelude -l app=postgres --tail=200 > /tmp/postgres.log

# Collect Kubernetes events (shows pod restarts and resource issues)
kubectl get events --all-namespaces --sort-by='.metadata.creationTimestamp' > /tmp/k8s-events.log

# Collect pod status
kubectl get pods --all-namespaces -o wide > /tmp/pod-status.log
```

---

## Information to Collect Before Opening a Case

| Item | Where to Find | How to Collect |
|---|---|---|
| Aria Automation version | `vracli version` or admin UI → About | CLI or UI |
| vSphere / vCenter version | vCenter About page | UI |
| NSX version | NSX Manager About page | UI |
| LCM version | LCM admin UI → Settings → System Details | UI |
| Support bundle | Generated via `vracli support-bundle` | CLI (see above) |
| Deployment event logs | UI: Deployments → deployment → History tab | UI or API |
| Kubernetes pod logs | `kubectl logs <pod> -n prelude` | CLI |
| Kubernetes pod status | `kubectl get pods --all-namespaces` | CLI |
| Description of the issue with exact timestamps | — | Incident notes |
| Steps to reproduce the issue | — | Incident notes |
| Impact — how many users / deployments affected | — | Incident notes |
| Timeline: last known good state → first failure | — | Incident notes |
| Any actions taken so far (pod restarts, config changes) | — | Incident notes |
| Screenshot or copy of error messages | UI or API response | Screenshot / text |

---

## SLA Tiers

| Priority | Definition | Initial Response SLA |
|---|---|---|
| **P1 — Critical** | Production environment down; no workaround; all provisioning blocked | 30 minutes (24x7) |
| **P2 — Major** | Significant functionality impacted; partial workaround available | 2 business hours (24x7) |
| **P3 — Minor** | Limited impact; workaround available; non-urgent | Next business day |
| **P4 — General** | How-to questions, enhancement requests, documentation queries | 2 business days |

For P1 cases:
1. Open the case via the portal immediately
2. Call the Broadcom 24x7 support line and reference the case number — do not wait for an email response
3. Request **duty manager escalation** if no engineer response within the SLA

---

## Escalation Path

1. Open the SR via [https://support.broadcom.com](https://support.broadcom.com) with all information listed above
2. Set the correct priority — do not understate impact (P3 for a full production outage will receive next-business-day response)
3. If no response within the SLA: use the portal **Escalate** button or call the support line with your case number
4. For P1: escalate to duty manager immediately after the SLA window passes
5. Engage your internal Broadcom TAM (Technical Account Manager) if available — TAMs can expedite case routing

---

## Pre-SR Diagnostic Checklist

Collect this before opening the SR — support will ask for all of it in the first response if it is not provided upfront:

```bash
ssh root@vra-prod-01.corp.local

# System information
vracli version
vracli status

# Disk space
df -h /

# Pod status summary
kubectl get pods --all-namespaces | awk 'NR>1 {print $4}' | sort | uniq -c | sort -rn

# Failing pods
kubectl get pods --all-namespaces | grep -v "Running\|Completed\|Succeeded"

# Recent Kubernetes events (last 50)
kubectl get events --all-namespaces --sort-by='.metadata.creationTimestamp' | tail -50

# VIDM connectivity (authentication dependency)
curl -sk https://vidm.corp.local/SAAS/API/1.0/REST/system/health
# Expected: {"status": "UP"}

# Cloud account reachability (vCenter)
curl -sk -o /dev/null -w "%{http_code}" https://vcenter-prod.corp.local/rest/com/vmware/cis/session
# Expected: 401 (reachable — authentication challenge)
```

---

## Useful Links

| Resource | URL |
|---|---|
| Broadcom Support Portal | [https://support.broadcom.com](https://support.broadcom.com) |
| Aria Automation Documentation | [https://docs.vmware.com/en/VMware-Aria-Automation/](https://docs.vmware.com/en/VMware-Aria-Automation/) |
| VMware Product Lifecycle Matrix | [https://lifecycle.vmware.com](https://lifecycle.vmware.com) |
| VMware Interoperability Matrix | [https://interopmatrix.vmware.com](https://interopmatrix.vmware.com) |
| Broadcom Security Advisories | [https://support.broadcom.com/security-advisory](https://support.broadcom.com/security-advisory) |
| VMware Knowledge Base | [https://kb.vmware.com](https://kb.vmware.com) |

**Useful KB search patterns for Aria Automation:**
- Deployment failures: `site:kb.vmware.com "vRealize Automation" "CREATE_FAILED"`
- Pod CrashLoopBackOff: `site:kb.vmware.com "vRealize Automation" CrashLoopBackOff`
- VIDM authentication: `site:kb.vmware.com "vRealize Automation" "identity manager"`
- Upgrade failures: `site:kb.vmware.com "vRealize Automation" upgrade failed`
- Cloud account errors: `site:kb.vmware.com "vRealize Automation" "cloud account" error`

---

## SR Handoff Checklist

Before handing an SR to the next shift or to a specialist:

- [ ] SR number documented in the incident ticket
- [ ] Support bundle uploaded to the SR (confirm upload completed in the portal)
- [ ] Exact Aria Automation version noted: `vracli version`
- [ ] Number of affected users / deployments documented
- [ ] Timeline: last known good state → first failure → all actions taken, with timestamps
- [ ] Any commands run on the appliance documented (with outputs if relevant)
- [ ] Current state of all VM snapshots: present or absent, age
- [ ] Broadcom support engineer name and direct contact method noted
- [ ] Next expected contact time agreed with support engineer
