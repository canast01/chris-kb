# ESXi Upgrade and Patching Readiness

## Current State

- Confirm current ESXi version and build on all hosts
- Note any hosts on a different version than the cluster standard

## Target Image or Baseline

- Identify the target ESXi image or patch baseline
- Confirm the image is compatible with the hardware (HCL)
- Confirm driver and firmware compatibility for NIC, HBA, and storage adapters

## Cluster Capacity

- Confirm the cluster has sufficient headroom to evacuate one host at a time
- Confirm DRS is enabled and set to at least Partially Automated

## Backup and Config Export

- Confirm vCenter file-based backup is current
- Export ESXi host configuration if required for the change record

## Remediation Order

For clusters with multiple hosts:
1. Patch one host at a time
2. Wait for each host to return from maintenance mode and vSAN to stabilize before patching the next
3. Do not patch all hosts simultaneously

## Post-Patch Validation

- Confirm host is Connected in vCenter
- Confirm ESXi version matches the target
- Confirm no new hardware or service alerts
- Confirm vSAN health is green if vSAN is used
- Confirm VMs are running normally
