# VxRail Pre-Upgrade Checklist

## Before Starting

- Confirm current VxRail version
- Confirm target VxRail version
- Review release notes for target version
- Confirm supported upgrade path

## Platform Health

- VxRail Manager is reachable and healthy
- vCenter is reachable and all hosts are connected
- vSAN Skyline Health is green
- No critical hardware alerts in iDRAC
- No active vSAN resyncs (or acceptable level)

## Infrastructure Validation

- DNS forward and reverse lookup working for all nodes
- NTP is synchronized across vCenter and ESXi hosts
- Certificates are valid and not expiring during the window
- Admin access confirmed for vCenter and VxRail Manager

## Backups and Recovery

- vCenter file-based backup is current
- VxRail configuration backup completed
- Rollback plan documented
- Dell support contact available if needed

## Approvals

- Maintenance window approved
- Stakeholders notified
- Change ticket approved
