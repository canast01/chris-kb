# NetBackup — Health Checks

## Daily Check Flow

```mermaid
flowchart TD
    start(["Start daily\nhealth check"])
    start --> jobSummary["bpjobs -summary\nReview totals\n(target: 0 failed)"]
    jobSummary --> failedJobs{"Any\nfailures?"}
    failedJobs -->|Yes| investigate["bpdbjobs -report -failed -hoursago 24\nInvestigate each failure\nNote error status code"]
    failedJobs -->|No| catalog["Verify catalog backup\nbplist -S <master> -policy NBU_Catalog\nMust have completed in last 6 hours"]
    investigate --> catalog
    catalog --> catalogOK{"Catalog backup\nOK?"}
    catalogOK -->|No| catAlert["CRITICAL: trigger manual\ncatalog backup immediately\nbpbackup -p NBU_Catalog_Backup"]
    catalogOK -->|Yes| storage["bpstulist — check all STUs\nTotal Capacity vs Free Space\nFlag STUs below 15% free"]
    catAlert --> storage
    storage --> mediaServers["nbemmcmd -listhosts -machinetype mediaserver\nVerify all media servers registered"]
    mediaServers --> alerts["Review OpsCenter\n/ Admin Console alerts"]
    alerts --> done(["Daily check complete\nDocument findings"])

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef warn fill:#be123c,stroke:#9f1239,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    class jobSummary,investigate,catalog,storage,mediaServers,alerts action
    class failedJobs,catalogOK decision
    class catAlert warn
    class start,done terminal
```

## Daily Checklist

Run these checks each morning to confirm a healthy NetBackup environment.

- [ ] `bpjobs -summary` — review totals; zero failed is the target
- [ ] `bpdbjobs -report -failed -hoursago 24` — investigate each failure
- [ ] Confirm catalog backup job completed successfully
- [ ] `bpstulist` — check `Total Capacity` vs `Free Space` on all disk STUs
- [ ] `nbemmcmd -listhosts` — verify all media servers are registered and reachable
- [ ] OpsCenter / Admin Console — review any active alerts

**Weekly**

- Verify tape media inventory if tape library in use (`tpconfig -d`, `vmquery -b`)
- Review policy schedule calendar for upcoming full backup windows
- Confirm deduplication ratio on OST storage units (Data Domain DDOS UI)

## Job Monitoring

Use this section for practical NetBackup job monitoring notes, checks, troubleshooting, commands, change notes, and field references.

### Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

### Useful commands

Add tested commands here.

### Known issues

Add known issues here as they come up.

## Validation

Use this section for practical NetBackup Validation notes, checks, troubleshooting, commands, change notes, and field references.

### Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

### Useful commands

Add tested commands here.

### Known issues

Add known issues here as they come up.
