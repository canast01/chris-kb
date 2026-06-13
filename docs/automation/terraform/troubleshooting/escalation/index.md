---
tags:
  - terraform
  - troubleshooting
search:
  boost: 1.5
---
# Terraform — Escalation


<div class="kb-summary">
Escalation reference covering Escalation Decision Tree, When to Escalate, What to Capture Before Escalating, Escalation Checklist, Raising the Escalation and 1 more sections.

*Applies to: Terraform 1.x*
</div>

```text
┌─────────────────────────────────────── Terraform — Escalation ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Escalate Terraform issues: provider bugs → GitHub, state corruption → HashiCorp support    │   │
│   │  Provider bugs: github.com/hashicorp/terraform-provider-<name>; include TF + provider version │   │
│   │        Terraform Cloud: support.hashicorp.com; TF Enterprise: emergency contact per SLA       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │                Info to Gather               │   │
│   │             State file corrupted             │  │           terraform version output          │   │
│   │            Provider panic / crash            │  │               Provider version              │   │
│   │           Lock cannot be released            │  │            TF_LOG=TRACE full log            │   │
│   │               TF Cloud outage                │  │            State file (sanitised)           │   │
│   │        Sentinel policy blocking apply        │  │               Plan JSON output              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  State corruption   = restore from S3 versioned backup; terraform state push prev-state.json  │   │
│   │  Provider GitHub    = github.com/hashicorp/terraform-provider-aws (replace aws with provider) │   │
│   │         HashiCorp support  = support.hashicorp.com; severity 1 for production outages         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Before you begin

- **Access:** Provider credentials configured (`terraform login` or env vars)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Escalation Decision Tree



## When to Escalate

Escalate when:

- State is corrupt or inconsistent and cannot be recovered with standard state commands
- A provider is returning persistent errors that are not related to credentials or configuration
- A `terraform apply` has partially completed and left infrastructure in an unknown state
- State is locked and the lock holder process cannot be identified or terminated
- The issue is causing or will cause production impact

## What to Capture Before Escalating

Gather the following before raising a ticket or paging someone:

- Full error message — copy from the terminal or log file (not a screenshot)
- Terraform version: `terraform version`
- Provider name and version: `terraform providers`
- Workspace: `terraform workspace show`
- Backend type and state file path (from `backend.tf`)
- The last successful `terraform plan` or `terraform apply` output
- Whether the state is currently locked and the lock ID if known
- Recent changes: provider version upgrades, new resources, backend changes

## Escalation Checklist

| Step | Done |
|---|---|
| Full error message and traceback captured | |
| Terraform and provider versions recorded | |
| Current workspace confirmed | |
| State lock status checked | |
| Last successful apply timestamp noted | |
| State backup taken before any recovery attempts | |
| Impact assessed (which resources or environments are affected) | |

## Raising the Escalation

Include in the ticket or message:

- **Summary:** One sentence describing what failed and the business impact
- **Error:** Full error output (use a code block)
- **Environment:** Terraform version, provider versions, workspace, backend type
- **Reproduction:** Steps to reproduce, or confirmation the issue is not reproducible
- **What was tried:** List of diagnostic and recovery steps already attempted
- **State status:** Whether state is locked, partially applied, or consistent
- **Recent changes:** Provider upgrades, configuration changes, or infrastructure changes in the last 48 hours

## State Recovery Reference

| Situation | Safe first step |
|---|---|
| State locked with no active run | `terraform force-unlock <lock-id>` |
| Partial apply | `terraform plan` to assess drift; `terraform apply` to reconcile |
| State file corrupt | Restore from backend version history; never edit state manually |
| Resource in wrong state | `terraform state rm` then `terraform import` |
| Provider version regression | Restore previous `.terraform.lock.hcl`; run `terraform init` |

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Terraform — Diagnostics](../diagnostics/)
- [Terraform — Common Issues](../common-issues/)
