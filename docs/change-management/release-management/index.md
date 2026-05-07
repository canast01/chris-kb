# Release Management

Coordinates planning, scheduling, and execution of software and infrastructure releases to minimise risk and ensure controlled delivery.
## Release Types

| Type | Description | Cadence | Approval |
|---|---|---|---|
| Major release | New features, architectural changes | Quarterly / planned | Full CAB |
| Minor release | Bug fixes, minor enhancements | Monthly | Team lead + service owner |
| Patch / hotfix | Security patch, critical bug fix | As needed | Emergency CAB or team lead |
| Configuration release | Config-only changes (no code) | Weekly or ad hoc | Standard change |

## Release Lifecycle

```
1. Scope definition
   → Features/fixes identified; linked to tickets/epics

2. Release planning
   → Target date agreed; release branch cut or tagged

3. Testing gate
   → Unit / integration / regression / UAT complete

4. Release review
   → RFC submitted; risk assessed; approval obtained

5. Deployment
   → Change window executed per deployment procedure

6. Verification
   → Smoke tests; monitoring soak; stakeholder sign-off

7. Release closure
   → RFC closed; release notes published; team briefed
```

## Release Readiness Checklist

- [ ] All in-scope tickets resolved and verified in non-prod
- [ ] Regression test suite passed
- [ ] UAT sign-off obtained from business/service owner
- [ ] Release notes drafted (changes, known issues, rollback instructions)
- [ ] Deployment runbook reviewed and updated
- [ ] Rollback procedure tested in staging
- [ ] Database migrations reviewed and backed out tested
- [ ] Third-party dependency versions locked and verified
- [ ] Security scan / DAST completed for application releases
- [ ] Change window booked; stakeholders notified

## Release Calendar — Blocked Periods

Avoid scheduling releases during:
- Month-end / quarter-end financial processing windows
- Major public holidays or low-staffing periods
- Active incidents or post-incident moratorium (72h after P1)
- Code/change freeze periods (pre-announced)

## Release Notes Template

```markdown
## Release vX.Y.Z — 2026-05-06

### Changes
- [Feature] Description of new capability (TICKET-123)
- [Fix] Description of bug fix (TICKET-456)
- [Security] CVE-YYYY-XXXXX patched in dependency X

### Known Issues
- [TICKET-789] Description — workaround: ...

### Deployment Notes
- Requires DB migration: run `migration_0042_up.sql` before service start
- Config change required: add `NEW_SETTING=value` to `/etc/app/config`

### Rollback
- Stop service; revert package to vX.Y.Z-1; run `migration_0042_down.sql`
```

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
