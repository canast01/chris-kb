---
tags:
  - scenarios
  - vmware
  - vxrail
description: "VxRail LCM upgrades are an all-or-nothing validated bundle: ESXi, vSAN, vCenter, drivers, and firmware must all upgrade together. A failure at any phase..."
---
# VxRail LCM Upgrade Failure

<div class="kb-summary">
VxRail LCM upgrades are an all-or-nothing validated bundle: ESXi, vSAN, vCenter, drivers, and firmware
must all upgrade together. A failure at any phase can leave nodes partially upgraded or the cluster in
a mixed-version state. This scenario covers identifying the failure stage, resolving the most common
pre-check failures, handling mid-upgrade node failures, and safely retrying after root cause is fixed.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_identify_the_failure_phase: "1. Identify the Failure Phase" {shape: rectangle}
2_precheck_failures: "2. Pre-check Failures" {shape: rectangle}
3_bundle_download_failure: "3. Bundle Download Failure" {shape: rectangle}
4_midupgrade_node_failure: "4. Mid-Upgrade Node Failure" {shape: rectangle}
5_use_rest_api_to_check_status_and_g: "5. Use REST API to Check Status and Generate\nSupport Bundle" {shape: rectangle}

products_involved -> 1_identify_the_failure_phase: uses
1_identify_the_failure_phase -> 2_precheck_failures: uses
2_precheck_failures -> 3_bundle_download_failure: uses
3_bundle_download_failure -> 4_midupgrade_node_failure: uses
4_midupgrade_node_failure -> 5_use_rest_api_to_check_status_and_g: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| VxRail Manager | LCM engine; orchestrates the entire upgrade sequence; holds upgrade history and logs |
| vCenter | Cluster state and DRS/HA must be healthy before and during upgrade; upgraded as part of bundle |
| ESXi | Target of the upgrade on each node; must enter and exit maintenance mode cleanly |
| vSAN | Health must be green before upgrade starts; resync must complete between nodes |
| iDRAC | Firmware update within LCM bundle; hardware event log for mid-upgrade node failures |

---

## 1. Identify the Failure Phase

Open VxRail Manager → **LCM → Upgrade History** and identify which node failed and at which phase.

| Phase | What it does | Common failures |
|---|---|---|
| Pre-check | Validates cluster health before any change | vSAN health, NTP skew, unsupported VIBs, host state |
| Download | Downloads the upgrade bundle from Dell or local repository | Proxy misconfiguration, bandwidth, certificate errors |
| Pre-upgrade validation | Re-validates immediately before touching the first node | vSAN resync still in progress |
| ESXi upgrade | Installs new ESXi build on each node in sequence | Boot failure, VIB conflict, maintenance mode stuck |
| Firmware update | iDRAC applies firmware within the bundle | Firmware package validation failure, iDRAC connectivity |
| Post-upgrade validation | Confirms all components are at target version | Version mismatch, service not started |

Note the failure phase and which node was being processed — this determines the investigation path.

---

## 2. Pre-check Failures

Pre-checks run before any change is made — the cluster is unmodified and safe to investigate.

```bash
ssh mystic@<vxm-ip>
tail -100 /var/log/mystic/lcm.log | grep -iE "pre-check|precheck|ERROR|FAIL"
```


```text title="Expected output"
Last login: Wed Mar 15 14:22:18 2024 from 10.45.32.18
[mystic@vxm-prod-01 ~]$ tail -100 /var/log/mystic/lcm.log | grep -iE "pre-check|precheck|ERROR|FAIL"
2024-03-15 14:18:32.445 [INFO] Starting pre-check validation for cluster upgrade
2024-03-15 14:18:45.221 [INFO] Pre-check: Validating vSAN health status
2024-03-15 14:18:47.892 [INFO] Pre-check: Checking ESXi host connectivity (8/8 hosts online)
2024-03-15 14:18:52.334 [INFO] Pre-check: Verifying storage capacity (1.2TB available, 340GB required)
2024-03-15 14:19:01.556 [INFO] Pre-check: Validating network configuration
2024-03-15 14:19:15.778 [INFO] Pre-check validation completed successfully
2024-03-15 14:19:22.445 [INFO] Beginning LCM upgrade sequence for vSAN 7.0.3 → 8.0.1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,gssapi-keyexchange)` | Verify SSH key is loaded with `ssh-add` or use password authentication with `ssh -o PubkeyAuthentication=no mystic@<vxm-ip>`. |
    | `tail: cannot open '/var/log/mystic/lcm.log' for reading: No such file or directory` | Confirm the VXM appliance is fully initialized and check the correct log path with `find /var/log -name "*lcm*" -type f`. |
