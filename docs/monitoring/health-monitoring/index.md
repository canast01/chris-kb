# Infrastructure Health Monitoring
## Daily Health Check Checklist

| Category | What to Check | Tool |
|---|---|---|
| Servers | CPU, memory, disk — no thresholds breached | CloudIQ / vROps / Zabbix |
| Storage arrays | Controller health, drive faults, capacity % | CloudIQ / Pure1 / ONTAP |
| SAN fabric | Port errors, ISL utilisation, zoning | DCNM / Network Advisor |
| Network | Interface errors, BGP/OSPF neighbour state | Nexus Dashboard / SolarWinds |
| Backup jobs | Last backup status, RPO met | Commvault / Veeam |
| Certificates | Expiry within 60 days | OpenSSL / Venafi |

## Server Health (Linux)

```bash
# High-level — one line per host
uptime
free -h
df -h | grep -vE '^tmpfs|^devtmpfs'

# Failed services
systemctl --failed

# Recent kernel errors
journalctl -p err -b --no-pager | tail -30
```

## Server Health (Windows)

```powershell
# Services not running that should be
Get-Service | Where-Object { $_.Status -ne 'Running' -and $_.StartType -eq 'Automatic' }

# Disk usage
Get-Volume | Select-Object DriveLetter, FileSystemLabel, @{N='UsedGB';E={[math]::Round(($_.Size - $_.SizeRemaining)/1GB,1)}}, @{N='FreeGB';E={[math]::Round($_.SizeRemaining/1GB,1)}}, @{N='Size';E={[math]::Round($_.Size/1GB,1)}}

# Recent system errors
Get-EventLog -LogName System -EntryType Error -Newest 20
```

## Storage Array Health

**NetApp ONTAP:**
```bash
system health status show          # overall health
system health alert show           # open alerts
storage disk show -broken          # failed disks
volume show -percent-used >85      # volumes near capacity
```

**Pure FlashArray:**
```bash
purecli array get                  # overall status
purecli drive list | grep -v healthy
purecli volume list --space        # capacity view
```

**Dell PowerMax / Unity:**
```bash
# PowerMax — Solutions Enabler
symcfg list -health
symsys -sid <sid> list -failed

# Unity — CLI
uemcli -d <ip> /sys/general show
uemcli -d <ip> /sys/alert show
```

## Network Health

```bash
# OSPF neighbours (Cisco IOS / NX-OS)
show ip ospf neighbor

# BGP summary
show bgp ipv4 unicast summary

# Interface error counters
show interface | include "line protocol|input errors|output errors|CRC"
```

## Monitoring Agent Validation

```bash
# Check monitoring agent is running (Zabbix example)
systemctl status zabbix-agent2

# Check last contact with monitoring server
grep "sending data" /var/log/zabbix/zabbix_agent2.log | tail -5
```

## Escalation Thresholds (reference)

| Metric | Warning | Critical |
|---|---|---|
| CPU (sustained 15 min) | >70% | >90% |
| Memory | >80% | >95% |
| Disk usage | >75% | >90% |
| Storage latency (avg) | >5ms | >20ms |
| Backup failure | 1 job | 2+ consecutive |
