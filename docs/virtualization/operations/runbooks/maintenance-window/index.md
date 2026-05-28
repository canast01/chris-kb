# Maintenance Window Runbook

```
┌───────────────────────────────────── Maintenance Window Runbook ──────────────────────────────────────┐
│                                                                                                       │
│    Use for all planned VMware work; follow pre/execute/post phases in order                           │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Phase       │   Key Actions    │   Gate Criteria   │     On FAIL      │      Owner       │   │
│   │  ──────────────  │  ──────────────  │  ───────────────  │  ──────────────  │  ──────────────  │   │
│   │  1  Pre-checks   │ Health + backups │     All green     │  Do not proceed  │  Infra engineer  │   │
│   │    2  Notify     │ Stakeholders out │  Comms confirmed  │   Delay window   │  Change manager  │   │
│   │    3  Execute    │  Perform change  │   Per procedure   │  Rollback plan   │  Infra engineer  │   │
│   │  4  Post-check   │ Validate health  │  All checks pass  │ → incident proc. │  Infra engineer  │   │
│   │   5  App check   │  Owner confirms  │ Sign-off received │  Escalate to P2  │    App owner     │   │
│   │     6  Close     │ Update CR + docs │     CR closed     │ Note exceptions  │  Change manager  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CR          = Change Record; ITSM ticket approved before work begins; closed after                 │
│    Rollback    = Pre-planned steps to undo the change if it fails; must be documented                 │
│    Comms       = Stakeholder notification; send before window opens and after it closes               │
│    App owner   = Business owner of the application; provides sign-off after maintenance               │
│    Gate        = Go/no-go check at each phase; any failure stops the window                           │
│    Exceptions  = Deviations from the plan; always document in the change record                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
