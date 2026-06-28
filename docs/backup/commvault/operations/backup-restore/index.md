---
tags:
  - commvault
  - operations
---
# Commvault Backup and Restore — Procedures
![Commvault Backup and Restore — Procedures](../../../../assets/backup-commvault-operations-backup-restore-index.svg)


```bash
curl -s -X POST "https://commserve.example.com/webconsole/api/Login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' | jq '.token'
```

```text
Subclient → Restore → In-Place → Overwrite existing data: Yes
```
```text
Subclient → Restore → Out-of-Place → Specify destination client and path
```
```bash
qoperation execscript -sn QS_ValidateCopy -si "StoragePolicyName" -si "CopyName"
```
```mermaid
flowchart TD
    A([Recovery Request]) --> B{What needs recovery?}
    B --> C[Entire VM]
    B --> D[Specific files/folders]
    B --> E[Application data\nExchange / SQL / AD]

    C --> F{Target location?}
    F --> G[Original location\nIn-Place Restore]
    F --> H[Alternate host/DS\nOut-of-Place Restore]

    D --> I{Source accessible?}
    I --> |Yes - live agent| J[File-Level Recovery\nvia live browse]
    I --> |No - offline VM| K[Mount backup as\nvirtual volume\nthen browse]

    E --> L{Application type?}
    L --> M[Exchange → Mailbox\nor Item Restore]
    L --> N[SQL → DB Restore\nor Table-level]
    L --> O[AD → Authoritative\nor Non-authoritative]

    G --> P[Validate services post-restore]
    H --> P
    J --> P
    K --> P
    M --> P
    N --> P
    O --> P

    P --> Q{Validation passed?}
    Q --> |Yes| R([Recovery Complete])
    Q --> |No| S[Escalate /\nRestore alternate point]
```

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Source\n(Commvault)" as SRC
participant "Backup Engine" as ENG
participant "Target / Vault" as TGT

SRC -> ENG: Verify
ENG -> TGT: Write
TGT --> ENG: Confirmed
ENG --> SRC: Done

@enduml
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy

---

## See also

- [Commvault — Procedures](../procedures/)
- [Commvault — Health Checks](../health-checks/)
- [Commvault — Common Issues](../../troubleshooting/common-issues/)
