---
tags:
  - operations
  - san
---
# Brocade SANnav — Install and Upgrade

```bash
# After VM powers on, access the console or SSH with default credentials
# Default credentials: admin / passw0rd (change on first login)
ssh admin@<sannav-ip>

# Verify network connectivity
ping 8.8.8.8       # or internal NTP/DNS server
hostname           # should return configured FQDN

# Check service startup
sannav status
# Wait 5-10 minutes for all services to start on first boot

# Change default admin password
passwd admin
```
```text
┌──────────────────────────────── Brocade SANnav — Install and Upgrade ─────────────────────────────────┐
│                                                                                                       │
│  SANnav deployment: OVA to vSphere, initial config, discover switches, upgrade path.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Fresh Install Steps              │  │            Initial Configuration            │   │
│   │       1. Download SANnav OVA from BCM        │  │         1. Set hostname + IP address        │   │
│   │           2. Deploy OVA in vSphere           │  │           2. Configure NTP servers          │   │
│   │          3. Power on + accept EULA           │  │            3. Set admin password            │   │
│   │        4. Assign: 4 vCPU / 16 GB RAM         │  │          4. Configure TACACS+/LDAP          │   │
│   │       5. 2 TB datastore for perf data        │  │         5. Discover fabric switches         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  OVA deployment is quick; NTP and TACACS+ must be configured before adding switches.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Upgrade Procedure               │  │           Post-Upgrade Validation           │   │
│   │          1. Backup SANnav DB to NFS          │  │        1. Verify all switches present       │   │
│   │          2. Download new SANnav OVA          │  │       2. Check MAPS alerts forwarding       │   │
│   │        3. Deploy standby; restore DB         │  │           3. Re-test TACACS+ auth           │   │
│   │        4. Validate standby operation         │  │        4. Verify NFS backup schedule        │   │
│   │           5. Swing DNS; decom old            │  │        5. Confirm zone management ok        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere host · shared 2 TB datastore · management network · NFS backup share                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA             = Open Virtual Appliance; SANnav package for vSphere deployment                      │
│  BCM             = Broadcom; download SANnav OVA from support.broadcom.com                            │
│  EULA            = End User License Agreement; accepted on first SANnav boot                          │
│  vCPU            = virtual CPU; SANnav minimum is 4 vCPU for production use                           │
│  Datastore       = vSphere storage; SANnav needs ~2 TB for 90-day perf history                        │
│  NFS backup      = SANnav DB backup destination; required before any upgrade                          │
│  Swing DNS       = update DNS A record to point to new SANnav VM after validation                     │
│  TACACS+         = centralised auth; must be re-tested after every SANnav upgrade                     │
│  MAPS forwarding = MAPS alerts from switches must flow to new SANnav after upgrade                    │
│  NTP servers     = time sync; must be configured before adding switches to SANnav                     │
│  Zone management = ability to push zone changes from SANnav GUI after upgrade                         │
│  Standby upgrade = deploy new SANnav version as standby; validate before DNS swing                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# On each switch (FOS CLI)
snmpconfig --set trapdest -index <n> -trapdest 0.0.0.0   # clear trap destination
userconfig --delete sannav_svc
```
