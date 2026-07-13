---
tags:
  - networking
description: "SNMP traps are unsolicited notifications sent from a device to a trap receiver (NMS) when an event occurs"
---
# SNMP Traps

<div class="kb-summary">
SNMP traps are unsolicited notifications sent from a device to a trap receiver (NMS) when an event occurs
</div>

        TRAP FLOW (device-initiated, async)

— a link going down, a threshold being crossed, or a hardware fault. Unlike polling, traps push alerts in real time.

```d2
direction: down

trap_vs_inform: "Trap vs Inform" {shape: rectangle}
configuring_trap_destinations: "Configuring Trap Destinations" {shape: rectangle}
testing_trap_delivery: "Testing Trap Delivery" {shape: rectangle}
common_trap_oids: "Common Trap OIDs" {shape: rectangle}
trap_receiver_snmptrapd: "Trap Receiver — snmptrapd" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

trap_vs_inform -> configuring_trap_destinations: uses
configuring_trap_destinations -> testing_trap_delivery: uses
testing_trap_delivery -> common_trap_oids: uses
common_trap_oids -> trap_receiver_snmptrapd: uses
trap_receiver_snmptrapd -> common_issues: uses
```

## Trap vs Inform

| Type | Acknowledgement | Reliability | Version |
|---|---|---|---|
| **Trap** | None | Fire-and-forget | v1, v2c, v3 |
| **Inform** | Manager sends ACK | Reliable delivery | v2c, v3 |

Use Informs where delivery confirmation matters (e.g. critical hardware alarms).

## Configuring Trap Destinations

### Linux (snmpd)

```bash
# /etc/snmp/snmpd.conf

# SNMPv2c trap destination
trapsink    <nms-ip>  <community>  162

# SNMPv2c inform destination
trap2sink   <nms-ip>  <community>  162

# SNMPv3 trap
trapsess -v 3 -u trapuser -l authPriv -a SHA -A <authpass> -x AES -X <privpass> <nms-ip>

systemctl restart snmpd
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`error on line 3: unknown token: trapsink`** — Use `trap2sink` for SNMPv2c traps, or verify snmpd version supports legacy `trapsink` syntax.
    **`error on line 9: Unknown user name "trapuser"`** — Create the SNMPv3 user first with `net-snmp-create-v3-user -A <authpass> -X <privpass> -a SHA -x AES trapuser` before restarting snmpd.
    **`Job for snmpd.service failed because the control process exited with error code`** — Check `/var/log/snmpd.log` or run `snmpd -f -L s 6` to validate configuration syntax before restart.
### Cisco IOS

```bash
snmp-server enable traps
snmp-server host <nms-ip> version 2c <community>

# Specific trap types
snmp-server enable traps snmp linkdown linkup
snmp-server enable traps envmon
snmp-server enable traps bgp

# Verify
show snmp host
show snmp trap
```


```text title="Expected output"
snmp-server enable traps
snmp-server host 192.168.100.50 version 2c public

snmp-server enable traps snmp linkdown linkup
snmp-server enable traps envmon
snmp-server enable traps bgp

Trap Receivers:
Address          Community  Port  Version
192.168.100.50   public     162   2c

Enabled Trap Types:
snmp
  linkdown
  linkup
envmon
bgp
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the NMS IP address format is valid (e.g., 192.168.x.x) and that the community string contains no spaces or special characters.
    **`% Incomplete command.`** — Ensure you specify both the NMS IP address and community string; `snmp-server host` requires at least these two parameters.
    **`% Unknown SNMP trap type 'envmon'`** — Check device platform support; some devices use `snmp-server enable traps enviromental` or `snmp-server enable traps entity` instead of `envmon`.
### Arista EOS

```text
snmp-server host <nms-ip> version 2c <community>
snmp-server enable traps
show snmp host
```

### Brocade FOS

```bash
snmpconfig --set mibCapability
# Enable trap categories via prompts

snmpconfig --set snmpv1
# Set trap recipient IP and community

snmpconfig --show mibCapability
```


```text title="Expected output"
MIB capability configuration updated successfully.
Setting SNMPv1 parameters...
Enter trap recipient IP address: 192.168.1.50
Enter community string: public
SNMPv1 trap configuration applied.

MIB Capability Settings:
  System: enabled
  Interface: enabled
  IP: enabled
  TCP: enabled
  UDP: enabled
  ICMP: enabled
  Trap Categories: linkDown, linkUp, coldStart, warmStart, authenticationFailure
```

