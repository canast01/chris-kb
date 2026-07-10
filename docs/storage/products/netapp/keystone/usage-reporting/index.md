---
tags:
  - netapp
---
# Keystone Usage Reporting

<div class="kb-summary">
Keystone Usage Reporting reference covering BlueXP Digital Wallet, Keystone Collector, Monthly Consumption Reports, Identifying High-Consuming Volumes (ONTAP CLI), Reporting Discrepancies and 1 more sections.

*Applies to: Keystone STaaS*
</div>

```d2
direction: down

bluexp_digital_wallet: "BlueXP Digital Wallet" {shape: rectangle}
keystone_collector: "Keystone Collector" {shape: rectangle}
monthly_consumption_reports: "Monthly Consumption Reports" {shape: rectangle}
identifying_highconsuming_volumes_on: "Identifying High-Consuming Volumes (ONTAP CLI)" {shape: rectangle}
reporting_discrepancies: "Reporting Discrepancies" {shape: rectangle}
key_metrics: "Key Metrics" {shape: rectangle}

bluexp_digital_wallet -> keystone_collector: uses
keystone_collector -> monthly_consumption_reports: uses
monthly_consumption_reports -> identifying_highconsuming_volumes_on: uses
identifying_highconsuming_volumes_on -> reporting_discrepancies: uses
reporting_discrepancies -> key_metrics: uses
```

## BlueXP Digital Wallet

Primary source for Keystone consumption reporting:

1. Log in to **BlueXP** (console.bluexp.netapp.com)
2. Navigate to **Digital Wallet → Keystone Subscriptions**
3. Select your subscription to view:
   - Committed capacity per service level
   - Consumed (logical) capacity per service level
   - Burst usage and burst limits
   - Month-to-date consumption trend

## Keystone Collector

The Keystone Collector is a virtual appliance deployed on-premises that collects and transmits consumption telemetry to NetApp:

```bash
# SSH to the Keystone Collector appliance
ssh admin@<collector_ip>

# Check collector service status
systemctl status keystone-collector

# View last collection run
journalctl -u keystone-collector --since "1 hour ago"
```


```text title="Expected output"
admin@collector-01.example.com's password: 
● keystone-collector.service - NetApp Keystone Collector
     Loaded: loaded (/etc/systemd/system/keystone-collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:18 UTC; 2h 45min ago
       Docs: https://docs.netapp.com/keystone/
    Process: 8421 ExecStart=/opt/keystone/bin/collector --config /etc/keystone/collector.conf (code=exited, status=0/SUCCESS)
   Main PID: 8422 (collector)
      Tasks: 12 (limit: 4096)
     Memory: 287.3M
        CPU: 2min 34.891s
     CGroup: /system.slice/keystone-collector.service
             └─8422 /opt/keystone/bin/collector --config /etc/keystone/collector.conf

Jan 17 14:32:18 collector-01 systemd[1]: Started NetApp Keystone Collector.
Jan 17 14:35:42 collector-01 keystone-collector[8422]: INFO: Collection cycle started for cluster ks-cluster-prod-01
Jan 17 14:36:15 collector-01 keystone-collector[8422]: INFO: Successfully collected metrics from 12 nodes
Jan 17 14:36:47 collector-01 keystone-collector[8422]: INFO: Usage data transmitted to Keystone portal (request_id: a7f2c9e1-4b8d-11ee-9c2a-0242ac120002)
Jan 17 14:37:22 collector-01 keystone-collector[8422]: INFO: Collection cycle completed successfully
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname <collector_ip>: Name or service not known`** — Replace `<collector_ip>` with the actual IP address or FQDN of your Keystone Collector appliance.
    **`Unit keystone-collector.service could not be found.`** — Verify the collector service is installed by running `dpkg -l | grep keystone` or `rpm -qa | grep keystone` and reinstall if necessary.
    **`Failed to get unit file state for keystone-collector.service: Connection refused`** — Ensure systemd is running and you have sudo/root privileges; try `sudo systemctl status keystone-collector` instead.
If the collector is offline, NetApp cannot generate accurate invoices — restore connectivity promptly.

## Monthly Consumption Reports

- Reports are generated monthly by NetApp
- Available in BlueXP Keystone dashboard before invoice generation
- Review consumption report against committed capacity before month-end
- If burst consumption is unexpected, identify the source before the invoice is finalized

## Identifying High-Consuming Volumes (ONTAP CLI)

```bash
# List volumes sorted by used capacity
volume show -vserver * -fields size,used,percent-used | sort -k4 -nr

# Identify volumes in burst service levels
qos statistics volume show
```


```text title="Expected output"
Vserver         Volume          Size       Used       Percent-Used
-------         ------          ----       ---        ------------
svm-prod-01     vol_data_tier1  10.0TB     8.7TB      87%
svm-prod-01     vol_logs        5.0TB      4.2TB      84%
svm-prod-02     vol_backup      20.0TB     15.3TB     76%
svm-dev-01      vol_test        2.0TB      1.1TB      55%
svm-prod-01     vol_archive     50.0TB     22.5TB     45%
...

Policy Group                Volume          Throughput(MB/s)  Latency(ms)
------------                ------          ----------------  -----------
qos_burst_premium            vol_data_tier1  450.2             2.1
qos_standard                 vol_logs        120.5             5.3
qos_burst_premium            vol_backup      380.1             3.7
qos_standard                 vol_test        45.3              8.9
```

!!! warning "Common errors"
    **`Error: command not found: volume show`** — Ensure you are connected to the NetApp cluster via SSH or the ONTAP CLI, not a local shell.
    **`Error: No matching volumes found`** — Verify the vserver exists and contains volumes by running `vserver show` first.
## Reporting Discrepancies

If the consumption report shows unexpected usage:

1. Compare ONTAP volume usage with Keystone report
2. Check for any large snapshots or recently provisioned volumes
3. Engage the Keystone Success Manager via the BlueXP support portal
4. Discrepancies must be raised before the invoice is finalized

## Key Metrics

| Metric | Where to Find | Normal |
|---|---|---|
| Committed capacity | BlueXP Digital Wallet | Contractual baseline |
| Burst usage | BlueXP Digital Wallet | 0 (or expected seasonal) |
| Collector health | Collector appliance status | Running, no errors |
| Telemetry latency | Last collection timestamp | Within last 24 hours |
