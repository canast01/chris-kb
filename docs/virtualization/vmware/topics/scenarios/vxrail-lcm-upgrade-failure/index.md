# VxRail LCM Upgrade Failure

<div class="kb-summary">
VxRail LCM upgrades are an all-or-nothing validated bundle: ESXi, vSAN, vCenter, drivers, and firmware
must all upgrade together. A failure at any phase can leave nodes partially upgraded or the cluster in
a mixed-version state. This scenario covers identifying the failure stage, resolving the most common
pre-check failures, handling mid-upgrade node failures, and safely retrying after root cause is fixed.
</div>

```text
┌──────────────────────────── VxRail LCM Upgrade — Failure Decision Flow ────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   │  START: VxRail Manager → LCM → Upgrade shows failure; identify phase from Upgrade History      │  │
│   └──────────────────────────────────────────┬──────────────────────────────────────────────────────┘ │
│                                              │                                                        │
│   ┌──────────────────────────────────────────▼──────────────────────────────────────────────────────┐ │
│   │   What phase failed?                                                                            │ │
│   └───────────┬─────────────────────┬────────────────────────┬───────────────────────────┬─────────┘  │
│               │                     │                        │                           │            │
│               ▼                     ▼                        ▼                           ▼            │
│   ┌───────────────────┐  ┌──────────────────┐   ┌───────────────────────┐  ┌──────────────────────┐   │
│   │   Pre-check       │  │   Download       │   │   ESXi / firmware     │  │   Post-upgrade       │   │
│   │   Fix underlying  │  │   Proxy / net    │   │   upgrade on node     │  │   validation         │   │
│   │   health issue    │  │   issue; re-dl   │   │   Check iDRAC + logs  │  │   Check cluster      │   │
│   │   then retry      │  │                  │   │                       │  │   health; resync     │   │
│   └───────────────────┘  └──────────────────┘   └───────────────────────┘  └──────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   │  Root cause fixed → VxRail Manager → LCM → Retry Upgrade (continues from failed node)         │   │
│   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Open VxRail Manager UI and navigate to **LCM → Upgrade History**. The history entry shows which node
failed and at which phase:

| Phase | What it does | Common failures |
|---|---|---|
| Pre-check | Validates cluster health before any change | vSAN health, NTP skew, unsupported VIBs, host state |
| Download | Downloads the upgrade bundle from Dell or local repository | Proxy misconfiguration, bandwidth, certificate errors |
| Pre-upgrade validation | Re-validates immediately before touching the first node | vSAN resync still in progress |
| ESXi upgrade | Installs new ESXi build on each node in sequence | Boot failure, VIB conflict, maintenance mode stuck |
| Firmware update | iDRAC applies firmware within the bundle | Firmware package validation failure, iDRAC connectivity |
| Post-upgrade validation | Confirms all components are at target version | Version mismatch, service not started |

Note the failure phase and which node was being processed. This determines the investigation path.

---

## 2. Pre-check Failures

Pre-checks run before any change is made and are the safest failure mode — the cluster is unmodified.
Check each failure category in the LCM log:

```bash
ssh mystic@<vxm-ip>
tail -100 /var/log/mystic/lcm.log | grep -iE "pre-check|precheck|ERROR|FAIL"
```

Common pre-check failures and their fixes:

**vSAN health not green:** Navigate to **Cluster → Monitor → vSAN → Skyline Health** and resolve all
red or yellow items. The most common blocking items are disk capacity imbalance, component rebuild in
progress, and network health warnings. LCM will not proceed with any vSAN health warning outstanding.

**Host not in correct state:** Check for any host stuck in maintenance mode in vCenter. A host that was
manually put into maintenance mode and never exited blocks LCM. Exit maintenance mode and retry.

**Unsupported customisation — non-LCM VIBs:** Check for VIBs installed outside of VxRail LCM:

```bash
esxcli software vib list | grep -v "VMware\|Dell\|Broadcom\|QLogic"
```

Remove any VIBs not in the VxRail approved list before retrying.

**NTP skew:** Check and fix NTP on all nodes — see the
[NTP Drift Scenario](../ntp-drift-sso-certificate/index.md) for the full procedure. Re-run the
pre-check after NTP is corrected.

---

## 3. Bundle Download Failure

If the bundle download fails, check:

- **Proxy settings:** VxRail Manager → **Settings → Proxy**. If a proxy is required in the environment,
  confirm the proxy address and credentials are correct and that the proxy allows HTTPS to
  `downloads.dell.com` and VMware download endpoints.
- **Manual bundle upload:** Download the bundle from Dell support portal on a machine with internet
  access and upload it directly to VxRail Manager via the **LCM → Upload Bundle** option.

After resolving the download issue, retry the upgrade — VxRail Manager resumes from the download phase.

---

## 4. Mid-Upgrade Node Failure

If a node fails during the ESXi upgrade or firmware update phase, the cluster is in a mixed-version
state. Do not reboot other nodes or attempt manual changes.

Check the failed node's iDRAC for firmware update status and hardware events:

- iDRAC → **System Event Log** — look for firmware update failures or hardware events during the
  upgrade window.
- iDRAC → **Job Queue** — confirm whether the firmware job completed, failed, or is still queued.

Check ESXi installation logs on the affected host if it is accessible:

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

Query VxRail Manager REST API for current upgrade status:

```bash
curl -k -u mystic:<password> \
  https://<vxm-ip>/rest/vxm/v1/lcm/upgrade/bundle/status
