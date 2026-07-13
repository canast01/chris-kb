---
tags:
  - netapp
  - operations
description: "Common Issues reference covering Keystone Collector Not Reporting, Subscription Consumption Shows Unexpected Spike, SnapMirror Lag Alert, Collector VM..."
---
# NetApp Keystone — Common Issues

<div class="kb-summary">
Common Issues reference covering Keystone Collector Not Reporting, Subscription Consumption Shows Unexpected Spike, SnapMirror Lag Alert, Collector VM Cannot Reach ONTAP Array, Keystone Portal Shows Wrong Committed Capacity and 1 more sections.

*Applies to: Keystone STaaS*
</div>
![NetApp Keystone — Common Issues](../../../../../assets/storage-netapp-keystone-operations-common-issues.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Keystone Collector Not Reporting

**Symptom:** Keystone portal shows arrays as "not reporting" or last collection timestamp is stale.

**Checks:**

```bash
# On Collector VM
keystone-collector status
keystone-collector show-last-collection

# Check network connectivity to Keystone cloud endpoints
curl -I https://keystone.netapp.com
curl -I https://api.keystone.netapp.com

# Check Collector logs
journalctl -u keystone-collector --since "1 hour ago"
```


```text title="Expected output"
Collector Status: RUNNING
Last Collection: 2024-01-15 14:32:18 UTC (successful)
Collection Duration: 2m 34s
Data Points Collected: 1,247
Next Collection: 2024-01-15 15:32:18 UTC

HTTP/1.1 200 OK
Server: nginx
Content-Type: application/json
Connection: keep-alive

HTTP/1.1 200 OK
Server: nginx
Content-Type: application/json
Connection: keep-alive

Jan 15 14:32:45 collector-vm keystone-collector[2847]: Collection cycle started
Jan 15 14:33:12 collector-vm keystone-collector[2847]: Connected to ONTAP cluster: prod-cluster-01
Jan 15 14:34:18 collector-vm keystone-collector[2847]: Data transmission to api.keystone.netapp.com completed
Jan 15 14:34:19 collector-vm keystone-collector[2847]: Collection cycle completed successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to keystone.netapp.com port 443: Connection timed out` | Verify network connectivity and firewall rules allow outbound HTTPS to NetApp Keystone endpoints. |
    | `Collector Status: STOPPED` | Restart the collector service with `systemctl restart keystone-collector` and check for configuration errors in `/etc/keystone-collector/config.yaml`. |
    | `Collection cycle failed: Authentication error - Invalid API credentials` | Verify the Keystone API credentials are correctly configured in the collector's authentication file and have not expired. |
**Resolution:**

1. Confirm outbound HTTPS (443) is allowed from Collector VM to NetApp cloud endpoints
2. Re-validate configuration: `keystone-config validate`
3. Force a collection: `keystone-collector collect --force`
4. If still failing, restart the service: `systemctl restart keystone-collector`

---

## Subscription Consumption Shows Unexpected Spike

**Symptom:** Keystone portal reports a sudden jump in consumed TiB not explained by provisioning.

**Checks:**

```bash
# On ONTAP — check which volumes grew
volume show -vserver <keystone-svm> -fields size,used,percent-used | sort -k3 -r

# Check for large snapshot accumulation
volume snapshot show -vserver <keystone-svm> -fields size

# Check for new qtrees or volumes provisioned without Keystone awareness
volume show -vserver <keystone-svm>
qtree show -vserver <keystone-svm>
```


```text title="Expected output"
Vserver                 Volume       Size       Used       Percent-Used
-------                 ------       ----       ---        ----
keystone-svm            vol_prod_01  2.5TB      2.1TB      84%
keystone-svm            vol_prod_02  1.8TB      1.4TB      78%
keystone-svm            vol_data_03  900GB      650GB      72%
keystone-svm            vol_archive  500GB      485GB      97%
keystone-svm            vol_temp     300GB      45GB       15%

Vserver                 Volume       Snapshot Name        Size
-------                 ------       ---------------      ----
keystone-svm            vol_prod_01  hourly.2024-01-15   180GB
keystone-svm            vol_prod_01  hourly.2024-01-14   175GB
keystone-svm            vol_prod_02  daily.2024-01-10    220GB
keystone-svm            vol_data_03  weekly.2024-01-08   95GB
...

Vserver     Volume              Aggregate  State  Type  Size
-------     ------              ---------  -----  ----  ----
keystone-svm vol_prod_01        aggr_01    online RW    2.5TB
keystone-svm vol_prod_02        aggr_01    online RW    1.8TB
keystone-svm vol_data_03        aggr_02    online RW    900GB
keystone-svm vol_archive        aggr_02    online RW    500GB
keystone-svm vol_temp           aggr_01    online RW    300GB

Vserver     Volume  Qtree        Style
-------     ------  -----        -----
keystone-svm vol_prod_01 qtree_finance unix
keystone-svm vol_prod_01 qtree_hr     unix
keystone-svm vol_prod_02 qtree_ops    mixed
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: command failed: permission denied for "volume show"` | Verify the ONTAP user account has cluster-admin or appropriate SVM-admin role assigned. |
    | `Error: Vserver "<keystone-svm>" does not exist` | Confirm the SVM name is correct and exists on the cluster using `vserver show`. |
**Common causes:** Snapshot accumulation from a missed cleanup job; a bulk data ingest; a new volume provisioned directly on the SVM outside of Keystone portal workflow.

---

## SnapMirror Lag Alert

**Symptom:** Keystone portal or ONTAP reports replication lag on a Keystone-backed SnapMirror relationship.

```bash
# Check SnapMirror relationship status
snapmirror show -vserver <svm> -fields state,lag-time,health

# Re-sync if relationship is broken
snapmirror resync -source-path <src> -destination-path <dst>

# Update immediately
snapmirror update -destination-path <dst>
```


```text title="Expected output"
Vserver: svm-prod-01
                                            Source Path: cluster1://vol_source
                                       Destination Path: cluster2://vol_dest
                                              Relation Type: XDP
                                          Lag Time: 00:00:15
                                          Mirror State: Snapmirrored
                                          Relationship Status: Idle
                                          Health Status: Healthy

Transfer in progress: false
Last Transfer Size: 2.1GB
Last Transfer Duration: 00:03:42
Network Compression Ratio: 1.2:1

(no output — command completes silently)

Transfer started on Mon Nov 20 14:32:18 UTC
Transfer in progress: true
Last Transfer Size: 856MB
Last Transfer Duration: 00:01:29
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: command failed: No SnapMirror relationship found for destination path "cluster2://vol_dest"` | Verify the destination path is correct and the relationship exists with `snapmirror show`. |
    | `Error: command failed: Snapmirror relationship is in "broken-off" state and cannot be resynced` | Release the broken relationship on the destination with `snapmirror release -relationship-info-only` before attempting resync. |
---

## Collector VM Cannot Reach ONTAP Array

**Symptom:** `keystone-collector list-arrays` shows an array as unreachable.

```bash
# Test from Collector VM
ping <ontap-mgmt-ip>
curl -sk -u admin:<pass> https://<ontap-mgmt-ip>/api/cluster | jq .name

# Check ONTAP management LIF status
network interface show -role cluster-mgmt
```


```text title="Expected output"
PING 192.168.1.50 (192.168.1.50) 56(84) bytes of data.
64 bytes from 192.168.1.50: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.1.50: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 192.168.1.50: icmp_seq=3 ttl=64 time=2.12 ms
--- 192.168.1.50 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 1.89/2.11/2.34/0.19 ms

"cluster-01"

Vserver     Interface       Address         Status
----------- --------------- --------------- ----------
cluster-01  cluster-mgmt    192.168.1.50    up
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to 192.168.1.50 port 443: Connection refused` | Verify the ONTAP management IP is correct and the HTTPS service is running on the cluster with `system services web show`. |
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to curl to skip SSL verification, or import the ONTAP cluster certificate into your Collector VM's certificate store. |
    | `Error: command not found` | Run the network interface command directly on the ONTAP cluster via SSH, not from the Collector VM; use `ssh admin@<ontap-mgmt-ip> "network interface show -role cluster-mgmt"` instead. |
**Resolution:** Confirm ONTAP management LIF is up, firewall rules allow 443 from Collector VM, and credentials stored in Collector config are current.

---

## Keystone Portal Shows Wrong Committed Capacity

**Symptom:** Portal committed TiB doesn't match the signed order.

**Action:** Open a support case with NetApp referencing subscription number. The committed values are provisioned by NetApp — they cannot be self-corrected.

---

## Quick Reference — Error Patterns

| Symptom | First Check |
|---|---|
| Stale last-collection timestamp | `keystone-collector status` + outbound 443 |
| Consumption spike | Snapshot accumulation on SVM |
| SnapMirror lag | `snapmirror show -fields lag-time,health` |
| Array unreachable | ONTAP mgmt LIF + firewall |
| Wrong committed capacity | NetApp support ticket |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [NetApp Keystone — Operations: Backup & Restore](backup-restore.md)
- [NetApp Keystone — Operations: CLI Reference](cli-reference.md)
- [Keystone — Health Checks](health-checks.md)
- [NetApp Keystone — Operations](index.md)
- [Keystone — Architecture](../../architecture/)
- [NetApp Keystone Security](../../security/)
- [NetApp Keystone Troubleshooting](../../troubleshooting/)
