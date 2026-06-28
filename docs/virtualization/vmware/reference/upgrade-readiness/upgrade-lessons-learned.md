---
tags:
  - reference
---
# Upgrade Lessons Learned

<div class="kb-summary">
Document post-upgrade findings to improve future upgrade runbooks. Complete this within 48 hours of change record closure while details are fresh.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
template: "Template" {shape: rectangle}
common_lessons_by_component: "Common Lessons by Component" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> template
template -> common_lessons_by_component
common_lessons_by_component -> validate
```

## Template

Copy this template to a new entry in your team's wiki or knowledge base after each significant upgrade.

---

**Upgrade**: [Component] [From Version] → [To Version]  
**Date**: [YYYY-MM-DD]  
**Duration**: [Planned Xh] / [Actual Xh]  
**Change Record**: [CR number]

### What Worked

- *e.g. Snapshot rollback procedure was clear and quick (< 5 minutes)*
- *e.g. Pre-upgrade certificate check caught an expiring cert that would have caused upgrade failure*
- *e.g. Offline depot workflow worked without internet access*

### What Failed or Caused Delays

- *e.g. ESXi host stuck in maintenance mode after upgrade — needed manual vCenter task cancellation*
- *e.g. vCenter VAMI backup took 45 minutes instead of the expected 10 — backup window was too tight*
- *e.g. NSX Manager backup failed silently — not noticed until post-upgrade validation*

### Issues Found

| Issue | Root Cause | Resolution | Time Lost |
|---|---|---|---|
| [Description] | [Cause] | [How resolved] | [Minutes] |

### Step-by-Step Timing

| Step | Planned Duration | Actual Duration | Notes |
|---|---|---|---|
| vCenter backup | 15 min | 45 min | VAMI backup slower than expected on full datastore |
| vCenter upgrade | 60 min | 75 min | Extra time for SSO reconfiguration |
| ESXi host upgrade (×N) | 20 min/host | 25 min/host | HBA driver reload added time |

### Vendor Case Numbers

| Vendor | Case # | Issue | Status |
|---|---|---|---|
| VMware/Broadcom | SR-XXXXXXXXX | [Description] | Closed/Open |

### Changes to Future Pre-Checks

- *e.g. Add: verify VAMI backup datastore has > 50 GB free before starting*
- *e.g. Add: test NSX Manager backup manually and verify output file before proceeding*
- *e.g. Remove: HCL check for model X — confirmed always compatible with vSphere 8.x*

### Updated Rollback Steps

If the rollback procedure needed adjustment during this upgrade, document the corrected steps here so the runbook can be updated.

### Final Validation Results

- All hosts at target version: Yes / No
- Zero new alarms post-upgrade: Yes / No
- Application owner sign-off received: Yes / No
- Upgrade rated: Successful / Partially Successful / Failed (rolled back)

---

## Common Lessons by Component

### vCenter

- Always check VAMI partition utilisation before starting — `/storage/log` fills during upgrade
- Allow 90 minutes minimum for vCenter upgrade — underestimating causes change record overruns
- After upgrade: verify all vSphere plugins (NSX, VxRail, SRM) load without errors

### ESXi

- Roll hosts one at a time through maintenance mode — parallel upgrades race for vSAN resync bandwidth
- Check for third-party VIBs before upgrade — some are not compatible with new ESXi builds

### NSX

- NSX upgrades can fail silently on a single Manager node — verify all three nodes complete
- Edge node upgrades are the most failure-prone step — allow extra time and have a rollback snapshot

### vSAN

- Never upgrade vSAN during active resync — wait for resync to complete first
- Post-upgrade: allow 30 minutes for vSAN health to settle before signing off the change
