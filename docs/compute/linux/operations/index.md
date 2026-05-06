# Linux Operations

Daily operational checks confirm server health before business hours and after any overnight maintenance. Key checks include reviewing failed systemd units with `systemctl --failed`, disk utilisation with `df -h`, memory pressure with `free -h`, load average with `uptime`, and failed login attempts with `lastb`. Error-level log entries are reviewed via `journalctl -p err` on systemd-based systems or `/var/log/messages` on older RHEL releases. Any failed units, disks above 80%, or repeated login failures are escalated for investigation.

- `systemctl --failed` — list any failed units
- `df -h` — disk usage across all filesystems
- `free -h` — memory and swap utilisation
- `uptime` — load averages (1, 5, 15 min)
- `lastb` — failed login attempts
- `journalctl -p err -n 50` — last 50 error-level log entries
