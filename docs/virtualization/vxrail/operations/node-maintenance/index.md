# VxRail Node Maintenance Procedure


<div class="kb-summary">
VxRail Node Maintenance Procedure reference covering Before Starting, Evacuation Mode Selection, Entering Maintenance Mode, Performing the Work, Exiting Maintenance Mode and 1 more sections.
</div>

Node Maintenance Mode Lifecycle
```text
┌──────────────────────────────────────────────────────────────┐
│  Pre-check: cluster health green · vSAN resync acceptable                                             │
│  capacity to absorb workload from this node                                                           │
└──────────────────────────────┬───────────────────────────────┘
```
                               │
                    ┌──────────▼──────────┐
                    │  Enter Maintenance  │
                    │  Mode              │
                    │  Evacuation type:  │
                    │  Ensure Access     │
                    │  Full Migration    │
                    │  (No Migration*)   │
                    └──────────┬──────────┘
                               │  * Dell guidance only
                    ┌──────────▼──────────┐
                    │  Perform Work        │
                    │  hardware · FW · etc │
                    │  stay in scope       │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Exit Maintenance   │
                    │  Mode               │
                    │  → host reconnects  │
                    │  → vSAN rebalances  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Validate           │
                    │  Connected · no     │
                    │  alerts · vSAN OK   │
                    └─────────────────────┘
```

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
```