Look for: the specific pre-check name that failed. Common failures and fixes:

**vSAN health not green:** Navigate to **Cluster → Monitor → vSAN → Skyline Health** and resolve all
red or yellow items. LCM will not proceed with any vSAN health warning outstanding.

**Host stuck in maintenance mode:** A host manually put into maintenance mode blocks LCM. Exit maintenance mode in vCenter and retry.

**Unsupported customisation — non-LCM VIBs:** Check for VIBs installed outside of VxRail LCM:

```bash
esxcli software vib list | grep -v "VMware\|Dell\|Broadcom\|QLogic"
```


```text title="Expected output"
esx-ui                                    1.45.0-20567896                VMware    CommunitySupported
lsi-mr3                                   7.714.06.00-1OEM.700.1.0.15160174  VMware    CommunitySupported
net-bnx2                                  2.2.5k-1OEM.700.1.0.15160174       VMware    CommunitySupported
scsi-megaraid-sas                         7.714.06.00-1OEM.700.1.0.15160174  VMware    CommunitySupported
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: (standard input): Permission denied` | Run the command with `sudo` or as root: `sudo esxcli software vib list | grep -v "VMware\|Dell\|Broadcom\|QLogic"` |
    | `esxcli: command not found` | Ensure you are running this command on an ESXi host directly (SSH session) or via vSphere CLI; this command does not work on vCenter Server. |
Remove any VIBs not in the VxRail approved list before retrying.

**NTP skew:** Check and fix NTP on all nodes — see the
[NTP Drift Scenario](ntp-drift-sso-certificate.md) for the full procedure. Re-run the
pre-check after NTP is corrected.

---

## 3. Bundle Download Failure

If the bundle download fails, check proxy and connectivity settings before retrying.

- **Proxy settings:** VxRail Manager → **Settings → Proxy**. Confirm the proxy address and credentials are correct and that the proxy allows HTTPS to `downloads.dell.com` and VMware download endpoints.
- **Manual bundle upload:** Download the bundle from Dell support portal and upload directly to VxRail Manager via **LCM → Upload Bundle**.

After resolving the download issue, retry the upgrade — VxRail Manager resumes from the download phase.

---

## 4. Mid-Upgrade Node Failure

If a node fails during the ESXi upgrade or firmware update phase, the cluster is in a mixed-version state — do not reboot other nodes or attempt manual changes.

Check the failed node's iDRAC for firmware update status:

- iDRAC → **System Event Log** — look for firmware update failures or hardware events during the upgrade window.
- iDRAC → **Job Queue** — confirm whether the firmware job completed, failed, or is still queued.

Check ESXi installation logs on the affected host if accessible:

```bash
cat /var/log/esxi_install.log | tail -50
```


```text title="Expected output"
2024-01-15T09:42:33Z [INFO] ESXi 8.0.1 installation started on host esx-prod-04.datacenter.local
2024-01-15T09:42:45Z [INFO] Detected hardware: Dell PowerEdge R750, 2x Intel Xeon Platinum 8380
2024-01-15T09:43:12Z [INFO] Network configuration: VLAN 100, IP 192.168.1.45/24, Gateway 192.168.1.1
2024-01-15T09:44:28Z [INFO] Storage detected: 4x 1.2TB SAS drives, 2x 960GB NVMe
2024-01-15T09:45:01Z [INFO] Partitioning disk /dev/sda with GPT layout
2024-01-15T09:46:15Z [INFO] Installing ESXi boot loader to /dev/sda1
2024-01-15T09:52:33Z [INFO] Copying system files to /dev/sda2 (progress: 87%)
2024-01-15T10:01:44Z [INFO] Configuring management network on vmnic0
2024-01-15T10:02:19Z [INFO] Setting hostname to esx-prod-04.datacenter.local
2024-01-15T10:03:05Z [INFO] Installation completed successfully
2024-01-15T10:03:22Z [INFO] System will reboot in 30 seconds
2024-01-15T10:03:52Z [INFO] Reboot initiated
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: /var/log/esxi_install.log: No such file or directory` | The log file only exists during active installation; check `/var/log/vmkernel.log` or `/var/log/hostd.log` on a running ESXi host instead. |
    | `tail: cannot open '/var/log/esxi_install.log' for reading: Permission denied` | Run the command with `ssh root@<esxi-host>` or execute it directly on the ESXi console with appropriate root privileges. |
