---
tags:
  - operations
  - vmware
  - vxrail
description: "VxRail LCM upgrade workflow from bundle download through post-upgrade validation. Covers obtaining and uploading the bundle, running pre-upgrade checks..."
---
# VxRail — Install & Upgrade

<div class="kb-summary">
VxRail LCM upgrade workflow from bundle download through post-upgrade validation. Covers obtaining and uploading the bundle, running pre-upgrade checks, the node-by-node upgrade sequence, monitoring progress, and a common LCM failure reference table.

*Applies to: VxRail 7.x / 8.x*
</div>
![VxRail — Install & Upgrade](../../../../../assets/virtualization-vmware-vxrail-operations-install-upgrade.svg)

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

!!! warning "Host enters maintenance mode"
    ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. Confirm DRS is Fully Automated and HA admission control is satisfied before starting.

## LCM Pre-Upgrade Checklist

Complete this checklist before initiating any VxRail LCM upgrade. LCM will run its own pre-check, but these manual verifications catch issues that may not surface in the automated check.

- [ ] vSAN health is all green — `esxcli vsan health cluster get`
- [ ] vSAN resync bytes = 0 — `esxcli vsan debug resync list`
- [ ] All VxRail nodes Online in VxRail Plugin
- [ ] vCenter and VxRail Manager are reachable and not reporting alarms
- [ ] Change window approved; storage and application teams notified
- [ ] VxRail Manager VM backup taken (Veeam or equivalent — not just a snapshot)
- [ ] VxRail Manager VM snapshot taken immediately before upgrade (temporary safety net — remove within 24h)
- [ ] vCenter file-based backup current (VAMI: `https://<vcenter>:5480`)
- [ ] Target bundle compatibility confirmed against Dell VxRail Software Compatibility Matrix
- [ ] DRS is configured to **Fully Automated** — VMs must migrate automatically during node maintenance
- [ ] Sufficient cluster capacity to run all VMs on N-1 nodes during upgrade

---

## Step 1 — Obtain the Upgrade Bundle

Download the VxRail Upgrade Bundle from Dell's support portal:

```text
https://www.dell.com/support
→ Product Support
→ Search for your VxRail serial or model
→ Drivers & Downloads
→ Filter: VxRail Manager Upgrade Bundle
```

The bundle is a single signed `.bin` file, typically 5–20 GB depending on the target version. Verify the SHA256 checksum after download:

```bash
# Verify bundle integrity (Linux/macOS)
sha256sum VxRail-7.0.401-bundle.bin

# Windows PowerShell
Get-FileHash -Algorithm SHA256 VxRail-7.0.401-bundle.bin
```


```text title="Expected output"
VxRail-7.0.401-bundle.bin: OK
a3f7e2c9d1b4f8e6a2c5d9e1f3b7a4c6d8e0f1a2b3c4d5e6f7a8b9c0d1e2f3

(PowerShell output on Windows)
Algorithm       : SHA256
Hash            : A3F7E2C9D1B4F8E6A2C5D9E1F3B7A4C6D8E0F1A2B3C4D5E6F7A8B9C0D1E2F3
Path            : C:\Downloads\VxRail-7.0.401-bundle.bin
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sha256sum: VxRail-7.0.401-bundle.bin: No such file or directory` | Verify the bundle file exists in the current directory using `ls -la` and navigate to the correct path. |
    | `Get-FileHash : Cannot find path 'C:\Downloads\VxRail-7.0.401-bundle.bin' because it does not exist.` | Check the file path and ensure the bundle has been downloaded completely to the specified directory. |
Compare the hash against the value shown on the Dell support page.

---

## Step 2 — Upload the Bundle

**Option A: VxRail Plugin (recommended for interactive uploads)**

In vCenter: **VxRail Plugin → Lifecycle Management → Upload Bundle → Browse**

Select the `.bin` file. Upload time depends on storage and network — allow 15–60 minutes for large bundles.

**Option B: VxRail Manager API (for automation or CLI preference)**

```bash
# Upload via multipart POST to VxRail Manager
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -F "file=@/tmp/VxRail-7.0.401-bundle.bin" \
  "https://<vxm-ip>/rest/vxm/v1/lcm/bundle"
```


