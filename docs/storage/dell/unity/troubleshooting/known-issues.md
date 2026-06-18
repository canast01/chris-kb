---
tags:
  - troubleshooting
  - unity
  - dell
  - known-issues
---
# Dell Unity — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Unity XT bugs, error codes, and workarounds covering Unisphere for Unity, NAS, SAN, and replication.

*Applies to: Unity XT / UnityVSA, OE 5.x*
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


## Before you begin

- Unity alerts appear in Unisphere for Unity → Alerts.
- Logs: `uemcli /sys/support/uemcli show` for service state; use service login for detailed logs.
- ESRS / SRS must be active for proactive Dell support.

## Host Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| iSCSI host not seeing LUN after mapping | Unity OE 5.x | Host object not created or initiator not registered | Register iSCSI IQN in Unisphere → Hosts; map storage resource to host | N/A |
| NFS export `Permission denied` on mapped host | Unity OE 5.x | Host access mode not set to `read/write` | Edit NFS share access → set host access to RW | N/A |

## Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Async replication session in `ERROR` state | Unity OE 5.x | Replication port 443 or 8888 blocked between sites | Verify TCP 443 and 8888 between both Unity management IPs | N/A |
| Replication failover leaves source in read-only mode | Unity OE 5.x | Expected behavior — source is read-only post-failover until reprotect | Run reprotect after confirming production is running on destination | N/A |

## Unisphere for Unity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Unisphere UI blank after OE upgrade | Unity OE 5.x | Browser cache incompatible with new UI | Clear browser cache and cookies; use private/incognito window | N/A |
| `uemcli login failed` after password change | Unity OE 5.x | Cached credential in uemcli config stale | Delete `~/.emc/unisphere/Unisphere.xml` and reconnect | N/A |

## See also

- [Dell Unity — Common Issues](common-issues/)
- [Dell CloudIQ — Known Issues](../../cloudiq/troubleshooting/known-issues.md)
