# VxRail LCM Failure Triage

```text
  ┌──────────────────────────────────────────────────────┐
  │          LCM Failure Triage Runbook                  │
  │                                                      │
  │  1. Collect logs                                     │
  │     VxRail Mgr → Support → Generate bundle          │
  │     /var/log/vmware/marvin/upgrade.log               │
  │                 │                                    │
  │                 ▼                                    │
  │  2. Identify stage                                   │
  │     ├── Pre-check failure ──► fix health / certs    │
  │     ├── Bundle validation ──► re-download / verify  │
  │     ├── Node remediation ──► check node + logs      │
  │     └── Post-check failure ──► review component     │
  │                 │                                    │
  │                 ▼                                    │
  │  3. Remediate                                        │
  │     ├── Resolve root cause (DNS / cert / hw fault)  │
  │     ├── Clear failed task in VxRail Manager          │
  │     └── Re-run LCM job                              │
  │                 │                                    │
  │                 ▼                                    │
  │  4. Retry / Escalate                                 │
  │     All clear ──► retry ──► monitor to completion   │
  │     Blocked  ──► bundle + timeline ──► Dell SR      │
  └──────────────────────────────────────────────────────┘
```

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