!!! warning "Common errors"
    **`snmpconfig: command not found`** — Verify SNMP tools are installed with `apt-get install snmp snmp-mibs-downloader` or equivalent for your distribution.
    **`Error: Unable to write configuration — Permission denied`** — Run the command with `sudo` or ensure your user has write access to `/etc/snmp/` configuration directories.
    **`Invalid IP address format`** — Enter the trap recipient IP in valid dotted-decimal notation (e.g., 192.168.1.50) without CIDR notation or hostnames.
## Testing Trap Delivery

```bash
# Send a test trap from Linux to NMS
snmptrap -v2c -c <community> <nms-ip> '' \
  1.3.6.1.6.3.1.1.5.3 \
  1.3.6.1.2.1.2.2.1.1.1 i 1

# Or use snmptrapd to listen and verify locally
snmptrapd -f -Lo -c /etc/snmp/snmptrapd.conf

# Check NMS received the trap
# → Zabbix: Monitoring → Latest Data → filter by host
# → Prometheus: check alertmanager log for SNMP trap receiver
```


```text title="Expected output"
0.0.0.0 [UDP: [127.0.0.1]:37821->[127.0.0.1]:162]:
DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (12345678) 1 day, 10:17:45.78
SNMPv2-MIB::snmpTrapOID.0 = OID: SNMPv2-SMI::enterprises.1.3.6.1.2.1.2.2.1.1.1
SNMPv2-SMI::enterprises.1.3.6.1.2.1.2.2.1.1.1 = INTEGER: 1

Listening at UDP: [0.0.0.0]:162
```

!!! warning "Common errors"
    **`snmptrap: Unknown host "<nms-ip>"`** — Replace `<nms-ip>` with a valid IP address or resolvable hostname (e.g., `192.168.1.100`).
    **`snmptrapd: Error opening specified endpoint "UDP: [0.0.0.0]:162"`** — Ensure snmptrapd is not already running on port 162 and that you have root/sudo privileges to bind to port 162.
    **`snmptrap: No response from <nms-ip>:162`** — Verify the NMS host is reachable, the SNMP community string matches the NMS configuration, and firewall rules allow UDP 162 inbound.
## Common Trap OIDs

| Trap | OID |
|---|---|
| Link Down | 1.3.6.1.6.3.1.1.5.3 |
| Link Up | 1.3.6.1.6.3.1.1.5.4 |
| Cold Start | 1.3.6.1.6.3.1.1.5.1 |
| Warm Start | 1.3.6.1.6.3.1.1.5.2 |
| Authentication Failure | 1.3.6.1.6.3.1.1.5.5 |

## Trap Receiver — snmptrapd

```bash
# /etc/snmp/snmptrapd.conf
authCommunity log,execute,net <community>

# Log all traps
logOption f /var/log/snmptrapd.log

# Forward to syslog
traphandle default /usr/sbin/snmptrapd-handler

systemctl enable --now snmptrapd
```


```text title="Expected output"
Created symlink /etc/systemd/system/multi-user.target.wants/snmptrapd.service → /usr/lib/systemd/system/snmptrapd.service.
(no output — command completes silently)
```

!!! warning "Common errors"
    **`error: [NET FAILURE] Unknown host name`** — Verify the SNMP trap source hostname/IP is resolvable; add it to `/etc/hosts` or ensure DNS is configured correctly.
    **`error opening specified logfile /var/log/snmptrapd.log: Permission denied`** — Create the log file with proper permissions: `touch /var/log/snmptrapd.log && chmod 644 /var/log/snmptrapd.log && chown snmp:snmp /var/log/snmptrapd.log`.
## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| No traps received at NMS | Destination IP/port wrong or UDP 162 blocked | `tcpdump -i any udp port 162` at NMS |
| Traps arrive but NMS ignores | Community mismatch | Verify community on device matches NMS config |
| Trap storm | Device sending traps in a loop | Check device state; apply trap rate limiting |
| Inform not acknowledged | NMS not configured for informs | Check NMS SNMP inform handling |
