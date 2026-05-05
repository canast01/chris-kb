# VxRail Hardware Health Review

## iDRAC

- Log into iDRAC for each node
- Confirm no critical hardware alerts
- Review Lifecycle Controller logs for recent events
- Confirm remote access is working

## Disk Health

- Confirm no failed or predictive failure disks
- Review disk group status in vSAN Skyline Health
- Check for any disk errors in iDRAC storage view

## Memory Health

- Confirm no memory errors in iDRAC
- Check for correctable or uncorrectable ECC errors

## CPU Health

- Confirm no CPU errors or throttling events
- Review thermal and power state

## Power Supply

- Confirm both PSUs are present and healthy
- Confirm no power redundancy warnings

## NIC Status

- Confirm all NICs are active and at expected speed
- Review NIC errors in iDRAC and ESXi

## Firmware Baseline

- Confirm all nodes are on the same approved firmware bundle
- Review VxRail Manager for firmware compliance status

## When to Open a Dell Support Case

- Any failed hardware component
- Predictive disk failure alert
- Memory ECC uncorrectable errors
- Firmware inconsistency that cannot be resolved by upgrade
- iDRAC unreachable on a node
