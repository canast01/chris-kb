---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
description: "NetApp Keystone Troubleshooting reference covering Common Issues, Diagnostic, Log Locations, Before Calling Support."
---
# NetApp Keystone Troubleshooting

<div class="kb-summary">
NetApp Keystone Troubleshooting reference covering Common Issues, Diagnostic, Log Locations, Before Calling Support.

*Applies to: Keystone STaaS*
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
common_issues: "Common Issues" {shape: rectangle}
diagnostic: "Diagnostic" {shape: rectangle}
log_locations: "Log Locations" {shape: rectangle}
before_calling_support: "Before Calling Support" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> common_issues: investigate
symptom -> diagnostic: investigate
symptom -> log_locations: investigate
symptom -> before_calling_support: investigate
symptom -> verify_resolution: investigate
common_issues -> resolution
diagnostic -> resolution
log_locations -> resolution
before_calling_support -> resolution
verify_resolution -> resolution
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Keystone Collector not reporting telemetry | Collector service stopped, network blocked to NetApp endpoint, or Collector credentials expired | Check `systemctl status keystone-collector`; review Collector logs; verify outbound HTTPS to `keystone.netapp.com`; refresh credentials via Collector TUI |
| Burst charges higher than expected | Recent volume provisioning added capacity to a committed tier without a review; snapshot growth consuming tier capacity | Review BlueXP Keystone dashboard; identify which tier is bursting; review recent provisioning and snapshot schedules; decommission unused volumes before month-end |
| Performance below SLA (latency or IOPS) | Workload exceeds the IOPS/TB ceiling for the assigned service level; underlying array under-provisioned | Review QoS statistics with `qos statistics performance show`; raise with Keystone Success Manager — NetApp manages the platform and must remediate infrastructure-level performance issues |
| Capacity not provisioning / headroom exhausted | Committed capacity for the service tier is fully consumed; burst limit reached | Check committed capacity headroom in BlueXP; contact Keystone Success Manager for emergency capacity amendment |
| BlueXP dashboard showing stale data | Keystone Collector connectivity issue; Collector stopped reporting | Check Collector service status; verify network path to NetApp endpoint; restart Collector service if stopped |
| Billing discrepancy | Collector reported burst that was not anticipated; billing period lag | Download consumption report from BlueXP digital wallet; reconcile against provisioned capacity per tier; raise a Keystone support case if data appears incorrect |
| Volume at wrong service level | AQoS policy-group not applied or wrong policy-group assigned at provisioning | Run `volume show -fields qos-policy-group`; use `volume modify -qos-policy-group <correct-psl>`; notify NetApp KSM to review billing impact |

## Diagnostic

```bash
# Check Keystone Collector service status (on Collector VM)
sudo systemctl status keystone-collector

# View Collector logs for reporting errors
sudo journalctl -u keystone-collector -n 100

# Test connectivity from Collector VM to NetApp endpoint
curl -v https://keystone.netapp.com

# On ONTAP — verify AQoS policy-groups assigned to Keystone volumes
volume show -fields qos-policy-group

# Review QoS performance statistics
qos statistics performance show

# Check ONTAP cluster capacity
volume show -fields size,used,percent-used
```


```text title="Expected output"
● keystone-collector.service - NetApp Keystone Collector
     Loaded: loaded (/etc/systemd/system/keystone-collector.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2 days ago
   Main PID: 8742 (keystone-collec)
      Tasks: 12 (limit: 4915)
     Memory: 287.4M
        CPU: 2h 14m 32s
     CGroup: /system.slice/keystone-collector.service
             └─8742 /opt/keystone/bin/keystone-collector --config /etc/keystone/collector.conf

Jan 15 14:32:18 ks-collector-01 systemd[1]: Started NetApp Keystone Collector.
Jan 15 14:32:25 ks-collector-01 keystone-collector[8742]: INFO: Collector initialized, version 5.2.1
Jan 15 14:32:26 ks-collector-01 keystone-collector[8742]: INFO: Connected to ONTAP cluster prod-cluster-01
Jan 15 14:33:01 ks-collector-01 keystone-collector[8742]: INFO: Metrics collected: 1247 datapoints
Jan 15 14:45:12 ks-collector-01 keystone-collector[8742]: WARNING: API response time 2847ms (threshold: 2000ms)

*   Trying 192.0.2.45:443...
* Connected to keystone.netapp.com (192.0.2.45) port 443 (#0)
* TLSv1.3 (OUT), TLS handshake, Client hello (1)
* TLSv1.3 (IN), TLS handshake, Server hello (1)
* TLSv1.3 (IN), TLS handshake, Certificate (4)
* TLSv1.3 (IN), TLS handshake, Finished (5)
* TLSv1.3 (OUT), TLS handshake, Finished (5)
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate: CN=keystone.netapp.com, O=NetApp Inc., C=US
< HTTP/1.1 200 OK

Vserver   Volume                QoS Policy Group
--------- -------------------- --------------------
prod-svm  keystone_vol_01       ks-gold-tier
prod-svm  keystone_vol_02       ks-silver-tier
prod-svm  keystone_vol_03       ks-gold-tier
prod-svm  keystone_vol_04       ks-bronze-tier

Policy Group          Workload Type    Throughput (ops/s)    Latency (ms)
------------------- --------------- -------------------- --------------------
ks-gold-tier        Mixed            8742                 1.2
ks-silver-tier      Mixed            4521                 2.8
ks-bronze-tier      Mixed            1203                 5.4

Vserver   Volume                Size       Used        Percent Used
--------- -------------------- ---------- ----------- -----------
```
Review the BlueXP Keystone dashboard for capacity consumption, burst status, and SLA compliance — most customer-visible issues are diagnosable from the dashboard without ONTAP CLI access.

## Log Locations

- **Keystone Collector logs** — on the Collector VM at `/var/log/keystone-collector/` or via `journalctl -u keystone-collector`
- **ONTAP EMS log** — `event log show -severity error` on the ONTAP cluster
- **BlueXP portal** — consumption history, burst events, and SLA compliance reports at https://activeiq.netapp.com
- **NetApp-managed platform logs** — accessible to NetApp SRE only; request via support case if platform-level diagnostics are needed

## Before Calling Support

Gather the following before opening a Keystone support case:

- Keystone subscription ID (from BlueXP portal)
- Keystone Collector version (`sudo keystone-collector --version`)
- Screenshot of the BlueXP Keystone dashboard showing the issue
- Collector VM status output (`systemctl status keystone-collector`)
- Consumption report for the affected period (download from BlueXP digital wallet)
- Clear description of the symptom and its business impact

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Architecture](../architecture/)
- [Cli Reference](../cli-reference/)
- [Design Standards](../design-standards/)
- [Integration](../integration/)
- [Learning Path](../learning-path/)
- [Lifecycle](../lifecycle/)
- [Operations](../operations/)
- [Scripts](../scripts/)
- [Security](../security/)
- [Service Levels](../service-levels/)
- [Usage Reporting](../usage-reporting/)
- [Vendor Support](../vendor-support/)
- [NetApp Keystone — Overview](../)