Look for:

```text
Installation failed: Conflict with existing VIB  → manual VIB present that blocks the upgrade VIB
Device not supported: <device-id>                → hardware not in the new bundle's HCL
Maintenance mode entry failed: timeout           → VM not evacuated before maintenance mode timeout
```

---

## 5. Use REST API to Check Status and Generate Support Bundle

Query VxRail Manager REST API for current upgrade status and generate a support bundle for Dell support.

```bash
curl -k -u mystic:<password> \
  https://<vxm-ip>/rest/vxm/v1/lcm/upgrade/bundle/status
```


```text title="Expected output"
{
  "id": "upgrade-bundle-20240115",
  "status": "READY",
  "version": "8.0.1",
  "buildNumber": "21493496",
  "releaseDate": "2024-01-15T00:00:00Z",
  "bundleSize": "2847563648",
  "checksum": "a7f3e9c2d1b4f8e6a9c3d5e7f1b3a5c7",
  "components": [
    {
      "name": "vxrail-manager",
      "version": "8.0.1",
      "status": "READY"
    },
    {
      "name": "vcenter-server",
      "version": "8.0.1",
      "status": "READY"
    }
  ],
  "lastChecked": "2024-01-16T14:32:18Z"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip SSL verification, or import the VXM's certificate into your system's CA bundle. |
    | `curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused` | Verify the VXM IP address is correct and the management interface is reachable on port 443 using `ping` or `nc -zv`. |
    | `{"error":"Unauthorized","code":401}` | Confirm the username and password are correct; use `curl -k -u mystic:$PASSWORD` with proper credential escaping if special characters are present. |
```bash
curl -k -u mystic:<password> \
  -X POST \
  https://<vxm-ip>/rest/vxm/v1/system/support-bundle
