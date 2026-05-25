# Maintenance Window Runbook

Use this for planned VMware work.

```text
Maintenance Window Flow
═══════════════════════════════════════════════════════════

  PRE-CHECKS
  ┌──────────────────────────────────────────────────────┐
  │  Review change ticket · confirm window · notify      │
  │  Confirm backups · confirm health · capture versions │
  │  Confirm rollback plan · confirm vendor support      │
  └──────────────────────────┬───────────────────────────┘
                             │
                             ▼
  COMMUNICATE (start of window)
  ┌──────────────────────────────────────────────────────┐
  │  Notify stakeholders: work starting                  │
  │  Open bridge / comms channel if P-level change       │
  └──────────────────────────┬───────────────────────────┘
                             │
                             ▼
  EXECUTE
  ┌──────────────────────────────────────────────────────┐
  │  Place host in maintenance mode (if required)        │
  │  Perform approved work steps                         │
  │  Monitor: cluster health · vSAN resync · DRS         │
  │  Capture screenshots at key milestones               │
  │  If unexpected issue → stop, assess, rollback/escalate│
  └──────────────────────────┬───────────────────────────┘
                             │
                             ▼
  VALIDATE
  ┌──────────────────────────────────────────────────────┐
  │  All hosts connected · VMs running · datastores OK   │
  │  Monitoring clean · backup jobs not broken           │
  │  App owner confirms (for production changes)         │
  └──────────────────────────┬───────────────────────────┘
                             │
                             ▼
  CLOSE
  └─ Update ticket · attach evidence · send completion notice
```

## Before Maintenance

- Review change ticket
- Confirm maintenance window
- Notify stakeholders
- Confirm backups
- Confirm current health
- Confirm rollback plan
- Capture versions
- Confirm access
- Confirm vendor support if needed

## During Maintenance

- Start maintenance window
- Place host in maintenance mode if required
- Perform approved work
- Monitor cluster and workload health
- Capture screenshots or logs
- Escalate if unexpected issues occur

## After Maintenance

- Validate cluster health
- Confirm VMs are running
- Confirm datastores are accessible
- Confirm monitoring is clean
- Confirm backups still work
- Update ticket with results
- Send completion notice
