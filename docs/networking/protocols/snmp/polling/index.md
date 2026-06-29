---
tags:
  - networking
---
# SNMP Polling

<div class="kb-summary">
SNMP polling is the process of an NMS periodically querying devices to collect metrics.
</div>

Unlike traps, polling is initiated by the manager on a schedule.

```d2
direction: down

poll_operations: "Poll Operations" {shape: rectangle}
common_cli_polling_commands: "Common CLI Polling Commands" {shape: rectangle}
common_oids_for_polling: "Common OIDs for Polling" {shape: rectangle}
polling_intervals: "Polling Intervals" {shape: rectangle}
zabbix_snmp_polling_config: "Zabbix SNMP Polling Config" {shape: rectangle}
prometheus_snmp_exporter: "Prometheus + SNMP Exporter" {shape: rectangle}

poll_operations -> common_cli_polling_commands: uses
common_cli_polling_commands -> common_oids_for_polling: uses
common_oids_for_polling -> polling_intervals: uses
polling_intervals -> zabbix_snmp_polling_config: uses
zabbix_snmp_polling_config -> prometheus_snmp_exporter: uses
```

## Poll Operations

| Operation | Version | Description |
|---|---|---|
| `GET` | v1, v2c, v3 | Retrieve a single OID value |
| `GETNEXT` | v1, v2c, v3 | Retrieve next OID in MIB tree |
| `GETBULK` | v2c, v3 | Retrieve multiple OIDs in one request (efficient for tables) |
| `SET` | v1, v2c, v3 | Write a value to a device (requires RW community) |

## Common CLI Polling Commands

```bash
# Single OID — system description
snmpget -v2c -c <community> <device-ip> sysDescr.0

# Walk a MIB subtree
snmpwalk -v2c -c <community> <device-ip> system
snmpwalk -v2c -c <community> <device-ip> interfaces
snmpwalk -v2c -c <community> <device-ip> ifTable

# Bulk walk (faster for large MIBs)
snmpbulkwalk -v2c -c <community> -Cn0 -Cr25 <device-ip> ifTable

# Translate OID to human-readable name
snmptranslate -On .1.3.6.1.2.1.1.1.0        # numeric → name
snmptranslate .1.3.6.1.2.1.1.1.0            # OID info
snmptranslate -Td sysDescr                  # detailed MIB info
```


```text title="Expected output"
SNMPv2-MIB::sysDescr.0 = STRING: "Cisco IOS Software, C2960X Software, Version 15.2(4)E10, RELEASE SOFTWARE"

SNMPv2-MIB::sysDescr.0 = STRING: "Device Description"
SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.9.9.46.1
SNMPv2-MIB::sysUpTime.0 = Timeticks: (487291840) 56 days, 8:08:08.00
SNMPv2-MIB::sysContact.0 = STRING: "admin@example.com"
SNMPv2-MIB::sysName.0 = STRING: "switch-core-01"
SNMPv2-MIB::sysLocation.0 = STRING: "Data Center 2, Rack A12"

IF-MIB::ifNumber.0 = INTEGER: 52
IF-MIB::ifIndex.1 = INTEGER: 1
IF-MIB::ifDescr.1 = STRING: "GigabitEthernet0/1"
IF-MIB::ifType.1 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifMtu.1 = INTEGER: 1500
IF-MIB::ifSpeed.1 = Gauge32: 1000000000
...

IF-MIB::ifIndex.48 = INTEGER: 48
IF-MIB::ifDescr.48 = STRING: "GigabitEthernet0/48"

SNMPv2-MIB::sysDescr.0 = STRING: "Cisco IOS Software"
SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.9.9.46.1
SNMPv2-MIB::sysUpTime.0 = Timeticks: (487291840) 56 days, 8:08:08.00
...

.1.3.6.1.2.1.1.1.0
SNMPv2-MIB::sysDescr.0

sysDescr OBJECT-TYPE
    SYNTAX      DisplayString (SIZE (0..255))
    MAX-ACCESS  read-only
    STATUS      current
    DESCRIPTION "A textual description of the entity."
```

!!! warning "Common errors"
    **`snmpget: Unknown host (192.0.2.1)`** — Verify the device IP address is reachable and correct; check network connectivity with `ping <device-ip>`.
    **`Timeout: No Response from 192.0.2.1`** — Confirm the SNMP community string is correct and SNMP is enabled on the device; check firewall rules allowing UDP 161.
    **`snmptranslate: Unknown Object Identifier ".1.3.6.1.2.1.1.1.0"`** — Load the appropriate MIB file using `snmptranslate -m +<MIB-NAME>` or ensure MIB files are installed in `/usr/share/snmp/mibs/`.
## Common OIDs for Polling

| OID | Name | Metric |
|---|---|---|
| `1.3.6.1.2.1.1.1.0` | sysDescr | Device description |
| `1.3.6.1.2.1.1.3.0` | sysUpTime | Uptime (hundredths of a second) |
| `1.3.6.1.2.1.1.5.0` | sysName | Device hostname |
| `1.3.6.1.2.1.2.1.0` | ifNumber | Number of interfaces |
| `1.3.6.1.2.1.2.2.1.10` | ifInOctets | Interface inbound bytes (counter) |
| `1.3.6.1.2.1.2.2.1.16` | ifOutOctets | Interface outbound bytes (counter) |
| `1.3.6.1.2.1.2.2.1.8` | ifOperStatus | Interface operational status (1=up, 2=down) |
| `1.3.6.1.4.1.9.9.109.1.1.1.1.3` | Cisco CPU utilisation | CPU % (Cisco) |
| `1.3.6.1.4.1.2021.10.1.3.1` | UCD-SNMP 1-min load | CPU load (Linux) |
| `1.3.6.1.4.1.2021.4.6.0` | memAvailReal | Available memory (Linux) |

## Polling Intervals

| Data type | Recommended interval | Why |
|---|---|---|
| Interface counters | 60–300s | Counters roll fast on 10/100G links |
| CPU/memory | 60–120s | Trend useful; sub-minute polling creates load |
| Interface status (up/down) | 30–60s | Quick detection of link events |
| Environmental (temp, PSU) | 300s | Changes slowly |
| Uptime | 300–600s | Only for reboot detection |

## Zabbix SNMP Polling Config

```yaml
# Zabbix item config (SNMP interface)
Type: SNMP agent
Key: ifOperStatus[{#SNMPINDEX}]
SNMP OID: .1.3.6.1.2.1.2.2.1.8.{#SNMPINDEX}
Update interval: 60s
```

## Prometheus + SNMP Exporter

```yaml
# snmp_exporter/snmp.yml — generator config snippet
modules:
  cisco_ios:
    walk:
      - 1.3.6.1.2.1.2.2          # interfaces
      - 1.3.6.1.2.1.31.1.1       # ifXTable
    metrics:
      - name: ifOperStatus
        oid:  1.3.6.1.2.1.2.2.1.8
        type: gauge

# prometheus.yml scrape config
scrape_configs:
  - job_name: snmp
    static_configs:
      - targets: [<device-ip>]
    metrics_path: /snmp
    params:
      module: [cisco_ios]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - target_label: __address__
        replacement: <snmp-exporter-host>:9116
```

## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| `Timeout: No Response` | Community wrong or UDP 161 blocked | `snmpget` manually; `tcpdump` on device |
| Counter resets | Interface or device reboot | Normal — NMS should handle counter wraps |
| Slow poll / timeouts | Device CPU overloaded by SNMP | Increase poll interval; use GETBULK |
| OID not found | MIB not supported by device | Check with `snmpwalk`; use vendor MIB file |
