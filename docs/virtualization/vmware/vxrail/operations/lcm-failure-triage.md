---
tags:
  - operations
  - vxrail
---
# VxRail LCM Failure Triage

<div class="kb-summary">
VxRail LCM Failure Triage reference covering Symptoms, Likely Causes, Commands, Troubleshooting Workflow, Resolution and 1 more sections.

*Applies to: VxRail 7.x / 8.x*
</div>

```d2
direction: right

symptoms: "Symptoms" {shape: rectangle}
likely_causes: "Likely Causes" {shape: rectangle}
commands: "Commands" {shape: rectangle}
troubleshooting_workflow: "Troubleshooting Workflow" {shape: rectangle}
resolution: "Resolution" {shape: rectangle}
prevention: "Prevention" {shape: rectangle}

symptoms -> likely_causes
likely_causes -> commands
commands -> troubleshooting_workflow
troubleshooting_workflow -> resolution
resolution -> prevention
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Symptoms

- VxRail lifecycle operation fails.
- Upgrade task stops or rolls back.
- VxRail Manager reports validation failure.
- Bundle install does not continue.

## Likely Causes

- Recent configuration change.
- DNS, certificate, or authentication issue.
- Resource pressure.
- Failed service.
- Storage or network dependency issue.
- Version or compatibility mismatch.

## Commands

```bash
# Add environment-specific commands here
```

## Troubleshooting Workflow

1. Confirm scope.
2. Check recent changes.
3. Review alarms and events.
4. Validate management connectivity.
5. Check logs.
6. Isolate the failing dependency.
7. Apply fix or escalate with evidence.

## Resolution

Document what changed, what fixed it, and how health was validated.

## Prevention

- Improve alerting.
- Add missing checks.
- Update the runbook.
- Capture known issue notes.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [VxRail — Backup & Restore](backup-restore.md)
- [VxRail — CLI Reference](cli-reference.md)
- [VxRail Cluster Expansion](cluster-expansion.md)
- [VxRail Operations](index.md)
- [VxRail — Architecture](../../architecture/)
- [VxRail — Deploy](../../deploy/)
- [VxRail Security](../../security/)
- [VxRail Troubleshooting](../../troubleshooting/)
