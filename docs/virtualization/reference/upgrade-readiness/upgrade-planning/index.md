# Upgrade Planning

Upgrade planning should start before the maintenance window.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                   Upgrade Planning Checklist                             │
├──────────────────────────┬───────────────────────────────────────────────┤
│  Planning Item           │  Detail / Action                              │
├──────────────────────────┼───────────────────────────────────────────────┤
│ Current version          │ Document all component versions now           │
│ Target version           │ Confirm target + supported upgrade path       │
│ Compatibility matrix     │ Check interopmatrix.vmware.com                │
│ Hardware compatibility   │ Check HCL for server/NIC/HBA/storage          │
│ Firmware/driver          │ Confirm approved baseline for target ESXi     │
│ Backup requirements      │ VCSA backup + NSX backup + snapshots          │
│ Maintenance window       │ Scope duration with buffer for rollback       │
│ Rollback plan            │ Document per-component rollback method        │
│ Support contacts         │ VMware SR, Dell, application owners           │
│ Application impact       │ Notify owners, confirm validation steps       │
│ Validation checklist     │ Define pass criteria before starting          │
└──────────────────────────┴───────────────────────────────────────────────┘
```

## Key Planning Items

- Current version
- Target version
- Supported upgrade path
- Compatibility matrix
- Hardware compatibility
- Firmware and driver requirements
- Backup requirements
- Maintenance window
- Rollback plan
- Support contacts
- Application impact
- Validation checklist
