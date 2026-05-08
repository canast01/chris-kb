# RecoverPoint — Hardening

> Part of the [RecoverPoint](../../) > [Security](../) reference.

---

## SSH Hardening

```bash
# Verify root login is disabled
grep PermitRootLogin /etc/ssh/sshd_config    # Should show: no

# Restrict SSH to management jump hosts only (RecoverPoint CLI)
set_system_ssh_restrictions -allow <jump_host_ip>/32
```

- SSH idle session timeout: 10 minutes (TMOUT=600 in /etc/profile)
- SSH host keys: document fingerprints in the CMDB entry for each RPA node
