# Superna Eyeglass — Install & Upgrade

## Version Compatibility Matrix

Eyeglass version must be compatible with the deployed PowerScale OneFS version. Always verify before upgrading either system.

```mermaid
flowchart TD
    start(["Plan upgrade"]) --> exportCfg
    exportCfg["Export configuration backup\nAdmin UI → Admin → Configuration Backup"]
    deployOVA["Deploy new Eyeglass OVA\nalongside existing appliance"]
    importCfg["Import configuration to new OVA\nRe-register clusters and DNS"]
    verifyScore["Verify DR Readiness Score\n= 100%"]
    validate24h["24-hour validation period\nConfirm SyncIQ state, shares, exports"]
    decommOld["Shut down old appliance"]
    done(["Upgrade complete"])

    exportCfg --> deployOVA --> importCfg --> verifyScore --> validate24h --> decommOld --> done
```

### Upgrade Process

1. Download new OVA from [Superna support portal](https://support.superna.net)
2. Deploy new Eyeglass OVA alongside the existing appliance (do not shut down existing)
3. Power on new appliance; set static IP (different from existing)
4. Import configuration backup to new appliance
5. Re-register PowerScale clusters and DNS servers
6. Verify DR readiness score returns to 100%
7. Shut down old appliance after 24-hour validation period

In-place upgrade support varies by version — check release notes before proceeding.

### Post-Upgrade Validation

- [ ] SyncIQ policies detected and showing correct state
- [ ] DR readiness score = 100%
- [ ] SMB shares visible and correctly mapped
- [ ] NFS exports visible and correctly mapped
- [ ] DNS integration verified (test DNS preview)
- [ ] SNMP/syslog notifications still reaching monitoring/SIEM
- [ ] Failover test with test shares (if possible in maintenance window)

## OneFS Upgrade Impact

After any PowerScale OneFS upgrade, re-validate Eyeglass policy detection:

```text
Post-OneFS upgrade checklist:
  1. Log in to Eyeglass Admin UI
  2. DR → Replication Policies → Rescan
  3. Verify all SyncIQ policies are detected
  4. DR → Readiness — confirm score returns to 100%
  5. Check for any new Eyeglass warnings about API changes
```

If Eyeglass shows API errors after OneFS upgrade, check if an Eyeglass update is required to support the new OneFS version.

## EOL Tracking

| Item | Check Location | Action Threshold |
|---|---|---|
| Eyeglass appliance version | support.superna.net → EOL | Upgrade plan at 6 months before EOL |
| OneFS compatibility | Superna compatibility matrix | Verify before any OneFS upgrade |
| License expiry | Admin UI → License | Renew 60 days before expiry |
| VM guest OS (Eyeglass appliance) | Admin UI → System Info | Align with Superna supported OS list |

## License Management

Eyeglass licensing is per-cluster (primary and DR) and per-node count:

1. Download license file from Superna licensing portal
2. Admin UI → License → Import License
3. Verify license file UUID matches the appliance UUID shown in the UI

If appliance shows "Unlicensed" after an upgrade, re-import the license — appliance UUID may have changed if deployed from new OVA.
