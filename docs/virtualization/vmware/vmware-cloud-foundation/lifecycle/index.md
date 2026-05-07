# VMware Cloud Foundation Lifecycle

VCF upgrades are orchestrated entirely through SDDC Manager, which downloads lifecycle bundles from the VMware depot (or an offline bundle depot) and applies them in a strictly enforced sequence.
## Upgrade Sequence

SDDC Manager enforces this order — you cannot skip steps:

1. **SDDC Manager** — always first; gates all other upgrades
2. **vCenter Server** — management domain, then VI workload domains
3. **ESXi hosts** — host remediation per cluster, one cluster at a time
4. **NSX-T** — NSX Manager cluster, then NSX Edge clusters
5. **vSAN** — firmware and driver updates validated against HCL

## Version Compatibility Matrix

| VCF Release | ESXi | vCenter | NSX-T | vSAN | EoGS |
|---|---|---|---|---|---|
| 5.2 | 8.0 U3 | 8.0 U3 | 4.2 | 8.0 U3 | Check Broadcom lifecycle |
| 5.1 | 8.0 U2 | 8.0 U2 | 4.1 | 8.0 U2 | Check Broadcom lifecycle |
| 4.5 | 7.0 U3 | 7.0 U3 | 3.2 | 7.0 U3 | Check Broadcom lifecycle |

Always verify against the [Broadcom VCF Release Notes](https://docs.vmware.com/en/VMware-Cloud-Foundation/) before upgrade.

## Bundle Management

```bash
# SDDC Manager UI: Lifecycle Management → Bundle Management
# Check for available bundles (requires internet or depot connectivity)

# Offline depot: configure custom depot in SDDC Manager
# Administration → Depot Settings → set offline depot URL
```

Bundles are downloaded automatically on a configured schedule or manually triggered.

## Async Patches

Async patches allow individual component updates (e.g., ESXi security patch) between full VCF releases.

- Must be validated against the VCF compatibility matrix before application
- Apply via SDDC Manager: Lifecycle Management → Async Patches
- Test in non-production domain first

## Pre-Upgrade Checklist

- [ ] vSAN health: all checks GREEN
- [ ] No active resync operations
- [ ] Snapshots removed from all management VMs (SDDC Manager, vCenter, NSX)
- [ ] Backup of SDDC Manager completed
- [ ] vCenter inventory backed up (File-Based Backup)
- [ ] NSX-T backup completed
- [ ] Maintenance window approved
- [ ] HCL validation passed for all hosts in target clusters
- [ ] Check VCF compatibility matrix for all third-party integrations

## SDDC Manager Backup

```bash
# SDDC Manager backup is configured under Administration → Backup
# Trigger manual backup before any lifecycle operation:
# Lifecycle Management → Backup and Restore → Backup Now
```

## Rolling Back

VCF does not support direct rollback of component upgrades. Recovery options:

| Component | Rollback Method |
|---|---|
| SDDC Manager | Restore from backup (separate SDDC Manager appliance) |
| vCenter | File-Based Restore to pre-upgrade backup |
| ESXi | Boot from previous bootbank: `esxcli system settings advanced set -o /UserVars.ESXiShellInteractiveTimeOut -i 0` then rollback VIB |
| NSX-T | Restore NSX Manager from backup |

Plan rollback paths before starting any upgrade.
