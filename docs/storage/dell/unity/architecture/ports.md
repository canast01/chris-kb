---
tags:
  - dell-unity
  - dell
  - networking
  - firewall
  - ports
  - storage
---
# Dell Unity — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell Unity XT storage arrays. Covers Unisphere management, NFS, SMB, iSCSI, and Unity native replication.

*Applies to: Dell Unity XT / Unity 500 / UnityOS 5.x*
</div>

```text
┌──────────────────────────────────────────── Dell Unity XT ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Unity XT: unified mid-range storage — block, file, and VMware vVols integration        │   │
│   │                          Protocols: FC · iSCSI · NFS · SMB · REST API                         │   │
│   │                                 Management: Unisphere / UEMCLI                                │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Ctrl            │  │         SP-A + SP-B         │  │        Cache mirrored       │   │
│   │             Pool            │  │       Dynamic FAST VP       │  │         Auto-tiering        │   │
│   │          NAS server         │  │        File protocols       │  │          Per-tenant         │   │
│   │           Snapshot          │  │        Writable snaps       │  │        Thin PiT copy        │   │
│   │         Replication         │  │         Async/Metro         │  │       Native or RP4VM       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    Unisphere     │  GUI / REST API  │       HTTPS       │    LDAP/local    │    SP-hosted     │   │
│   │      UEMCLI      │  CLI management  │    SSH / HTTPS    │   Local admin    │  All operations  │   │
│   │    NAS server    │  File services   │      NFS/SMB      │  Kerberos/NTLM   │ Virtual file se  │   │
│   │   RecoverPoint   │ Continuous prote │   Encrypted TCP   │   Certificate    │   Journal CDP    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Unity XT 380F/480F/680F/880F · dual SPs · DPE/DAE expansion · 10/25 GbE                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Unity XT           = Dell unified mid-range array; block LUNs, file NAS, and VMware vVols          │
│    Unisphere          = HTML5 GUI and REST API for Unity XT management; SP-hosted management portal   │
│    UEMCLI             = CLI for Unity XT; uemcli -d <ip> -u admin -p <pw> /show commands              │
│    Storage pool       = collection of drives forming a usable pool; FAST VP tiers data automatically  │
│    FAST VP            = Fully Automated Storage Tiering VP; moves hot and cold data between tiers     │
│    NAS server         = virtual file server on Unity; each has its own IP, DNS, and CIFS/NFS shares   │
│    Data Mover         = older EMC term for NAS server; used in VNX and early Unity documentation      │
│    SP-A / SP-B        = storage processors; active-active HA pair with mirrored cache                 │
│    Snapshot           = space-efficient PiT copy of LUN or FS; writable snapshots supported           │
│    RecoverPoint       = RP4VM; journal-based continuous data protection for Unity volumes             │
│    Metro              = synchronous replication between two Unity XT sites; active-active zero RPO    │
│    vVols              = Virtual Volumes; VASA provider exposes per-VM storage objects to vCenter      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Inbound — Management

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin workstations | Unisphere for Unity web UI and REST API |
| 22 | TCP | Jump hosts | SSH — Unity Unisphere CLI (uemcli) |
| 80 | TCP | Clients | HTTP — redirects to 443 |
| 161 | UDP | Monitoring | SNMP polling |

## Outbound

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 162 | UDP | SNMP receiver | SNMP traps |
| 514 | UDP | Syslog server | Syslog forwarding |
| 123 | UDP | NTP | Time sync |
| 25 | TCP | SMTP relay | Alert email |
| 443 | TCP | esrs.dell.com, cloudiq.dell.com | ESRS / CloudIQ |

## Data Protocols

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 2049 | TCP/UDP | NFS clients | NFS file access |
| 111 | TCP/UDP | NFS v3 clients | rpcbind |
| 445 | TCP | SMB clients | SMB file access |
| 3260 | TCP | iSCSI initiators | iSCSI block storage |

## Replication

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 443 | TCP | Unity A mgmt IP ↔ Unity B mgmt IP | Unity native replication control and data |
| 8888 | TCP | Unity A ↔ Unity B | Unity replication data channel (some versions) |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin clients | Unity mgmt IP | 443, 22 | Unisphere UI and CLI |
| NFS clients | Unity NFS data IPs | 2049, 111 | NFS |
| SMB clients | Unity SMB data IPs | 445 | SMB |
| iSCSI hosts | Unity iSCSI ports | 3260 | Block |
| Unity A mgmt | Unity B mgmt | 443 | Replication |

## Verify

```bash
# From admin workstation — test Unisphere
curl -sk -o /dev/null -w "%{http_code}" https://<unity-mgmt-ip>/api/types/basicSystemInfo/instances

# From NFS client
showmount -e <unity-nfs-ip>

# From iSCSI host
iscsiadm -m discovery -t sendtargets -p <unity-iscsi-ip>:3260
```

## See also

- [Dell Unity — Architecture](how-it-works/)
- [Dell PowerStore — Ports](../../powerstore/architecture/ports/)
