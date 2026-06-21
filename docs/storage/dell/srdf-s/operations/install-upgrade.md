---
tags:
  - dell
  - operations
---
# SRDF/S — Install & Upgrade
![SRDF/S — Install & Upgrade](../../../../assets/storage-dell-srdf-s-operations-install-upgrade.svg)


```bash
symcfg list -v | grep "Microcode"
```

```mermaid
flowchart TD
    preCheck["Verify All Pairs Synchronized\nsymrdf -g rdfg query | grep -v Synchronized"]
    notifyApps["Notify Application Teams\nTemporary RPO degradation during window"]
    convertAsync["Convert to SRDF/A\nsymrdf -g rdfg set mode async"]
    nduSource["NDU on Source Array\n(Dell NDU runbook)"]
    nduTarget["NDU on Target Array"]
    convertSync["Re-establish Synchronous Mode\nsymrdf -g rdfg set mode sync"]
    waitResync["Wait for Synchronized State\n(SyncInProg expected)"]
    postValidate["Post-Upgrade Validation\nAll pairs Synchronized within 30 min"]
    closeChange["Close Change Ticket"]

    preCheck --> notifyApps
    notifyApps --> convertAsync
    convertAsync --> nduSource
    nduSource --> nduTarget
    nduTarget --> convertSync
    convertSync --> waitResync
    waitResync --> postValidate
    postValidate --> closeChange

    style preCheck fill:#7c3aed,color:#fff
    style convertAsync fill:#b45309,color:#fff
    style convertSync fill:#2563eb,color:#fff
    style closeChange fill:#15803d,color:#fff
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

- [Srdf S — Procedures](procedures/)
- [Srdf S — Health Checks](health-checks/)
- [Srdf S — Deploy](../deploy/)
