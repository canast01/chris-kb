---
tags:
  - dell
  - operations
---
# Dell VPLEX — Backup & Restore


<div class="kb-summary">
Backup configuration, restore procedures, and validation for Dell VPLEX.

*Applies to: VPLEX*
</div>
```text
┌─────────────────────────────────── Dell VPLEX — Backup and Restore ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       VPLEX backup: snapshots, replication, and external backup application integration       │   │
│   │        Snapshot schedule: hourly for 24 h, daily for 7 days, weekly for 4 weeks minimum       │   │
│   │            Replication: async or sync to DR site for off-site data protection copy            │   │
│   │       Restore: volume-level or file-level restore from snapshot; test restore quarterly       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Snapshot → replicate to DR → verify → document → test restore                                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │        Virtualisation       │  │         Backend LUNs        │  │      Abstracted to VVs      │   │
│   │            Metro            │  │         Sync stretch        │  │        <5ms RTT sites       │   │
│   │             Geo             │  │      Async replication      │  │         Any distance        │   │
│   │          Clustering         │  │        Active-active        │  │       Shared namespace      │   │
│   │            Quorum           │  │          Witness VM         │  │      Split-brain guard      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Type       │     Schedule     │     Retention     │     Offsite?     │    Test cycle    │   │
│   │     Snapshot     │   Hourly/daily   │    7/30/90 days   │        No        │     Monthly      │   │
│   │   Replication    │  Policy-driven   │     Per policy    │     Yes (DR)     │    Quarterly     │   │
│   │    Backup app    │ Daily full+incr  │      90+ days     │ Yes (tape/cloud  │    Quarterly     │   │
│   │     Archive      │     Monthly      │      7+ years     │   Yes (object)   │      Annual      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: VPLEX VS2/VS6 appliance · FC fabric · backend arrays · WAN link (Metro/Geo)              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VPLEX              = Dell storage federation; aggregates arrays into virtual volumes across vendors│
│    Virtual volume     = VPLEX-abstracted LUN presented to hosts; backend is array LUNs                │
│    VPLEX Metro        = synchronous active-active stretch cluster; same VV served from two sites      │
│    VPLEX Geo          = asynchronous active-active replication; higher RPO, no distance constraint    │
│    Distributed VV     = virtual volume spanning two sites for Metro active-active host access         │
│    Witness            = third-site quorum arbiter for Metro; prevents split-brain island scenarios    │
│    WAN-COM            = WAN communication module in VPLEX Geo; manages inter-site replication traffic │
│    Management Server  = embedded Linux VM in VPLEX engine; serves web UI and vplex CLI                │
│    Consistency group  = set of virtual volumes that failover together maintaining write order         │
│    Backend volume     = LUN from underlying array presented to VPLEX engine for virtualisation        │
│    Local device       = RAID device or extent of backend volumes on a single VPLEX cluster            │
│    Cluster            = single VPLEX installation; Metro topology requires exactly two clusters       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Overview

VPLEX is a storage virtualisation layer; it does not store data itself — data resides on the backend arrays. VPLEX configuration backup covers the management and virtualisation layer. Data protection is the responsibility of the backend arrays and the applications using VPLEX volumes.

## Configuration Backup

Back up the following VPLEX configuration artefacts regularly:

| Artefact | Method | Frequency |
|---|---|---|
| VMS VM snapshot | Hypervisor snapshot or backup | Before every change and weekly |
| VPLEX configuration export | `vplexcli` configuration export commands | Weekly and before major changes |
| Storage view inventory | `ll /clusters/*/exports/storage-views/` export | Weekly |
| Consistency group membership | `ll /distributed-storage/consistency-groups/` export | Weekly |
| Distributed device mapping | `ll /distributed-storage/distributed-devices/` export | Weekly |

**VMS VM backup is critical**: VMS is a management plane VM. Its loss does not affect I/O (hosts continue to access volumes), but without a VMS backup, configuration recovery requires manual re-creation or Dell support assistance.

## Collecting a Support Bundle

A VPLEX support bundle captures configuration, logs, and health state for troubleshooting and support case submission:

```bash
# From within vplexcli
collect-support-log -f /var/log/support_bundle.tar.gz

# Copy to a jump host from VMS OS shell
scp service@<VMS_IP>:/var/log/support_bundle.tar.gz admin@<jump_host>:/tmp/
```

## Recovery Scenarios

**VMS loss (management plane only):**
- Host I/O continues uninterrupted — VPLEX directors do not depend on VMS for data path
- Restore the VMS VM from the most recent backup or snapshot
- If no backup exists, VMS must be re-deployed and the VPLEX configuration re-imported; engage Dell support

**Director failure:**
- A single director failure within a director pair reduces redundancy but does not interrupt I/O (cache mirroring continues on the surviving director)
- Replace the failed director hardware using the Dell VPLEX Director Replacement guide
- Verify director health post-replacement: `ll /engines/*/directors/*/hardware/`

**Metro site failure:**
- The Witness automatically grants quorum to the surviving cluster
- Hosts at the surviving site continue I/O on distributed volumes
- After the failed site recovers: reconnect the ICL, verify Witness connectivity, allow distributed devices to resync
- Monitor resync progress: `ll /distributed-storage/distributed-devices/*/health-indications/`

```mermaid
flowchart TD
    subgraph "VMS Loss"
        vmsLost["VMS VM unavailable\n(management plane only)"]
        ioOk["Host I/O continues\nDirectors unaffected"]
        restoreVms["Restore VMS VM\nfrom snapshot / backup"]
        vmsLost --> ioOk
        vmsLost --> restoreVms
    end
    subgraph "Director Failure"
        dirFail["Single director failure\nWithin a pair"]
        pairDegraded["Director pair degraded\nCache on surviving director"]
        replaceDir["Replace failed director\nDell FSE hardware replacement"]
        verifyDir["ll /engines/*/directors/*/hardware/\nConfirm health-state: ok"]
        dirFail --> pairDegraded --> replaceDir --> verifyDir
    end
    subgraph "Metro Site Failure"
        siteFail["Site failure / ICL down\nWitness grants quorum"]
        survivorIo["Surviving cluster continues I/O\nDistributed volumes accessible"]
        siteRecover["Site recovers\nICL reconnected"]
        resync["Distributed devices resync\nmonitor rebuild-progress"]
        siteFail --> survivorIo --> siteRecover --> resync
    end
```

## Validation

After any recovery:

- [ ] `health-check --full` returns no errors
- [ ] `ll /distributed-storage/distributed-devices/*/health-indications/` — all devices `health-state: ok`
- [ ] `ll /distributed-storage/consistency-groups/` — all CGs `operational-status: ok`
- [ ] Host path validation: `powermt display dev=all` or `multipath -ll` shows all expected paths active
- [ ] Application owners confirm I/O has resumed normally

---

## Verify

- `health-check --full` returns no errors across all VPLEX components
- `ll /distributed-storage/distributed-devices/*/health-indications/` — all devices show `health-state: ok`
- `ll /distributed-storage/consistency-groups/` — all CGs show `operational-status: ok`
- Host multipath check (`multipath -ll` or `powermt display dev=all`) shows all expected paths active
