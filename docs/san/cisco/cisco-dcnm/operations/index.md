# Cisco DCNM — Operations


<div class="kb-summary">
Cisco DCNM — Operations reference.
</div>

```
┌─────────────────────────────────────── Cisco DCNM — Operations ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        DCNM day-2 operations: discovery management, zone changes, analytics, and backup       │   │
│   │          Discovery: add switch via IP, provide SSH credentials, DCNM polls SNMP + SSH         │   │
│   │        Zone workflow: create device aliases → build zones → add to zone set → activate        │   │
│   │            Analytics: IOPS/latency dashboards, top-N flows, threshold-based alerts            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Discovery → inventory → zone management → performance analytics → backup                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Discovery Ops        │  │           Zone Ops          │  │        Analytics Ops        │   │
│   │       Add switch by IP      │  │     Create device alias     │  │       Enable telemetry      │   │
│   │       Set credentials       │  │      Build zone members     │  │      View IOPS/latency      │   │
│   │      Rediscover fabric      │  │       Add zone to set       │  │         Top-N flows         │   │
│   │        Template push        │  │      Activate zone set      │  │       Alert thresholds      │   │
│   │       Inventory export      │  │       Verify no_change      │  │        Report export        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Backup: DCNM > Administration > Backup and Restore; schedule daily; test restore                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │    DCNM path     │     Key field     │      Verify      │      Notes       │   │
│   │    Add switch    │ Discovery>Disc.  │      Seed IP      │    Reachable     │    SSH creds     │   │
│   │   Zone create    │    SAN>Zoning    │    VSAN select    │   Active zone    │   Alias first    │   │
│   │    Analytics     │  SAN>Analytics   │    Flow filter    │    IOPS graph    │   Lic. active    │   │
│   │      Backup      │   Admin>Backup   │      Schedule     │    File size     │   Off-box copy   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: DCNM management VM · OOB switch mgmt ports · SAN Analytics telemetry path                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Device alias    = Named alias for a port WWN in DCNM; use instead of raw WWNs in zones             │
│    Zone set        = Named collection of zones; only one zone set can be active per VSAN              │
│    Activate        = Push zone set to all switches in VSAN; disrupts traffic if done wrong            │
│    Rediscover      = Force DCNM to re-poll switch topology; clears stale inventory                    │
│    Template push   = DCNM applies a config template to one or more switches via SSH                   │
│    IOPS            = Input/Output Operations Per Second; primary SAN throughput metric                │
│    Top-N flows     = Analytics view of highest-throughput initiator/target pairs                      │
│    Threshold alert = DCNM alarm triggered when IOPS/latency exceeds configured limit                  │
│    Backup          = DCNM config export: database + switch discovered state snapshot                  │
│    Seed IP         = First switch IP given to DCNM; discovery fans out from this seed                 │
│    Credentials     = Switch SSH username/password stored in DCNM for config operations                │
│    Verify          = Post-zone-change check: show zoneset active vsan X on each switch                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────── Cisco DCNM — Operations ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        DCNM day-2 operations: discovery management, zone changes, analytics, and backup       │   │
│   │          Discovery: add switch via IP, provide SSH credentials, DCNM polls SNMP + SSH         │   │
│   │        Zone workflow: create device aliases → build zones → add to zone set → activate        │   │
│   │            Analytics: IOPS/latency dashboards, top-N flows, threshold-based alerts            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Discovery → inventory → zone management → performance analytics → backup                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Discovery Ops        │  │           Zone Ops          │  │        Analytics Ops        │   │
│   │       Add switch by IP      │  │     Create device alias     │  │       Enable telemetry      │   │
│   │       Set credentials       │  │      Build zone members     │  │      View IOPS/latency      │   │
│   │      Rediscover fabric      │  │       Add zone to set       │  │         Top-N flows         │   │
│   │        Template push        │  │      Activate zone set      │  │       Alert thresholds      │   │
│   │       Inventory export      │  │       Verify no_change      │  │        Report export        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Backup: DCNM > Administration > Backup and Restore; schedule daily; test restore                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │    DCNM path     │     Key field     │      Verify      │      Notes       │   │
│   │    Add switch    │ Discovery>Disc.  │      Seed IP      │    Reachable     │    SSH creds     │   │
│   │   Zone create    │    SAN>Zoning    │    VSAN select    │   Active zone    │   Alias first    │   │
│   │    Analytics     │  SAN>Analytics   │    Flow filter    │    IOPS graph    │   Lic. active    │   │
│   │      Backup      │   Admin>Backup   │      Schedule     │    File size     │   Off-box copy   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: DCNM management VM · OOB switch mgmt ports · SAN Analytics telemetry path                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Device alias    = Named alias for a port WWN in DCNM; use instead of raw WWNs in zones             │
│    Zone set        = Named collection of zones; only one zone set can be active per VSAN              │
│    Activate        = Push zone set to all switches in VSAN; disrupts traffic if done wrong            │
│    Rediscover      = Force DCNM to re-poll switch topology; clears stale inventory                    │
│    Template push   = DCNM applies a config template to one or more switches via SSH                   │
│    IOPS            = Input/Output Operations Per Second; primary SAN throughput metric                │
│    Top-N flows     = Analytics view of highest-throughput initiator/target pairs                      │
│    Threshold alert = DCNM alarm triggered when IOPS/latency exceeds configured limit                  │
│    Backup          = DCNM config export: database + switch discovered state snapshot                  │
│    Seed IP         = First switch IP given to DCNM; discovery fans out from this seed                 │
│    Credentials     = Switch SSH username/password stored in DCNM for config operations                │
│    Verify          = Post-zone-change check: show zoneset active vsan X on each switch                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
