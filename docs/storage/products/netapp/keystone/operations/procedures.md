---
tags:
  - netapp
  - operations
description: "NetApp Keystone procedures: burst capacity activation, storage tier changes, scheduled report export, and capacity rebalancing requests via NetApp support."
---
# Keystone — Procedures

<div class="kb-summary">
NetApp Keystone procedures: burst capacity activation, storage tier changes, scheduled report export, and capacity rebalancing requests via NetApp support.

*Applies to: Keystone STaaS*
</div>

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Verify Keystone Collector service is running | `systemctl status keystone-collector` | |
| [ ] Check last collection timestamp in collector logs | `journalctl -u keystone-collector -n 50 \| grep -i "collection\|reported\|error"` | |
| [ ] Open BlueXP → Digital Wallet → Keystone | | |
| [ ] Check burst usage | | flag if any service level is consuming burst > 10% above committed tier |
| [ ] Run `volume show -fields qos-policy-group` on the ONTAP cluster | `volume show -fields qos-policy-group` | confirm all Keystone volumes have an AQoS policy assigned |
| [ ] Check for unclassified volumes (missing or incorrect QoS policy group) | | |
| [ ] Review the Keystone Collector health dashboard in BlueXP for any collection errors | | |

## Health Check

- [ ] Collector service is active and not in a failed or activating loop
- [ ] Last successful telemetry report is within the expected collection interval (typically 1 hour)
- [ ] No collection errors in `/var/log/keystone-collector/` or systemd journal
- [ ] BlueXP Keystone dashboard reflects current capacity — data is not stale
- [ ] No service-level SLA breaches flagged (availability, latency, IOPS/TB)
- [ ] All volumes are assigned to the correct Keystone service-level AQoS policy group
- [ ] Burst usage is within acceptable range — not approaching the burst limit

```bash
# On the Keystone Collector VM — check collector service status
sudo systemctl status keystone-collector

# View recent collector logs for errors or collection timestamps
sudo journalctl -u keystone-collector -n 100

# Tail the collector log file directly
sudo tail -100 /var/log/keystone-collector/keystone-collector.log

# On the ONTAP cluster — verify AQoS policies exist for all Keystone service levels
qos policy-group show

# Check that all volumes have a Keystone AQoS policy group assigned
volume show -fields volume,svm,qos-policy-group

# Confirm ONTAP cluster is reachable from the Collector VM
curl -sk https://<cluster-mgmt-lif>/api/cluster | python3 -m json.tool
```


```text title="Expected output"
● keystone-collector.service - NetApp Keystone Collector Service
     Loaded: loaded (/etc/systemd/system/keystone-collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2 days ago
   Main PID: 2847 (python3)
     CGroup: /system.slice/keystone-collector.service
             └─2847 /usr/bin/python3 /opt/keystone-collector/collector.py

Jan 18 14:35:42 keystone-collector-01 keystone-collector[2847]: Collection cycle started for tenant_id=a7f3c9e1-2b4d-11ee-be56-0242ac120002
Jan 18 14:36:18 keystone-collector-01 keystone-collector[2847]: Successfully collected metrics from cluster prod-cluster-01
Jan 18 14:37:05 keystone-collector-01 keystone-collector[2847]: Uploaded 1247 capacity records to Keystone portal
Jan 18 14:38:12 keystone-collector-01 keystone-collector[2847]: Collection cycle completed in 156 seconds

Policy Group          VSERVER  Workload Type  Max Throughput
ks-gold              svm-prod  User Defined   10000 IOPS
ks-silver            svm-prod  User Defined   5000 IOPS
ks-bronze            svm-prod  User Defined   2000 IOPS
ks-standard          svm-dr    User Defined   3000 IOPS

Volume              SVM         QoS Policy Group
vol_prod_db01       svm-prod    ks-gold
vol_prod_app02      svm-prod    ks-silver
vol_prod_backup     svm-prod    ks-bronze
vol_dr_replica      svm-dr      ks-standard
...

{
  "version": {
    "full": "NetApp Release 9.13.1: 2e69f755"
  },
  "generation": 20230815,
  "cluster": {
    "uuid": "1cd8a442-86d1-11ee-ab7e-005056b34711",
    "name": "prod-cluster-01"
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag (already in the command) or import the cluster's CA certificate into the collector VM's trust store.
    **`qos policy-group show: command not found`** — Ensure you are logged into the ONTAP cluster CLI via SSH, not running the command on the collector VM.
    **`Connection refused` or `No route to host`** — Verify the cluster management LIF IP is correct and reachable from the collector VM using `ping` or `nc -zv <cluster-mgmt-lif> 443`.
## Change Readiness

- [ ] Keystone Collector is running and last reported telemetry within the expected interval
- [ ] Confirm the change is not scheduled immediately before the monthly billing close (avoid capacity spikes at billing cutover)
- [ ] All volumes involved in the change have correct AQoS policy-group assignments — verify before and after
- [ ] If adding new volumes, the target Keystone service level has sufficient committed capacity headroom
- [ ] If decommissioning volumes, confirm snapshot copies on those volumes are also being removed to avoid lingering capacity charges
- [ ] Collector configuration backup taken: copy `/etc/keystone-collector/` and current config before any Collector changes
- [ ] BlueXP dashboard reviewed for current consumed vs. committed — document baseline before change

| Item | Status | Notes |
|---|---|---|
| Collector reporting current telemetry | | |
| Change timed away from billing close | | |
| AQoS policy-group assignments verified | | |
| Target service level has capacity headroom | | |
| Baseline consumption documented in BlueXP | | |

## Maintenance Window

1. Record the current consumed capacity baseline from BlueXP Digital Wallet before starting
2. If performing Collector maintenance: stop the Collector with `systemctl stop keystone-collector`; complete changes; restart with `systemctl start keystone-collector`
3. For ONTAP cluster changes that affect Keystone-reported volumes: complete the ONTAP change following the standard ONTAP maintenance procedure
4. After ONTAP changes, verify AQoS policy-group assignments are still intact: `volume show -fields qos-policy-group`
5. Restart Keystone Collector if any ONTAP credentials or cluster management LIF changed: update the Collector configuration via the TUI first
6. Monitor Collector logs for the next collection cycle to confirm successful telemetry reporting
7. Validate the BlueXP Keystone dashboard reflects accurate consumption within one reporting cycle before closing the maintenance window

## Post-Change Validation

- [ ] Keystone Collector is running and not in an error state: `systemctl status keystone-collector`
- [ ] New collection timestamp visible in logs — telemetry resumed after the change
- [ ] BlueXP Keystone dashboard shows updated consumption data (not stale from before the change)
- [ ] All volumes — including any newly provisioned during the window — have correct AQoS policy-group assignments
- [ ] No unclassified volumes: `volume show -fields qos-policy-group` shows no blanks for Keystone volumes
- [ ] Consumed capacity in BlueXP is consistent with expected provisioned capacity post-change
- [ ] No unexpected burst activation triggered by the change

---

## Usage Reporting

### BlueXP Digital Wallet

![BlueXP Digital Wallet](../../../../../assets/keystone-proc-bluexp-digital-wallet.svg)

Primary source for Keystone consumption reporting:

1. Log in to **BlueXP** (console.bluexp.netapp.com)
2. Navigate to **Digital Wallet → Keystone Subscriptions**
3. Select your subscription to view:
   - Committed capacity per service level
   - Consumed (logical) capacity per service level
   - Burst usage and burst limits
   - Month-to-date consumption trend

### Monthly Consumption Reports

![Monthly Consumption Reports](../../../../../assets/keystone-proc-monthly-consumption-reports.svg)

- Reports are generated monthly by NetApp
- Available in BlueXP Keystone dashboard before invoice generation
- Review consumption report against committed capacity before month-end
- If burst consumption is unexpected, identify the source before the invoice is finalized

### Identifying High-Consuming Volumes (ONTAP CLI)

![Identifying High-Consuming Volumes (ONTAP CLI)](../../../../../assets/keystone-proc-identifying-high-consuming-volumes-ontap-cli.svg)

```bash
# List volumes sorted by used capacity
volume show -vserver * -fields size,used,percent-used | sort -k4 -nr

