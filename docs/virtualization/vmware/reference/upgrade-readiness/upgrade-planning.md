---
tags:
  - reference
---
# Upgrade Planning


<div class="kb-summary">
Upgrade planning should start before the maintenance window.

*Applies to: vSphere 7.x / 8.x*
</div>
![Upgrade Planning](../../../../assets/virtualization-vmware-reference-upgrade-readiness-upgrade-pl.svg)




```d2
direction: right

plan: "Plan" {shape: oval}
key_planning_items: "Key Planning Items" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> key_planning_items
key_planning_items -> validate
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
