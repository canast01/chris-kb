# Linux CLI Reference

This section covers the most commonly used Linux administration commands, grouped by category. Commands apply to both RHEL and Ubuntu unless otherwise noted. Package management commands differ by distribution: `dnf`/`yum` for RHEL, `apt` for Ubuntu. All other commands are standard across distributions.

| Category | Commands |
|---|---|
| Service management | `systemctl start/stop/restart/status/enable/disable` |
| Logging | `journalctl -u <service>`, `journalctl -p err`, `journalctl --since` |
| Package management (RHEL) | `dnf install/remove/update/list`, `yum history` |
| Package management (Ubuntu) | `apt install/remove/upgrade`, `apt list --installed` |
| Network | `ss -tulnp`, `ip addr`, `ip route`, `ip link` |
| Disk/storage | `lsblk`, `lvdisplay`, `vgdisplay`, `pvdisplay`, `df -h`, `du -sh` |
| Process/performance | `top`, `htop`, `ps aux`, `uptime`, `vmstat`, `iostat` |
| User/session | `last`, `lastb`, `who`, `w`, `id`, `getent passwd` |
| Firewall (RHEL) | `firewall-cmd --list-all`, `firewall-cmd --add-service`, `--permanent` |
| Firewall (Ubuntu) | `ufw status`, `ufw allow`, `ufw deny` |
