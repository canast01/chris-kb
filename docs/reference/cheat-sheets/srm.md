---
tags:
  - srm
  - backup-dr
---
# SRM Cheat Sheet

<div class="kb-summary">
Top-10 SRM commands for protection groups, recovery plans, test failover, and failover operations via PowerCLI and REST API.
</div>

```text
┌───────────────────────────────────────── SRM Cheat Sheet ─────────────────────────────────────────────┐
│  PowerCLI: Connect-SrmServer  ·  REST API: https://srm/api  ·  Requires: VMware.VimAutomation.Srm     │
│  Categories: Protection Groups · Recovery Plans · Test Failover · Reprotect · Failback                │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## PowerCLI

```powershell
Import-Module VMware.VimAutomation.Srm
$srm = Connect-SrmServer -Server srm.lab.local -User admin -Password VMware1!

# Protection groups
$pg = $srm.ExtensionData.Protection.ListProtectionGroups()
$pg | Select Name, State, ProtectionState                                  # group list + state

# Recovery plans
$rp = $srm.ExtensionData.Recovery.ListPlans()
$rp | Select Name, State                                                   # plan list + state

# Test failover
$plan = ($rp | Where { $_.Name -eq "MyPlan" }).MoRef
$srm.ExtensionData.Recovery.Start($plan, @{RunMode="test"})               # start test

# Cleanup test failover
$srm.ExtensionData.Recovery.Start($plan, @{RunMode="cleanupTest"})        # cleanup

# Real failover (planned migration)
$srm.ExtensionData.Recovery.Start($plan, @{RunMode="migration"})          # planned failover

# Reprotect
$srm.ExtensionData.Recovery.Reprotect($plan)                              # reverse protection
```

## REST API

```bash
BASE="https://srm/api"
AUTH="-u admin:VMware1!"

curl -sk $AUTH $BASE/pairing | python3 -m json.tool                        # site pairing info
curl -sk $AUTH $BASE/plans | python3 -m json.tool                          # all recovery plans
curl -sk $AUTH $BASE/plans/<id>/history | python3 -m json.tool             # plan run history
```

## See also

- [SRM Operations](../../virtualization/vmware/srm/operations/procedures/)
- [SRM Troubleshooting](../../virtualization/vmware/srm/troubleshooting/common-issues/)
