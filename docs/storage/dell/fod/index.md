# Dell Flex on Demand

<div class="kb-summary">
Dell Flex on Demand — consumption-based capacity metering on PowerMax, PowerStore, and PowerScale. Covers architecture, operations, security, and troubleshooting for FOD subscription management.
</div>

```
┌──────────────────────────────────── Dell Features on Demand (FoD) ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FoD: Dell software feature licensing; unlock array capabilities via license key purchase   │   │
│   │    Features unlocked: extra protocols, replication, snapshots, encryption, tiering, FAST VP   │   │
│   │      Key applied via array management UI or CLI; feature active instantly without reboot      │   │
│   │     Supported on PowerStore, PowerMax, Unity XT, PowerScale; managed via Licensing Portal     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify needed feature → purchase FoD key → download → apply via array GUI → feature live         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Feature Types        │  │        Array Support        │  │          Management         │   │
│   │          Protocols          │  │          PowerStore         │  │       Licensing portal      │   │
│   │         Replication         │  │       PowerMax / VMAX       │  │        Array GUI/CLI        │   │
│   │          Snapshots          │  │           Unity XT          │  │       CloudIQ monitor       │   │
│   │          Encryption         │  │          PowerScale         │  │        Support portal       │   │
│   │       FAST VP tiering       │  │         PowerStore-X        │  │         Dell account        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    FoD keys are array-serial-number bound; not transferable between arrays                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │       Role       │       Owner       │       Tool       │      Notes       │   │
│   │     FoD key      │ Unlocks feature  │   Customer buys   │ Licensing portal │      Per SN      │   │
│   │    Array mgr     │   Applies key    │    Storage eng.   │    GUI or CLI    │  Instant effect  │   │
│   │  License portal  │   Key purchase   │    Storage lead   │   Dell portal    │ All key history  │   │
│   │     CloudIQ      │  Feature status  │    Storage ops    │   SaaS portal    │     Optional     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: no hardware change needed; FoD unlocks software capability already on the array          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FoD            = Features on Demand; Dell software feature licensing model for array capabilities  │
│    FoD key        = License file purchased and downloaded from Dell Licensing Portal                  │
│    Protocol FoD   = Unlock NFS, SMB, iSCSI, FC, or NVMe-oF protocol support on an array               │
│    Replication FoD = Unlock array-based replication (e.g. PowerStore replication, SRDF on VMAX)       │
│    Snapshot FoD   = Unlock snapshot creation beyond the base limit included in hardware purchase      │
│    Encryption FoD = Unlock data-at-rest encryption capability; AES-256 via array controller           │
│    FAST VP        = Fully Automated Storage Tiering for Virtual Pools; automated data placement       │
│    SN bound       = FoD key cryptographically tied to a specific array serial number                  │
│    Instant effect = Feature visible in array UI seconds after key is applied; no reboot               │
│    Licensing portal = Dell portal for purchasing, downloading, and tracking FoD license keys          │
│    Base license   = Features included with array purchase without FoD; varies by model/SKU            │
│    Bundle key     = Some FoD products sold as a bundle; single key unlocks multiple features          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Dell Features on Demand (FoD) ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FoD: Dell software feature licensing; unlock array capabilities via license key purchase   │   │
│   │    Features unlocked: extra protocols, replication, snapshots, encryption, tiering, FAST VP   │   │
│   │      Key applied via array management UI or CLI; feature active instantly without reboot      │   │
│   │     Supported on PowerStore, PowerMax, Unity XT, PowerScale; managed via Licensing Portal     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify needed feature → purchase FoD key → download → apply via array GUI → feature live         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Feature Types        │  │        Array Support        │  │          Management         │   │
│   │          Protocols          │  │          PowerStore         │  │       Licensing portal      │   │
│   │         Replication         │  │       PowerMax / VMAX       │  │        Array GUI/CLI        │   │
│   │          Snapshots          │  │           Unity XT          │  │       CloudIQ monitor       │   │
│   │          Encryption         │  │          PowerScale         │  │        Support portal       │   │
│   │       FAST VP tiering       │  │         PowerStore-X        │  │         Dell account        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    FoD keys are array-serial-number bound; not transferable between arrays                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │       Role       │       Owner       │       Tool       │      Notes       │   │
│   │     FoD key      │ Unlocks feature  │   Customer buys   │ Licensing portal │      Per SN      │   │
│   │    Array mgr     │   Applies key    │    Storage eng.   │    GUI or CLI    │  Instant effect  │   │
│   │  License portal  │   Key purchase   │    Storage lead   │   Dell portal    │ All key history  │   │
│   │     CloudIQ      │  Feature status  │    Storage ops    │   SaaS portal    │     Optional     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: no hardware change needed; FoD unlocks software capability already on the array          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FoD            = Features on Demand; Dell software feature licensing model for array capabilities  │
│    FoD key        = License file purchased and downloaded from Dell Licensing Portal                  │
│    Protocol FoD   = Unlock NFS, SMB, iSCSI, FC, or NVMe-oF protocol support on an array               │
│    Replication FoD = Unlock array-based replication (e.g. PowerStore replication, SRDF on VMAX)       │
│    Snapshot FoD   = Unlock snapshot creation beyond the base limit included in hardware purchase      │
│    Encryption FoD = Unlock data-at-rest encryption capability; AES-256 via array controller           │
│    FAST VP        = Fully Automated Storage Tiering for Virtual Pools; automated data placement       │
│    SN bound       = FoD key cryptographically tied to a specific array serial number                  │
│    Instant effect = Feature visible in array UI seconds after key is applied; no reboot               │
│    Licensing portal = Dell portal for purchasing, downloading, and tracking FoD license keys          │
│    Base license   = Features included with array purchase without FoD; varies by model/SKU            │
│    Bundle key     = Some FoD products sold as a bundle; single key unlocks multiple features          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Authentication, access control, encryption, and hardening.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostics, and escalation.</span></a>
</div>
