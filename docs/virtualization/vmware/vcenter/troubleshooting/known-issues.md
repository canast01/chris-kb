---
tags:
  - troubleshooting
  - vcenter
  - vmware
  - known-issues
  - vsphere-8
---
# vCenter — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known vCenter / VCSA bugs, error codes, and workarounds. Each entry includes the affected version range, cause, and resolution or workaround status.

*Applies to: vSphere 7.x / 8.x*
</div>

## Before you begin

- Cross-reference VMware KB articles at `kb.vmware.com` using the KB ID listed below.
- Check VMware Release Notes for your specific build — patch releases often fix bugs silently.
- For STS certificate expiry issues (the most common root cause of login failures), see [Common Issues](common-issues.md).

## Authentication and SSO

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot connect to vCenter — certificate expired` | vSphere 6.7–8.0 | STS signing certificate expires after 2 years | Run `fixsts.sh` script (KB 76719) or manually reissue STS cert | Requires manual intervention — not patched automatically |
| `Error 503 — Service Unavailable` on vSphere Client login | vSphere 7.x | SSO token service down or Lookup Service unresponsive | Restart `vmware-stsd` and `vmware-rhttpproxy` via `service-control` | Varies by build |
| `Token validation failed` after AD domain password change | vSphere 7.x / 8.x | vCenter service account password expired in AD | Update AD account password in vCenter Identity Sources | N/A |
| PSC replication failure after network partition | External PSC deployments (6.7) | Topology split causing PSC sync lag | Run `dir-cli replication status`; force resync or converge to embedded PSC | 7.0 (embedded PSC mandatory) |

## Certificate Management

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VAMI certificate replacement fails with `STS health check failed` | vSphere 7.0.x | STS cert references old chain during replacement | Replace STS cert first (KB 2097936), then replace Machine/VMCA cert | 8.0 U2 |
| `Failed to push new certificate to hosts` | vSphere 7.x–8.x | ESXi host not in connected state during cert push | Reconnect disconnected hosts, retry certificate push | N/A |
| Self-signed certificate warning in browser after upgrade | All versions | Browser cached old cert fingerprint | Clear browser cache; install vCenter CA cert in OS trust store | N/A |

## Host Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| ESXi host shows `Not Responding` in vCenter after maintenance | vSphere 7.x | vpxa service crash on host | SSH to host: `service vpxa restart`; reconnect from vCenter | Varies |
| Host disconnects intermittently after 24–72 hours | vSphere 7.0 U1 | vpxa memory leak (KB 81830) | Apply patch 7.0 U2 or higher | 7.0 U2 |
| `Cannot synchronize host` after vCenter IP change | All | vCenter FQDN/IP change not propagated to vpxa | Re-register host with new vCenter address | N/A |

## Storage

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Datastore space alarm not clearing after freeing space | vSphere 7.x | Alarm state cached; stat collection lag | Reconfigure or manually reset the alarm | 8.0 |
| vSAN datastore not visible after VCSA restore from backup | vSphere 7.x | VCSA backup restores config but not vSAN cluster membership | Re-add hosts to vSAN cluster manually; cluster data intact | N/A |

## Upgrade and Migration

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VCSA upgrade fails at `Copying data` stage | 6.7 → 7.0 | Source VCSA disk performance too slow for time window | Run upgrade on lower-latency storage; increase timeout (KB 2143838) | N/A |
| Lifecycle Manager (vLCM) image import fails with `Hash mismatch` | vSphere 7.x | Partial download of VIB/ISO to depot | Re-download from Broadcom; clear LCM depot cache | N/A |

## Disk Space

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `/storage/log` partition full — services crash | All versions | Log rotation misconfigured or audit logging volume | Run `df -h` in VAMI shell; purge old logs; resize partition via VAMI if possible | N/A |
| `Database disk usage critical` alarm | vSphere 7.x | Stats retention defaults accumulate large DB | Reduce stats retention via vCenter Settings → Statistics; run `vacuum` on PostgreSQL | N/A |

## See also

- [vCenter — Common Issues](common-issues.md)
- [vCenter — Diagnostics](diagnostics.md)
- [VMware ESXi — Known Issues](../../esxi/troubleshooting/known-issues/)
- [VMware vSAN — Known Issues](../../vsan/troubleshooting/known-issues/)
