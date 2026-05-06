# CSV Exports

> Part of the [Pure FlashArray CLI Reference](../).

---

## CSV Exports

Use `--csv` with `>` to create a new file or `>>` to append to an existing one. To run from a remote terminal:

```bash
ssh pureuser@<array_ip> "purevol list --csv" > local_file.csv
```

### Array & System

```bash
purearray list --csv > array_inventory.csv
purearray list --space --csv >> array_inventory.csv
purearray list --controller --csv >> array_inventory.csv
purearray list --ntpserver --csv >> array_inventory.csv
purearray list --syslogserver --csv >> array_inventory.csv
purearray monitor --csv >> array_performance.csv
purearray monitor --latency --csv >> array_performance.csv
purearray monitor --bandwidth --csv >> array_performance.csv
purearray monitor --iops --csv >> array_performance.csv
purearray monitor --size --csv >> array_performance.csv
purearray monitor --queue-depth --csv >> array_performance.csv
purearray list --connection-key --csv >> array_config.csv
purearray phonehome list --csv >> support_history.csv
purearray upgrade list --csv >> system_updates.csv
purearray list --banner --csv >> security_audit.csv
purearray list --console-lockout --csv >> security_audit.csv
purearray remoteassist --status --csv >> support_history.csv
```

### Volumes & Data

```bash
purevol list --csv > volume_report.csv
purevol list --all --csv >> volume_report.csv
purevol list --snap --csv >> volume_report.csv
purevol list --pending-only --csv >> volume_report.csv
purevol list --space --csv >> volume_report.csv
purevol list --obj-name --csv >> volume_report.csv
purevol list --shared --csv >> volume_report.csv
purevol list --snap --space --csv >> snapshot_usage.csv
purevol list --filter "size > 100G" --csv >> filtered_volumes.csv
purevol monitor --csv > volume_performance.csv
purevol monitor --historical 24h --csv >> volume_performance.csv
```

### Hosts & Connectivity

```bash
purehost list --csv > host_mapping.csv
purehost list --all --csv >> host_mapping.csv
purehost list --connect --csv >> active_connections.csv
purehost list --wwn --csv >> initiator_list.csv
purehost list --iqn --csv >> initiator_list.csv
purehost monitor --balance --csv > connectivity_health.csv
purehost monitor --bandwidth --csv >> host_performance.csv
purehost monitor --iops --csv >> host_performance.csv
purehgroup list --csv > group_mapping.csv
purehgroup list --host --csv >> group_mapping.csv
purehgroup list --space --csv >> group_mapping.csv
```

### Hardware & Health

```bash
purehw list --csv > hardware_health.csv
purehw list --type eth --csv >> hardware_health.csv
purehw list --type fc --csv >> hardware_health.csv
purehw list --type bay --csv >> hardware_health.csv
purehw list --type fan --csv >> hardware_health.csv
purehw list --type psu --csv >> hardware_health.csv
purehw list --type nvram --csv >> hardware_health.csv
purehw list --type sas --csv >> hardware_health.csv
puredrive list --csv > drive_inventory.csv
pureport list --csv > port_config.csv
pureport list --initiator --csv >> port_config.csv
```

### Admin & Security

```bash
pureadmin list --csv > admin_users.csv
pureadmin list --lockout --csv >> security_report.csv
pureadmin list --api-token --csv >> admin_users.csv
purealert list --csv > system_alerts.csv
purealert list --filter "state='open'" --csv >> critical_alerts.csv
pureaudit list --csv > audit_trail.csv
pureds list --csv > directory_services.csv
puredns list --csv >> network_config.csv
```
