# SRDF/A — Authentication

> Part of the [SRDF/A](../../index.md) reference.

---

## Credential Rotation

- Solutions Enabler service accounts: rotate passwords every 90 days
- Unisphere API tokens: rotate client certificates annually or on personnel change
- Verify no shared credentials between monitoring and DR automation accounts

---

## Service Account Policy

Create a dedicated service account per automation system; never use the root Solutions Enabler account:

```bash
symauth -sid <SID> add -username svc_dr_automation -role StorageAdmin -scope rdfg:<group_number>
```

Each automation system (monitoring, SRM, runbook scripts) should use a dedicated account scoped to the minimum required RDF groups and roles.