```

Generate a support bundle for submission to Dell support:

```bash
curl -k -u mystic:<password> \
  -X POST \
  https://<vxm-ip>/rest/vxm/v1/system/support-bundle
```

The support bundle includes LCM logs, cluster health snapshots, iDRAC data, and vSAN status at the
time of failure. Dell support requires this bundle before proceeding with escalation.

Check current cluster and VxRail node versions:

```bash
curl -k -u mystic:<password> \
  https://<vxm-ip>/rest/vxm/v1/hosts | python3 -m json.tool
```

---

## 6. Rollback and Re-image Considerations

VxRail LCM does not provide a rollback option for a partially completed upgrade. If a node fails
mid-upgrade and LCM's automatic recovery also fails:

1. **Do not manually reinstall ESXi on the node.** Contact Dell support first. A Dell-guided
   re-image procedure maintains the node's VxRail identity and allows LCM to re-adopt it.
2. **Collect the LCM support bundle before any re-image.** The bundle is required for root cause
   analysis and warranty support.
3. **The cluster continues operating on remaining nodes** while the failed node is offline, provided
   vSAN can maintain object redundancy with the remaining nodes.

---

## 7. Retry After Root Cause Is Fixed

Once the root cause is resolved, use the Retry function in VxRail Manager:

**VxRail Manager → LCM → [current upgrade] → Retry Upgrade**

The retry does not restart the upgrade from scratch. It resumes from the failed node and phase,
applying the bundle to nodes that were not yet upgraded. This is safe to use after any pre-check
failure or after a single-node mid-upgrade failure is resolved.

Verify before retrying:

- vSAN health is green (all items)
- All hosts show "Connected" in vCenter
- No hosts are in manual maintenance mode
- NTP is synchronised on all nodes
- vSAN resync queue is empty (no pending resyncs from the partial upgrade)

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

- [vCenter Down / Unreachable](../vcenter-down/index.md) — if the VxRail LCM bundle includes a vCenter
  upgrade that fails, the vCenter recovery procedure applies.
- [PSOD — ESXi Kernel Panic](../psod-esxi-kernel-panic/index.md) — a PSOD after an LCM upgrade often
  indicates a driver/firmware combination issue within the bundle; open a Dell support case.
- [NTP Drift Causing SSO or Certificate Errors](../ntp-drift-sso-certificate/index.md) — NTP skew
  is one of the pre-check failures that blocks LCM from starting the upgrade sequence.
