# FabricOS — Backup & Restore

> Part of the [Operations](../) reference.

---

## configupload / configdownload

```bash
# Backup the switch configuration to an SCP server
configupload -all scp://<username>:<password>@<server>/<path>/switch-config.txt

# Restore configuration (use during replacement or recovery)
configdownload -all scp://<username>:<password>@<server>/<path>/switch-config.txt
```

Configurations should be backed up:
- Before any firmware upgrade
- Before any major zone change
- On a scheduled basis (weekly minimum)

---

## Backup Schedule

Add backup procedures and schedule details here as they are defined.

---

## Restore Validation

Add restore validation steps here.