```


```text title="Expected output"
{
  "request_id": "req-8f4c2b91-7d3e-4a9e-b2f1-c5e8d9a1f6b3",
  "status": "INITIATED",
  "bundle_name": "vxm-support-bundle-20240115-143022.tar.gz",
  "estimated_size_mb": 2847,
  "location": "/var/log/vmware/vxm/bundles/vxm-support-bundle-20240115-143022.tar.gz",
  "created_at": "2024-01-15T14:30:22Z",
  "message": "Support bundle generation started. Check status with request_id."
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip certificate verification, or import the VXM's CA certificate into your system trust store. |
    | `curl: (401) Unauthorized` | Verify the username and password are correct; use `curl -u mystic:password` with the actual password or store credentials in `~/.netrc`. |
    | `curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused` | Confirm the VXM IP address is correct and the management interface is running; check network connectivity with `ping <vxm-ip>`. |
Check current cluster and node versions:

```bash
curl -k -u mystic:<password> \
  https://<vxm-ip>/rest/vxm/v1/hosts | python3 -m json.tool
```


```text title="Expected output"
{
  "hosts": [
    {
      "id": "host-42",
      "name": "esx-prod-01.datacenter.local",
      "ipAddress": "192.168.1.105",
      "version": "7.0.3",
      "status": "ONLINE",
      "cpuCount": 24,
      "memoryGB": 512
    },
    {
      "id": "host-43",
      "name": "esx-prod-02.datacenter.local",
      "ipAddress": "192.168.1.106",
      "version": "7.0.3",
      "status": "ONLINE",
      "cpuCount": 24,
      "memoryGB": 512
    },
    {
      "id": "host-44",
      "name": "esx-prod-03.datacenter.local",
      "ipAddress": "192.168.1.107",
      "version": "7.0.2",
      "status": "MAINTENANCE",
      "cpuCount": 16,
      "memoryGB": 256
    }
  ],
  "totalCount": 3
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused` | Verify the VXM appliance is running and the IP address is correct with `ping <vxm-ip>`. |
    | `curl: (60) SSL certificate problem: self signed certificate` | The `-k` flag should bypass this; if persisting, ensure you're using HTTPS and not HTTP. |
    | `jq: parse error: Invalid JSON at line 1` | Verify the API endpoint is correct and the VXM service is responding; check VXM logs with `ssh <vxm-ip> tail -f /var/log/vmware/vxm/vxm.log`. |
Look for: bundle status showing `FAILED` with a phase name; support bundle creation returning a bundle ID that you can download and attach to a Dell support case.

---

## 6. Rollback and Re-image Considerations

VxRail LCM does not provide a rollback option for a partially completed upgrade.

1. **Do not manually reinstall ESXi on the node.** Contact Dell support first — a Dell-guided re-image maintains the node's VxRail identity and allows LCM to re-adopt it.
2. **Collect the LCM support bundle before any re-image.** Required for root cause analysis and warranty support.
3. **The cluster continues operating on remaining nodes** provided vSAN can maintain object redundancy with the nodes still available.

---

## 7. Retry After Root Cause Is Fixed

Use the Retry function in VxRail Manager once the root cause is resolved.

**VxRail Manager → LCM → [current upgrade] → Retry Upgrade**

The retry resumes from the failed node and phase — it does not restart from scratch. Verify before retrying:

- vSAN health is green (all items)
- All hosts show "Connected" in vCenter
- No hosts are in manual maintenance mode
- NTP is synchronised on all nodes
- vSAN resync queue is empty (no pending resyncs from the partial upgrade)

---

## Key Terms

| Term | Definition |
|---|---|
| VxRail Manager | The Dell appliance management VM that runs the LCM engine, holds upgrade history and logs, and exposes the REST API used to trigger and monitor upgrades |
| LCM | Lifecycle Manager — the VxRail upgrade engine that orchestrates ESXi, vCenter, vSAN, driver, and firmware upgrades as a single validated bundle across all cluster nodes |
| Bundle | The versioned upgrade package distributed by Dell that contains specific validated versions of ESXi, vSAN, vCenter, drivers, and firmware for a given VxRail release |
| mystic | The service account used to SSH into VxRail Manager for log access and REST API authentication; primary account for LCM diagnostics |
| iDRAC | Integrated Dell Remote Access Controller — the out-of-band management interface on each VxRail node; used during LCM to apply firmware updates and accessible via the Job Queue to check firmware job status |
| OMIVV | OpenManage Integration for VMware vCenter — the Dell plugin for vCenter that manages VxRail inventory and firmware visibility; a PSOD after an OMIVV-triggered update indicates LCM bypass |
| Pre-check | The LCM phase that validates cluster health before any node is touched; the safest failure mode as no changes have been applied to the cluster |
| SupportAssist | Dell's automated support data collection service that can generate and upload diagnostic bundles directly to Dell; used alongside the VxRail REST API support bundle for escalation |
| VIB | vSphere Installation Bundle — the package format for ESXi drivers and components; non-LCM VIBs installed manually on VxRail nodes are a common pre-check failure that blocks upgrades |
| vSAN resync | The background process where vSAN rebuilds component redundancy after a node enters or exits maintenance mode; an active resync during LCM means reduced redundancy and risks data unavailability |
| REST API | The HTTP API exposed by VxRail Manager on port 443 at `/rest/vxm/v1/`; used to query upgrade status, trigger support bundle generation, and check node versions |
| VxRail Manager log path | Primary LCM log location: `/var/log/mystic/lcm.log` inside the VxRail Manager VM; contains phase-by-phase upgrade events, pre-check results, and error details |

---

## Common Mistakes

- **Retrying the upgrade before fixing the root cause.** LCM runs pre-checks again on retry. If the
  underlying issue is not fixed, the upgrade fails in the same place immediately. Read the log and
  fix the cause before clicking Retry.
- **Manually upgrading ESXi outside of VxRail LCM.** Installing an ESXi patch or driver directly
  using esxcli or vSphere Lifecycle Manager on a VxRail node places the node outside VxRail's
  validated bundle matrix. Future LCM upgrades may fail or require a re-image to recover.
- **Not waiting for vSAN resync to complete before starting the upgrade.** If a vSAN component resync
  is in progress when LCM begins, the cluster is already in a degraded redundancy state. Upgrading
  during resync means each node entering maintenance mode further reduces available redundancy and
  risks data unavailability.
- **Not having a vCenter file-based backup before upgrading.** If vCenter upgrade within the LCM
  bundle fails, a VAMI backup is the only recovery path without rebuilding vCenter from scratch.

---

## Related Scenarios

- [vCenter Down / Unreachable](vcenter-down.md) — if the VxRail LCM bundle includes a vCenter
  upgrade that fails, the vCenter recovery procedure applies.
- [PSOD — ESXi Kernel Panic](psod-esxi-kernel-panic.md) — a PSOD after an LCM upgrade often
  indicates a driver/firmware combination issue within the bundle; open a Dell support case.
- [NTP Drift Causing SSO or Certificate Errors](ntp-drift-sso-certificate.md) — NTP skew
  is one of the pre-check failures that blocks LCM from starting the upgrade sequence.
