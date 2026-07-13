---
tags:
  - aria-operations
  - operations
  - vmware
description: "Infrastructure Health Monitoring reference covering Server Health (Windows), Storage Array Health, Network Health, Monitoring Agent Validation, Escalation..."
---
# Infrastructure Health Monitoring

<div class="kb-summary">
Infrastructure Health Monitoring reference covering Server Health (Windows), Storage Array Health, Network Health, Monitoring Agent Validation, Escalation Thresholds (reference).

*Applies to: Aria Ops 8.x*
</div>

**Pure FlashArray:**
```bash
purecli array get                  # overall status
purecli drive list | grep -v healthy
purecli volume list --space        # capacity view
```


```text title="Expected output"
Name             Status      Version
flasharray-prod  Optimal     6.4.2.1
flasharray-dr    Optimal     6.4.2.1

Name       Slot  Status      Capacity
SSD-001    1.0   Predictive  1.92TB
SSD-042    3.7   Predictive  1.92TB
NVMe-156   5.2   Unhealthy   3.84TB

Name                  Provisioned  Virtual    Snapshots  Total
vm-datastore-01       2.5TB        1.8TB      450GB      2.75TB
vm-datastore-02       1.2TB        890GB      120GB      1.31TB
vm-backup-tier        3.8TB        2.1TB      1.2TB      4.2TB
vm-archive-01         5.0TB        4.2TB      800GB      5.8TB
...
```

!!! warning "Common errors"
    **`purecli: command not found`** — Install the Pure Storage CLI package or add its installation directory to your PATH environment variable.
    **`Error: Invalid credentials or unable to connect to array`** — Verify the array IP/hostname is reachable and run `purecli login` with valid credentials before executing commands.
**Dell PowerMax / Unity:**
```bash
# PowerMax — Solutions Enabler
symcfg list -health
symsys -sid <sid> list -failed

# Unity — CLI
uemcli -d <ip> /sys/general show
uemcli -d <ip> /sys/alert show
```

```d2
direction: right

network_health: "Network Health" {shape: rectangle}
monitoring_agent_validation: "Monitoring Agent Validation" {shape: rectangle}
escalation_thresholds_reference: "Escalation Thresholds (reference)" {shape: rectangle}
verify: "Verify" {shape: rectangle}

network_health -> monitoring_agent_validation
monitoring_agent_validation -> escalation_thresholds_reference
escalation_thresholds_reference -> verify
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Network Health

```bash
# OSPF neighbours (Cisco IOS / NX-OS)
show ip ospf neighbor

# BGP summary
show bgp ipv4 unicast summary

# Interface error counters
show interface | include "line protocol|input errors|output errors|CRC"
```


```text title="Expected output"
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.0.0.1         1   FULL/DR         00:00:38    192.168.1.1     Gi0/0
10.0.0.2         1   FULL/BDR        00:00:35    192.168.1.2     Gi0/1
10.0.0.3         0   FULL/DROTHER    00:00:39    192.168.1.3     Gi0/2

BGP router identifier 10.50.0.5, local AS number 65001

Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.50.0.10      4 65002   45821   45819  1048576    0    0 5w2d     125
10.50.0.11      4 65002   43102   43105  1048576    0    0 4w6d     89

GigabitEthernet0/0 is up, line protocol is up
  Input errors: 0, CRC: 0, frame: 0, overrun: 0, ignored: 0
  Output errors: 0, collisions: 0, interface resets: 0
GigabitEthernet0/1 is up, line protocol is up
  Input errors: 127, CRC: 45, frame: 12, overrun: 0, ignored: 0
  Output errors: 3, collisions: 0, interface resets: 0
GigabitEthernet0/2 is down, line protocol is down
  Input errors: 892, CRC: 234, frame: 89, overrun: 0, ignored: 0
  Output errors: 156, collisions: 0, interface resets: 2
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the device is running Cisco IOS/NX-OS and use the exact command syntax without extra characters.
    **`% Incomplete command.`** — Complete the command with a valid keyword such as `show ip ospf neighbor detail` or check device configuration mode.
    **`Connection refused` or `Connection timed out`** — Ensure SSH/Telnet connectivity to the device and verify network reachability before running diagnostic commands.
## Monitoring Agent Validation

```bash
# Check monitoring agent is running (Zabbix example)
systemctl status zabbix-agent2

# Check last contact with monitoring server
grep "sending data" /var/log/zabbix/zabbix_agent2.log | tail -5
```


```text title="Expected output"
● zabbix-agent2.service - Zabbix Agent 2
     Loaded: loaded (/usr/lib/systemd/system/zabbix-agent2.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2 days ago
       Docs: https://www.zabbix.com/documentation/current/manual/installation/agent
    Process: 2847 ExecStart=/usr/sbin/zabbix_agent2 (code=exited, status=0/SUCCESS)
   Main PID: 2848 (zabbix_agent2)
      Tasks: 12 (limit: 4915)
     Memory: 28.4M
        CPU: 2min 34.821s
     CGroup: /system.slice/zabbix-agent2.service
             └─2848 /usr/sbin/zabbix_agent2

2024-01-15 14:35:42 Zabbix agent2 [esx-vm-prod-04]: sending data to server [10.42.8.15:10051]
2024-01-15 14:36:12 Zabbix agent2 [esx-vm-prod-04]: sending data to server [10.42.8.15:10051]
2024-01-15 14:36:42 Zabbix agent2 [esx-vm-prod-04]: sending data to server [10.42.8.15:10051]
2024-01-15 14:37:12 Zabbix agent2 [esx-vm-prod-04]: sending data to server [10.42.8.15:10051]
2024-01-15 14:37:42 Zabbix agent2 [esx-vm-prod-04]: sending data to server [10.42.8.15:10051]
```

!!! warning "Common errors"
    **`Unit zabbix-agent2.service could not be found.`** — Install the Zabbix agent2 package with `apt-get install zabbix-agent2` or `yum install zabbix-agent2` depending on your distribution.
    **`grep: /var/log/zabbix/zabbix_agent2.log: No such file or directory`** — Ensure the Zabbix agent2 service has started at least once and check that `/var/log/zabbix/` directory exists with proper permissions.
    **`Active: inactive (dead) since Mon 2024-01-15 10:15:33 UTC`** — Start the service with `systemctl start zabbix-agent2` and verify connectivity to the monitoring server in `/etc/zabbix/zabbix_agent2.conf`.
## Escalation Thresholds (reference)

| Metric | Warning | Critical |
|---|---|---|
| CPU (sustained 15 min) | >70% | >90% |
| Memory | >80% | >95% |
| Disk usage | >75% | >90% |
| Storage latency (avg) | >5ms | >20ms |
| Backup failure | 1 job | 2+ consecutive |

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier

## See also

- [Alert Management](alert-management.md)
- [Aria Operations: Alert Definitions and Policies](alerts.md)
- [Aria Operations Backup & Restore](backup-restore.md)
- [Aria Operations — Operations](index.md)
- [Aria Operations — Architecture](../../architecture/)
- [Aria Operations — Deploy](../../deploy/)
- [Aria Operations — Security](../../security/)
- [Aria Operations — Troubleshooting](../../troubleshooting/)
