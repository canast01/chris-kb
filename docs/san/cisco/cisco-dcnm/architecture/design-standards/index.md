---
tags:
  - architecture
  - san
---
# Cisco DCNM — Design Standards

```bash
# On each MDS switch (NX-OS CLI)
zone default-zone permit vsan 10
# Expected after setting deny:
no zone default-zone permit vsan 10
# Verify:
show zone status vsan 10
# Mode: Basic, Default-zone: deny
```
```text
┌──────────────────────────────────── Cisco DCNM — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│  DCNM design: HA deployment, management VLAN, RBAC, TLS, backup, and scale limits.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Deployment Standards             │  │              Security Standards             │   │
│   │          HA pair: primary + standby          │  │            TLS 1.2+ for all HTTPS           │   │
│   │          Dedicated management VLAN           │  │          TACACS+ via ISE mandatory          │   │
│   │          8 vCPU / 32 GB RAM (large)          │  │          RBAC: operator = read-only         │   │
│   │            NTP for all timestamps            │  │         SNMPv3 only; disable v1/v2c         │   │
│   │          Dedicated DNS entries mgmt          │  │           IP whitelist API access           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  HA and dedicated management VLAN are baseline; ISE + TLS are security minimums.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Operational Standards             │  │            Scalability Guidelines           │   │
│   │         Backup: nightly NFS; 30-day          │  │          Max 2,000 switches / node          │   │
│   │        Alert review: daily SNMP check        │  │           Max 200,000 ports / node          │   │
│   │         Zone changes: change ticket          │  │          Separate SAN vs LAN domain         │   │
│   │            Firmware via DCNM only            │  │           Scale-out: multi-cluster          │   │
│   │            Quarterly DCNM upgrade            │  │          2 TB storage perf history          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere host · 2 TB datastore · management Ethernet · NFS backup share                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HA pair         = DCNM primary + standby VMs; database replication between them                      │
│  Management VLAN = isolated VLAN for OOB switch management and DCNM traffic                           │
│  ISE             = Cisco Identity Services Engine; provides TACACS+ for DCNM                          │
│  TLS 1.2+        = minimum TLS version for DCNM HTTPS GUI and REST API                                │
│  RBAC            = Role-Based Access Control; network-admin/operator/read-only                        │
│  SNMPv3          = SNMP version 3; auth + privacy mode; disable v1/v2c in DCNM                        │
│  IP whitelist    = restrict REST API source IPs to automation host subnet                             │
│  NFS backup      = nightly DCNM config and database export to NFS mount                               │
│  2,000 switches  = Cisco-recommended maximum MDS/Nexus per DCNM instance                              │
│  SAN vs LAN      = DCNM manages both; separate logical domains per best practice                      │
│  Multi-cluster   = multiple DCNM instances federated; each manages a subset                           │
│  Change ticket   = ITSM requirement; all zone and config changes pre-approved                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
