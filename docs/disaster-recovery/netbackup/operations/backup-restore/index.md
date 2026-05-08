# NetBackup — Backup & Restore

## Purpose

Use this page for practical NetBackup Restores notes, checks, troubleshooting, commands, change notes, and field references.

## Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

## Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Useful commands

Add tested commands here.

## Known issues

Add known issues here as they come up.

## Catalog

### MSDP Architecture and Dedup Pool Flow

```mermaid
flowchart LR
    subgraph mediaServer [Media Server — MSDP Host]
        bpbrm["bpbrm\nbackup manager"]
        pdde["PDDE engine\n(dedup processing)"]
        ddbLocal[("MSDP Catalog\nfingerprint DB\n+ container files")]
        bpbrm --> pdde
        pdde --> ddbLocal
    end

    clientData(["Client backup\ndata stream"])
    clientData --> bpbrm

    ddbLocal -->|"unique blocks only"| storage[("MSDP Storage\nContainer files\n(partitioned volumes)")]
    storage -->|"optimised replication\nover WAN"| drMSDP[("DR Site MSDP\nsecondary copy")]

    classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef host fill:#15803d,stroke:#166534,color:#fff
    class bpbrm,pdde ctrl
    class ddbLocal,storage,drMSDP store
    class clientData host
```

Use this section for practical NetBackup Catalog notes, checks, troubleshooting, commands, change notes, and field references.

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
