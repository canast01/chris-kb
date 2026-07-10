---
tags:
  - operations
  - veeam
---
# Veeam — Scripts

<div class="kb-summary">
PowerShell scripts for Veeam job management, capacity reporting, SLA health checks, and backup copy automation.

*Applies to: Veeam 12.x*
</div>

- Store VBR credentials using Windows Credential Manager or retrieve from CyberArk at runtime.
- Use `Try/Catch/Finally` blocks to ensure `Disconnect-VBRServer` is called even on error.

```d2
direction: down

verify: "Verify" {shape: rectangle}

```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy

---

## See also

- [Veeam — Procedures](../procedures/)
- [Veeam — CLI Reference](../cli-reference/)
- [Veeam — Health Checks](../health-checks/)
