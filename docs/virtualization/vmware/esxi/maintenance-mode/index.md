# ESXi Host Maintenance Mode Process

## Pre-Checks

- Confirm cluster has sufficient capacity to absorb workload
- Confirm DRS is enabled and set to at least Partially Automated
- Check for VMs with DRS anti-affinity or must-run-on rules
- Confirm vSAN evacuation setting if vSAN is in use

## Entering Maintenance Mode

1. In vCenter, right-click the host → **Maintenance Mode** → **Enter Maintenance Mode**
2. Select evacuation option:
   - **Move powered-off and suspended VMs** (standard)
   - **Ensure accessibility** (vSAN — leaves data accessible but does not fully evacuate)
   - **Full data migration** (vSAN — migrates all data off the host)
3. Click OK and monitor the task

## Monitoring the Process

- Watch DRS task progress in Recent Tasks
- Confirm VMs are migrating to other hosts
- Check vSAN resync if full migration was selected — wait for it to complete before proceeding

## Completing Approved Work

- Perform hardware, firmware, or patching work as planned
- Do not extend beyond the approved maintenance window without notification

## Exiting Maintenance Mode

1. Right-click the host → **Maintenance Mode** → **Exit Maintenance Mode**
2. Confirm the host reconnects and shows as Connected
3. Wait for vSAN to rebalance if applicable

## Post-Maintenance Validation

- Confirm host is Connected in vCenter
- Confirm no new alerts on the host
- Confirm vSAN health is green if vSAN is used
- Confirm VMs are distributed as expected by DRS
- Confirm host hardware health in iDRAC
