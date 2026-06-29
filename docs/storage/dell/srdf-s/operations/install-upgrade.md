---
tags:
  - dell
  - operations
---
# SRDF/S — Install & Upgrade

*Applies to: Dell EMC Storage*
![SRDF/S — Install & Upgrade](../../../../assets/storage-dell-srdf-s-operations-install-upgrade.svg)

```bash
symcfg list -v | grep "Microcode"
```

```d2
direction: right

preCheck: "Verify All Pairs Synchronized\nsymrdf -g rdfg query | grep -v Synchronized" {shape: rectangle}
notifyApps: "Notify Application Teams\nTemporary RPO degradation during window" {shape: rectangle}
convertAsync: "Convert to SRDF/A\nsymrdf -g rdfg set mode async" {shape: rectangle}
nduSource: "NDU on Source Array\n(Dell NDU runbook" {shape: rectangle}
nduTarget: "NDU on Target Array" {shape: rectangle}
convertSync: "Re-establish Synchronous Mode\nsymrdf -g rdfg set mode sync" {shape: rectangle}
waitResync: "Wait for Synchronized State\n(SyncInProg expected" {shape: rectangle}
postValidate: "Post-Upgrade Validation\nAll pairs Synchronized within 30 min" {shape: rectangle}
closeChange: "Close Change Ticket" {shape: rectangle}

preCheck -> notifyApps
notifyApps -> convertAsync
convertAsync -> nduSource
nduSource -> nduTarget
nduTarget -> convertSync
convertSync -> waitResync
waitResync -> postValidate
postValidate -> closeChange
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Srdf S — Procedures](../procedures/)
- [Srdf S — Health Checks](../health-checks/)
- [Srdf S — Deploy](../../deploy/)
