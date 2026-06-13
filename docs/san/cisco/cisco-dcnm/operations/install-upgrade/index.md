---
tags:
  - operations
  - san
---
# Cisco DCNM — Install and Upgrade

```bash
# On the primary (active) DCNM node
ssh root@dcnm-dc1-active.corp.example.com

# Run HA setup utility
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-setup.sh \
  --primary \
  --vip 10.10.5.15 \
  --peer 10.10.5.11 \
  --password <ha-password>

# On the secondary (standby) node
ssh root@dcnm-dc1-standby.corp.example.com

/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-setup.sh \
  --secondary \
  --vip 10.10.5.15 \
  --peer 10.10.5.10 \
  --password <ha-password>

# Verify HA status from active node
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-status.sh
# Expected: ACTIVE/STANDBY pair, VIP reachable
```
```text
┌────────────────────────────────── Cisco DCNM — Install and Upgrade ───────────────────────────────────┐
│                                                                                                       │
│  DCNM deployment: OVA/ISO to vSphere, initial config, switch discovery, upgrade path.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Fresh Install Steps              │  │            Initial Configuration            │   │
│   │        1. Download DCNM OVA from CCO         │  │          1. Set hostname + IP + DNS         │   │
│   │           2. Deploy OVA in vSphere           │  │           2. Configure NTP servers          │   │
│   │       3. Boot + initial config wizard        │  │           3. Set admin credentials          │   │
│   │        4. 8 vCPU / 32 GB RAM (large)         │  │           4. Configure ISE TACACS+          │   │
│   │          5. 2 TB datastore for perf          │  │           5. Discover MDS switches          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  OVA deployment is automated; ISE and NTP must be configured before adding switches.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Upgrade Procedure               │  │           Post-Upgrade Validation           │   │
│   │           1. Backup DCNM DB to NFS           │  │         1. Verify all switches shown        │   │
│   │           2. Download new DCNM OVA           │  │         2. Check SNMP alert forward         │   │
│   │        3. Deploy standby; restore DB         │  │         3. Re-test ISE TACACS+ auth         │   │
│   │         4. Validate standby function         │  │        4. Verify NFS backup schedule        │   │
│   │          5. Swing DNS; decom old VM          │  │          5. Confirm zone push works         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere host · 2 TB datastore · management network · NFS backup share                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CCO             = Cisco Connection Online; software download portal (software.cisco.com)             │
│  OVA             = Open Virtual Appliance; DCNM packaged as vSphere-ready VM template                 │
│  Config wizard   = DCNM first-boot setup; sets IP, NTP, credentials interactively                     │
│  ISE             = Cisco Identity Services Engine; provides TACACS+ for DCNM auth                     │
│  NFS backup      = nightly DCNM DB backup; required before any upgrade                                │
│  Swing DNS       = update DNS A record to new DCNM VM IP after validation                             │
│  Standby upgrade = deploy new DCNM version as standby first; validate then swing                      │
│  SNMP forwarding = DCNM forwards switch alerts to NMS; test after every upgrade                       │
│  Zone push test  = verify DCNM can activate zone set on MDS switch after upgrade                      │
│  vCPU / RAM      = DCNM large mode: 8 vCPU / 32 GB; medium: 4 vCPU / 16 GB                            │
│  2 TB datastore  = DCNM storage for 90-day performance data; Elasticsearch store                      │
│  NTP             = Network Time Protocol; timestamps required for event correlation                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# On each MDS switch
no snmp-server host <dcnm-ip> traps version 3 priv dcnm_poll

# Remove syslog forwarding to DCNM
no logging server <dcnm-ip>

# Remove DCNM service account
no username dcnm_mgmt
```
