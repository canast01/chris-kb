---
tags:
  - operations
  - veeam
description: "Install & Upgrade reference covering Release Cadence, Decommission Procedure."
---
# Veeam — Install & Upgrade

<div class="kb-summary">
Install & Upgrade reference covering Release Cadence, Decommission Procedure.

*Applies to: Veeam 12.x*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
release_cadence: "Release Cadence" {shape: rectangle}
decommission_procedure: "Decommission Procedure" {shape: rectangle}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> release_cadence
release_cadence -> decommission_procedure
decommission_procedure -> verify
verify -> validate
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Release Cadence

Veeam releases major versions (VBR 12, 12.1, 12.2) annually with cumulative patches (P-releases) throughout the year.

### Upgrade Component Order

Store the config backup off the Backup Server — it is useless if the server hosting it is lost.

## Decommission Procedure

When retiring a Veeam Backup Server:
1. Export and archive all backup job configuration
2. Migrate retention-period backups to a new repository or archive
3. Un-register all proxies and repositories
4. Deregister vCenter credentials
5. Update CMDB to reflect decommission

---

## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy

---

## See also

- [Veeam — Deploy](../../deploy/)
