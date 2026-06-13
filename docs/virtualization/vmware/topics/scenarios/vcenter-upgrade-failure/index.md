---
tags:
  - scenarios
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter Upgrade Failure / Rollback

<div class="kb-summary">
A vCenter upgrade using the VCSA installer or the in-place upgrade wizard fails partway through, leaving
vCenter in a partially upgraded, non-functional, or non-booting state. This scenario covers the upgrade
stages, where failures occur, how to use the auto-snapshot rollback built into the VCSA upgrade process,
how to fall back to the source appliance when rollback is not available, and what to fix before retrying.
ESXi hosts and running VMs are unaffected during a vCenter upgrade — only management is disrupted.
</div>

```text
┌──────────────────────────── vCenter Upgrade Failure — Investigation Flow ─────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  ESXi hosts and running VMs are unaffected during a vCenter upgrade — only management is disrupted    │
│  VCSA upgrade is two-stage; failure at each stage has a different recovery path                       │
│                                                                                                       │
│  START: VCSA upgrade fails — installer error · appliance won't boot · UI unreachable post-upgrade     │
│                                                                                                       │
│  STAGE 1 FAILURE — Deploy appliance did not complete                                                  │
│  Source VCSA still running — no management impact                                                     │
│  Resolution: fix the install error and simply re-run Stage 1                                          │
│                                                                                                       │
│  STAGE 2 FAILURE — Migrate data / configure new VCSA                                                  │
│  Rollback snapshot available? Apply it on the new VCSA appliance                                      │
│  No snapshot: revert to source VCSA if it is still intact                                             │
│                                                                                                       │
│  POST-UPGRADE FAILURE — UI down or services failing                                                   │
│  Check services via SSH: service-control --status --all                                               │
│  Check disk space on new VCSA · check certificate dates · check SSO token validity                    │
│                                                                                                       │
│  CLOSE: vCenter accessible · all hosts connected · services healthy · upgrade log clean               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter VCSA | Upgrading appliance (source and destination) |
| ESXi (host running VCSA) | Hosts the VCSA VM; snapshot rollback requires host access |
| vSAN | VCSA may run on vSAN datastore; space and health affect upgrade success |
| Aria SuiteLC | Manages VCSA lifecycle in Aria Suite deployments; alternative upgrade path |
| NSX Manager | Does not upgrade with VCSA; NSX compatibility matrix must be checked before starting |

---

## 1. Understand the VCSA Upgrade Stages

The VCSA upgrade uses a two-stage process from the installer ISO. Understanding which stage failed determines the recovery path.

```text
Stage 1 — Deploy new appliance
  A new VCSA VM is deployed alongside the source VCSA.
  The source VCSA continues running — management is fully available throughout Stage 1.
  Stage 1 can fail and be re-run any number of times without impact.

Stage 2 — Migrate data and cutover
  Source VCSA is shut down.
  All inventory, permissions, certificates, and configuration are copied to the new appliance.
  The new VCSA takes over the same IP/hostname as the source.
  Management is DOWN for 15–90 minutes during this stage.
  A snapshot is taken of the new VCSA at the start of Stage 2 to enable rollback.
```

Look for: always confirm Stage 1 completed successfully before beginning Stage 2. Do not start Stage 2 without a verified backup of the source VCSA from VAMI.

---

## 2. Pre-Upgrade Checklist — Failures Prevented Here

Most upgrade failures are caused by conditions that could be caught before starting. Review these before retry.

```text
[ ] vCenter version supports direct upgrade path to target version
    (check VMware Product Interoperability Matrix — some versions require an intermediate hop)
[ ] Source VCSA disk space: all partitions below 70% (especially /storage/log, /storage/db)
[ ] NTP is synchronised on source VCSA (check: timedatectl status)
[ ] SSO password policy is met — default SSO admin password expiry causes Stage 2 auth failures
[ ] DNS forward and reverse resolution working for both source and new VCSA FQDN
[ ] All ESXi hosts in the inventory are connected and not in maintenance mode
[ ] vSAN health is green — any degraded components may cause Stage 2 data migration to fail
[ ] NSX and other products checked against the vCenter compatibility matrix for the target version
[ ] Backup of source VCSA via VAMI is complete and tested within the last 24 hours
[ ] Snapshot of source VCSA VM taken on the ESXi host (additional rollback option)
```

---

## 3. Stage 1 Failure — Source VCSA Still Running

If Stage 1 (deploy new appliance) fails, the source VCSA is unaffected. Read the installer log to find the exact error.

Installer log location on the machine running the installer:

```text
Windows: %TEMP%\vcsaInstallXXXXX\
macOS / Linux: /tmp/vcsaInstallXXXXX/
```

```text
Common Stage 1 failures:
  "No space left on datastore"           → target datastore has insufficient free space
  "Failed to connect to host"            → installer cannot reach the target ESXi host; check credentials, firewall
  "Certificate verification failed"      → ESXi thumbprint changed; re-enter the correct thumbprint
  "Timeout waiting for appliance start"  → new VCSA VM deployed but didn't boot; check ESXi host resources
  "Network configuration failed"         → IP/hostname conflict; DNS not resolving new VCSA FQDN
