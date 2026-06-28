---
tags:
  - scenarios
  - vmware
  - vxrail
---
# VxRail LCM Upgrade Failure

<div class="kb-summary">
VxRail LCM upgrades are an all-or-nothing validated bundle: ESXi, vSAN, vCenter, drivers, and firmware
must all upgrade together. A failure at any phase can leave nodes partially upgraded or the cluster in
a mixed-version state. This scenario covers identifying the failure stage, resolving the most common
pre-check failures, handling mid-upgrade node failures, and safely retrying after root cause is fixed.

*Applies to: vSphere 7.x / 8.x*
</div>

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

Look for: the specific pre-check name that failed. Common failures and fixes:

**vSAN health not green:** Navigate to **Cluster → Monitor → vSAN → Skyline Health** and resolve all
red or yellow items. LCM will not proceed with any vSAN health warning outstanding.

**Host stuck in maintenance mode:** A host manually put into maintenance mode blocks LCM. Exit maintenance mode in vCenter and retry.

**Unsupported customisation — non-LCM VIBs:** Check for VIBs installed outside of VxRail LCM:

```bash
esxcli software vib list | grep -v "VMware\|Dell\|Broadcom\|QLogic"
```

Remove any VIBs not in the VxRail approved list before retrying.

**NTP skew:** Check and fix NTP on all nodes — see the
[NTP Drift Scenario](ntp-drift-sso-certificate/index.md) for the full procedure. Re-run the
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

```bash
curl -k -u mystic:<password> \
  -X POST \
  https://<vxm-ip>/rest/vxm/v1/system/support-bundle
```

Check current cluster and node versions:

```bash
curl -k -u mystic:<password> \
  https://<vxm-ip>/rest/vxm/v1/hosts | python3 -m json.tool
```

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

- [vCenter Down / Unreachable](vcenter-down/index.md) — if the VxRail LCM bundle includes a vCenter
  upgrade that fails, the vCenter recovery procedure applies.
- [PSOD — ESXi Kernel Panic](psod-esxi-kernel-panic/index.md) — a PSOD after an LCM upgrade often
  indicates a driver/firmware combination issue within the bundle; open a Dell support case.
- [NTP Drift Causing SSO or Certificate Errors](ntp-drift-sso-certificate/index.md) — NTP skew
  is one of the pre-check failures that blocks LCM from starting the upgrade sequence.