# Identify volumes in burst service levels
qos statistics volume show
```


```text title="Expected output"
Vserver         Volume                Size       Used        Percent-Used
-------         ------                ----       ---         ------------
svm-prod-01     vol_data_tier1        2.0TB      1.8TB       90%
svm-prod-01     vol_logs_archive      500GB      475GB       95%
svm-prod-02     vol_backup_secondary  1.5TB      1.2TB       80%
svm-dev-01      vol_test_workspace    750GB      620GB       83%
svm-prod-03     vol_snapshot_reserve  1.0TB      450GB       45%
...

Policy Group                 Volume              Throughput (MB/s)  Latency (ms)  Service Level
-----------                 ------              -----------------  -----------   -------------
qos_burst_premium            vol_data_tier1      850                 2.1          Burst
qos_standard                 vol_logs_archive    120                 5.3          Standard
qos_burst_standard           vol_backup_secondary 650               3.8          Burst
qos_standard                 vol_test_workspace  95                  6.2          Standard
qos_burst_premium            vol_snapshot_reserve 720               2.4          Burst
```

!!! warning "Common errors"
    **`Error: command not found: volume show`** — Ensure you are connected to the NetApp cluster management interface (SSH to the cluster IP) and not a local shell.
    **`Error: No matching Vserver found`** — Verify that Vservers exist on the cluster using `vserver show` and confirm the cluster is in healthy state.
### Reporting Discrepancies

![Reporting Discrepancies](../../../../../assets/keystone-proc-reporting-discrepancies.svg)

If the consumption report shows unexpected usage:

1. Compare ONTAP volume usage with Keystone report
2. Check for any large snapshots or recently provisioned volumes
3. Engage the Keystone Success Manager via the BlueXP support portal
4. Discrepancies must be raised before the invoice is finalized

---

## Request a Capacity Increase

1. Log in to the Keystone portal (or BlueXP Digital Wallet if your subscription is managed there)
2. Navigate to **Subscriptions** and select the relevant subscription
3. Click **Request Capacity Increase**
4. Specify the additional committed TiB required per service tier (Extreme, Performance, or Standard)
5. Submit the request — Dell/NetApp provisions the additional capacity within the contracted SLA window
6. Monitor the request status in the portal and confirm the new committed capacity is reflected in the dashboard once provisioned

---

## Generate a Consumption Report

1. Log in to the Keystone portal
2. Navigate to **Reporting → Consumption**
3. Select the desired date range for the report
4. Click **Export CSV** to download the consumption data
5. Share the exported report with the finance team for chargeback or showback processing
6. Review the report for any burst usage — identify the volumes or service levels driving burst before sharing with finance

---

## Raise a Keystone Service Ticket

1. Log in to the Keystone portal
2. Navigate to **Support → New Case**
3. Select the service affected (storage service level, Keystone Collector, billing discrepancy, etc.)
4. Describe the issue clearly — include subscription ID, affected service level, and any relevant timestamps or error messages
5. Submit the case — the NetApp Keystone team will respond according to the contracted SLA for the reported severity level
6. Monitor case progress in the portal and provide additional information if requested by the support team

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Keystone — Health Checks](../health-checks/)
- [Keystone — CLI Reference](../cli-reference/)
