---
tags:
  - reference
  - vcenter
  - vsphere-8
description: "vCenter Upgrade Readiness Checklist reference covering Current State, Target Version, Pre-Upgrade Checks, Post-Upgrade Validation."
---
# vCenter Upgrade Readiness Checklist

<div class="kb-summary">
vCenter Upgrade Readiness Checklist reference covering Current State, Target Version, Pre-Upgrade Checks, Post-Upgrade Validation.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
current_state: "Current State" {shape: rectangle}
target_version: "Target Version" {shape: rectangle}
preupgrade_checks: "Pre-Upgrade Checks" {shape: rectangle}
postupgrade_validation: "Post-Upgrade Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> current_state
current_state -> target_version
target_version -> preupgrade_checks
preupgrade_checks -> postupgrade_validation
postupgrade_validation -> validate
```

## Current State

- Confirm current vCenter version and build number
- Confirm current ESXi versions and ensure they are compatible with the target vCenter

## Target Version

- Confirm target vCenter version and supported upgrade path
- Review VMware upgrade path tool: supported paths only

## Pre-Upgrade Checks

- vCenter file-based backup completed
- SSO domain health confirmed
- Certificate health confirmed — no expiring certs during the window
- All disk partitions have sufficient free space
- All hosts are Connected
- No critical active alarms
- Plugin compatibility confirmed (backup, monitoring, etc.)
- vCenter and PSC in the same SSO domain are upgraded together

## Post-Upgrade Validation

- Confirm vSphere Client is accessible on the new version
- Confirm all hosts are still Connected
- Confirm vSAN health is green if applicable
- Confirm NSX is functioning if applicable
- Confirm Aria integrations are working
- Confirm backup and monitoring plugins are working
- Capture new version and build number for records
