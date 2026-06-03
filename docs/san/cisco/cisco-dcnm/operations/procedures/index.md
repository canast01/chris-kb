```bash
# CSV format: alias_name,wwn
# esxi01-hba0,500010000abcdef0
# esxi01-hba1,500010000abcdef1

# REST API bulk import
curl -sk -b dcnm-cookie.txt -X POST \
  "${DCNM}/rest/san/devicealias?fabricName=DC1-FABRIC-A" \
  -H "Content-Type: application/json" \
  -d '{
    "aliases": [
      {"aliasName": "esxi01-hba0", "pwwn": "50:00:10:00:00:ab:cd:ef"},
      {"aliasName": "purestor01-ct0-fc0", "pwwn": "52:4a:93:70:ab:cd:ef:00"}
    ]
  }' | python3 -m json.tool
```

```text
┌───────────────────────────────── Cisco DCNM — Operations Procedures ──────────────────────────────────┐
│                                                                                                       │
│  DCNM day-2 procedures: zone changes, switch adds, firmware upgrades, health monitoring.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Zone Change Procedure             │  │             Switch Add / Remove             │   │
│   │         1. Create device alias (WWN)         │  │           1. Add switch IP in DCNM          │   │
│   │         2. Create zone with aliases          │  │          2. Set SNMPv3 credentials          │   │
│   │           3. Add zone to zone set            │  │           3. Discover: verify VSAN          │   │
│   │         4. Review zone diff in DCNM          │  │         4. Set SNMP threshold rules         │   │
│   │         5. Activate zone set in VSAN         │  │           5. Verify NX-OS version           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Zone set activation requires change ticket; always review diff before activation.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Firmware Management              │  │          Health Monitoring Routine          │   │
│   │         1. Upload NX-OS to DCNM repo         │  │           Daily: SNMP alert review          │   │
│   │          2. Validate compatibility           │  │          Weekly: port error report          │   │
│   │           3. ISSU upgrade via DCNM           │  │           Monthly: ISL utilisation          │   │
│   │          4. Verify via show version          │  │          Quarterly: zone set audit          │   │
│   │         5. Post-upgrade traffic test         │  │             Annual: DCNM upgrade            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · management network · Cisco MDS switch chassis · SFP transceivers                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Device alias    = named mapping for WWN in VSAN; used as zone member instead of raw WWN              │
│  Zone set        = collection of zones applied to a VSAN; only one active at a time                   │
│  Zone diff       = DCNM shows before/after comparison before activating zone set                      │
│  zoneset activate= NX-OS command; activates zone set in VSAN; DCNM triggers remotely                  │
│  ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic disruption              │
│  SNMPv3          = SNMP v3 credentials required for DCNM switch discovery and polling                 │
│  VSAN            = Virtual SAN; logical FC fabric partition; zones are per-VSAN                       │
│  Port error report= weekly DCNM report on CRC/discard/loss-of-sync per port                           │
│  Zone set audit  = quarterly review of all zones for stale aliases and orphaned WWNs                  │
│  Change ticket   = ITSM approval required before zone activation or firmware upgrade                  │
│  ISL utilisation = monthly DCNM ISL throughput trend; > 70% = add more ISLs                           │
│  NX-OS repo      = DCNM internal firmware storage; images staged before upgrade                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
