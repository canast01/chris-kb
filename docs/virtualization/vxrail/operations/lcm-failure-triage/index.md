# VxRail LCM Failure Triage

## Symptoms

- VxRail lifecycle operation fails.
- Upgrade task stops or rolls back.
- VxRail Manager reports validation failure.
- Bundle install does not continue.

## Likely Causes

- Recent configuration change.
- DNS, certificate, or authentication issue.
- Resource pressure.
- Failed service.
- Storage or network dependency issue.
- Version or compatibility mismatch.

## Commands

~~~bash
# Add environment-specific commands here
~~~

## Troubleshooting Workflow

1. Confirm scope.
2. Check recent changes.
3. Review alarms and events.
4. Validate management connectivity.
5. Check logs.
6. Isolate the failing dependency.
7. Apply fix or escalate with evidence.

## Resolution

Document what changed, what fixed it, and how health was validated.

## Prevention

- Improve alerting.
- Add missing checks.
- Update the runbook.
- Capture known issue notes.