```

After fixing the root cause, simply re-run the installer — Stage 1 can be repeated as many times as needed.

---

## 4. Stage 2 Failure — Rollback the New VCSA

If Stage 2 fails, the installer automatically prompts to roll back via the snapshot taken at Stage 2 start. This restores the source VCSA to its pre-upgrade state.

```text
Rollback options the installer presents:
  1. Roll back source VCSA from snapshot (restore original appliance)
  2. Keep the failed new VCSA (not recommended unless data migration completed)
```

If the installer rollback prompt is not available (installer was closed, network failure), roll back manually:

```bash
# SSH to the ESXi host running the VCSA VMs
vim-cmd vmsvc/getallvms | grep -i vcenter

# List snapshots for the source VCSA VM ID (replace <vmid>)
vim-cmd vmsvc/snapshot.get <vmid>

# Revert to the pre-Stage-2 snapshot
vim-cmd vmsvc/snapshot.revert <vmid> <snapshot-id> 0

# Power on the source VCSA
vim-cmd vmsvc/power.on <vmid>
```

After rollback, SSH to the source VCSA and confirm all services are running:

```bash
service-control --status --all | grep -i stopped
```

---

## 5. Stage 2 Failure — Read the Upgrade Logs

If rollback succeeds but you need to understand the failure before retrying, read the upgrade logs on the new VCSA before rolling it back.

```bash
# SSH to the new (failed) VCSA
# Upgrade logs are in:
ls /var/log/vmware/upgrade/

# Main upgrade orchestration log
tail -100 /var/log/vmware/upgrade/vcsa-upgrade.log

# Stage 2 data migration log
tail -100 /var/log/vmware/upgrade/dbmigration.log

# Certificate migration log
tail -100 /var/log/vmware/upgrade/certmigration.log
```

Common Stage 2 failure patterns:

```text
"Database migration failed: out of disk space"
  → /storage/db partition on new VCSA too small; re-deploy with larger storage profile

"SSO authentication failed during migration"
  → SSO administrator@vsphere.local password expired on source VCSA before migration
  → Fix: unlock SSO admin account on source VCSA before retrying

"Failed to configure network: IP already in use"
  → Source VCSA did not shut down cleanly; old IP still responding
  → Fix: force power off source VCSA, wait 60 seconds, retry cutover

"Certificate migration failed: chain validation error"
  → Expired certificates on source VCSA; renew with certificate-manager before retrying

"Services failed to start: address already in use"
  → Port conflict; another appliance (PSC, old VCSA) still active on same IP
```

---

## 6. Post-Upgrade Validation — New VCSA Accessible But Issues Remain

If Stage 2 completed but the new VCSA has service or connectivity issues, use the standard VCSA diagnostic tools before rolling back.

```bash
# On the new VCSA — check services
service-control --status --all | grep -i stopped

# Check disk space
df -h

# Check NTP synchronisation
timedatectl status

# Check SSO health
/usr/lib/vmware-vmafd/bin/vmafd-cli get-domain-state --server-name localhost

# Check certificate validity
for svc in vpxd-extension machine vsphere-webclient; do
    /usr/lib/vmware-vmafd/bin/vecs-cli entry list --store $svc | grep -E "Alias|Not After"
done
```

If the new VCSA boots but hosts are not reconnecting within 15 minutes:

```bash
# Re-trigger reconnect for all hosts via PowerCLI on the new vCenter
Get-VMHost | Where-Object { $_.ConnectionState -eq "Disconnected" } `
  | ForEach-Object { $_ | Set-VMHost -State Connected }
```

---

## 7. Aria SuiteLC Upgrade Path

If vCenter is managed by Aria Suite Lifecycle (SuiteLC), do not use the standalone VCSA installer ISO — use SuiteLC's built-in upgrade orchestration.

