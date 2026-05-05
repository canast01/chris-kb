# VxRail Support Bundle Collection

## When to Collect

- Dell or VMware support requests logs for an open case
- Upgrade pre-check or upgrade failure
- Node hardware alert requiring investigation
- VxRail Manager issue
- vSAN health issue on VxRail cluster

## Bundle Sources

| Source | What It Contains |
|---|---|
| VxRail Manager | Cluster state, upgrade logs, VxRail service logs |
| vCenter | Events, tasks, VC logs, SSO logs |
| ESXi hosts | hostd, vpxa, vmkernel, vobd logs |
| vSAN logs | Object health, disk group state, network |
| iDRAC / hardware | Lifecycle Controller, hardware events, firmware |

## Collection Process

1. Log into VxRail Manager
2. Navigate to **Support** → **Bundle Collection**
3. Select the bundle type (cluster, node, or full)
4. Wait for collection to complete
5. Download and save the bundle
6. For ESXi or vCenter logs, collect via the vSphere Client or SSH

## What to Include with a Dell Support Case

- VxRail Manager support bundle
- Error messages and screenshots
- Approximate time the issue started
- What changed before the issue
- Current VxRail version and target version if upgrade-related
- iDRAC IP addresses for affected nodes

## Naming Convention

Use a consistent name when saving bundles:

```
vxrail-support-<cluster-name>-<YYYY-MM-DD>.zip
```
