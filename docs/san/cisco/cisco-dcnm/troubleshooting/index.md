# Cisco DCNM — Troubleshooting


<div class="kb-summary">
Cisco DCNM — Troubleshooting reference.
</div>

```
┌──────────────────────────────────── Cisco DCNM — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    DCNM troubleshooting: discovery failures, analytics data gaps, zone errors, DB recovery    │   │
│   │           Discovery fails: verify SSH creds, SNMP community, management reachability          │   │
│   │           Analytics gaps: confirm SAN Analytics licence, telemetry collector running          │   │
│   │          Zone push fails: check VSAN state, active zone conflict; test with POAP off          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom → collect DCNM logs → isolate layer → resolve and verify → document                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Discovery Issues      │  │       Analytics Issues      │  │         Zone Issues         │   │
│   │      Switch unreachable     │  │        No data shown        │  │        Push rejected        │   │
│   │         Auth failure        │  │       Licence missing       │  │        VSAN mismatch        │   │
│   │         SNMP timeout        │  │        Collector down       │  │       Active conflict       │   │
│   │       Stale inventory       │  │        Telemetry gap        │  │          Alias dup          │   │
│   │        DB corruption        │  │       Flow filter err       │  │        Zone set lock        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Logs: /var/log/dcnm/ on DCNM appliance; enable debug level for discovery and zoning                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │   First check    │    Key command    │    Resolution    │    Escalation    │   │
│   │   Disc. fails    │   Ping mgmt IP   │    ssh admin@SW   │    Fix creds     │    TAC + logs    │   │
│   │   No analytics   │    Lic. page     │     show lic.     │  Add SAN Anlt.   │    Cisco Lic.    │   │
│   │    Zone fails    │    VSAN state    │    show vsan X    │   Resolve VSAN   │  TAC if locked   │   │
│   │    DB corrupt    │   DCNM status    │   appmgr status   │  Restore backup  │    TAC + snap    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: verify OOB reachability switch mgmt port → DCNM VM NIC · check SAN Analytics NIC         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    appmgr        = DCNM appliance service manager; use to check/restart DCNM services                 │
│    Discovery fail = DCNM cannot SSH or SNMP poll a switch; check creds, reachability, ACLs            │
│    Stale inventory = Switch shows in DCNM but data is outdated; trigger manual rediscover             │
│    SAN Analytics  = DCNM performance module; requires separate licence and telemetry collector        │
│    Telemetry gap  = No flow data in DCNM analytics; check gRPC telemetry on switch                    │
│    Active conflict = Zone push rejected because active zone set has different member count            │
│    Zone set lock  = DCNM or switch holds zone change lock; clear with no zone commit abort            │
│    DB corruption  = DCNM PostgreSQL DB integrity failure; restore from scheduled backup               │
│    POAP           = Power-On Auto-Provisioning; disable during zone troubleshooting                   │
│    gRPC telemetry = Switch streaming protocol pushing port counters/flow stats to DCNM                │
│    Alias dup      = Duplicate device alias for different WWNs causes zone push rejection              │
│    Licence page   = DCNM > Administration > Licensing; shows installed and missing features           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Cisco DCNM — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    DCNM troubleshooting: discovery failures, analytics data gaps, zone errors, DB recovery    │   │
│   │           Discovery fails: verify SSH creds, SNMP community, management reachability          │   │
│   │           Analytics gaps: confirm SAN Analytics licence, telemetry collector running          │   │
│   │          Zone push fails: check VSAN state, active zone conflict; test with POAP off          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom → collect DCNM logs → isolate layer → resolve and verify → document                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Discovery Issues      │  │       Analytics Issues      │  │         Zone Issues         │   │
│   │      Switch unreachable     │  │        No data shown        │  │        Push rejected        │   │
│   │         Auth failure        │  │       Licence missing       │  │        VSAN mismatch        │   │
│   │         SNMP timeout        │  │        Collector down       │  │       Active conflict       │   │
│   │       Stale inventory       │  │        Telemetry gap        │  │          Alias dup          │   │
│   │        DB corruption        │  │       Flow filter err       │  │        Zone set lock        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Logs: /var/log/dcnm/ on DCNM appliance; enable debug level for discovery and zoning                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │   First check    │    Key command    │    Resolution    │    Escalation    │   │
│   │   Disc. fails    │   Ping mgmt IP   │    ssh admin@SW   │    Fix creds     │    TAC + logs    │   │
│   │   No analytics   │    Lic. page     │     show lic.     │  Add SAN Anlt.   │    Cisco Lic.    │   │
│   │    Zone fails    │    VSAN state    │    show vsan X    │   Resolve VSAN   │  TAC if locked   │   │
│   │    DB corrupt    │   DCNM status    │   appmgr status   │  Restore backup  │    TAC + snap    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: verify OOB reachability switch mgmt port → DCNM VM NIC · check SAN Analytics NIC         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    appmgr        = DCNM appliance service manager; use to check/restart DCNM services                 │
│    Discovery fail = DCNM cannot SSH or SNMP poll a switch; check creds, reachability, ACLs            │
│    Stale inventory = Switch shows in DCNM but data is outdated; trigger manual rediscover             │
│    SAN Analytics  = DCNM performance module; requires separate licence and telemetry collector        │
│    Telemetry gap  = No flow data in DCNM analytics; check gRPC telemetry on switch                    │
│    Active conflict = Zone push rejected because active zone set has different member count            │
│    Zone set lock  = DCNM or switch holds zone change lock; clear with no zone commit abort            │
│    DB corruption  = DCNM PostgreSQL DB integrity failure; restore from scheduled backup               │
│    POAP           = Power-On Auto-Provisioning; disable during zone troubleshooting                   │
│    gRPC telemetry = Switch streaming protocol pushing port counters/flow stats to DCNM                │
│    Alias dup      = Duplicate device alias for different WWNs causes zone push rejection              │
│    Licence page   = DCNM > Administration > Licensing; shows installed and missing features           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
