---
tags:
  - servicenow
---
# Release Management

<div class="kb-summary">
Coordinates planning, scheduling, and execution of software and infrastructure releases to minimise risk and ensure controlled delivery.

*Applies to: ServiceNow*
</div>

```d2
direction: down

release_types: "Release Types" {shape: rectangle}
release_lifecycle: "Release Lifecycle" {shape: rectangle}
go_nogo_decision: "Go / No-Go Decision" {shape: rectangle}
postrelease_actions: "Post-Release Actions" {shape: rectangle}

release_types -> release_lifecycle: uses
release_lifecycle -> go_nogo_decision: uses
go_nogo_decision -> postrelease_actions: uses
```

## Release Types

| Type | Description | Cadence | Approval |
|---|---|---|---|
| Major release | New features, architectural changes | Quarterly / planned | Full CAB |
| Minor release | Bug fixes, minor enhancements | Monthly | Team lead + service owner |
| Patch / hotfix | Security patch, critical bug fix | As needed | Emergency CAB or team lead |
| Configuration release | Config-only changes (no code) | Weekly or ad hoc | Standard change |

## Release Lifecycle

## Go / No-Go Decision

At the start of the change window, explicitly confirm go/no-go:

| Check | Go Condition |
|---|---|
| Source environment healthy | All services green in staging |
| Target environment healthy | No active incidents in prod |
| Team available | Implementer + approver + on-call present |
| Rollback confirmed available | Rollback steps validated < 4h ago |
| Stakeholders notified | Notification acknowledged |

If any check fails: defer the release; communicate delay to stakeholders.

## Post-Release Actions

- Monitor for 30–60 min (production soak)
- Publish release notes to internal wiki / changelog
- Update CMDB with new software versions
- Close all linked change and release tickets
- Schedule post-release review for major releases (within 1 week)
