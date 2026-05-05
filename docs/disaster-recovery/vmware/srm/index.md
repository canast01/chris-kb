# VMware Site Recovery Manager (SRM)

## Overview

VMware Site Recovery Manager automates disaster recovery for VMware virtual machines using replication technologies and predefined recovery plans.

## Daily Checks

- Verify SRM service status
- Check protection group health
- Validate recovery plans
- Review replication status

## Health Commands

```bash
service-control --status vmware-dr
dr-config status
dr-recovery-plan list
```

## Failover Procedure

1. Initiate recovery plan
2. Monitor VM startup sequence
3. Validate network connectivity
4. Confirm application availability

## Failback Procedure

1. Reprotect workloads
2. Synchronize replication
3. Execute failback recovery plan
4. Validate production services
