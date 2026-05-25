# MDS — Backup & Restore

> Part of the [Cisco MDS](../../index.md) reference.

---

## Backup Configuration

Save running configuration to startup and copy off-switch before any change.

```bash
# Save running to startup config
copy running-config startup-config

# Copy running config off-switch via SCP
copy running-config scp://<user>@<server>/<path>/<filename>

# Copy running config off-switch via TFTP
copy running-config tftp://<server>/<filename>

# Display full running config (for manual capture)
show running-config
```

---

## Checkpoint (Named Snapshot)

NX-OS supports named checkpoints to capture configuration state.

```bash
# Save a named checkpoint
checkpoint <checkpoint_name>

# List all checkpoints
show checkpoint summary

# View a specific checkpoint
show checkpoint <checkpoint_name>
```

---

## Restore Procedures

```bash
# Rollback to a named checkpoint
rollback running-config checkpoint <checkpoint_name>

# Restore from a TFTP file
copy tftp://<server>/<filename> running-config

# Restore from SCP
copy scp://<user>@<server>/<path>/<filename> running-config
```

> After restoring, always verify: `show interface brief`, `show flogi database`, and `show zoneset active vsan all`.

---

## Post-Restore Validation

- [ ] All FC interfaces back in connected/up state: `show interface brief`
- [ ] FLOGI database complete — all expected hosts and storage logged in: `show flogi database`
- [ ] Active zoneset matches expected: `show zoneset active vsan all`
- [ ] No error entries in recent syslog: `show logging last 50`
- [ ] Save restored config to startup: `copy running-config startup-config`