```text title="Expected output"
% Total    % Received % Xferd  Average Speed   Time    Current
                                 Dload  Upload   Total   Spent    Left Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--:--
100  2847M  100  2847M    0     0  18.5M      0 --:--:-- 153s --:--:-- --:--:--
{"bundle_id":"b7f2c9e1-4a3d-11ed-9e2a-0050569b8d4e","status":"UPLOADING","progress":100,"message":"Bundle uploaded successfully"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip SSL verification (already present in example; if error persists, verify the VxM hostname matches the certificate CN). |
    | `curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused` | Confirm the VxM IP address is correct and the VxRail Manager REST API service is running with `systemctl status vxrail-rest-api`. |
    | `{"error":"Invalid credentials","code":401}` | Verify the base64-encoded credentials are correct by decoding with `echo 'bXlzdGljOnBhc3N3b3Jk' | base64 -d` and confirm the VxM admin username and password. |
**Verify the bundle is listed after upload:**

```bash
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/lcm/upgrade" | python3 -m json.tool
```


```text title="Expected output"
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "READY",
  "currentVersion": "7.0.510",
  "targetVersion": "7.0.520",
  "estimatedDuration": 3600,
  "components": [
    {
      "name": "vxrail-manager",
      "currentVersion": "7.0.510",
      "targetVersion": "7.0.520",
      "status": "PENDING"
    },
    {
      "name": "vcenter",
      "currentVersion": "7.0.200",
      "targetVersion": "7.0.210",
      "status": "PENDING"
    },
    {
      "name": "esxi",
      "currentVersion": "7.0.1",
      "targetVersion": "7.0.2",
      "status": "PENDING"
    }
  ],
  "lastUpgradeTime": "2024-01-15T08:30:00Z",
  "nextScheduledUpgrade": null
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip SSL verification (already present in the example, but ensure it's not removed). |
    | `Authorization header missing or invalid` | Verify the base64-encoded credentials are correct by testing `echo -n 'mystic:password' | base64` separately and confirm the VXM API user has proper permissions. |
    | `curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused` | Confirm the VXM IP address is correct, reachable from your network, and the VXM appliance is running and has completed initialization. |
---

## Step 3 — Run Pre-Upgrade Checks

**VxRail Plugin: Lifecycle Management → Pre-Check → Run Pre-Check**

The pre-check validates:

- Cluster health is green (all nodes reachable)
- No active vSAN resync
- Bundle version is compatible with the current cluster version
- vCenter credentials stored in VxRail Manager are valid
- All nodes are at the expected current version (no partial upgrades)
- Sufficient disk space on VxRail Manager for the upgrade process

```bash
# Check pre-check results via API
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/lcm/precheck/status" | python3 -m json.tool
```


```text title="Expected output"
{
  "id": "precheck-2024-01-15-08:32:14",
  "status": "COMPLETED",
  "startTime": "2024-01-15T08:32:14.000Z",
  "endTime": "2024-01-15T08:45:22.000Z",
  "overallStatus": "PASSED",
  "checkResults": [
    {
      "checkName": "Disk Space Validation",
      "status": "PASSED",
      "message": "All nodes have sufficient disk space"
    },
    {
      "checkName": "Network Connectivity",
      "status": "PASSED",
      "message": "All cluster nodes are reachable"
    },
    {
      "checkName": "vSAN Health",
      "status": "PASSED",
      "message": "vSAN cluster is healthy"
    },
    {
      "checkName": "License Compliance",
      "status": "WARNING",
      "message": "License expiration in 45 days"
    }
  ],
  "nodeDetails": [
    {
      "nodeId": "node-1",
      "hostname": "esx-vxrail-01.lab.local",
      "status": "READY"
    },
    {
      "nodeId": "node-2",
      "hostname": "esx-vxrail-02.lab.local",
      "status": "READY"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification (already present in example, but ensure it's included if removed). |
    | `curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused` | Verify the VXM IP address is correct and the VXM appliance is running and accessible on the network. |
    | `jq: parse error: Invalid JSON at line 1` | Ensure the API endpoint is correct and the VXM service is responding; check VXM logs if the endpoint returns HTML error pages instead of JSON. |
**Do not proceed if any pre-check item shows FAILED.** Resolve the listed issue and re-run the pre-check.

---

## Step 4 — Run the Upgrade

**VxRail Plugin: Lifecycle Management → Upgrade → Start Upgrade**

Confirm the target bundle version and click **Start**.

The LCM upgrades the cluster node by node:

1. **Node enters maintenance mode** — DRS migrates all VMs to other nodes; vSAN evacuates data objects
2. **ESXi and firmware updates applied** — BIOS, iDRAC, NIC, HBA, and disk controller firmware updated first, then ESXi patched
3. **Node reboots** — may reboot multiple times if multiple firmware updates are staged
4. **Node exits maintenance mode** — rejoins the vSphere cluster
5. **vSAN resyncs** — LCM waits until vSAN resync bytes = 0 before moving to the next node

After all nodes are done, VxRail Manager and vCenter Server are upgraded (order may vary by bundle version).

**Estimated duration:** 30–120 minutes per node. A 4-node cluster typically takes 3–6 hours total.

---

## Step 5 — Monitor Progress

**VxRail Plugin: Lifecycle Management → Upgrade Status**

Or poll via API:

```bash
# Poll LCM upgrade job status (run repeatedly)
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/lcm/upgrade" | python3 -m json.tool
```


```text title="Expected output"
{
  "id": "upgrade-job-12847",
  "status": "IN_PROGRESS",
  "progress": 65,
  "currentStep": "Upgrading vSAN cluster",
  "startTime": "2024-01-15T08:32:14Z",
  "estimatedTimeRemaining": 1847,
  "nodes": [
    {
      "hostname": "vxrail-node-01.lab.local",
      "status": "COMPLETED",
      "version": "8.0.210"
    },
    {
      "hostname": "vxrail-node-02.lab.local",
      "status": "IN_PROGRESS",
      "version": "8.0.210"
    },
    {
      "hostname": "vxrail-node-03.lab.local",
      "status": "PENDING",
      "version": "7.0.510"
    }
  ],
  "warnings": [],
  "errors": []
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip SSL verification (already present in the example, but ensure it's not removed). |
    | `curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused` | Verify the VXM IP address is correct and the VXM management interface is reachable on port 443. |
    | `jq: parse error: Invalid JSON at line 1` | Ensure the VXM API is responding with valid JSON; check authentication credentials and that the endpoint is accessible. |
Key fields in the API response:

| Field | Meaning |
|---|---|
| `state` | `IN_PROGRESS`, `COMPLETED`, `FAILED`, `PAUSED` |
| `percent_complete` | Overall progress percentage |
| `current_host` | Node currently being upgraded |
| `error_message` | Set if state is FAILED |

During upgrade, also watch:

- vCenter Tasks panel for maintenance mode events
- vSAN resync: `esxcli vsan debug resync list` from any remaining node

---

## Step 6 — Post-Upgrade Validation

Run these checks as soon as the LCM job reports COMPLETED:

```powershell
# Verify all nodes are at the expected ESXi version and build
Get-VMHost | Select-Object Name,
    @{N="Version"; E={$_.Version}},
    @{N="Build"; E={$_.Build}} |
  Sort-Object Name | Format-Table -AutoSize

# Verify vSAN health is green
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" |
  Select-Object OverallHealth, OverallHealthDescription

# Check for any policy compliance issues post-upgrade
Get-VM | Get-SpbmEntityConfiguration |
  Select-Object Entity, StoragePolicy, ComplianceStatus |
  Where-Object {$_.ComplianceStatus -ne "compliant"} |
  Format-Table -AutoSize
```

```bash
# Verify VxRail Manager version via API
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/system" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('VxRail Version:', d.get('version','?'))
print('Build Number:  ', d.get('build_number','?'))
"

# Check iDRAC firmware version on each node
racadm getversion -f idrac
racadm getversion -f bios
```


```text title="Expected output"
VxRail Version: 7.0.510
Build Number:   7.0.510-26.0.11248.1

iDRAC Version: 6.10.40.00
BIOS Version: 2.14.3 (Release Date: 04/15/2024)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip SSL verification, or import the VxRail Manager's certificate into your system's trusted store. |
    | `bash: racadm: command not found` | Install Dell OMECLI tools or run this command directly on the iDRAC host; `racadm` is not available on VxRail Manager nodes. |
    | `Authorization header invalid or credentials incorrect` | Verify the base64-encoded credentials are correct by testing `echo -n 'mystic:password' | base64` and confirm the VxRail Manager user has API access permissions. |
Post-upgrade checklist:

- [ ] All nodes Online in VxRail Plugin
- [ ] vSAN health all green, resync = 0
- [ ] ESXi version matches the target bundle version (consistent across all nodes)
- [ ] VxRail Manager version matches the target bundle version
- [ ] No new vCenter alarms
- [ ] VMs running normally and accessible
- [ ] iDRAC FW version matches expected (verify against bundle release notes)
- [ ] Pre-LCM snapshot of VxRail Manager VM **deleted** (snapshots degrade vSAN performance)

---

## Common LCM Failure Table

| Failure | Cause | Resolution |
|---|---|---|
| Pre-check fails: vSAN health not green | vSAN disk or network issue | Fix vSAN health errors before retrying; check disk groups and network connectivity |
| Pre-check fails: resync bytes > 0 | vSAN rebuilding or rebalancing | Wait for resync to complete; do not force upgrade while resync is active |
| Pre-check fails: node unreachable | Node offline or management network issue | Bring node online; check iDRAC and management network connectivity |
| Pre-check fails: credential invalid | vCenter credentials in VxRail Manager are stale | Update vCenter credentials in VxRail Manager settings |
| Pre-check fails: bundle incompatible | Attempting a multi-hop upgrade (skipping versions) | Check Dell upgrade path requirements; may need intermediate upgrade first |
| Upload fails: insufficient disk space | VxRail Manager VM disk is full | Expand the VxRail Manager VM disk or remove old bundle files |
| Upgrade stuck: node in maintenance mode | vSAN evacuation taking too long (large data set) | Wait; if stuck > 4h check vSAN for degraded objects that can't evacuate |
| Upgrade fails mid-node: ESXi patch fails | Incompatible or corrupt bundle; disk failure | Check VxRail Manager logs; contact Dell support with support bundle |
| Upgrade fails: vCenter update fails | vCenter unreachable or disk full during update | Check vCenter VAMI; ensure vCenter has sufficient disk space |
| Post-upgrade: version mismatch on one node | Node was offline during upgrade | Re-run LCM upgrade — it will apply to the skipped node only |
| Post-upgrade: vSAN health warning persists | Rebuild in progress or clock skew | Wait for rebuild; check NTP on all nodes if warning is clock-related |

---

## See also

- [VxRail — Health Checks](../health-checks/)
- [VxRail — Common Issues](../../troubleshooting/common-issues/)
- [VxRail — Procedures](../procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
