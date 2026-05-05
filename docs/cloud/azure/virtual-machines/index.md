# Azure Virtual Machines

## Overview

Azure Virtual Machines provide compute resources for Windows and Linux workloads in Microsoft Azure.

## Daily Checks

- Review VM health
- Check disk capacity and performance
- Validate backup status
- Review update compliance
- Confirm monitoring alerts

## Health Commands

```bash
az vm list -o table
az vm get-instance-view --resource-group RG --name VM
az monitor metrics list --resource VM_RESOURCE_ID --metric Percentage CPU
az backup job list --resource-group RG --vault-name VAULT
```

## Upgrade Workflow

1. Confirm backup restore point
2. Validate maintenance window
3. Apply OS patches
4. Reboot if required
5. Confirm VM and application health
