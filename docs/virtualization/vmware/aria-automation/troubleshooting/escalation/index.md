# Aria Automation — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, When to Escalate, Generating a Support Bundle, Information to Collect Before Opening a Case, SLA Tiers and 4 more sections.
</div>

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
ssh root@vra-prod-01.example.local

# Generate the support bundle (this takes 5–15 minutes)
vracli support-bundle

# Bundle is saved to /tmp/ — check the filename
ls -lh /tmp/vracli-support-bundle*.tar.gz

# Copy to a local machine for upload
scp root@vra-prod-01.example.local:/tmp/vracli-support-bundle*.tar.gz /tmp/
```
```
┌──────────────────────────────────── Aria Automation — Escalation ─────────────────────────────────────┐
│                                                                                                       │
│  Escalate vRA issues when self-service diagnostics are exhausted and impact is unresolved.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │          Prepare Before Escalating          │   │
│   │          vRA service down > 30 min           │  │       Support bundle (LCM logscraper)       │   │
│   │      Data loss or corruption suspected       │  │         vRA version and patch level         │   │
│   │         Upgrade failure mid-process          │  │        Timeline of events and changes       │   │
│   │       Security breach or data exposure       │  │         Deployment events + pod logs        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Open VMware SR with P1 priority for service-down; provide bundle and timeline.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             VMware Support Path              │  │             Internal Escalation             │   │
│   │         SR: my.vmware.com or portal          │  │      Platform team: notify stakeholders     │   │
│   │       P1: live call with GSS engineer        │  │       Change freeze if upgrade-related      │   │
│   │     TAM: escalate for critical accounts      │  │       DR: consider vRA failover if HA       │   │
│   │        KB: search kb.vmware.com first        │  │        Post-incident: RCA within 48h        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance cluster · LCM · Postgres · vIDM · vCenter · support upload endpoint                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SR                = Support Request; formal case opened with VMware GSS                              │
│  P1 priority       = Critical severity; service down with no workaround; live engineer call           │
│  GSS               = Global Support Services; VMware technical support team                           │
│  TAM               = Technical Account Manager; premium support contact for critical accounts         │
│  LCM logscraper    = Diagnostic archive tool; collect before calling support                          │
│  Support bundle    = Generated from VAMI or LCM; contains pod logs, DB state, configs                 │
│  Change freeze     = Halt all non-critical changes during active incident investigation               │
│  RCA               = Root Cause Analysis; post-incident document describing failure and fix           │
│  vRA HA            = High Availability mode; second vRA node can serve if primary fails               │
│  kb.vmware.com     = VMware Knowledge Base; search before opening SR to find known fixes              │
│  Timeline          = Chronological record of events, changes, and symptoms before the issue           │
│  Stakeholder notif = Communicate impact and ETA to application owners and business units              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
