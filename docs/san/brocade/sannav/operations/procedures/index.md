```bash
# SSH to the affected switch
ssh admin@switch-ip

# List available MAPS policies
mapsPolicy --show

# Activate a MAPS policy
mapsPolicy --enable dflt_aggressive_policy

# Verify active policy
mapsPolicy --show
```

```text
┌─────────────────────────────── Brocade SANnav — Operations Procedures ────────────────────────────────┐
│                                                                                                       │
│  Day-to-day SANnav procedures: zone changes, switch adds, firmware, health monitoring.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Zone Change Procedure             │  │             Switch Add / Remove             │   │
│   │         1. Create alias for HBA WWN          │  │          1. Add switch IP in SANnav         │   │
│   │         2. Add alias to target zone          │  │          2. Set SNMP v3 credentials         │   │
│   │         3. Add zone to active config         │  │          3. Discover: verify ports          │   │
│   │          4. Review diff before push          │  │           4. Configure MAPS policy          │   │
│   │            5. cfgsave + cfgenable            │  │           5. Verify firmware level          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Zone changes require change ticket; always review diff before activating config.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Firmware Management              │  │          Health Monitoring Routine          │   │
│   │         1. Upload FOS to SANnav repo         │  │           Daily: MAPS alert review          │   │
│   │        2. Validate against switch ver        │  │          Weekly: port error report          │   │
│   │          3. Schedule upgrade window          │  │          Monthly: utilisation trend         │   │
│   │         4. HA upgrade: standby first         │  │            Quarterly: zone audit            │   │
│   │        5. Verify version post-upgrade        │  │            Annual: SANnav upgrade           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · management network · Brocade FC switch chassis · SFP transceivers                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Alias           = named WWN or alias group; used as zone member instead of raw WWN                   │
│  Zone diff       = SANnav shows before/after view of zone changes before activating                   │
│  cfgsave/cfgenable= save and activate zone config; SANnav executes these on switches                  │
│  MAPS            = Monitoring and Alerting Policy Suite; daily alert review priority                  │
│  HA upgrade      = firmware activated on standby CP first; switchover then active                     │
│  FOS repo        = SANnav local repository for staging Fabric OS firmware images                      │
│  Port error report= weekly SANnav report on CRC/loss-of-sync per port                                 │
│  Zone audit      = quarterly review of all zones for unused aliases and orphaned WWNs                 │
│  Change ticket   = ITSM-required approval before any zone or fabric configuration change              │
│  WWN             = World Wide Name; 64-bit identifier for HBAs and switch ports                       │
│  Utilisation trend= monthly SANnav capacity report; identifies approaching saturation                 │
│  SNMP v3         = SNMPv3 credentials required for SANnav to discover and poll switches               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
