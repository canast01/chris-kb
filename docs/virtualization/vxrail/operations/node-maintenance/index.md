# VxRail Node Maintenance Procedure
## Before Starting

- Confirm cluster health in vCenter — no critical alarms
- Confirm vSAN Skyline Health is green
- Confirm no active vSAN resyncs (or they are at an acceptable level)
- Confirm cluster has capacity to absorb the workload from this node

## Evacuation Mode Selection

When entering maintenance mode on a VxRail node:

| Option | When to Use |
|---|---|
| Ensure Accessibility | Standard maintenance — keeps data accessible without full migration |
| Full Data Migration | Before disk replacement or extended maintenance |
| No Data Migration | Only with Dell support guidance |

## Entering Maintenance Mode

1. In vCenter, right-click the VxRail node → **Maintenance Mode** → **Enter Maintenance Mode**
2. Select the appropriate evacuation mode
3. Monitor vSAN resync if full migration is selected
4. Wait for maintenance mode to complete before starting hardware or firmware work

## Performing the Work

- Complete only the approved scope of work
- Do not extend beyond the maintenance window without notification
- Confirm iDRAC access throughout the maintenance if hardware is involved

## Exiting Maintenance Mode

1. Right-click the host → **Maintenance Mode** → **Exit Maintenance Mode**
2. Confirm host reconnects to vCenter
3. Monitor vSAN rebalancing — this is expected and may take time
4. Confirm vSAN object health is green after rebalancing completes

## Post-Maintenance Validation

- Host is Connected in vCenter
- No new critical alerts
- vSAN Skyline Health is green
- VxRail Manager shows the node as healthy
- Firmware matches the approved cluster baseline
