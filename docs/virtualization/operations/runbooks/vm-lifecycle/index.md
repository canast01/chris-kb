# VM Lifecycle Runbook


<div class="kb-summary">
VM Lifecycle Runbook reference covering Overview, Pre-Checks, Steps, Validation, Rollback and 1 more sections.
</div>

```
┌──────────────────────────────────────── VM Lifecycle Runbook ─────────────────────────────────────────┐
│                                                                                                       │
│    Standard steps for VM deploy, reconfigure, ownership review, and decommission                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Build            │  │       Operate + Review      │  │         Decommission        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Validate request      │  │        Confirm owner        │  │        Owner approval       │   │
│   │        Confirm sizing       │  │        Review sizing        │  │         Final backup        │   │
│   │     Deploy from template    │  │         Check backup        │  │         Power off VM        │   │
│   │    Apply naming standard    │  │       Check monitoring      │  │     Delete from vCenter     │   │
│   │     Assign backup policy    │  │       Patch compliance      │  │      Remove from backup     │   │
│   │      Add to monitoring      │  │        Annual review        │  │         Update CMDB         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Template     = Golden image VM used as the base for new deployments; keep patched                  │
│    Naming std   = Consistent VM name format; e.g. SITE-ROLE-NN; critical for CMDB                     │
│    Backup policy = Defines schedule, retention, and target for the VM backup job                      │
│    CMDB         = Configuration Management Database; tracks all VMs and their owners                  │
│    Annual review = Yearly check that VM is still needed and owner is still valid                      │
│    Decommission  = Remove VM, backup exclusions, monitoring, DNS, and CMDB in that order              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── VM Lifecycle Runbook ─────────────────────────────────────────┐
│                                                                                                       │
│    Standard steps for VM deploy, reconfigure, ownership review, and decommission                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Build            │  │       Operate + Review      │  │         Decommission        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Validate request      │  │        Confirm owner        │  │        Owner approval       │   │
│   │        Confirm sizing       │  │        Review sizing        │  │         Final backup        │   │
│   │     Deploy from template    │  │         Check backup        │  │         Power off VM        │   │
│   │    Apply naming standard    │  │       Check monitoring      │  │     Delete from vCenter     │   │
│   │     Assign backup policy    │  │       Patch compliance      │  │      Remove from backup     │   │
│   │      Add to monitoring      │  │        Annual review        │  │         Update CMDB         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Template     = Golden image VM used as the base for new deployments; keep patched                  │
│    Naming std   = Consistent VM name format; e.g. SITE-ROLE-NN; critical for CMDB                     │
│    Backup policy = Defines schedule, retention, and target for the VM backup job                      │
│    CMDB         = Configuration Management Database; tracks all VMs and their owners                  │
│    Annual review = Yearly check that VM is still needed and owner is still valid                      │
│    Decommission  = Remove VM, backup exclusions, monitoring, DNS, and CMDB in that order              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

Use this for VM build, change, ownership, review, retirement, and cleanup.

## Pre-Checks

- Confirm VM owner.
- Confirm business purpose.
- Confirm sizing.
- Confirm backup policy.
- Confirm monitoring.
- Confirm network and security requirements.
- Confirm naming standard.

## Steps

1. Validate request details.
2. Build or update VM.
3. Apply naming and tagging standards.
4. Confirm backup and monitoring.
5. Validate access and connectivity.
6. Record owner and lifecycle notes.
7. Review unused VMs regularly.
8. Decommission cleanly when approved.

## Validation

- VM has owner.
- VM follows naming standard.
- Backup is assigned.
- Monitoring is active.
- Tags or inventory notes are current.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
