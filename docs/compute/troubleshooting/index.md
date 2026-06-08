# Compute — Troubleshooting

<div class="kb-summary">
Cross-platform compute troubleshooting — Linux, Windows Server, Active Directory, and database failures; symptom-to-section reference.
</div>

## Symptom Index

| Symptom | Platform | Where to look |
|---|---|---|
| High CPU / load | Linux | `top`, `perf top`, `ps aux --sort=-%cpu` |
| High CPU | Windows | Task Manager → Resource Monitor → CPU tab |
| Memory exhaustion / OOM | Linux | `dmesg | grep oom`, `/var/log/messages` |
| Service won't start | Linux | `journalctl -u <svc> -n 50`, `systemctl status` |
| Service won't start | Windows | Event Viewer → Windows Logs → System/Application |
| Disk full | Linux | `df -h`, `du -sh /*` |
| Disk I/O bottleneck | Linux | `iostat -xz 1 5`, `iotop` |
| Network unreachable | Both | `ping`, `traceroute`/`tracert`, `ss -tnp`/`netstat -an` |
| DNS failure | Both | `dig @<server>`, `nslookup`, `Resolve-DnsName` |
| DB connection refused | MySQL/PG/MSSQL | Check service running, port open, firewall, pg_hba/login |
| Replication broken | MySQL/PG/MSSQL | `SHOW REPLICA STATUS` / `pg_stat_replication` / AG DMVs |
| AD login failures | Windows | `dcdiag /test:dns`, Event ID 4625 in Security log |

## Common Linux Diagnostic Commands

```bash
# System load and CPU
uptime; top -bn1 | head -20

# Memory
free -h; cat /proc/meminfo | grep -E 'MemFree|Cached|SwapFree'

# Disk
df -h; iostat -xz 1 3

# Network
ss -tnp; ip route; ip addr

# Processes
ps aux --sort=-%mem | head -15
```

## Common Windows Diagnostic Commands

```powershell
# System resources
Get-Process | Sort-Object CPU -Descending | Select-Object -First 15
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 5

# Disk
Get-PSDrive -PSProvider FileSystem
Get-Counter '\PhysicalDisk(*)\% Disk Time' -SampleInterval 2 -MaxSamples 5

# Network
netstat -an | findstr ESTABLISHED | wc -l
Test-NetConnection -ComputerName <host> -Port <port>

# Event log
Get-EventLog -LogName System -EntryType Error -Newest 20
```

## When to Escalate

- Load average sustained > 4× CPU count for > 10 minutes
- Available memory < 100 MB (Linux) or paging file usage > 80% (Windows)
- Disk < 5% free on any production volume
- Database replication lag > 5 minutes or replication stopped
- AD domain controller unreachable or SYSVOL not shared
