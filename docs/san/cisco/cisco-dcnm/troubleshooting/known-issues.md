---
tags:
  - troubleshooting
  - cisco-dcnm
  - san
  - known-issues
---
# Cisco DCNM — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Cisco DCNM (Data Center Network Manager) bugs, error codes, and workarounds covering switch discovery, deployment, and licensing.

*Applies to: Cisco DCNM 11.x / NDFC 12.x*
</div>

## Before you begin

- DCNM errors appear in the DCNM Dashboard → Alarms.
- DCNM → Administration → Logs for service-level diagnostics.
- Most discovery failures are SSH or SNMP connectivity issues.

## Switch Discovery

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot discover switch — SSH timeout` | DCNM 11.x | TCP 22 blocked from DCNM to switch management IP | Verify TCP 22 from DCNM server to switch management IP | N/A |
| Switch discovered but showing `Out of Sync` | DCNM 11.x | Config in DCNM DB doesn't match live switch config | Trigger sync: DCNM → Inventory → Devices → right-click → Sync | N/A |

## Deployment

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Config deployment fails: `Cannot push to switch` | DCNM 11.x | DCNM write credentials (SSH) no longer valid | Update switch credentials in DCNM → Administration → Credentials | N/A |
| `Deployment preview differs from expected` | DCNM 11.x | Manual change made directly on switch (out-of-band) | Review diff in DCNM; reconcile with `Recalculate` before deploying | N/A |

## See also

- [Cisco DCNM — Common Issues](common-issues.md)
- [Cisco MDS — Known Issues](../../mds/troubleshooting/known-issues/)
- [Cisco Nexus Dashboard — Known Issues](../../nexus-dashboard/troubleshooting/known-issues/)
