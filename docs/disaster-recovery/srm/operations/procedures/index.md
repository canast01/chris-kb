# SRM Operations — Procedures

## SRM Operational Flow Overview

The three primary SRM operations — Recovery Plan test, planned migration, and cleanup — each follow a distinct sequence governed by the same underlying orchestration engine.

```mermaid
flowchart TD
    start([Trigger event]) --> assess{Planned or\nunplanned?}

    assess -->|Planned| pm[Planned Migration]
    assess -->|Unplanned / DR| fo[Emergency Failover]
    assess -->|Drill / Test| tf[Test Failover]

    pm --> pmShutdown[Quiesce & shut down\nprotected-site VMs]
    pmShutdown --> pmSync[Final replication sync]
    pmSync --> pmPresent[Present datastores\nat recovery site]
    pmPresent --> pmBoot[Power on VMs\nper boot sequence]
    pmBoot --> pmValidate[Validate services]
    pmValidate --> pmReprotect[Reprotect\nreverse direction]

    fo --> foPresent[Present last-good\nreplica datastores]
    foPresent --> foBoot[Power on VMs\nat recovery site]
    foBoot --> foValidate[Validate services]
    foValidate --> foFailback[Plan failback\nwhen ready]

    tf --> tfSnapshot[Create isolated\ntest snapshot]
    tfSnapshot --> tfBoot[Boot VMs in\nbubble network]
    tfBoot --> tfCheck[Run health checks]
    tfCheck --> tfCleanup[Cleanup — remove\nsnapshot and powered-off VMs]

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    class pmShutdown,pmSync,pmPresent,pmBoot,pmValidate,pmReprotect action
    class foPresent,foBoot,foValidate,foFailback action
    class tfSnapshot,tfBoot,tfCheck,tfCleanup action
    class assess decision
    class start,pm,fo,tf terminal
```

---

## Recovery Plans

Use this section for practical SRM Recovery Plans notes, checks, troubleshooting, commands, change notes, and field references.

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident Notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

### Useful Commands

Add tested commands here.

### Known Issues

Add known issues here as they come up.

---

## Test Failover

### Test Failover Sequence

```mermaid
sequenceDiagram
    participant Admin
    participant SRM as SRM Server
    participant SRA as SRA / vSphere Rep
    participant Storage as DR Storage
    participant ESXI as Recovery ESXi

    Admin->>SRM: Start Test (recovery plan)
    SRM->>SRA: Create test snapshot / FlexClone
    SRA->>Storage: Snapshot R2 LUNs (no production impact)
    Storage-->>SRA: Snapshot ready
    SRM->>ESXI: Present snapshot datastores
    ESXI-->>SRM: Datastores accessible
    SRM->>ESXI: Register VMs from snapshot datastores
    SRM->>ESXI: Power on VMs (boot sequence)
    ESXI-->>SRM: VMs online (bubble network)
    SRM-->>Admin: Test running — validate services
    Admin->>SRM: Cleanup / Cancel test
    SRM->>ESXI: Power off test VMs
    SRM->>SRA: Remove test snapshot
    SRA->>Storage: Delete snapshot / FlexClone
    SRM-->>Admin: Test cleanup complete
```

Use this section for practical SRM Test Failover notes, checks, troubleshooting, commands, change notes, and field references.

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident Notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

### Useful Commands

Add tested commands here.

### Known Issues

Add known issues here as they come up.

---

## Planned Migration

### Planned Migration vs Failback Flow

```mermaid
flowchart LR
    subgraph siteA [Protected Site A]
        vmA(["Production VMs\nrunning"])
        storA[("Primary\nDatastores")]
    end

    subgraph replLink [Replication]
        direction TB
        rep(["vSphere Replication\nor SRA array rep"])
    end

    subgraph siteB [Recovery Site B]
        vmB(["VMs powered off\n(placeholders)"])
        storB[("Replica\nDatastores")]
    end

    vmA --> storA
    storA -->|"continuous\nreplication"| rep
    rep --> storB

    siteA -->|"1. Quiesce & shutdown"| migration{{"Planned\nMigration"}}
    migration -->|"2. Final sync"| storB
    migration -->|"3. Power on"| vmB

    vmB -->|"Failback triggered"| failback{{"Reprotect &\nFailback"}}
    failback -->|"Reverse replication"| storA
    failback -->|"Power on original site"| vmA

    classDef site fill:#1e3a5f,stroke:#1d4ed8,color:#fff
    classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef action fill:#b45309,stroke:#92400e,color:#fff
    class vmA,vmB site
    class storA,storB store
    class migration,failback action
```

Use this section for practical SRM Planned Migration notes, checks, troubleshooting, commands, change notes, and field references.

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident Notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

### Useful Commands

Add tested commands here.

### Known Issues

Add known issues here as they come up.

---

## Cleanup

Use this section for practical SRM Cleanup notes, checks, troubleshooting, commands, change notes, and field references.

### Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

### Incident Notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

### Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

### Useful Commands

Add tested commands here.

### Known Issues

Add known issues here as they come up.
