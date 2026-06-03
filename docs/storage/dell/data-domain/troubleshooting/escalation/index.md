# Dell Data Domain Escalation

```bash
# 1. System identification
system show  # DDOS version, serial number, model

# 2. Current alert status
alerts show current

# 3. Filesystem status and space
filesys status
filesys show space
filesys show compression

# 4. Replication status (if replication is the issue)
replication show
replication status

# 5. Hardware status
disk show state

# 6. Network status
net show all
net show stats

# 7. Generate and send an AutoSupport bundle
autosupport send <case-number>

# 8. Manually generate a support bundle (if AutoSupport is not working)
support bundle generate
# Bundle is saved to /ddr/var/support/ — download via SCP or SFTP
```

```text
┌───────────────────────────────────── Dell Data Domain Escalation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Escalate to Dell Support with SR; attach support bundle and alert list            │   │
│   │            Hardware faults (disk/NVRAM): Dell dispatches field engineer with parts            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Before Escalating               │  │               Escalation Steps              │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │      DDOS version (system show version)      │  │         Open SR at support.dell.com         │   │
│   │           Support bundle collected           │  │         Upload support bundle via SR        │   │
│   │       Alert list (alerts show current)       │  │         Describe exact error/symptom        │   │
│   │         Service tag / serial number          │  │          Request hardware dispatch          │   │
│   │         Disk state (disk show state)         │  │          Confirm maintenance window         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Service tag    = Dell asset identifier; required for support case and warranty lookup              │
│    Hardware dispatch= Dell field engineer brings replacement part (disk, NVRAM, PSU, etc.)            │
│    Maintenance window= Coordinate hardware replacement with ops team; some replacements hot-swap      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