Navigate to **Aria SuiteLC → Lifecycle Operations → Environments → [Environment] → View Details → Upgrade**.

SuiteLC handles:
- Pre-upgrade compatibility checks across all Aria Suite products
- Sequential upgrade orchestration (upgrade order matters: vCenter → NSX → Aria Operations)
- Snapshot and backup coordination before upgrade
- Post-upgrade health validation

```text
Upgrade order for Aria Suite environments:
  1. vCenter (VCSA)
  2. NSX Manager (after vCenter upgrade completes)
  3. Aria Operations, Aria Logs, Aria Networks (after NSX)
  4. VxRail Manager (if present — must be last)
```

Look for: never upgrade NSX before vCenter — NSX compatibility is validated against the running vCenter version. Always check the Aria Suite Compatibility Matrix before starting any product upgrade.

---

## Key Terms

| Term | Definition |
|---|---|
| Stage 1 | The first phase of the VCSA two-stage upgrade: deploying a new VCSA appliance VM alongside the source; source remains running and management is fully available |
| Stage 2 | The second phase: source VCSA shuts down, data migrates to new appliance, IP/hostname cutover happens; management is unavailable for the duration |
| Rollback snapshot | An automatic VM snapshot taken of the new VCSA at the start of Stage 2; used to revert to the pre-migration state if Stage 2 fails |
| Source VCSA | The existing vCenter appliance being upgraded; remains running during Stage 1; shuts down only during Stage 2 cutover |
| Destination VCSA | The newly deployed VCSA VM that receives the migrated inventory and configuration during Stage 2 |
| SuiteLC | Aria Suite Lifecycle — the VMware lifecycle management platform that orchestrates upgrades for all Aria Suite and vCenter components in a coordinated, dependency-aware order |
| SSO admin expiry | The SSO administrator@vsphere.local account has a configurable password expiry (default 90 days); expired SSO admin credentials cause Stage 2 authentication failures during data migration |
| VCSA installer ISO | The VMware-provided installer disc image containing both the Stage 1 appliance deploy wizard and the Stage 2 migration engine; must match the exact target vCenter version |
| Product Interoperability Matrix | VMware's online compatibility tool that defines which source-to-target upgrade paths are supported and which products require intermediate version stops |
| timedatectl | The Linux system tool on VCSA for checking NTP synchronisation status; critical to verify before upgrade since NTP drift causes certificate and SSO failures |
| vecs-cli | VMware Endpoint Certificate Store CLI; used to inspect certificate validity dates for all VCSA-managed certificates |

---

## Common Mistakes

- **Starting Stage 2 without a VAMI backup.** Stage 2 shuts down the source VCSA. If rollback fails (host crash, storage outage, snapshot corruption), without a VAMI backup the only recovery is a rebuild. Always have a tested backup before Stage 2.
- **Not checking DNS before Stage 1.** If the new VCSA's FQDN does not resolve in both directions (forward and reverse), Stage 2 will fail at network cutover even though Stage 1 succeeded. DNS check takes 30 seconds.
- **Upgrading NSX before vCenter.** NSX Manager validates its compatibility against the running vCenter version. Upgrading NSX first with an older vCenter may break connectivity or leave NSX in an unsupported state.
- **Using the standalone installer when SuiteLC manages the environment.** Running the VCSA installer ISO outside SuiteLC bypasses SuiteLC's compatibility checks and breaks the managed lifecycle model — SuiteLC will no longer recognise the vCenter version and future upgrades will fail.
- **Closing the upgrade installer browser tab during Stage 2.** The installer orchestrates Stage 2 from the browser session. Closing it does not stop Stage 2 but removes the automatic rollback prompt if failure occurs mid-migration.

---

## Related Scenarios

- [vCenter Down / Unreachable](../vcenter-down/index.md) — Post-upgrade service failures use the same VCSA diagnostic tools (VAMI, service-control, vpxd.log); reference this scenario for service recovery steps.
- [NTP Drift / SSO and Certificate Errors](../ntp-drift-sso-certificate/index.md) — NTP drift and certificate expiry are pre-conditions that cause Stage 2 failures; resolve them before upgrading.
- [VxRail LCM Upgrade Failure](../vxrail-lcm-upgrade-failure/index.md) — VxRail LCM orchestrates vCenter upgrades on VxRail clusters; a VxRail LCM upgrade failure has the same rollback mechanics described here.
